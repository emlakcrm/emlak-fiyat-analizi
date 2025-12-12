import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. GİZLİ AYARLAR (SECRETS) ---
try:
    GÖNDEREN_EMAIL = st.secrets["GÖNDEREN_EMAIL"]
    UYGULAMA_ŞİFRESİ = st.secrets["UYGULAMA_SIFRESI"]
    ALICI_EMAIL = GÖNDEREN_EMAIL 
except Exception:
    GÖNDEREN_EMAIL = "sizin_mailiniz@gmail.com" 
    UYGULAMA_ŞİFRESİ = "o_16_karakterli_kod" 
    ALICI_EMAIL = "sizin_mailiniz@gmail.com"

# --- 2. VERİ OKUMA ---
try:
    df = pd.read_csv('emlak_verileri.csv', sep=None, engine='python', encoding='utf-8-sig')
    df.columns = df.columns.str.strip()
except Exception as e:
    st.error(f"⚠️ Veri dosyası okunamadı: {e}")
    st.stop()

# --- 3. MAİL GÖNDERME FONKSİYONU ---
def mail_gonder(konu, icerik):
    try:
        mesaj = MIMEMultipart()
        mesaj['From'] = GÖNDEREN_EMAIL
        mesaj['To'] = ALICI_EMAIL
        mesaj['Subject'] = konu
        mesaj.attach(MIMEText(icerik, 'plain'))
        sunucu = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        sunucu.login(GÖNDEREN_EMAIL, UYGULAMA_ŞİFRESİ)
        sunucu.sendmail(GÖNDEREN_EMAIL, ALICI_EMAIL, mesaj.as_string())
        sunucu.quit()
        return True
    except Exception as e:
        st.error(f"❌ Mail gönderilemedi: {e}")
        return False

# --- 4. WEB ARAYÜZÜ ---
st.set_page_config(page_title="Emlak Fiyat Analizi", page_icon="🏡", layout="centered")
st.title("🏡 Gayrimenkul Ön Fiyat Analizi")
st.markdown("Hızlıca mülk özelliklerini girin, bölge ortalamasına göre tahmini değer aralığını öğrenin.")

with st.form(key='emlak_formu'):
    st.header("🏠 Konut Detayları")
    
    col1, col2 = st.columns(2)
    with col1:
        mahalle = st.selectbox("📍 Mahalle Seçiniz:", df['Mahalle'].unique())
        oda_sayisi = st.selectbox("🛏️ Oda Sayısı:", ["1+0", "1+1", "2+1", "3+1", "4+1", "4+2", "5+1"])
        bulundugu_kat = st.selectbox("⬆️ Bulunduğu Kat:", ["Giriş Kat", "Bahçe Katı", "1", "2", "3", "4", "5", "6-10 Arası", "10 Üzeri", "En Üst Kat"])
        
    with col2:
        metrekare = st.number_input("📏 Brüt Metrekare (m²):", 30, 1000, 100)
        bina_yasi = st.number_input("⏳ Bina Yaşı:", 0, 100, 5)
        isinma = st.selectbox("🔥 Isınma Tipi:", ["Doğalgaz (Kombi)", "Merkezi (Pay Ölçer)", "Klima", "Soba", "Yerden Isıtma"])

    daire_aciklamasi = st.text_area("📝 Eklemek İstediğiniz Detaylar:", 
                                     placeholder="Örn: Güney cephe, ebeveyn banyolu, site içerisinde...")

    st.markdown("---")
    st.header("👤 İletişim Bilgileri")
    ad_soyad = st.text_input("Adınız Soyadınız:")
    telefon = st.text_input("Telefon Numaranız (Başında 0 olmadan):")
    
    submit = st.form_submit_button(label='Ücretsiz Analiz Yap')

# --- 5. HESAPLAMA VE SONUÇ ---
if submit:
    if not ad_soyad or not telefon:
        st.warning("⚠️ Lütfen iletişim bilgilerinizi eksiksiz doldurun.")
    else:
        # Veriden fiyat çekme
        veriler = df[(df['Mahalle'] == mahalle) & (df['Oda_Sayisi'] == oda_sayisi)]
        
        if not veriler.empty:
            min_f = f"₺{int(veriler['Fiyat'].min()):,}".replace(',', '.')
            max_f = f"₺{int(veriler['Fiyat'].max()):,}".replace(',', '.')
        else:
            min_f, max_f = "Bölge Ortalaması Alınıyor...", "Bölge Ortalaması Alınıyor..."

        # Mail İçeriği (Yeni alanlar eklendi)
        mail_icerik = f"""
🚀 YENİ ANALİZ TALEBİ GELDİ!

👤 Müşteri Bilgileri:
- Ad Soyad: {ad_soyad}
- Telefon: {telefon}

🏠 Mülk Özellikleri:
- Mahalle: {mahalle}
- Oda Sayısı: {oda_sayisi}
- Metrekare: {metrekare} m²
- Bina Yaşı: {bina_yasi}
- Bulunduğu Kat: {bulundugu_kat}
- Isınma Tipi: {isinma}

📝 Müşteri Notu:
{daire_aciklamasi}
        """
        
        if mail_gonder("🏠 YENİ TALEP: " + ad_soyad, mail_icerik):
            st.success("✅ Talebiniz başarıyla gönderildi!")
            st.balloons()
            
            # Şık Görsel Sonuç Paneli
            st.markdown(f"""
                <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; border:1px solid #ddd; text-align:center;">
                    <h3 style="color:#1f77b4; margin-bottom:5px;">Tahmini Değer Aralığı</h3>
                    <p style="font-size:24px; font-weight:bold; color:#2e7d32;">{min_f} - {max_f}</p>
                    <p style="font-size:14px; color:#555;">Net ekspertiz raporu için uzmanımız sizinle iletişime geçecektir.</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            # WhatsApp Linkini Güncelleyelim (Tüm detayları içersin)
            wa_mesaj = f"Merhaba, {mahalle} mahallesindeki {oda_sayisi} dairem için yaptığım analiz sonrası detaylı bilgi almak istiyorum. (Ad: {ad_soyad})"
            wa_link = f"https://wa.me/905355739260?text={wa_mesaj.replace(' ', '%20')}"
            st.link_button("💬 Şimdi WhatsApp'tan Detayları Görüşün", wa_link)
