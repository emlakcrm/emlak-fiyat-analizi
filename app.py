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
    st.error("Veri dosyası bulunamadı.")
    st.stop()

# --- TASARIM (CSS) ---
st.set_page_config(page_title="Analiz | Selman Güneş", page_icon="🏡", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #ffffff;
    }

    /* ÜST MENÜ VE PARLAMA EFEKTİ */
    .header-wrapper {
        text-align: center;
        padding: 40px 0 20px 0;
        background: #ffffff;
    }
    
    .header-wrapper h1 {
        color: #1e293b;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 5px;
    }

    nav {
        margin-top: 25px;
        border-top: 1px solid #f1f5f9;
        border-bottom: 1px solid #f1f5f9;
        padding: 15px 0;
    }

    nav a {
        color: #64748b !important;
        text-decoration: none !important;
        margin: 0 20px;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease-in-out;
        display: inline-block;
    }

    /* İSTEDİĞİN PARLAMA BURADA */
    nav a:hover {
        color: #059669 !important; /* Canlı Yeşil */
        text-shadow: 0px 0px 12px rgba(5, 150, 105, 0.4); /* Parlama Efekti */
        transform: translateY(-2px);
    }

    /* FORM GÜZELLEŞTİRME */
    .stForm {
        border: 1px solid #e2e8f0 !important;
        border-radius: 16px !important;
        padding: 50px !important;
        background-color: #f8fafc !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05) !important;
    }

    /* BUTONLAR */
    .stButton>button {
        background: #1A4339 !important; /* Koyu Antrasit */
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 15px 30px !important;
        font-weight: 600 !important;
        transition: 0.3s !important;
        width: 100%;
    }

    .stButton>button:hover {
        background: #059669 !important; /* Hover'da Yeşil */
        box-shadow: 0 0 20px rgba(5, 150, 105, 0.3) !important;
    }

    /* KARTLAR */
    .feature-card {
        background: white;
        padding: 30px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        text-align: center;
        transition: 0.3s;
    }
    .feature-card:hover {
        border-color: #059669;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }
    .feature-card h4 { color: #1e293b; font-weight: 700; margin-bottom: 10px; }
    .feature-card p { color: #64748b; font-size: 14px; }

    /* FOOTER SADELEŞTİRİLDİ */
    .simple-footer {
        text-align: center;
        padding: 60px 0;
        margin-top: 80px;
        background: #1A4339;
        color: #94a3b8;
        border-radius: 20px 20px 0 0;
    }
    .simple-footer b { color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- ÜST KISIM (HEADER) ---
st.markdown("""
    <div class="header-wrapper">
        <h1>EMLAK FİRMASI</h1>
        <p style="color:#1A4339; font-size:16px;">Gayrimenkul Yatırım Danışmanlığı</p>
        <nav>
            <a href="https://emlakcrm.github.io/emlak/index.html">Ana Sayfa</a>
            <a href="https://emlakcrm.github.io/emlak/hakkimizda.html">Hakkımızda</a>
            <a href="https://emlakcrm.github.io/emlak/ilanlar.html">İlanlar</a>
            <a href="https://emlakcrm.github.io/emlak/form.html">Form</a>
            <a href="https://emlakcrm.github.io/emlak/analiz.html">Analiz</a>
            <a href="https://emlakcrm.github.io/emlak/iletisim.html">İletişim</a>
        </nav>
    </div>
    """, unsafe_allow_html=True)

# --- ANA FORM ---
st.markdown("<br>", unsafe_allow_html=True)
col_l, col_c, col_r = st.columns([1, 4, 1])

with col_c:
    st.markdown("<h2 style='text-align:center; color:#1e293b;'>Mülkünüzün Değerini Öğrenin</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#64748b;'>Bilgilerinizi bırakın, en doğru piyasa analizini sizin için yapalım.</p>", unsafe_allow_html=True)
    
    with st.form("vip_form"):
        st.markdown("#### 🏠 Gayrimenkul Bilgileri")
        f1, f2 = st.columns(2)
        with f1:
            mahalle = st.selectbox("📍 Bölge / Mahalle:", df['Mahalle'].unique())
            oda = st.selectbox("🛏️ Oda Sayısı:", ["1+1", "2+1", "3+1", "4+1", "5+1", "Dubleks"])
            m2 = st.number_input("📏 Net Metrekare:", 30, 1000, 100)
        with f2:
            bina_yasi = st.number_input("⏳ Bina Yaşı:", 0, 100, 5)
            kat = st.selectbox("⬆️ Dairenin Katı:", ["Giriş", "Ara Kat", "En Üst", "Bahçe"])
            asansor = st.radio("🛗 Asansör:", ["Var", "Yok"], horizontal=True)
        
        notlar = st.text_area("📝 Notlar (Opsiyonel):", placeholder="Mülkünüzün özel bir durumu varsa buraya yazabilirsiniz...")
        
        st.markdown("<br>#### 👤 İletişim Bilgileriniz", unsafe_allow_html=True)
        ad = st.text_input("Adınız ve Soyadınız:")
        tel = st.text_input("Telefon Numaranız:")
        
        st.markdown("<br>", unsafe_allow_html=True)
        btn1, btn2 = st.columns(2)
        s_mail = btn1.form_submit_button("ANALİZİ MAİL İLE AL")
        s_wa = btn2.form_submit_button("WHATSAPP İLE SOR")

# --- SONUÇ PANELİ ---
if (s_mail or s_wa) and ad and tel:
    filtre = df[(df['Mahalle'] == mahalle) & (df['Oda_Sayisi'] == oda)]
    min_v = int(filtre['Fiyat'].min()) if not filtre.empty else 0
    max_v = int(filtre['Fiyat'].max()) if not filtre.empty else 0
    tahmin = f"₺{min_v:,} - ₺{max_v:,}".replace(',', '.') if min_v > 0 else "Görüşme Gerekli"

    if s_wa:
        msg = f"Merhaba, {ad} isimli müşteri {mahalle} bölgesi için analiz istedi. Tahmin: {tahmin}"
        st.link_button("📲 WHATSAPP MESAJINI İLET", f"https://wa.me/{WHATSAPP_NUMARASI}?text={urllib.parse.quote(msg)}", use_container_width=True)

    st.markdown(f"""
        <div style="background:#ffffff; padding:30px; border-radius:12px; border-left:8px solid #059669; box-shadow:0 10px 15px -3px rgba(0,0,0,0.1); margin-top:20px;">
            <p style="color:#64748b; margin:0;">Bölge Bazlı Tahmini Değer</p>
            <h1 style="color:#1e293b; margin:0;">{tahmin}</h1>
        </div>
    """, unsafe_allow_html=True)

# --- TANITIM KARTLARI ---
st.markdown("<br><br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="feature-card"><h4>📍 Veri Analizi</h4><p>Gerçek satış rakamları ve aktif ilanların ortalaması alınır.</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="feature-card"><h4>📏 Detaylı Rapor</h4><p>Binanın yapısal durumu ve teknik detayları incelenir.</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="feature-card"><h4>🤝 Şeffaf Süreç</h4><p>Piyasa koşullarına en uygun, gerçekçi fiyatlama yapılır.</p></div>', unsafe_allow_html=True)

# --- SADE FOOTER ---
st.markdown(f"""
    <div class="simple-footer">
        <b>Selman Güneş Gayrimenkul</b><br>
        Kepez / Antalya<br><br>
        <div style="font-size:12px; opacity:0.6;">
            © 2024 Tüm Hakları Saklıdır.<br>
            İletişim: {WHATSAPP_NUMARASI}
        </div>
    </div>
    """, unsafe_allow_html=True)

