import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# =========================================================
# 🛠️ AYARLAR (Buradaki bilgiler silinmediği sürece sistem çalışır)
# =========================================================
# Secrets varsa oradan okur, yoksa aşağıdaki bilgileri kullanır.
def ayar_getir(anahtar, varsayilan):
    try:
        return st.secrets[anahtar]
    except:
        return varsayilan

GÖNDEREN_EMAIL = ayar_getir("GÖNDEREN_EMAIL", "piyazsosu@gmail.com")
UYGULAMA_SIFRESI = ayar_getir("UYGULAMA_SIFRESI", "ikafvsebounnuhng")
WHATSAPP_NUMARASI = ayar_getir("WHATSAPP_NUMARASI", "905355739260")

# =========================================================
# 📊 VERİ OKUMA
# =========================================================
try:
    df = pd.read_csv('emlak_verileri.csv', sep=None, engine='python', encoding='utf-8-sig')
    df.columns = df.columns.str.strip()
except:
    st.error("⚠️ 'emlak_verileri.csv' dosyası bulunamadı!")
    st.stop()

# =========================================================
# 📧 MAİL GÖNDERME
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
    except Exception as e:
        # Hata olursa ekranda göster (Hata ayıklamak için önemli)
        st.sidebar.error(f"Mail Hatası: {e}")
        return False

# =========================================================
# 🖥️ ARAYÜZ TASARIMI
# =========================================================
st.set_page_config(page_title="Selman Güneş Emlak | Fiyat Analizi", page_icon="🏡", layout="wide")

# Görsel şıklık için CSS
st.markdown("""
    <style>
    .hero-box { text-align: center; padding: 30px; background-color: #1e3d59; color: white; border-radius: 15px; margin-bottom: 25px; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; font-weight: bold; background-color: #2e7d32; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Yan Menü (Sidebar)
with st.sidebar:
    st.title("Selman Güneş")
    st.write("📍 Antalya Gayrimenkul Danışmanı")
    st.write("---")
    st.link_button("📸 Instagram Profilim", "https://instagram.com/selmangunesemlak", use_container_width=True)
    st.link_button("🔵 Facebook Sayfam", "https://facebook.com/emlakfirma", use_container_width=True)
    st.link_button("💬 WhatsApp İletişim", f"https://wa.me/{WHATSAPP_NUMARASI}", use_container_width=True)

# Ana Başlık
st.markdown("""
    <div class="hero-box">
        <h1>Gayrimenkul Ön Fiyat Analiz Sistemi</h1>
        <p>Bilgileri girin, mülkünüzün piyasa değerini anında öğrenin.</p>
    </div>
    """, unsafe_allow_html=True)

# Form
with st.form("ekspertiz_formu"):
    col1, col2 = st.columns(2)
    with col1:
        mahalle = st.selectbox("Mahalle Seçiniz:", df['Mahalle'].unique())
        oda = st.selectbox("Oda Sayısı:", ["1+1", "2+1", "3+1", "4+1", "5+1", "Dubleks"])
        bina_yasi = st.number_input("Bina Yaşı:", 0, 100, 5)
        asansor = st.radio("Asansör:", ["Var", "Yok"], horizontal=True)

    with col2:
        cephe = st.selectbox("Cephe:", ["Güney", "Kuzey", "Doğu", "Batı", "Güney-Doğu", "Güney-Batı"])
        kat_sayisi = st.number_input("Binadaki Toplam Kat:", 1, 50, 5)
        bulundugu_kat = st.selectbox("Dairenin Katı:", ["Giriş", "1", "2", "3", "4", "5", "10+", "En Üst"])
        m2 = st.number_input("Net Metrekare:", 30, 1000, 100)

    notlar = st.text_area("Ek Detaylar (Cephe, manzara, tadilat vb.):")
    
    st.markdown("---")
    ad = st.text_input("Adınız Soyadınız:")
    tel = st.text_input("Telefon Numaranız:")
    
    c1, c2 = st.columns(2)
    with c1:
        submit_mail = st.form_submit_button("📧 Mail Gönder ve Analiz Et")
    with c2:
        submit_wa = st.form_submit_button("💬 WhatsApp'tan Bilgi Al")

# Hesaplama ve Sonuç
if submit_mail or submit_wa:
    if not ad or not tel:
        st.warning("⚠️ Lütfen adınızı ve telefonunuzu yazın.")
    else:
        filtre = df[(df['Mahalle'] == mahalle) & (df['Oda_Sayisi'] == oda)]
        min_f = f"{int(filtre['Fiyat'].min()):,}".replace(',', '.') if not filtre.empty else "Bölge Ortalaması"
        max_f = f"{int(filtre['Fiyat'].max()):,}".replace(',', '.') if not filtre.empty else "Bölge Ortalaması"
        
        ozet_mesaj = f"""
        👤 Müşteri: {ad} | Tel: {tel}
        📍 Mülk: {mahalle} - {oda}
        🏢 Kat: {bulundugu_kat}/{kat_sayisi} | Yaş: {bina_yasi} | Cephe: {cephe}
        📏 Alan: {m2} m2 | Asansör: {asansor}
        📝 Notlar: {notlar}
        💰 Tahmin: {min_f} - {max_f} TL
        """

        if submit_mail:
            if mail_gonder(f"Yeni Analiz - {ad}", ozet_mesaj):
                st.success("✅ Talebiniz e-posta ile iletildi.")
                st.balloons()

        if submit_wa:
            st.success("💬 WhatsApp yönlendirmesi hazır.")
            wa_link = f"https://wa.me/{WHATSAPP_NUMARASI}?text={ozet_mesaj.replace(' ', '%20').replace('\n', '%0A')}"
            st.link_button("📲 Mesajı Bana İlet", wa_link, use_container_width=True)

        st.markdown(f"""
            <div style="background-color:#f0f7f1; padding:25px; border-radius:15px; border:2px solid #2e7d32; text-align:center; margin-top:15px;">
                <h3 style="color:#2e7d32; margin-bottom:0px;">Tahmini Piyasa Değeri</h3>
                <h2 style="color:#1b5e20;">₺{min_f} - ₺{max_f}</h2>
            </div>
        """, unsafe_allow_html=True)
