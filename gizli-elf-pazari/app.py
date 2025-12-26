# app.py - TAMAMEN GÜNCELLENDİ (TL + YENİ KATEGORİLER + PROFESYONEL YAPI)
from flask import Flask, render_template, request, redirect, url_for, session
import os
import json
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'elf-gizli-anahtar-2024-noel'

# STATİK DOSYA KONFİGÜRASYONU
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Yeni Kategoriler
CATEGORIES = [
    "🎁 Noel Hediyeleri",
    "👕 Noel Temalı Giysiler", 
    "🍫 Özel Çikolatalar",
    "☕ Noel Bardakları",
    "🏠 Ev Dekorasyonu",
    "🎄 Noel Süsleri",
    "🎅 Noel Baba Koleksiyonu",
    "✨ Işıklı Ürünler",
    "🧦 Noel Çorapları",
    "📚 Kitap & Dergi"
]

# Ürün isimleri (kategoriye özel)
PRODUCT_NAMES = {
    "🎁 Noel Hediyeleri": [
        "Elf Yapımı Özel Hediye Kutusu",
        "Noel Şekerleme Seti",
        "Kişiye Özel Hediye Paketi",
        "Büyülü Hediye Sepeti",
        "Premium Noel Koleksiyonu"
    ],
    "👕 Noel Temalı Giysiler": [
        "Noel Desenli Kazak",
        "Noel Baba Sweatshirt",
        "Ren Geyiği Desenli Tişört",
        "Elf Şapkalı Pijama Takımı",
        "Noel Temalı Atkı & Bere Seti"
    ],
    "🍫 Özel Çikolatalar": [
        "Elf Yapımı Çikolata Kutusu",
        "Noel Çikolata Kalıpları",
        "Premium Bitter Çikolata",
        "Kar Taneli Beyaz Çikolata",
        "Çikolata Kaplı Fındık Seti"
    ],
    "☕ Noel Bardakları": [
        "Noel Temalı Seramik Bardak",
        "Termos Noel Kupası",
        "Kişiye Özel Baskılı Bardak",
        "Noel Işıklı Bardak",
        "Luxury Kahve Seti"
    ],
    "🏠 Ev Dekorasyonu": [
        "Noel Kapı Süsü",
        "Mantar Perde Aksesuarı",
        "Noel Rüyası Avize",
        "Elf Desenli Halı",
        "Duvar Dekorasyon Seti"
    ],
    "🎄 Noel Süsleri": [
        "Kristal Noel Topu",
        "Elf Figürlü Süs",
        "Işıklı Dallar Seti",
        "Yıldız Çıngırak",
        "Gümüş Renkli Süsler"
    ],
    "🎅 Noel Baba Koleksiyonu": [
        "Noel Baba Figürü",
        "Noel Baba Şapkası",
        "Sakallı Noel Baba Heykeli",
        "Noel Baba Anahtarlığı",
        "Koleksiyonluk Noel Baba"
    ],
    "✨ Işıklı Ürünler": [
        "LED Noel Işıkları",
        "Pilates Topu LED",
        "Işıklı Noel Ağacı",
        "Fiber Optik Dekor",
        "Renk Değiştiren Lamba"
    ],
    "🧦 Noel Çorapları": [
        "Noel Desenli Çorap",
        "Ren Geyiği Çorap",
        "Kar Tanesi Desenli",
        "Noel Baba Çorabı",
        "Çift Kişilik Çorap Seti"
    ],
    "📚 Kitap & Dergi": [
        "Noel Hikayeleri Kitabı",
        "Yemek Tarifleri Dergisi",
        "El Sanatları Rehberi",
        "Noel Şarkıları Notası",
        "Özel Baskı Albüm"
    ]
}

def generate_products():
    """150 benzersiz ürün oluştur"""
    products = []
    
    for i in range(1, 151):
        category = random.choice(CATEGORIES)
        name_list = PRODUCT_NAMES.get(category, ["Noel Ürünü"])
        name = f"{random.choice(name_list)} {random.choice(['Deluxe', 'Premium', 'Limited', 'Special', 'Gold'])}"
        
        # Fiyat aralıkları (TL)
        price_ranges = {
            "🎁 Noel Hediyeleri": (150, 1200),
            "👕 Noel Temalı Giysiler": (200, 800),
            "🍫 Özel Çikolatalar": (50, 400),
            "☕ Noel Bardakları": (80, 350),
            "🏠 Ev Dekorasyonu": (100, 1500),
            "🎄 Noel Süsleri": (30, 300),
            "🎅 Noel Baba Koleksiyonu": (120, 900),
            "✨ Işıklı Ürünler": (150, 1200),
            "🧦 Noel Çorapları": (40, 200),
            "📚 Kitap & Dergi": (25, 180)
        }
        
        min_price, max_price = price_ranges.get(category, (50, 500))
        price = round(random.uniform(min_price, max_price), 2)
        
        products.append({
            "id": i,
            "name": f"{name} #{i}",
            "description": generate_description(category),
            "price": price,
            "category": category,
            "image": f"urun_{((i-1) % 30) + 1}.jpg",
            "in_stock": random.choice([True, True, True, False]),  # %75 stokta
            "rating": round(random.uniform(3.5, 5.0), 1),
            "discount": random.choice([0, 0, 0, 10, 15, 20, 25]),  # Bazıları indirimli
            "featured": i <= 20,  # İlk 20 ürün öne çıkan
            "created_at": datetime.now().strftime("%Y-%m-%d")
        })
    
    return products

def generate_description(category):
    """Kategoriye özel açıklama oluştur"""
    descriptions = {
        "🎁 Noel Hediyeleri": "Özel olarak hazırlanmış, sevdiklerinize verebileceğiniz en güzel hediye. Elf ustalarının el emeği ile üretilmiştir.",
        "👕 Noel Temalı Giysiler": "%100 pamuk, yumuşak ve konforlu kumaş. Noel ruhunu yansıtan özel tasarım.",
        "🍫 Özel Çikolatalar": "Belçika çikolatası kullanılarak üretilmiştir. Gluten içermez, doğal aroma ile tatlandırılmıştır.",
        "☕ Noel Bardakları": "Seramik yapı, el dekorasyonu. Bulaşık makinesinde yıkanabilir, mikrodalgaya uygun.",
        "🏠 Ev Dekorasyonu": "Evini noel ruhuyla süsle. Kaliteli malzeme, uzun ömürlü kullanım.",
        "🎄 Noel Süsleri": "El yapımı, her biri özenle hazırlanmış. Işık yansıtıcı özel kaplama.",
        "🎅 Noel Baba Koleksiyonu": "Koleksiyon değeri olan, sınırlı sayıda üretilmiş özel parça.",
        "✨ Işıklı Ürünler": "LED teknolojisi, enerji tasarruflu, uzaktan kumandalı.",
        "🧦 Noel Çorapları": "Yumuşak pamuk, esnek yapı. Çift kişilik set halinde sunulmaktadır.",
        "📚 Kitap & Dergi": "Özel ciltleme, kaliteli kağıt. Noel ruhunu yaşatan içerikler."
    }
    
    return descriptions.get(category, "Özel noel ürünü, sınırlı stok!")

def load_products():
    """Ürünleri yükle veya oluştur"""
    try:
        with open('products.json', 'r', encoding='utf-8') as f:
            products = json.load(f)
            # Eski ürünleri yeni formata dönüştür
            if products and 'price' in products[0] and products[0]['price'] > 1000:  # Altın kontrolü
                print("⚠️  Eski ürünler tespit edildi, yeni formata dönüştürülüyor...")
                products = generate_products()
                save_products(products)
            return products
    except FileNotFoundError:
        print("📦 Ürün dosyası bulunamadı, yeni ürünler oluşturuluyor...")
        products = generate_products()
        save_products(products)
        return products

def save_products(products):
    """Ürünleri kaydet"""
    with open('products.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=4)

PRODUCTS = load_products()

# Sepet işlemleri
def get_cart():
    if 'cart' not in session:
        session['cart'] = []
    return session['cart']

def add_to_cart(product_id, quantity=1):
    cart = get_cart()
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] += quantity
            session.modified = True
            return
    
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product:
        discounted_price = product['price'] * (1 - product.get('discount', 0) / 100)
        cart.append({
            'product_id': product_id,
            'quantity': quantity,
            'name': product['name'],
            'price': discounted_price,
            'original_price': product['price'],
            'discount': product.get('discount', 0),
            'image': product['image'],
            'category': product['category']
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

# Rotalar
@app.route('/')
def index():
    return render_template('index.html', 
                          cart_count=get_cart_count(),
                          categories=CATEGORIES)

@app.route('/magic_shop')
def magic_shop():
    return render_template('magic_shop.html', 
                          products=PRODUCTS,
                          categories=CATEGORIES,
                          cart_count=get_cart_count())

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return "Ürün bulunamadı", 404
    
    # Benzer ürünler (aynı kategoriden)
    similar_products = [p for p in PRODUCTS 
                       if p['category'] == product['category'] 
                       and p['id'] != product_id][:6]
    
    # İndirimli fiyat
    discounted_price = product['price'] * (1 - product.get('discount', 0) / 100)
    
    return render_template('product_detail.html', 
                          product=product,
                          discounted_price=discounted_price,
                          similar_products=similar_products,
                          cart_count=get_cart_count())

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart_route(product_id):
    add_to_cart(product_id)
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart_route(product_id):
    remove_from_cart(product_id)
    return redirect(url_for('cart'))

@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart_route(product_id):
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
    cart_items = get_cart()
    total = get_cart_total()
    return render_template('cart.html', 
                          cart_items=cart_items, 
                          total=total,
                          cart_count=len(cart_items))

@app.route('/clear_cart')
def clear_cart():
    session['cart'] = []
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    cart_items = get_cart()
    if not cart_items:
        return redirect(url_for('cart'))
    
    total = get_cart_total()
    return render_template('checkout.html', 
                          cart_items=cart_items, 
                          total=total,
                          cart_count=len(cart_items))

@app.route('/category/<category_name>')
def category_products(category_name):
    filtered_products = [p for p in PRODUCTS if p['category'] == category_name]
    return render_template('magic_shop.html',
                         products=filtered_products,
                         categories=CATEGORIES,
                         selected_category=category_name,
                         cart_count=get_cart_count())

# API endpoint'leri
@app.route('/api/products')
def api_products():
    return json.dumps(PRODUCTS, ensure_ascii=False)

@app.route('/api/cart')
def api_cart():
    return json.dumps(get_cart(), ensure_ascii=False)

@app.route('/api/stats')
def api_stats():
    return json.dumps({
        'total_products': len(PRODUCTS),
        'categories': len(CATEGORIES),
        'total_value': sum(p['price'] for p in PRODUCTS),
        'in_stock': sum(1 for p in PRODUCTS if p['in_stock'])
    })

if __name__ == '__main__':
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    if not os.path.exists('products.json'):
        save_products(PRODUCTS)
    
    print("\n" + "="*70)
    print("🎅 GİZLİ ELF PAZARI - PROFESYONEL NOEL ALIŞVERİŞ SİTESİ 🎄")
    print("="*70)
    print("\n✨ ÖZELLİKLER:")
    print("   ✅ 10 Farklı Kategori")
    print("   ✅ 150 Benzersiz Ürün")
    print("   ✅ Türk Lirası (₺) Desteği")
    print("   ✅ İndirimli Ürün Sistemi")
    print("   ✅ Kategori Filtreleme")
    print("   ✅ Responsive Tasarım")
    print("   ✅ Sepet Sistemi")
    print("   ✅ Büyülü Orman Teması")
    print("\n📦 KATEGORİLER:")
    for i, cat in enumerate(CATEGORIES, 1):
        count = sum(1 for p in PRODUCTS if p['category'] == cat)
        print(f"   {i:2d}. {cat} ({count} ürün)")
    print("\n💰 TOPLAM DEĞER: {:,} ₺".format(int(sum(p['price'] for p in PRODUCTS))))
    print("🌐 Tarayıcınızda açın: http://localhost:5000")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)