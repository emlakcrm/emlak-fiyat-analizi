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

# --- VERİ YÜKLEME ---
try:
    df = pd.read_csv('emlak_verileri.csv', sep=None, engine='python', encoding='utf-8-sig')
    df.columns = df.columns.str.strip()
except:
    st.error("Veri dosyası yüklenemedi.")
    st.stop()

# --- ÖZEL CSS ENJEKSİYONU (SİZİN STİLLERİNİZ) ---
st.set_page_config(page_title="Ekspertiz | Selman Güneş", page_icon="🏡", layout="wide")

st.markdown(f"""
    <style>
        /* 1. DEĞİŞKENLER VE TEMEL STİLLER */
        :root {{
            --main-dark: #1A4339;
            --main-light: #C4D8BF;
            --accent-color: #E7A44E;
            --cta-dark: #D45B25;
            --bg-color: #f6f7fb;
            --text-color: #1A1A1A;
        }}

        .main {{ background: var(--bg-color); }}
        
        /* 2. HEADER VE NAVİGASYON */
        header {{
            background: var(--main-dark);
            color: #fff;
            padding: 30px 0;
            text-align: center;
            border-radius: 0 0 20px 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        header h1 {{ font-size: 32px !important; color: #ffffff !important; font-weight: 700 !important; margin-bottom: 5px !important; }}
        .lead {{ color: var(--main-light); font-size: 18px; margin-bottom: 20px; }}
        
        nav a {{
            color: var(--main-light) !important;
            margin: 0 15px;
            font-weight: 600;
            text-decoration: none !important;
            transition: all 0.3s;
            text-transform: uppercase;
            font-size: 14px;
        }}
        
        nav a:hover {{
            color: var(--accent-color) !important;
            text-shadow: 0 0 8px rgba(231, 164, 78, 0.5);
        }}

        /* 3. FORM VE BUTONLAR */
        .stForm {{
            background: white !important;
            border: 1px solid var(--main-light) !important;
            border-radius: 15px !important;
            padding: 40px !important;
            box-shadow: 0 8px 24px rgba(26, 67, 57, 0.08) !important;
        }}

        .stButton>button {{
            background-color: var(--main-dark) !important;
            color: white !important;
            border-radius: 6px !important;
            font-weight: 700 !important;
            border: none !important;
            transition: 0.3s !important;
            height: 3.5em !important;
        }}

        .stButton>button:hover {{
            background-color: var(--cta-dark) !important;
            color: white !important;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(212, 91, 37, 0.3);
        }}

        /* 4. BİLGİ KARTLARI */
        .info-card {{
            background: #fff;
            padding: 25px;
            border-radius: 12px;
            border-left: 5px solid var(--accent-color);
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            text-align: center;
            height: 100%;
        }}
        .info-card h4 {{ color: var(--main-dark); font-weight: 700; }}

        /* 5. FOOTER */
        .footer {{
            background: var(--main-dark);
            color: var(--main-light);
            text-align: center;
            padding: 40px 0;
            margin-top: 50px;
            border-radius: 20px 20px 0 0;
        }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER BÖLÜMÜ ---
st.markdown("""
    <header>
        <div class="wrap">
            <h1>Antalya Gayrimenkul Danışmanı</h1>
            <p class="lead">Güven, Şeffaflık ve Sonuç Odaklı Gayrimenkul Danışmanlığı</p>
            <nav>
                <a href="https://emlakcrm.github.io/emlak/index.html">Ana Sayfa</a>
                <a href="https://emlakcrm.github.io/emlak/hakkimizda.html">Hakkımızda</a>
                <a href="https://emlakcrm.github.io/emlak/ilanlar.html">İlanlar</a>
                <a href="https://emlakcrm.github.io/emlak/form.html">Form</a>
                <a href="https://emlakcrm.github.io/emlak/analiz.html">Analiz</a>
                <a href="https://emlakcrm.github.io/emlak/iletisim.html">İletişim</a>
            </nav>
        </div>
    </header>
    """, unsafe_allow_html=True)

# --- ANA FORM ALANI ---
st.markdown("<br>", unsafe_allow_html=True)
c_left, c_mid, c_right = st.columns([1, 6, 1])

with c_mid:
    st.markdown("<h2 style='text-align:center; color:#1A4339;'>Gayrimenkul Analiz & Değerleme</h2>", unsafe_allow_html=True)
    
    with st.form("main_form"):
        col1, col2 = st.columns(2)
        with col1:
            mahalle = st.selectbox("📍 Mahalle:", df['Mahalle'].unique())
            oda = st.selectbox("🛏️ Oda Sayısı:", ["1+1", "2+1", "3+1", "4+1", "5+1", "Dubleks"])
            m2 = st.number_input("📐 Metrekare (Brüt):", 30, 1000, 100)
        with col2:
            bina_yasi = st.number_input("⏳ Bina Yaşı:", 0, 100, 5)
            kat = st.selectbox("🏢 Kat Durumu:", ["Giriş", "Ara Kat", "En Üst"])
            asansor = st.radio("🛗 Asansör:", ["Var", "Yok"], horizontal=True)

        notlar = st.text_area("📝 Ek Özellikler:", placeholder="Dairenin cephesi, manzara, tadilat durumu vb.")
        
        st.markdown("<hr style='border: 0.5px solid #C4D8BF;'>", unsafe_allow_html=True)
        ad = st.text_input("Adınız Soyadınız:")
        tel = st.text_input("Telefon Numaranız:")
        
        btn_mail, btn_wa = st.columns(2)
        s_mail = btn_mail.form_submit_button("📩 ANALİZİ E-POSTA İLE AL")
        s_wa = btn_wa.form_submit_button("💬 WHATSAPP'TAN SOR")

# --- ANALİZ SONUCU ---
if (s_mail or s_wa) and ad and tel:
    filtre = df[(df['Mahalle'] == mahalle) & (df['Oda_Sayisi'] == oda)]
    min_f = int(filtre['Fiyat'].min()) if not filtre.empty else 0
    max_f = int(filtre['Fiyat'].max()) if not filtre.empty else 0
    sonuc = f"₺{min_f:,} - ₺{max_f:,}".replace(',', '.') if min_f > 0 else "Bölge Analizi Bekleniyor"

    if s_wa:
        msg = f"Selman Bey Merhaba, {ad} ({tel}) {mahalle} mahallesindeki {oda} dairesi için analiz istedi. Tahmini Değer: {sonuc}"
        st.link_button("📲 WHATSAPP İLE BİLGİ GÖNDER", f"https://wa.me/{WHATSAPP_NUMARASI}?text={urllib.parse.quote(msg)}", type="primary", use_container_width=True)

    st.markdown(f"""
        <div style="background:var(--main-light); padding:25px; border-radius:10px; border:2px solid var(--main-dark); text-align:center; margin-top:20px;">
            <h4 style="color:var(--main-dark); margin:0;">Tahmini Piyasa Değer Aralığı</h4>
            <h1 style="color:var(--cta-dark); margin:10px 0;">{sonuc}</h1>
        </div>
    """, unsafe_allow_html=True)

# --- ÖZELLİK KARTLARI ---
st.markdown("<br>", unsafe_allow_html=True)
k1, k2, k3 = st.columns(3)
with k1:
    st.markdown('<div class="info-card"><h4>📍 Bölge Analizi</h4><p>Mahallenizdeki güncel piyasa verilerini ve son satışları inceliyoruz.</p></div>', unsafe_allow_html=True)
with k2:
    st.markdown('<div class="info-card"><h4>📏 Teknik Kriterler</h4><p>Kat, cephe, m2 ve bina yaşı gibi faktörleri yapay zeka ile harmanlıyoruz.</p></div>', unsafe_allow_html=True)
with k3:
    st.markdown('<div class="info-card"><h4>🤝 Uzman Desteği</h4><p>Mülkünüzü en doğru fiyata pazarlıyoruz.</p></div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown(f"""
    <div class="footer">
        <h3>Selman Güneş Emlak</h3>
        <p>Kepez / Antalya — Sizin İçin En Doğru Değer</p>
        <p style="font-size:13px; opacity:0.8;">© 2025 Tüm Hakları Saklıdır. | İletişim: {WHATSAPP_NUMARASI}</p>
    </div>
    """, unsafe_allow_html=True)

