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
    st.error("⚠️ Veri dosyası bulunamadı.")
    st.stop()

# =========================================================
# 📧 3. E-POSTA MOTORU
# =========================================================
def mail_gonder(konu, icerik):
    try:
        mesaj = MIMEMultipart()
        mesaj['From'] = GÖNDEREN_EMAIL
        mesaj['To'] = GÖNDEREN_EMAIL
        mesaj['Subject'] = konu
        mesaj.attach(MIMEText(icerik, 'plain'))
        sunucu = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        sunucu.login(GÖNDEREN_EMAIL, UYGULAMA_SIFRESI.replace(" ", ""))
        sunucu.sendmail(GÖNDEREN_EMAIL, GÖNDEREN_EMAIL, mesaj.as_string())
        sunucu.quit()
        return True
    except:
        return False

# =========================================================
# 🎨 4. GÖRSEL TASARIM (EMLAK CRM RENKLERİ)
# =========================================================
st.set_page_config(page_title="Emlak Firmasi | Analiz", page_icon="🏡", layout="wide")

st.markdown("""
    <style>
    /* Genel Font ve Arka Plan */
    .main { background-color: #f4f7f6; }
    
    /* Header & Navigasyon */
    header {
        background-color: #1A4339;
        color: white;
        padding: 40px 20px;
        text-align: center;
        border-radius: 0 0 20px 20px;
        margin-bottom: 30px;
    }
    header h1 { color: #ffffff !important; font-size: 28px !important; margin-bottom: 10px; }
    header .lead { font-size: 18px; opacity: 0.9; margin-bottom: 20px; }
    header nav a {
        color: #3498db !important;
        text-decoration: none;
        margin: 0 15px;
        font-weight: bold;
        font-size: 15px;
    }
    header nav a:hover { color: white !important; }

    /* Form Kutusu */
    .stForm {
        background-color: white !important;
        padding: 30px !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        border: none !important;
    }

    /* Tanıtım Kartları */
    .info-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border-top: 4px solid #3498db;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin: 10px 0;
        min-height: 150px;
    }
    .info-card h4 { color: #2c3e50; margin-bottom: 10px; }
    .info-card p { color: #7f8c8d; font-size: 14px; }

    /* Footer */
    .footer {
        text-align: center;
        padding: 40px;
        background-color: #2c3e50;
        color: #bdc3c7;
        margin-top: 50px;
        border-radius: 20px 20px 0 0;
    }
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# 🏗️ 5. SAYFA YAPISI (HEADER)
# =========================================================
st.markdown("""
    <header>
        <div class="wrap">
            <h1>Selman Güneş — Kepez & Antalya Gayrimenkul Danışmanı</h1>
            <p class="lead">Kepez bölgesinde güven, şeffaflık ve sonuç odaklı emlak danışmanlığı.</p>
            <nav>
                <a href="https://emlakcrm.github.io/emlak/index.html">Ana Sayfa</a>
                <a href="#">Hakkımızda</a>
                <a href="#">İlanlar</a>
                <a href="#">Antalya</a>
                <a href="#">Form</a>
                <a href="#">İletişim</a>
            </nav>
        </div>
    </header>
    """, unsafe_allow_html=True)

# =========================================================
# 📋 6. ANA FORM (EKSPERTİZ)
# =========================================================
with st.form("ekspertiz_formu"):
    st.subheader("🏡 Ücretsiz Mülk Değerleme Formu")
    col1, col2 = st.columns(2)
    
    with col1:
        mahalle = st.selectbox("📍 Mahalle:", df['Mahalle'].unique())
        oda = st.selectbox("🛏️ Oda Sayısı:", ["1+1", "2+1", "3+1", "4+1", "5+1", "Dubleks"])
        bina_yasi = st.number_input("⏳ Bina Yaşı:", 0, 100, 5)
        asansor = st.radio("🛗 Asansör:", ["Var", "Yok"], horizontal=True)

    with col2:
        cephe = st.selectbox("☀️ Cephe:", ["Güney", "Kuzey", "Doğu", "Batı", "Güney-Doğu", "Güney-Batı"])
        kat_sayisi = st.number_input("🏢 Toplam Kat:", 1, 50, 5)
        bulundugu_kat = st.selectbox("⬆️ Dairenin Katı:", ["Giriş", "1", "2", "3", "4", "5", "10+", "En Üst"])
        m2 = st.number_input("📏 Net Metrekare:", 30, 1000, 100)

    notlar = st.text_area("📝 Ek Özellikler:", placeholder="Daireniz hakkında bilmemiz gereken detaylar...")
    
    st.markdown("---")
    ad_soyad = st.text_input("Adınız Soyadınız:")
    telefon = st.text_input("Telefon Numaranız:")
    
    c_mail, c_wa = st.columns(2)
    with c_mail:
        sub_mail = st.form_submit_button("📧 Mail İle Analiz İstiyorum")
    with c_wa:
        sub_wa = st.form_submit_button("💬 WhatsApp İle Devam Et")

# =========================================================
# ⚙️ 7. İŞLEMLER VE ANALİZ KARTI
# =========================================================
if sub_mail or sub_wa:
    if not ad_soyad or not telefon:
        st.warning("⚠️ Lütfen iletişim bilgilerinizi eksiksiz girin.")
    else:
        filtre = df[(df['Mahalle'] == mahalle) & (df['Oda_Sayisi'] == oda)]
        min_f = int(filtre['Fiyat'].min()) if not filtre.empty else 0
        max_f = int(filtre['Fiyat'].max()) if not filtre.empty else 0
        f_sonuc = f"₺{min_f:,} - ₺{max_f:,}".replace(',', '.') if min_f > 0 else "Bölge Uzmanına Danışın"
        
        bilgi = (f"Yeni Talep: {ad_soyad}\nTel: {telefon}\n"
                 f"Mülk: {mahalle} - {oda} - {m2}m2\n"
                 f"Detay: Kat {bulundugu_kat}, {bina_yasi} Yaş, {cephe} Cephe\n"
                 f"Not: {notlar}\n\nTahmini Değer: {f_sonuc}")

        if sub_mail:
            if mail_gonder(f"Yeni Analiz - {ad_soyad}", bilgi):
                st.success("✅ Talebiniz e-posta ile iletildi.")
                st.balloons()

        if sub_wa:
            encoded_text = urllib.parse.quote(bilgi)
            st.success("✅ Analiz Raporu Hazır!")
            st.link_button("📲 WHATSAPP MESAJINI TAMAMLA", f"https://wa.me/{WHATSAPP_NUMARASI}?text={encoded_text}", type="primary", use_container_width=True)

        st.markdown(f"""
            <div style="background-color:#ffffff; padding:30px; border-radius:15px; border:2px solid #3498db; text-align:center; margin-top:20px;">
                <h3 style="color:#2c3e50; margin:0;">Tahmini Piyasa Değeri</h3>
                <h1 style="color:#2980b9; font-size:42px; margin:10px 0;">{f_sonuc}</h1>
            </div>
        """, unsafe_allow_html=True)

st.write("---")

# =========================================================
# 🃏 8. TANITIM KARTLARI (AŞAĞI TAŞINDI)
# =========================================================
card_col1, card_col2, card_col3 = st.columns(3)
with card_col1:
    st.markdown('<div class="info-card"><h4>📍 Bölge Analizi</h4><p>Mahallenizdeki benzer ilanların gerçek satış verileri incelenir.</p></div>', unsafe_allow_html=True)
with card_col2:
    st.markdown('<div class="info-card"><h4>📏 Detaylı Kriter</h4><p>Kat, cephe ve bina yaşı gibi 10 farklı kriter baz alınır.</p></div>', unsafe_allow_html=True)
with card_col3:
    st.markdown('<div class="info-card"><h4>🤝 Uzman Desteği</h4><p>Analiz sonrası Selman Güneş size özel yol haritası sunar.</p></div>', unsafe_allow_html=True)

# =========================================================
# 🏁 9. FOOTER (ALT BİLGİ)
# =========================================================
st.markdown(f"""
    <div class="footer">
        <p>© 2024 Selman Güneş Emlak | Tüm Hakları Saklıdır.</p>
        <p>İletişim: {WHATSAPP_NUMARASI} | Antalya / Türkiye</p>
    </div>
    """, unsafe_allow_html=True)
