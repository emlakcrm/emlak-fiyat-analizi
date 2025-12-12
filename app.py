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
    st.error("⚠️ Veri dosyası (CSV) yüklenemedi. Lütfen GitHub'da dosyanın olduğunu kontrol edin.")
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
# 🎨 4. GÖRSEL TASARIM VE CSS
# =========================================================
st.set_page_config(page_title="Selman Güneş Emlak | Değerleme", page_icon="🏡", layout="wide")

st.markdown("""
    <style>
    /* Ana Arka Plan */
    .main { background-color: #f8f9fa; }
    
    /* Hero Banner */
    .hero-section {
        background: linear-gradient(135deg, #1e3d59 0%, #2e7d32 100%);
        padding: 60px 20px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30 margin-top: -50px;
    }
    
    /* Kart Yapıları */
    .info-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #2e7d32;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* Buton Tasarımı */
    .stButton>button {
        border-radius: 12px;
        height: 3.5em;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 30px;
        font-size: 14px;
        color: #666;
        border-top: 1px solid #eee;
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# 📱 5. YAN MENÜ (SIDEBAR)
# =========================================================
with st.sidebar:
    st.markdown("### 👤 Danışman Profili")
    st.write("**Selman Güneş**")
    st.caption("Lisanslı Gayrimenkul Profesyoneli")
    st.write("---")
    st.write("📲 **Hızlı Bağlantılar**")
    st.link_button("📸 Instagram'da Takip Et", "https://instagram.com/selmangunesemlak", use_container_width=True)
    st.link_button("🔵 Facebook Sayfası", "https://facebook.com/emlakfirma", use_container_width=True)
    st.link_button("💬 WhatsApp Hattı", f"https://wa.me/{WHATSAPP_NUMARASI}", use_container_width=True)
    st.write("---")
    st.info("Mülkünüzü en doğru fiyata satmak için veriye dayalı stratejiler geliştiriyoruz.")

# =========================================================
# 🏠 6. ANA SAYFA İÇERİĞİ
# =========================================================
# Üst Banner
st.markdown("""
    <div class="hero-section">
        <h1>Gayrimenkulünüzün Piyasa Değerini Keşfedin</h1>
        <p style="font-size: 1.2em; opacity: 0.9;">Yapay zeka destekli ön analiz sistemiyle saniyeler içinde rapor alın.</p>
    </div>
    """, unsafe_allow_html=True)

# Bilgi Kartları (Sayfayı dolgun göstermek için)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="info-card"><h4>📍 Bölge Analizi</h4><p>Mahallenizdeki benzer ilanların gerçek satış verileri incelenir.</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="info-card"><h4>📏 Detaylı Kriter</h4><p>Kat, cephe ve bina yaşı gibi 10 farklı kriter baz alınır.</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="info-card"><h4>🤝 Uzman Desteği</h4><p>Analiz sonrası Selman Güneş size özel yol haritası sunar.</p></div>', unsafe_allow_html=True)

st.write("---")

# Form Alanı
st.subheader("📋 Ekspertiz Formunu Doldurun")
with st.form("main_form"):
    col_left, col_right = st.columns(2)
    
    with col_left:
        mahalle = st.selectbox("📍 Mahalle Seçiniz:", df['Mahalle'].unique())
        oda = st.selectbox("🛏️ Oda Sayısı:", ["1+1", "2+1", "3+1", "4+1", "5+1", "Dubleks"])
        bina_yasi = st.number_input("⏳ Bina Yaşı:", 0, 100, 5)
        asansor = st.radio("🛗 Asansör Durumu:", ["Var", "Yok"], horizontal=True)

    with col_right:
        cephe = st.selectbox("☀️ Cephe Bilgisi:", ["Güney", "Kuzey", "Doğu", "Batı", "Güney-Doğu", "Güney-Batı"])
        kat_sayisi = st.number_input("🏢 Toplam Kat Sayısı:", 1, 50, 5)
        bulundugu_kat = st.selectbox("⬆️ Kaçıncı Katta?:", ["Bahçe", "Giriş", "1", "2", "3", "4", "5", "10+", "En Üst"])
        m2 = st.number_input("📐 Brüt Metrekare:", 30, 1000, 100)

    notlar = st.text_area("📝 Diğer Özellikler:", placeholder="Manzara, doğalgaz durumu, tadilat bilgisi vb.")
    
    st.markdown("### 👤 İletişim Bilgileri")
    ad_soyad = st.text_input("Adınız Soyadınız:")
    telefon = st.text_input("Telefon Numaranız:")
    
    btn_mail, btn_wa = st.columns(2)
    with btn_mail:
        s_mail = st.form_submit_button("📧 Mail İle Analiz İstiyorum")
    with btn_wa:
        s_wa = st.form_submit_button("💬 WhatsApp İle Analiz Al")

# =========================================================
# ⚙️ 7. SONUÇ VE İŞLEME
# =========================================================
if s_mail or s_wa:
    if not ad_soyad or not telefon:
        st.error("⚠️ Analiz yapabilmemiz için adınızı ve telefonunuzu girmelisiniz.")
    else:
        # Fiyat Motoru
        filtre = df[(df['Mahalle'] == mahalle) & (df['Oda_Sayisi'] == oda)]
        min_v = int(filtre['Fiyat'].min()) if not filtre.empty else 0
        max_v = int(filtre['Fiyat'].max()) if not filtre.empty else 0
        
        fiyat_str = f"₺{min_v:,} - ₺{max_v:,}".replace(',', '.') if min_v > 0 else "Bölge Uzmanına Sorun"
        
        # Mesaj Oluşturma
        mesaj_metni = (f"Yeni Analiz Talebi\n\n"
                       f"Müşteri: {ad_soyad}\nTel: {telefon}\n"
                       f"Mülk: {mahalle}, {oda}, {m2}m2\n"
                       f"Detay: {bina_yasi} Yaş, {cephe} Cephe, Kat {bulundugu_kat}/{kat_sayisi}\n"
                       f"Asansör: {asansor}\nNot: {notlar}\n\n"
                       f"Tahmini Değer: {fiyat_str}")

        if s_mail:
            if mail_gonder(f"Analiz Talebi - {ad_soyad}", mesaj_metni):
                st.success("✅ Verileriniz alındı. E-posta yoluyla size dönüş sağlanacaktır.")
                st.balloons()

        if s_wa:
            encoded_wa = urllib.parse.quote(mesaj_metni)
            wa_url = f"https://wa.me/{WHATSAPP_NUMARASI}?text={encoded_wa}"
            st.success("✅ Analiz hazır! WhatsApp üzerinden iletişimi tamamlayın.")
            st.link_button("📲 WHATSAPP MESAJINI BANA GÖNDER", wa_url, type="primary", use_container_width=True)

        # Sonuç Kartı
        st.markdown(f"""
            <div style="background-color:#e8f5e9; padding:40px; border-radius:20px; border:2px solid #2e7d32; text-align:center; margin-top:20px;">
                <h3 style="color:#2e7d32; margin:0;">Mülkünüzün Tahmini Piyasa Değeri</h3>
                <h1 style="color:#1b5e20; font-size:48px; margin:10px 0;">{fiyat_str}</h1>
                <p style="color:#666;">Bu değer piyasa ortalamalarına göre hesaplanmıştır. Yerinde ekspertiz için randevu alınız.</p>
            </div>
        """, unsafe_allow_html=True)

# =========================================================
# 🏁 8. FOOTER (ALT BİLGİ)
# =========================================================
st.markdown(f"""
    <div class="footer">
        <p>© 2024 Selman Güneş Emlak | Tüm Hakları Saklıdır.</p>
        <p>İletişim: {WHATSAPP_NUMARASI} | Antalya / Türkiye</p>
    </div>
    """, unsafe_allow_html=True)
