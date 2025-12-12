import streamlit as st
import pandas as pd
import smtplib
import urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- AYARLAR ---
def ayar_getir(anahtar, varsayilan):
    try: return st.secrets[anahtar]
    except: return varsayilan

GÖNDEREN_EMAIL = ayar_getir("GÖNDEREN_EMAIL", "piyazsosu@gmail.com")
UYGULAMA_SIFRESI = ayar_getir("UYGULAMA_SIFRESI", "ikafvsebounnuhng")
WHATSAPP_NUMARASI = ayar_getir("WHATSAPP_NUMARASI", "905355739260")

# --- VERİ ---
try:
    df = pd.read_csv('emlak_verileri.csv', sep=None, engine='python', encoding='utf-8-sig')
    df.columns = df.columns.str.strip()
except:
    st.error("⚠️ Veri yüklenemedi!")
    st.stop()

# --- TASARIM (CSS) ---
st.set_page_config(page_title="Analiz | Selman Güneş", page_icon="🏡", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; background-color: #f9f9f9; }

    /* LIGHT HEADER (ÜST KISIM) */
    .light-header {
        background-color: #ffffff;
        padding: 25px 0;
        text-align: center;
        border-bottom: 2px solid #eeeeee;
        margin-bottom: 30px;
    }
    .light-header h1 {
        color: #1a1a1a !important;
        font-size: 26px !important;
        font-weight: 700 !important;
        margin-bottom: 5px;
        letter-spacing: -0.5px;
    }
    .light-header p { color: #666; font-size: 15px; margin-bottom: 20px; }
    
    /* NAVİGASYON */
    nav { margin-top: 10px; }
    nav a {
        color: #333 !important;
        text-decoration: none;
        margin: 0 15px;
        font-size: 14px;
        font-weight: 600;
        transition: 0.3s;
        text-transform: uppercase;
    }
    nav a:hover { color: #2e7d32 !important; border-bottom: 2px solid #2e7d32; }

    /* FORM KUTUSU */
    .stForm {
        background-color: #ffffff !important;
        padding: 40px !important;
        border-radius: 8px !important;
        border: 1px solid #e0e0e0 !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05) !important;
    }
    
    /* BUTONLAR */
    .stButton>button {
        background-color: #0b3d2e !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        font-weight: 600 !important;
        padding: 12px 20px !important;
        transition: 0.3s !important;
    }
    .stButton>button:hover {
        background-color: #2e7d32 !important;
        transform: scale(1.02);
    }

    /* KARTLAR */
    .card-row { margin-top: 40px; }
    .info-card {
        background: #fff;
        padding: 25px;
        border-radius: 8px;
        border: 1px solid #eee;
        text-align: center;
        transition: 0.3s;
    }
    .info-card:hover { border-color: #2e7d32; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
    .info-card h4 { color: #0b3d2e; margin-bottom: 10px; font-weight: 700; }
    .info-card p { color: #777; font-size: 14px; line-height: 1.6; }

    /* FOOTER (ALT KISIM) */
    .modern-footer {
        background-color: #1a1a1a;
        color: #ffffff;
        padding: 60px 20px;
        text-align: center;
        margin-top: 80px;
        border-radius: 10px 10px 0 0;
    }
    .footer-links a {
        color: #aaa;
        text-decoration: none;
        margin: 0 10px;
        font-size: 14px;
        transition: 0.3s;
    }
    .footer-links a:hover { color: #fff; }
    .footer-social { margin: 25px 0; }
    .footer-social a {
        display: inline-block;
        width: 40px;
        height: 40px;
        line-height: 40px;
        background: #333;
        border-radius: 50%;
        color: white;
        margin: 0 5px;
        text-decoration: none;
        transition: 0.3s;
    }
    .footer-social a:hover { background: #2e7d32; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER (LIGHT) ---
st.markdown("""
    <div class="light-header">
        <h1>SELMAN GÜNEŞ</h1>
        <p>Kepez & Antalya Gayrimenkul Danışmanı</p>
        <nav>
            <a href="https://emlakcrm.github.io/emlak/index.html">Ana Sayfa</a>
            <a href="https://emlakcrm.github.io/emlak/hakkimizda.html">Hakkımızda</a>
            <a href="https://emlakcrm.github.io/emlak/ilanlar.html">İlanlar</a>
            <a href="https://emlakcrm.github.io/emlak/analiz.html">Analiz</a>
            <a href="https://emlakcrm.github.io/emlak/iletisim.html">İletişim</a>
        </nav>
    </div>
    """, unsafe_allow_html=True)

# --- ANA İÇERİK ---
col_main_l, col_main_c, col_main_r = st.columns([1, 8, 1])
with col_main_c:
    st.subheader("🏡 Ücretsiz Ekspertiz Formu")
    st.info("Aşağıdaki bilgileri doldurarak mülkünüzün piyasa değerini öğrenebilirsiniz.")

    with st.form("ekspertiz_formu"):
        c1, c2 = st.columns(2)
        with c1:
            mahalle = st.selectbox("📍 Mahalle Seçiniz:", df['Mahalle'].unique())
            oda = st.selectbox("🛏️ Oda Sayısı:", ["1+1", "2+1", "3+1", "4+1", "5+1", "Dubleks"])
            bina_yasi = st.number_input("⏳ Bina Yaşı:", 0, 100, 5)
            asansor = st.radio("🛗 Asansör:", ["Var", "Yok"], horizontal=True)

        with c2:
            cephe = st.selectbox("☀️ Cephe Bilgisi:", ["Güney", "Kuzey", "Doğu", "Batı", "G.-Doğu", "G.-Batı"])
            kat_sayisi = st.number_input("🏢 Toplam Kat:", 1, 50, 5)
            bulundugu_kat = st.selectbox("⬆️ Dairenin Katı:", ["Giriş", "1", "2", "3", "4", "5", "10+", "En Üst"])
            m2 = st.number_input("📐 Net Metrekare:", 30, 1000, 100)

        notlar = st.text_area("📝 Ek Notlar (Manzara, tadilat vb.):")
        st.write("---")
        ad = st.text_input("Adınız Soyadınız:")
        tel = st.text_input("Telefon Numaranız:")
        
        btn_mail, btn_wa = st.columns(2)
        s_mail = btn_mail.form_submit_button("📧 ANALİZİ BAŞLAT")
        s_wa = btn_wa.form_submit_button("💬 WHATSAPP İLE SOR")

# --- ANALİZ SONUCU ---
if s_mail or s_wa:
    if not ad or not tel:
        st.error("⚠️ Devam etmek için iletişim bilgilerini girmelisiniz.")
    else:
        filtre = df[(df['Mahalle'] == mahalle) & (df['Oda_Sayisi'] == oda)]
        min_f = int(filtre['Fiyat'].min()) if not filtre.empty else 0
        max_f = int(filtre['Fiyat'].max()) if not filtre.empty else 0
        fiyat_sonuc = f"₺{min_f:,} - ₺{max_f:,}".replace(',', '.') if min_f > 0 else "Bize Danışın"
        
        bilgi_ozet = (f"Analiz İsteyen: {ad}\nTel: {tel}\nMülk: {mahalle} {oda}\nTahmini: {fiyat_sonuc}")

        if s_wa:
            st.success("Analiz hazır! WhatsApp'a yönlendiriliyorsunuz.")
            st.link_button("📲 MESAJI GÖNDER", f"https://wa.me/{WHATSAPP_NUMARASI}?text={urllib.parse.quote(bilgi_ozet)}", type="primary", use_container_width=True)

        st.markdown(f"""
            <div style="background-color:#ffffff; padding:30px; border-radius:8px; border:2px solid #2e7d32; text-align:center; margin-top:20px;">
                <p style="color:#666; margin:0;">Hesaplanan Değer Aralığı</p>
                <h1 style="color:#0b3d2e; font-size:40px; margin:10px 0;">{fiyat_sonuc}</h1>
            </div>
        """, unsafe_allow_html=True)

# --- TANITIM KARTLARI (Kullanıcı Talebine Göre Aşağıda) ---
st.write("---")
k1, k2, k3 = st.columns(3)
with k1:
    st.markdown('<div class="info-card"><h4>📍 Bölge Analizi</h4><p>Mahallenizdeki güncel satış ve ilan verileri anlık olarak taranır.</p></div>', unsafe_allow_html=True)
with k2:
    st.markdown('<div class="info-card"><h4>📏 Detaylı Kriter</h4><p>Kat, cephe, m2 ve bina yaşı gibi 10 kritik faktör hesaplanır.</p></div>', unsafe_allow_html=True)
with k3:
    st.markdown('<div class="info-card"><h4>🤝 Uzman Desteği</h4><p>Selman Güneş, mülkünüzün en doğru fiyata satılması için rehberlik eder.</p></div>', unsafe_allow_html=True)

# --- MODERN FOOTER ---
st.markdown(f"""
    <div class="modern-footer">
        <h2 style="color:white; margin-bottom:10px;">Selman Güneş Gayrimenkul</h2>
        <p style="color:#aaa;">Kepez / Antalya — Güvenilir Çözüm Ortağınız</p>
        <div class="footer-social">
            <a href="https://instagram.com/selmangunesemlak">IG</a>
            <a href="https://facebook.com/emlakfirma">FB</a>
            <a href="https://wa.me/{WHATSAPP_NUMARASI}">WA</a>
        </div>
        <div class="footer-links">
            <a href="https://emlakcrm.github.io/emlak/index.html">Ana Sayfa</a> |
            <a href="https://emlakcrm.github.io/emlak/hakkimizda.html">Hakkımızda</a> |
            <a href="https://emlakcrm.github.io/emlak/iletisim.html">İletişim</a>
        </div>
        <hr style="opacity:0.1; margin:30px 0;">
        <p style="font-size:12px; opacity:0.6;">© 2024 Selman Güneş Emlak. Tüm Hakları Saklıdır.</p>
        <p style="font-size:12px; opacity:0.6;">İletişim: {WHATSAPP_NUMARASI}</p>
    </div>
    """, unsafe_allow_html=True)
