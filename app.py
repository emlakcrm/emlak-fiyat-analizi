import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. GİZLİ AYARLAR (SECRETS) ---
try:
    # Streamlit Cloud'da (İnternette) çalışırken buradan okur
    GÖNDEREN_EMAIL = st.secrets["GÖNDEREN_EMAIL"]
    UYGULAMA_ŞİFRESİ = st.secrets["UYGULAMA_SIFRESI"]
    ALICI_EMAIL = GÖNDEREN_EMAIL 
except Exception:
    # Bilgisayarınızda test ederken (Yerelde) hata almamak için burayı kullanır
    # NOT: GitHub'a yüklemeden önce bu tırnak içlerini temizleyebilirsiniz
    GÖNDEREN_EMAIL = "sizin_mailiniz@gmail.com" 
    UYGULAMA_ŞİFRESİ = "o_16_karakterli_kod" 
    ALICI_EMAIL = "sizin_mailiniz@gmail.com"

# --- 2. VERİ OKUMA ---
try:
    df = pd.read_csv('emlak_verileri.csv', sep=None, engine='python', encoding='utf-8-sig')
    df.columns = df.columns.str.strip() # Sütun isimlerindeki boşlukları temizler
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
st.set_page_config(page_title="Emlak Fiyat Analizi", page_icon="🏡")
st.title("🏡 Gayrimenkul Ön Fiyat Analizi")

with st.form(key='emlak_formu'):
    st.header("Konut Bilgileri")
    
    col1, col2 = st.columns(2)
    with col1:
        mahalle = st.selectbox("📍 Mahalle:", df['Mahalle'].unique())
        oda_sayisi = st.selectbox("🛏️ Oda Sayısı:", ["1+1", "2+1", "3+1", "4+1"])
    with col2:
        metrekare = st.number_input("📏 Metrekare (m²):", 30, 500, 100)
        bina_yasi = st.number_input("⏳ Bina Yaşı:", 0, 50, 5)

    ad_soyad = st.text_input("👤 Adınız Soyadınız:")
    telefon = st.text_input("📱 Telefon Numaranız:")
    
    submit = st.form_submit_button(label='Fiyat Analizi Yap')

# --- 5. HESAPLAMA VE SONUÇ ---
if submit:
    if not ad_soyad or not telefon:
        st.warning("⚠️ Lütfen iletişim bilgilerinizi eksiksiz girin.")
    else:
        # Basit Filtreleme ve Fiyat Tahmini
        veriler = df[(df['Mahalle'] == mahalle) & (df['Oda_Sayisi'] == oda_sayisi)]
        
        if not veriler.empty:
            min_f = f"₺{int(veriler['Fiyat'].min()):,}".replace(',', '.')
            max_f = f"₺{int(veriler['Fiyat'].max()):,}".replace(',', '.')
        else:
            min_f, max_f = "Analiz Ediliyor...", "Analiz Ediliyor..."

        # Mail İçeriği
        mail_icerik = f"Yeni Talep!\n\nİsim: {ad_soyad}\nTel: {telefon}\nMahalle: {mahalle}\nm2: {metrekare}\nOda: {oda_sayisi}"
        
        if mail_gonder("🏠 YENİ İLAN ANALİZ TALEBİ", mail_icerik):
            st.success("✅ Analiz Talebiniz Alındı!")
            st.balloons()
            
            # Sonuç Ekranı
            st.subheader("📊 Tahmini Değer Aralığı")
            c1, c2 = st.columns(2)
            c1.metric("Minimum", min_f)
            c2.metric("Maksimum", max_f)
            
            # WhatsApp Butonu
            st.markdown("---")
            wa_mesaj = f"Merhaba, {mahalle} mahallesindeki {oda_sayisi} dairem için yaptığım analiz sonrası detaylı bilgi almak istiyorum."
            wa_link = f"https://wa.me/905355739260?text={wa_mesaj.replace(' ', '%20')}"
            st.link_button("💬 Uzmanımıza WhatsApp'tan Yazın", wa_link)

