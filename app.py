import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- SABİT AYARLAR ---
GÖNDEREN_EMAIL = "piyazsosu@gmail.com"
UYGULAMA_SIFRESI = "ikafvsebounnuhng"
WHATSAPP_NUMARASI = "905355739260"

# --- VERİ OKUMA ---
try:
    df = pd.read_csv('emlak_verileri.csv', sep=None, engine='python', encoding='utf-8-sig')
    df.columns = df.columns.str.strip()
except:
    st.error("⚠️ Veri dosyası yüklenemedi!")
    st.stop()

# --- MAİL GÖNDERME ---
def mail_gonder(konu, icerik):
    try:
        mesaj = MIMEMultipart()
        mesaj['From'] = GÖNDEREN_EMAIL
        mesaj['To'] = GÖNDEREN_EMAIL
        mesaj['Subject'] = konu
        mesaj.attach(MIMEText(icerik, 'plain'))
        sunucu = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        sunucu.login(GÖNDEREN_EMAIL, UYGULAMA_SIFRESI)
        sunucu.sendmail(GÖNDEREN_EMAIL, GÖNDEREN_EMAIL, mesaj.as_string())
        sunucu.quit()
        return True
    except:
        return False

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Emlak Firması | Fiyat Analizi", page_icon="🏡", layout="wide")

# --- STİL DÜZENLEME (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #fcfcfc; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; font-weight: bold; }
    .hero-text { text-align: center; padding: 20px; background-color: #1e3d59; color: white; border-radius: 15px; margin-bottom: 25px; }
    .feature-box { padding: 20px; border-radius: 10px; border: 1px solid #eee; background-color: white; text-align: center; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- YAN MENÜ (SIDEBAR) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/608/608978.png", width=100)
    st.title("Selman Güneş")
    st.subheader("Gayrimenkul Danışmanı")
    st.write("📍 Bölgenizdeki mülklerin doğru değerini bulması için profesyonel destek sunuyorum.")
    
    st.write("---")
    st.write("📱 **Beni Takip Edin**")
    st.link_button("📸 Instagram", "https://instagram.com/selmangunesemlak", use_container_width=True)
    st.link_button("🔵 Facebook", "https://facebook.com/emlakfirma", use_container_width=True)
    st.link_button("💬 WhatsApp Destek", f"https://wa.me/{WHATSAPP_NUMARASI}", use_container_width=True)
    st.write("---")
    st.info("Hafta içi & Sonu: 09:00 - 20:00")

# --- ANA SAYFA GİRİŞ (HERO SECTION) ---
st.markdown("""
    <div class="hero-text">
        <h1>Mülkünüzün Gerçek Değerini Bugün Öğrenin!</h1>
        <p>Yanlış fiyatlandırma zaman ve nakit kaybettirir. Uzman verileriyle doğru başlangıç yapın.</p>
    </div>
    """, unsafe_allow_html=True)

# --- AVANTAJLAR (NEDEN BİZ?) ---
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""<div class="feature-box"><h3>🔍 Güncel Veri</h3><p>Piyasadaki son 6 ayın gerçek satış rakamlarını baz alıyoruz.</p></div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="feature-box"><h3>⚡ Hızlı Ekspertiz</h3><p>Formu doldurduktan sonra 24 saat içinde detaylı rapor sunuyoruz.</p></div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""<div class="feature-box"><h3>🤝 Ücretsiz Danışmanlık</h3><p>Analiz sonrası satış stratejinizi birlikte belirliyoruz.</p></div>""", unsafe_allow_html=True)

st.write("---")

# --- ANALİZ FORMU ---
st.header("📋 Ücretsiz Ön Analiz Formu")
st.write("Lütfen mülkünüzün detaylarını girin, piyasa verileriyle kıyaslayalım.")

with st.form("ekspertiz_formu"):
    col_a, col_b = st.columns(2)
    with col_a:
        mahalle = st.selectbox("📍 Mahalle:", df['Mahalle'].unique())
        oda = st.selectbox("🛏️ Oda Sayısı:", ["1+1", "2+1", "3+1", "4+1", "5+1", "Dubleks"])
        bina_yasi = st.number_input("⏳ Bina Yaşı:", 0, 100, 5)
        asansor = st.radio("🛗 Asansör Durumu:", ["Var", "Yok"], horizontal=True)

    with col_b:
        cephe = st.selectbox("☀️ Cephe Bilgisi:", ["Güney", "Kuzey", "Doğu", "Batı", "Güney-Doğu", "Güney-Batı"])
        kat_sayisi = st.number_input("🏢 Binadaki Toplam Kat:", 1, 50, 5)
        bulundugu_kat = st.selectbox("⬆️ Dairenin Katı:", ["Giriş", "1", "2", "3", "4", "5", "10+", "En Üst"])
        m2 = st.number_input("📏 Net Metrekare:", 30, 1000, 100)

    notlar = st.text_area("📝 Dairenizin Ayırt Edici Özellikleri:", placeholder="Örn: Deniz manzaralı, yeni tadilatlı, site içerisinde...")
    
    st.markdown("### 👤 İletişim")
    ad = st.text_input("Adınız Soyadınız:")
    tel = st.text_input("Telefon Numaranız:")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        submit_mail = st.form_submit_button("📧 Mail İle Analiz İste")
    with col_f2:
        submit_wa = st.form_submit_button("💬 WhatsApp'tan Bilgi Al")

# --- SONUÇ VE AKSİYON ---
if submit_mail or submit_wa:
    if not ad or not tel:
        st.warning("⚠️ Lütfen size ulaşabilmemiz için adınızı ve telefonunuzu girin.")
    else:
        filtre = df[(df['Mahalle'] == mahalle) & (df['Oda_Sayisi'] == oda)]
        min_f = f"{int(filtre['Fiyat'].min()):,}".replace(',', '.') if not filtre.empty else "---"
        max_f = f"{int(filtre['Fiyat'].max()):,}".replace(',', '.') if not filtre.empty else "---"
        
        bilgi_metni = f"""
        YENİ MÜŞTERİ TALEBİ!
        Müşteri: {ad} | Tel: {tel}
        Mülk: {mahalle}, {oda}, {bina_yasi} Yaş, {cephe} Cephe
        Kat: {bulundugu_kat}/{kat_sayisi}, Asansör: {asansor}, Alan: {m2}m2
        Müşteri Notu: {notlar}
        Tahmini Aralık: {min_f} - {max_f} TL
        """

        if submit_mail:
            if mail_gonder(f"Yeni Analiz - {ad}", bilgi_metni):
                st.success("✅ Talebiniz başarıyla e-posta ile iletildi. En kısa sürede döneceğim.")
                st.balloons()

        if submit_wa:
            st.success("💬 Analiz verileriniz hazırlandı, WhatsApp'a yönlendiriliyorsunuz...")
            wa_link = f"https://wa.me/{WHATSAPP_NUMARASI}?text={bilgi_metni.replace(' ', '%20').replace('\n', '%0A')}"
            st.link_button("📲 Mesajı Selman Güneş'e Gönder", wa_link, type="primary", use_container_width=True)

        st.markdown(f"""
            <div style="background-color:#e8f4ea; padding:30px; border-radius:15px; border:2px solid #2e7d32; text-align:center; margin-top:20px;">
                <h3 style="color:#2e7d32;">Bölgenizdeki Tahmini Değer Aralığı</h3>
                <h2 style="color:#1b5e20;">₺{min_f} - ₺{max_f}</h2>
                <p style="color:#555;">Bu rakamlar piyasa ortalamasıdır. Net fiyat için mülkünüzü ziyaret etmemiz gerekir.</p>
            </div>
        """, unsafe_allow_html=True)
