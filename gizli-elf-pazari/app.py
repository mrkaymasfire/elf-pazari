# app.py - TAMAMEN GÜNCELLENDİ (RESİM DESTEĞİ + DİNAMİK ÜRÜNLER)
from flask import Flask, render_template, request, redirect, url_for, session
import os
import json

app = Flask(__name__)
app.secret_key = 'elf-gizli-anahtar-2024'

# STATİK DOSYA KONFİGÜRASYONU
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Ürün verileri JSON dosyasından yükle (kolay düzenleme için)
def load_products():
    try:
        with open('products.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Varsayılan ürünler (150 ürün)
        products = []
        for i in range(1, 151):
            products.append({
                "id": i,
                "name": f"Büyülü Noel Süsü {i}",
                "description": f"Yeni Yıl Kaşifleri tarafından hazırlanmış, ışık saçan özel süs. Her biri el yapımı ve benzersiz.",
                "price": (i % 10 + 1) * 25 + (i % 3) * 5 + 9.99,
                "category": ["Noel Süsleri", "Büyülü Eşyalar", "Elf Yapımı", "Işık Saçanlar", "Antik Tarifler"][i % 5],
                "image": f"product_{i % 10 + 1}.jpg" if os.path.exists(f'static/images/product_{i % 10 + 1}.jpg') else "default.jpg",
                "in_stock": True,
                "rating": round(3 + (i % 5) * 0.5, 1)
            })
        return products

# Ürünleri kaydet (admin paneli için temel)
def save_products(products):
    with open('products.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=4)

PRODUCTS = load_products()

# Sepet işlemleri (oturum tabanlı)
def get_cart():
    if 'cart' not in session:
        session['cart'] = []
    return session['cart']

def add_to_cart(product_id, quantity=1):
    cart = get_cart()
    # Ürünü sepette ara
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] += quantity
            session.modified = True
            return
    
    # Yeni ürün ekle
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product:
        cart.append({
            'product_id': product_id,
            'quantity': quantity,
            'name': product['name'],
            'price': product['price'],
            'image': product['image']
        })
        session.modified = True

def remove_from_cart(product_id):
    cart = get_cart()
    session['cart'] = [item for item in cart if item['product_id'] != product_id]

def get_cart_total():
    cart = get_cart()
    total = sum(item['price'] * item['quantity'] for item in cart)
    return round(total, 2)

def get_cart_count():
    cart = get_cart()
    return sum(item['quantity'] for item in cart)

@app.route('/')
def index():
    """Ana sayfa - Büyülü orman girişi"""
    return render_template('index.html', cart_count=get_cart_count())

@app.route('/magic_shop')
def magic_shop():
    """Elf Pazarı - 150 ürünlü mağaza"""
    return render_template('magic_shop.html', 
                          products=PRODUCTS, 
                          cart_count=get_cart_count())

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Ürün detay sayfası"""
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return "Ürün bulunamadı", 404
    
    # Benzer ürünler (aynı kategoriden 4 ürün)
    similar_products = [p for p in PRODUCTS if p['category'] == product['category'] and p['id'] != product_id][:4]
    
    return render_template('product_detail.html', 
                          product=product, 
                          similar_products=similar_products,
                          cart_count=get_cart_count())

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart_route(product_id):
    """Sepete ekle"""
    add_to_cart(product_id)
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart_route(product_id):
    """Sepetten çıkar"""
    remove_from_cart(product_id)
    return redirect(url_for('cart'))

@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart_route(product_id):
    """Sepet miktarını güncelle"""
    quantity = int(request.form.get('quantity', 1))
    cart = get_cart()
    
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] = quantity
            session.modified = True
            break
    
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    """Sepet sayfası"""
    cart_items = get_cart()
    total = get_cart_total()
    return render_template('cart.html', 
                          cart_items=cart_items, 
                          total=total,
                          cart_count=len(cart_items))

@app.route('/clear_cart')
def clear_cart():
    """Sepeti temizle"""
    session['cart'] = []
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    """Ödeme sayfası"""
    cart_items = get_cart()
    if not cart_items:
        return redirect(url_for('cart'))
    
    total = get_cart_total()
    return render_template('checkout.html', 
                          cart_items=cart_items, 
                          total=total,
                          cart_count=len(cart_items))

# Basit admin paneli (ürün düzenleme için)
@app.route('/admin/products')
def admin_products():
    """Ürün yönetimi (basit)"""
    return render_template('admin_products.html', products=PRODUCTS)

@app.route('/admin/update_product/<int:product_id>', methods=['POST'])
def update_product(product_id):
    """Ürün güncelle"""
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product:
        product['name'] = request.form.get('name', product['name'])
        product['description'] = request.form.get('description', product['description'])
        product['price'] = float(request.form.get('price', product['price']))
        product['category'] = request.form.get('category', product['category'])
        save_products(PRODUCTS)
    
    return redirect(url_for('admin_products'))

# Statik dosyalar
@app.route('/static/<path:filename>')
def serve_static(filename):
    return app.send_static_file(filename)

if __name__ == '__main__':
    # Gerekli klasörleri oluştur
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # Ürünler JSON dosyasını oluştur
    if not os.path.exists('products.json'):
        save_products(PRODUCTS)
    
    print("\n" + "="*60)
    print("🎄 GİZLİ ELF PAZARI - BÜYÜLÜ ALIŞVERİŞ SİTESİ 🎁")
    print("="*60)
    print("\n✨ ÖZELLİKLER:")
    print("   ✅ Büyülü orman atmosferi (Tamamen CSS)")
    print("   ✅ Scroll ile hikaye anlatımı")
    print("   ✅ 150 büyülü ürün")
    print("   ✅ Resim destekli ürünler")
    print("   ✅ Tam çalışan sepet sistemi")
    print("   ✅ Ürün detay sayfaları")
    print("   ✅ Karanlıktan aydınlığa geçiş efekti")
    print("   ✅ Büyülü kapı animasyonu")
    print("   ✅ Responsive tasarım")
    print("\n🛒 SEPET ÖZELLİKLERİ:")
    print("   • Sepete ekle/çıkar")
    print("   • Toplam fiyat hesaplama")
    print("   • Sepeti temizle")
    print("   • Oturum tabanlı depolama")
    print("\n📦 RESİM YÜKLEME:")
    print("   • static/images/ klasörüne resimleri yükleyin")
    print("   • product_1.jpg, product_2.jpg, ... şeklinde")
    print("   • Varsayılan: default.jpg")
    print("   • Ortodoks ikonu: orthodoksikon.jpg")
    print("\n🌐 Tarayıcınızda açın: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)