from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Ana sayfa - büyülü orman giriş sayfası"""
    return render_template('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Statik dosyaları sun"""
    return send_from_directory('static', filename)

@app.route('/magic_shop')
def magic_shop():
    """Büyülü alışveriş sayfası"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Büyülü Yeni Yıl Pazarı | Yapım Aşamasında</title>
        <style>
            body {
                background: #0a150a;
                color: #d4af37;
                font-family: 'Cinzel Decorative', serif;
                text-align: center;
                padding: 50px;
                background-image: 
                    radial-gradient(circle at 20% 30%, rgba(212, 175, 55, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 80% 70%, rgba(42, 111, 151, 0.1) 0%, transparent 50%);
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: rgba(10, 30, 10, 0.9);
                padding: 50px;
                border-radius: 30px;
                border: 3px solid rgba(212, 175, 55, 0.5);
                box-shadow: 
                    0 0 50px rgba(212, 175, 55, 0.3),
                    inset 0 0 50px rgba(0, 0, 0, 0.5);
            }
            h1 {
                font-size: 3.5rem;
                margin-bottom: 30px;
                text-shadow: 0 0 20px rgba(212, 175, 55, 0.8);
            }
            p {
                font-size: 1.5rem;
                margin-bottom: 20px;
                line-height: 1.6;
            }
            .magic {
                font-size: 4rem;
                margin: 30px 0;
                animation: float 3s infinite ease-in-out;
            }
            @keyframes float {
                0%, 100% { transform: translateY(0) rotate(0deg); }
                50% { transform: translateY(-20px) rotate(5deg); }
            }
            a {
                color: #ffde7d;
                text-decoration: none;
                border: 2px solid #d4af37;
                padding: 15px 40px;
                border-radius: 30px;
                display: inline-block;
                margin-top: 40px;
                font-size: 1.3rem;
                background: rgba(212, 175, 55, 0.1);
                transition: all 0.3s ease;
            }
            a:hover {
                background: rgba(212, 175, 55, 0.3);
                transform: scale(1.1);
                box-shadow: 0 0 30px rgba(212, 175, 55, 0.5);
            }
            .coming-soon {
                display: flex;
                justify-content: center;
                gap: 30px;
                margin-top: 40px;
                flex-wrap: wrap;
            }
            .item {
                background: rgba(26, 90, 26, 0.5);
                padding: 20px;
                border-radius: 15px;
                border: 1px solid rgba(212, 175, 55, 0.3);
                width: 150px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="magic">🧝‍♀️🎄✨🧙‍♂️🎁</div>
            <h1>Büyülü Yeni Yıl Pazarı</h1>
            <p>Elf zanaatkarları ve peri tasarımcıları pazarı hazırlıyor...</p>
            <p>🎁 Yeni Yıl'a özel büyülü ürünler yakında sizlerle!</p>
            <p>⏳ Lütfen biraz daha bekleyin, sihir devam ediyor!</p>
            
            <div class="coming-soon">
                <div class="item">✨ Büyülü Süsler</div>
                <div class="item">🎄 Elf El Yapımı Hediyeler</div>
                <div class="item">🔮 Peri Tozu</div>
                <div class="item">📜 Antik Tarifler</div>
            </div>
            
            <a href="/">Ormana Geri Dön</a>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎄 BÜYÜLÜ YENİ YIL ORMANI 🎄")
    print("="*60)
    print("\n🌲 Sunucu başlatılıyor...")
    print("🌐 Lütfen tarayıcınızda şu adresi açın:")
    print("   → http://localhost:5000")
    print("\n🎮 KULLANIM KILAVUZU:")
    print("   📍 AŞAĞI OK tuşu veya fare tekerleği ile aşağı kaydırın")
    print("   📍 YUKARI OK tuşu ile yukarı kaydırın")
    print("   📍 TAB tuşu ile bölümler arasında geçiş yapın")
    print("   📍 Başlangıç/Kapıya Git butonları ile hızlı geçiş")
    print("   📍 3 saniye sonra otomatik keşif başlayacak")
    print("\n✨ YENİ ÖZELLİKLER:")
    print("   ✅ Gerçekçi çam, meşe ve kavak ağaçları")
    print("   ✅ Karanlık geceden mavi şafağa geçiş")
    print("   ✅ Karakter ışığı yolda ilerledikçe güçleniyor")
    print("   ✅ 3 farklı ağaç katmanı (uzak/orta/yakın)")
    print("   ✅ Yıldızlar ve ateşböcekleri efekti")
    print("   ✅ Büyük kapı tam açılıyor")
    print("   ✅ JavaScript KULLANILMADI - Sadece CSS/HTML")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)