import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- AYARLARINIZI BURAYA GİRİN ---
GÖNDEREN_EMAIL = "piyazsosu@gmail.com" 
UYGULAMA_ŞİFRESİ = "wwanupzypysvmftx" 
ALICI_EMAIL = "sizin_email_adresiniz@gmail.com"

# --- VERİ OKUMA (HATA GİDERİLMİŞ HALİ) ---
try:
    # sep=None ve engine='python' sayesinde virgül veya noktalı virgülü kendi bulur
    df = pd.read_csv('emlak_verileri.csv', sep=None, engine='python', encoding='utf-8-sig')
    
    # Sütun isimlerindeki gizli boşlukları temizleyelim
    df.columns = df.columns.str.strip()
    
except Exception as e:
    st.error(f"Dosya okuma hatası: {e}")
    st.stop()

# --- FONKSİYON: MAİL GÖNDERME ---
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
        st.error(f"Mail gönderilemedi: {e}")
        return False

# --- WEB SAYFASI ---
st.title("🏡 Gayrimenkul Ön Fiyat Analizi")

# Eğer 'Mahalle' sütunu yoksa kullanıcıya uyaralım
if 'Mahalle' not in df.columns:
    st.error(f"CSV dosyasında 'Mahalle' başlığı bulunamadı. Mevcut başlıklar: {list(df.columns)}")
    st.stop()

with st.form(key='fiyat_analiz_formu'):
    st.header("Konut Bilgileri")
    
    mahalle = st.selectbox("📍 Mahalle Seçiniz:", df['Mahalle'].unique())
    oda_sayisi = st.selectbox("🛏️ Oda Sayısı:", ["1+1", "2+1", "3+1", "4+1"])
    metrekare = st.number_input("📏 Brüt Metrekare (m²):", min_value=30, max_value=500, value=100)
    bina_yasi = st.number_input("⏳ Bina Yaşı:", min_value=0, max_value=50, value=5)
    kat = st.number_input("⬆️ Bulunduğu Kat:", min_value=0, max_value=50, value=3)
    
    asansor_var = st.checkbox("Asansör Var mı?")
    aciklama = st.text_area("Ek Açıklamalar:")
    
    st.header("İletişim Bilgileri")
    ad_soyad = st.text_input("👤 Adınız Soyadınız:")
    telefon = st.text_input("📱 Telefon Numaranız:")
    
    # Buton mutlaka formun içinde olmalı (with bloğunun hizasında)
    submit_button = st.form_submit_button(label='Fiyat Belirle / Tahmin Et')

if submit_button:
    if not ad_soyad or not telefon:
        st.warning("Lütfen iletişim bilgilerinizi doldurun.")
    else:
        # Analiz kısmı
        filtre = df[(df['Mahalle'] == mahalle) & (df['Oda_Sayisi'] == oda_sayisi)]
        
        if filtre.empty:
            st.warning("Bu mahalle ve oda sayısına göre tam eşleşen veri yok, genel bir tahmin yapılıyor.")
            min_fiyat, max_fiyat = "Bilinmiyor", "Bilinmiyor"
        else:
            min_val = filtre['Fiyat'].min()
            max_val = filtre['Fiyat'].max()
            min_fiyat = f"₺{int(min_val):,}".replace(',', '.')
            max_fiyat = f"₺{int(max_val):,}".replace(',', '.')

        # Mail içeriği
        icerik = f"İsim: {ad_soyad}\nTel: {telefon}\nMahalle: {mahalle}\nm2: {metrekare}\nNot: {aciklama}"
        
        if mail_gonder("YENİ EMLAK TALEBİ", icerik):
            st.success(f"Analiz Tamamlandı! Tahmini Aralığınız: {min_fiyat} - {max_fiyat}")
            st.balloons()
# Analiz bittiğinde gösterilecek bölümün içine eklenebilir
whatsapp_mesaji = f"Merhaba, {mahalle} mahallesindeki {oda_sayisi} dairem için yaptığım ön analiz sonucunda detaylı bilgi almak istiyorum."
whatsapp_linki = f"https://wa.me/905355739260?text={whatsapp_mesaji.replace(' ', '%20')}"

st.link_button("💬 Detaylı Analiz İçin Uzmanımıza WhatsApp'tan Yazın", whatsapp_linki)