import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- AYARLAR ---
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
st.set_page_config(page_title="Selman Güneş Emlak | Fiyat Analizi", page_icon="🏡", layout="wide")

# --- STİL DÜZENLEME (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    .hero-text { text-align: center; padding: 30px; background-color: #1e3d59; color: white; border-radius: 15px; margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- YAN MENÜ (SIDEBAR) ---
with st.sidebar:
    st.title("Selman Güneş")
    st.subheader("Gayrimenkul Danışmanı")
    st.write("Bölgenizdeki mülklerin doğru değerini bulması için profesyonel destek sunuyorum.")
    
    st.write("---")
    st.write("📱 **Beni Takip Edin**")
    st.link_button("📸 Instagram", "https://instagram.com/selmangunesemlak", use_container_width=True)
    st.link_button("🔵 Facebook", "https://facebook.com/emlakfirma", use_container_width=True)
    st.link_button("💬 WhatsApp İletişim", f"https://wa.me/{WHATSAPP_NUMARASI}", use_container_width=True)
    st.write("---")
    st.info("Hızlı analiz ve profesyonel hizmet için doğru yerdesiniz.")

# --- ANA SAYFA GİRİŞ ---
st.markdown("""
    <div class="hero-text">
        <h1>Gayrimenkul Ön Fiyat Analiz Sistemi</h1>
        <p>Aşağıdaki bilgileri eksiksiz doldurarak mülkünüzün tahmini değerini hemen öğrenebilirsiniz.</p>
    </div>
    """, unsafe_allow_html=True)

# --- ANALİZ FORMU ---
with st.form("ekspertiz_formu"):
    st.subheader("🏠 Mülk Bilgileri")
    col_a, col_b = st.columns(2)
    with col_a:
        mahalle = st.selectbox("📍 Mahalle Seçiniz:", df['Mahalle'].unique())
        oda = st.selectbox("🛏️ Oda Sayısı:", ["1+1", "2+1", "3+1", "4+1", "5+1", "Dubleks"])
        bina_yasi = st.number_input("⏳ Bina Yaşı:", 0, 100, 5)
        asansor = st.radio("🛗 Asansör:", ["Var", "Yok"], horizontal=True)

    with col_b:
        cephe = st.selectbox("☀️ Cephe:", ["Güney", "Kuzey", "Doğu", "Batı", "Güney-Doğu", "Güney-Batı"])
        kat_sayisi = st.number_input("🏢 Binadaki Toplam Kat:", 1, 50, 5)
        bulundugu_kat = st.selectbox("⬆️ Dairenin Katı:", ["Giriş", "1", "2", "3", "4", "5", "10+", "En Üst"])
        m2 = st.number_input("📏 Net Metrekare:", 30, 1000, 100)

    notlar = st.text_area("📝 Ek Bilgiler:", placeholder="Daireniz hakkında eklemek istediğiniz detaylar (Örn: masrafsız, yeni tadilatlı vb.)")
    
    st.markdown("### 👤 İletişim")
    ad = st.text_input("Adınız Soyadınız:")
    tel = st.text_input("Telefon Numaranız:")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        submit_mail = st.form_submit_button("📧 Mail İle Analiz Gönder")
    with col_f2:
        submit_wa = st.form_submit_button("💬 WhatsApp İle Analiz Al")

# --- SONUÇ VE İŞLEM ---
if submit_mail or submit_wa:
    if not ad or not tel:
        st.warning("⚠️ Size geri dönebilmemiz için isim ve telefon gereklidir.")
    else:
        filtre = df[(df['Mahalle'] == mahalle) & (df['Oda_Sayisi'] == oda)]
        min_f = f"{int(filtre['Fiyat'].min()):,}".replace(',', '.') if not filtre.empty else "---"
        max_f = f"{int(filtre['Fiyat'].max()):,}".replace(',', '.') if not filtre.empty else "---"
        
        bilgi_metni = f"""
👤 Müşteri: {ad}
📱 Tel: {tel}
📍 Mülk: {mahalle} - {oda}
⏳ Yaş: {bina_yasi} | Cephe: {cephe}
🏢 Kat: {bulundugu_kat}/{kat_sayisi} | {m2} m2
🛗 Asansör: {asansor}
📝 Notlar: {notlar}
💰 Tahmini Değer: {min_f} - {max_f} TL
        """

        if submit_mail:
            if mail_gonder(f"Yeni Analiz - {ad}", bilgi_metni):
                st.success("✅ Talebiniz başarıyla e-posta ile iletildi.")
                st.balloons()

        if submit_wa:
            st.success("💬 Veriler hazırlandı, WhatsApp'a yönlendiriliyorsunuz...")
            wa_link = f"https://wa.me/{WHATSAPP_NUMARASI}?text={bilgi_metni.replace(' ', '%20').replace('\n', '%0A')}"
            st.link_button("📲 Mesajı Selman Güneş'e İlet", wa_link, type="primary", use_container_width=True)

        st.markdown(f"""
            <div style="background-color:#f0f7f1; padding:30px; border-radius:15px; border:2px solid #2e7d32; text-align:center; margin-top:20px;">
                <h3 style="color:#2e7d32;">Bölgenizdeki Tahmini Değer Aralığı</h3>
                <h2 style="color:#1b5e20;">₺{min_f} - ₺{max_f}</h2>
                <p style="color:#555;">Bu rakamlar önizleme amaçlıdır. Net değerleme için yerinde ekspertiz gereklidir.</p>
            </div>
        """, unsafe_allow_html=True)
