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
    st.error("CSV dosyası bulunamadı.")
    st.stop()

# --- MAİL GÖNDERME FONKSİYONU ---
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

# --- ARAYÜZ ---
st.set_page_config(page_title="Emlak Analiz", page_icon="🏡")
st.title("🏡 Gayrimenkul Fiyat Analizi")

with st.form("analiz_formu"):
    st.subheader("Daire Bilgileri")
    mahalle = st.selectbox("📍 Mahalle Seçiniz:", df['Mahalle'].unique())
    oda = st.selectbox("🛏️ Oda Sayısı:", ["1+1", "2+1", "3+1", "4+1"])
    aciklama = st.text_area("📝 Dairenizi Kısaca Anlatın:", placeholder="Katı, cephesi, tadilat durumu...")
    
    st.subheader("İletişim")
    ad = st.text_input("👤 Adınız Soyadınız:")
    tel = st.text_input("📱 Telefon Numaranız:")
    
    col1, col2 = st.columns(2)
    with col1:
        btn_mail = st.form_submit_button("📧 Mail Gönder")
    with col2:
        btn_wa = st.form_submit_button("💬 WhatsApp Gönder")

# --- İŞLEMLER ---
if btn_mail or btn_wa:
    if not ad or not tel:
        st.warning("Lütfen iletişim bilgilerinizi girin.")
    else:
        # Fiyat Analizi (CSV'den çekilen min-max)
        filtre = df[(df['Mahalle'] == mahalle) & (df['Oda_Sayisi'] == oda)]
        min_f = f"{int(filtre['Fiyat'].min()):,}".replace(',', '.') if not filtre.empty else "---"
        max_f = f"{int(filtre['Fiyat'].max()):,}".replace(',', '.') if not filtre.empty else "---"
        
        bilgi_notu = f"Talep Sahibi: {ad}\nTel: {tel}\nMahalle: {mahalle}\nOda: {oda}\nAçıklama: {aciklama}\nTahmin: {min_f} - {max_f} TL"

        if btn_mail:
            if mail_gonder(f"Yeni Talep - {ad}", bilgi_notu):
                st.success("✅ Bilgileriniz mail olarak gönderildi!")
                st.balloons()
            else:
                st.error("❌ Mail gönderilirken bir hata oluştu.")

        if btn_wa:
            st.success("✅ Analiz hazır! WhatsApp'a yönlendiriliyorsunuz...")
            wa_mesaj = f"Merhaba, mülk analizi istiyorum:\n{bilgi_notu}"
            wa_link = f"https://wa.me/{WHATSAPP_NUMARASI}?text={wa_mesaj.replace(' ', '%20').replace('\n', '%0A')}"
            st.link_button("📲 WhatsApp'tan Mesajı Tamamla", wa_link, type="primary")

        # Sonuç Paneli
        st.markdown(f"""
            <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; text-align:center; margin-top:20px;">
                <h3>Tahmini Değer Aralığı</h3>
                <h2 style="color:#2e7d32;">₺{min_f} - ₺{max_f}</h2>
            </div>
        """, unsafe_allow_html=True)
