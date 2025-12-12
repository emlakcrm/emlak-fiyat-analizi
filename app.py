import streamlit as st
import pandas as pd
import smtplib
import urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# =========================================================
# 🛠️ 1. AYARLAR VE GÜVENLİK
# =========================================================
def ayar_getir(anahtar, varsayilan):
    try:
        return st.secrets[anahtar]
    except:
        return varsayilan

GÖNDEREN_EMAIL = ayar_getir("GÖNDEREN_EMAIL", "piyazsosu@gmail.com")
UYGULAMA_SIFRESI = ayar_getir("UYGULAMA_SIFRESI", "ikafvsebounnuhng")
WHATSAPP_NUMARASI = ayar_getir("WHATSAPP_NUMARASI", "905355739260")

# =========================================================
# 📊 2. VERİ YÜKLEME
# =========================================================
try:
    df = pd.read_csv('emlak_verileri.csv', sep=None, engine='python', encoding='utf-8-sig')
    df.columns = df.columns.str.strip()
except:
    st.error("⚠️ Veri dosyası (CSV) bulunamadı.")
    st.stop()

# =========================================================
# 🎨 3. GÖRSEL TASARIM (EMLAK CRM KOYU YEŞİL TEMA)
# =========================================================
st.set_page_config(page_title="Analiz | Selman Güneş", page_icon="🏡", layout="wide")

st.markdown("""
    <style>
    /* Ana Font ve Arka Plan */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    .main { background-color: #f8faf9; }

    /* Header Tasarımı */
    header {
        background-color: #0b3d2e; /* Koyu Orman Yeşili */
        color: white;
        padding: 40px 20px;
        text-align: center;
        border-radius: 0 0 30px 30px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    header h1 { color: #ffffff !important; font-size: 32px !important; font-weight: 600; margin-bottom: 10px; }
    header .lead { font-size: 18px; opacity: 0.9; margin-bottom: 25px; }
    
    /* Navigasyon ve Hover Efekti */
    header nav a {
        color: #ffffff !important;
        text-decoration: none;
        margin: 0 15px;
        font-weight: 500;
        padding: 8px 15px;
        transition: 0.3s all ease;
        border-radius: 5px;
    }
    header nav a:hover {
        background-color: #2e7d32; /* Üzerine gelince yeşil */
        color: white !important;
    }

    /* Form ve Buton Tasarımı */
    .stForm {
        background-color: white !important;
        padding: 40px !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05) !important;
        border: 1px solid #e1e8e5 !important;
    }
    .stButton>button {
        background-color: #0b3d2e !important;
        color: white !important;
        border-radius: 10px !important;
        height: 3.5em !important;
        width: 100%;
        font-weight: bold;
        transition: 0.4s ease;
    }
    .stButton>button:hover {
        background-color: #2e7d32 !important; /* Buton hover */
        border: none;
        transform: translateY(-2px);
    }

    /* Kartlar */
    .info-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        border-bottom: 4px solid #0b3d2e;
        transition: 0.3s;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    }
    .info-card:hover { transform: translateY(-5px); box-shadow: 0 8px 20px rgba(0,0,0,0.08); }
    .info-card h4 { color: #0b3d2e; }

    /* Footer */
    .footer {
        text-align: center;
        padding: 50px;
        background-color: #0b3d2e;
        color: #e1e8e5;
        margin-top: 60px;
        border-radius: 30px 30px 0 0;
    }
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# 🏗️ 4. HEADER BÖLÜMÜ
# =========================================================
st.markdown("""
    <header>
        <div class="wrap">
            <h1>Selman Güneş — Kepez & Antalya Gayrimenkul Danışmanı</h1>
            <p class="lead">Kepez bölgesinde güven, şeffaflık ve sonuç odaklı emlak danışmanlığı.</p>
            <nav>
                <a href="https://emlakcrm.github.io/emlak/index.html">Ana Sayfa</a>
                <a href="https://emlakcrm.github.io/emlak/hakkimizda.html">Hakkımızda</a>
                <a href="https://emlakcrm.github.io/emlak/ilanlar.html">İlanlar</a>
                <a href="https://emlakcrm.github.io/emlak/analiz.html">Analiz</a>
                <a href="https://emlakcrm.github.io/emlak/iletisim.html">İletişim</a>
            </nav>
        </div>
    </header>
    """, unsafe_allow_html=True)

# =========================================================
# 📋 5. ANALİZ FORMU (Lead Generation)
# =========================================================
st.markdown("### 📊 Gayrimenkul Ön Analiz Formu")
st.write("Bilgilerinizi bırakın, bölge verileriyle mülkünüzü saniyeler içinde analiz edelim.")

with st.form("ekspertiz_formu"):
    c1, c2 = st.columns(2)
    with c1:
        mahalle = st.selectbox("📍 Mahalle Seçiniz:", df['Mahalle'].unique())
        oda = st.selectbox("🛏️ Oda Sayısı:", ["1+1", "2+1", "3+1", "4+1", "5+1", "Dubleks"])
        bina_yasi = st.number_input("⏳ Bina Yaşı:", 0, 100, 5)
        asansor = st.radio("🛗 Asansör:", ["Var", "Yok"], horizontal=True)

    with c2:
        cephe = st.selectbox("☀️ Cephe:", ["Güney", "Kuzey", "Doğu", "Batı", "Güney-Doğu", "Güney-Batı"])
        kat_sayisi = st.number_input("🏢 Toplam Kat:", 1, 50, 5)
        bulundugu_kat = st.selectbox("⬆️ Dairenin Katı:", ["Giriş", "1", "2", "3", "4", "5", "10+", "En Üst"])
        m2 = st.number_input("📏 Net Metrekare:", 30, 1000, 100)

    notlar = st.text_area("📝 Eklemek İstediğiniz Detaylar:", placeholder="Örn: Site içerisinde, havuz manzaralı, yeni tadilatlı...")
    
    st.markdown("---")
    st.markdown("#### 👤 İletişim Bilgileri")
    ad = st.text_input("Adınız Soyadınız:")
    tel = st.text_input("Telefon Numaranız:")
    
    btn1, btn2 = st.columns(2)
    submit_mail = btn1.form_submit_button("📧 Mail İle Analiz İstiyorum")
    submit_wa = btn2.form_submit_button("💬 WhatsApp İle Bilgi Al")

# =========================================================
# ⚙️ 6. İŞLEMLER VE SONUÇ
# =========================================================
if submit_mail or submit_wa:
    if not ad or not tel:
        st.warning("⚠️ Size ulaşabilmemiz için adınızı ve telefonunuzu girmelisiniz.")
    else:
        # Fiyat Tahmini
        filtre = df[(df['Mahalle'] == mahalle) & (df['Oda_Sayisi'] == oda)]
        min_v = int(filtre['Fiyat'].min()) if not filtre.empty else 0
        max_v = int(filtre['Fiyat'].max()) if not filtre.empty else 0
        f_goster = f"₺{min_v:,} - ₺{max_v:,}".replace(',', '.') if min_v > 0 else "Bölge Uzmanına Danışın"
        
        mesaj = (f"Selman Bey Yeni Analiz Talebi!\n"
                 f"👤 Müşteri: {ad}\n📞 Tel: {tel}\n"
                 f"📍 Mahalle: {mahalle} | {oda}\n"
                 f"📐 Alan: {m2}m2 | Kat: {bulundugu_kat}/{kat_sayisi}\n"
                 f"📝 Not: {notlar}\n💰 Tahmin: {f_goster}")

        if submit_wa:
            encoded_wa = urllib.parse.quote(mesaj)
            st.success("✅ Verileriniz hazırlandı!")
            st.link_button("📲 ANALİZİ WHATSAPP'TAN TAMAMLA", f"https://wa.me/{WHATSAPP_NUMARASI}?text={encoded_wa}", type="primary", use_container_width=True)

        st.markdown(f"""
            <div style="background-color:white; padding:35px; border-radius:20px; border:3px solid #0b3d2e; text-align:center; margin-top:20px;">
                <h3 style="color:#0b3d2e; margin:0;">Mülkünüz İçin Tahmini Değer</h3>
                <h1 style="color:#2e7d32; font-size:48px; margin:10px 0;">{f_sonuc if 'f_sonuc' in locals() else f_goster}</h1>
                <p style="color:#666;">Piyasa ortalamasıdır. Net rapor için Selman Güneş ile iletişime geçiniz.</p>
            </div>
        """, unsafe_allow_html=True)

# =========================================================
# 🃏 7. TANITIM KARTLARI
# =========================================================
st.write("---")
k1, k2, k3 = st.columns(3)
with k1:
    st.markdown('<div class="info-card"><h4>📍 Bölge Analizi</h4><p>Kepez ve çevresindeki gerçek satış verilerini süzüyoruz.</p></div>', unsafe_allow_html=True)
with k2:
    st.markdown('<div class="info-card"><h4>📏 Detaylı Kriter</h4><p>Bina yaşı, cephe ve kat gibi teknik detayları hesaplıyoruz.</p></div>', unsafe_allow_html=True)
with k3:
    st.markdown('<div class="info-card"><h4>🤝 Uzman Desteği</h4><p>Selman Güneş ile mülkünüzün satış sürecini profesyonelleştirin.</p></div>', unsafe_allow_html=True)

# =========================================================
# 🏁 8. FOOTER (SOSYAL BAĞLANTILAR)
# =========================================================
st.markdown(f"""
    <div class="footer">
        <h3>Selman Güneş Gayrimenkul</h3>
        <p>Kepez / Antalya</p>
        <div style="margin: 20px 0;">
            <a href="https://instagram.com/selmangunesemlak" style="color:white; margin:0 10px; text-decoration:none;">📸 Instagram</a> | 
            <a href="https://facebook.com/emlakfirma" style="color:white; margin:0 10px; text-decoration:none;">🔵 Facebook</a> | 
            <a href="https://wa.me/{WHATSAPP_NUMARASI}" style="color:white; margin:0 10px; text-decoration:none;">💬 WhatsApp</a>
        </div>
        <hr style="opacity:0.2;">
        <p>© 2024 Selman Güneş Emlak | Tüm Hakları Saklıdır.</p>
        <p>İletişim: {WHATSAPP_NUMARASI}</p>
    </div>
    """, unsafe_allow_html=True)
