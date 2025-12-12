import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. AYARLARINIZ (Burayı Doldurun) ---
GÖNDEREN_EMAIL = "piyazsosu@gmail.com" 
UYGULAMA_SIFRESI = "ikafvsebounnuhng" # Google'dan aldığınız boşluksuz kod
ALICI_EMAIL = GÖNDEREN_EMAIL
WHATSAPP_NUMARASI = "905355739260X" # Başında 90 olacak şekilde numaranız

# --- 2. VERİ YÜKLEME ---
try:
    df = pd.read_csv('emlak_verileri.csv', sep=None, engine='python', encoding='utf-8-sig')
    df.columns = df.columns.str.strip()
except Exception as e:
    st.error("Veri dosyası (emlak_verileri.csv) bulunamadı veya hatalı.")
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
        sunucu.login(GÖNDEREN_EMAIL, UYGULAMA_SIFRESI)
        sunucu.sendmail(GÖNDEREN_EMAIL, ALICI_EMAIL, mesaj.as_string())
        sunucu.quit()
        return True
    except Exception as e:
        st.error(f"E-posta gönderilemedi: {e}")
        return False

# --- 4. ARAYÜZ ---
st.set_page_config(page_title="Emlak Analiz", page_icon="🏠")
st.title("🏠 Hızlı Gayrimenkul Analizi")

with st.form("analiz_formu"):
    st.subheader("Mülk Bilgileri")
    col1, col2 = st.columns(2)
    with col1:
        mahalle = st.selectbox("Mahalle", df['Mahalle'].unique())
        oda = st.selectbox("Oda Sayısı", ["1+1", "2+1", "3+1", "4+1"])
    with col2:
        m2 = st.number_input("Metrekare", 30, 500, 100)
        yas = st.number_input("Bina Yaşı", 0, 50, 5)
    
    notlar = st.text_area("Ek Notlar (Kat, Cephe vb.)")
    
    st.subheader("İletişim Bilgileri")
    ad = st.text_input("Ad Soyad")
    tel = st.text_input("Telefon")
    
    submit = st.form_submit_button("Analiz Et ve Gönder")

# --- 5. İŞLEM SONUCU ---
if submit:
    if ad and tel:
        # Fiyat Hesaplama
        filtre = df[(df['Mahalle'] == mahalle) & (df['Oda_Sayisi'] == oda)]
        if not filtre.empty:
            min_f = f"₺{int(filtre['Fiyat'].min()):,}".replace(',', '.')
            max_f = f"₺{int(filtre['Fiyat'].max()):,}".replace(',', '.')
        else:
            min_f, max_f = "Bölge Ortalaması", "Bölge Ortalaması"

        # Mail Hazırlama
        icerik = f"Yeni Talep!\n\nAd: {ad}\nTel: {tel}\nMahalle: {mahalle}\nOda: {oda}\nm2: {m2}\nNot: {notlar}"
        
        # Mail Gönder ve Sonucu Göster
        if mail_gonder("🏠 Yeni Ekspertiz Talebi", icerik):
            st.success("Talebiniz bize ulaştı!")
            st.balloons()
            
            # Fiyatları Göster
            st.markdown(f"### Tahmini Değer Aralığı: **{min_f} - {max_f}**")
            
            # --- WHATSAPP BUTONU BURADA ---
            st.write("---")
            wa_mesaj = f"Merhaba, {mahalle} mahallesindeki mülküm için detaylı ekspertiz istiyorum. (Ad: {ad})"
            wa_link = f"https://wa.me/{WHATSAPP_NUMARASI}?text={wa_mesaj.replace(' ', '%20')}"
            st.link_button("💬 WhatsApp'tan Uzmana Bağlan", wa_link)
    else:
        st.warning("Lütfen ad ve telefon bilgilerini girin.")
