# app.py - GÜNCELLENMİŞ
from flask import Flask, render_template, send_from_directory
import os
import json

app = Flask(__name__)

# Ürün verileri (150 ürün)
PRODUCTS = [
    {
        "id": i,
        "name": f"Büyülü Noel Süsü {i}",
        "description": "Elf zanaatkarları tarafından hazırlanmış, ışık saçan özel süs",
        "price": f"{(i % 10 + 1) * 25}.99",
        "image": f"product_{(i % 20) + 1}.jpg" if i < 20 else "product_default.jpg"
    }
    for i in range(1, 151)
]

@app.route('/')
def index():
    """Ana sayfa - Gizli Elf Pazarı büyülü giriş"""
    return render_template('index.html')

@app.route('/magic_shop')
def magic_shop():
    """Elf Pazarı ana sayfası - 150 ürünlü"""
    return render_template('magic_shop.html', products=PRODUCTS)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Ürün detay sayfası"""
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return "Ürün bulunamadı", 404
    return render_template('product_detail.html', product=product)

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Statik dosyaları sun"""
    return send_from_directory('static', filename)

@app.route('/images/<path:filename>')
def serve_images(filename):
    """Resim dosyalarını sun"""
    return send_from_directory('images', filename)

if __name__ == '__main__':
    # Gerekli klasörleri oluştur
    os.makedirs('static', exist_ok=True)
    os.makedirs('images', exist_ok=True)
    
    print("\n" + "="*60)
    print("🎄 PROFESYONEL ELF PAZARI - BÜYÜLÜ ALIŞVERİŞ 🎁")
    print("="*60)
    print("\n✨ ÖZELLİKLER:")
    print("   ✅ Profesyonel elf karakter tasarımı")
    print("   ✅ Gerçekçi orman atmosferi")
    print("   ✅ Düzgün patika tasarımı")
    print("   ✅ 150 ürünlük pazar alanı")
    print("   ✅ Ürün kartları ve detay sayfaları")
    print("   ✅ Büyük Noel ağacı ve Ortodoks ikonu")
    print("   ✅ Gelişmiş scrollbar tasarımı")
    print("   ✅ Responsive ve modern tasarım")
    print("\n🛒 ÜRÜN SAYISI: 150 adet")
    print("🌲 RESİM KLASÖRÜ: /images/")
    print("🎨 TASARIM: Tamamen CSS + HTML")
    print("\n🌐 Tarayıcınızda açın: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)