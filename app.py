import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# =========================================================
# 🛠️ 1. ADIM: AYARLARINIZI BURAYA GİRİN
# =========================================================
GÖNDEREN_EMAIL = "piyazsosu@gmail.com" # Gmail adresiniz
UYGULAMA_SIFRESI = "ikafvsebounnuhng"     # 16 haneli Google uygulama şifreniz (boşluklu veya boşluksuz fark etmez)
ALICI_EMAIL = GÖNDEREN_EMAIL
WHATSAPP_NUMARASI = "905355739260"         # Başında 90 ile kendi numaranız (Örn: 905321234567)

# Şifredeki boşlukları temizleyelim (hata almamak için)
TEMIZ_SIFRE = UYGULAMA_SIFRESI.replace(" ", "")

# =========================================================
# 📊 2. ADIM: VERİ OKUMA SİSTEMİ
# =========================================================
try:
    # CSV dosyanızı okur
    df = pd.read_csv('emlak_verileri.csv', sep=None, engine='python', encoding='utf-8-sig')
    df.columns = df.columns.str.strip()
except Exception as e:
    st.error("⚠️ 'emlak_verileri.csv' dosyası GitHub'da bulunamadı veya hatalı.")
    st.stop()

# =========================================================
# 📧 3. ADIM: MAİL GÖNDERME FONKSİYONU
# =========================================================
def mail_gonder(konu, icerik):
    try:
        mesaj = MIMEMultipart()
        mesaj['From'] = GÖNDEREN_EMAIL
        mesaj['To'] = ALICI_EMAIL
        mesaj['Subject'] = konu
        mesaj.attach(MIMEText(icerik, 'plain'))
        
        sunucu = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        sunucu.login(GÖNDEREN_EMAIL, TEMIZ_SIFRE)
        sunucu.sendmail(GÖNDEREN_EMAIL, ALICI_EMAIL, mesaj.as_string())
        sunucu.quit()
        return True
    except Exception as e:
        st.error(f"❌ Mail Gönderilemedi: {e}")
        return False

# =========================================================
# 🖥️ 4. ADIM: WEB ARAYÜZÜ (SIDEBAR & FORM)
# =========================================================
st.set_page_config(page_title="Emlak Fiyat Analizi", page_icon="🏡", layout="wide")

# --- YAN MENÜ (SIDEBAR) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3722/3722927.png", width=80)
    st.title("Hızlı İletişim")
    st.write("Emlak danışmanımıza her an ulaşabilir, detaylı ekspertiz desteği alabilirsiniz.")
    
    wa_link = f"https://wa.me/{WHATSAPP_NUMARASI}?text=Merhaba,%20web%20siteniz%20üzerinden%20size%20ulaşıyorum."
    st.link_button("💬 WhatsApp üzerinden Yazın", wa_link, use_container_width=True)
    
    st.write("---")
    st.info("Bu sistem geçmiş satış verilerine dayanarak ön analiz yapar. Net fiyat için mülkün yerinde görülmesi gerekir.")

# --- ANA SAYFA ---
st.title("🏡 Gayrimenkul Ön Fiyat Analiz Sistemi")
st.markdown("Aşağıdaki bilgileri doldurarak bölgenizdeki tahmini piyasa değerini öğrenebilirsiniz.")

with st.form(key='analiz_formu'):
    st.header("🏠 Mülk Özellikleri")
    
    col1, col2 = st.columns(2)
    with col1:
        mahalle = st.selectbox("📍 Mahalle Seçiniz:", df['Mahalle'].unique())
        oda_sayisi = st.selectbox("🛏️ Oda Sayısı:", ["1+1", "2+1", "3+1", "4+1", "Dupleks"])
        bulundugu_kat = st.selectbox("⬆️ Bulunduğu Kat:", ["Bahçe/Giriş", "1", "2", "3", "4", "5", "10+", "En Üst Kat"])
        
    with col2:
        metrekare = st.number_input("📏 Metrekare (Brüt):", 30, 1000, 100)
        bina_yasi = st.number_input("⏳ Bina Yaşı:", 0, 100, 5)
        isinma = st.selectbox("🔥 Isınma Tipi:", ["Doğalgaz (Kombi)", "Merkezi", "Klima", "Yerden Isıtma"])

    daire_aciklamasi = st.text_area("📝 Eklemek İstediğiniz Detaylar:", placeholder="Örn: Güney cephe, masrafsız, site içerisinde...")

    st.header("👤 İletişim Bilgileri")
    ad_soyad = st.text_input("Adınız Soyadınız:")
    telefon = st.text_input("Telefon Numaranız:")
    
    submit_button = st.form_submit_button(label='Ücretsiz Analiz Talebi Gönder')

# =========================================================
# ⚙️ 5. ADIM: ANALİZ VE SONUÇ EKRANI
# =========================================================
if submit_button:
    if ad_soyad and telefon:
        # Verileri Filtrele
        filtre = df[(df['Mahalle'] == mahalle) & (df['Oda_Sayisi'] == oda_sayisi)]
        
        if not filtre.empty:
            min_fiyat = f"₺{int(filtre['Fiyat'].min()):,}".replace(',', '.')
            max_fiyat = f"₺{int(filtre['Fiyat'].max()):,}".replace(',', '.')
        else:
            min_fiyat, max_fiyat = "Bölge Ortalaması", "Bölge Ortalaması"

        # Mail İçeriği Oluştur
        mail_icerigi = f"""
        YENİ ANALİZ TALEBİ!
        -------------------
        Müşteri: {ad_soyad}
        Telefon: {telefon}
        
        Mülk Bilgileri:
        - Mahalle: {mahalle}
        - Oda: {oda_sayisi}
        - Kat: {bulundugu_kat}
        - Isınma: {isinma}
        - m2: {metrekare}
        - Yaş: {bina_yasi}
        
        Müşteri Notu:
        {daire_aciklamasi}
        """
        
        # Gönderim İşlemi
        if mail_gonder(f"🏠 Analiz Talebi - {ad_soyad}", mail_icerigi):
            st.success("✅ Bilgileriniz alındı. Aşağıda tahmini analiz sonucunu görebilirsiniz.")
            st.balloons()
            
            # Şık Fiyat Paneli
            st.markdown(f"""
                <div style="background-color:#f8f9fa; padding:25px; border-radius:15px; border:2px solid #2e7d32; text-align:center;">
                    <h2 style="color:#2e7d32; margin-bottom:10px;">Tahmini Değer Aralığı</h2>
                    <p style="font-size:32px; font-weight:bold; color:#1b5e20;">{min_fiyat} - {max_fiyat}</p>
                    <p style="color:#666;">Detaylı ekspertiz raporu için uzmanımız sizi arayacaktır.</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Lütfen analiz yapabilmemiz için adınızı ve telefon numaranızı yazın.")
