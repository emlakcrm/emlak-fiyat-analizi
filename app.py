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
    # Veri dosyasının bulunamaması durumunda boş DataFrame oluşturma
    df = pd.read_csv('emlak_verileri.csv', sep=None, engine='python', encoding='utf-8-sig')
    df.columns = df.columns.str.strip()
except:
    # Boş bir DataFrame oluşturulup devam edilebilir (örnek amaçlı)
    # Gerçek uygulamada st.stop() daha doğru bir yaklaşım olabilir.
    st.error("Veri dosyası yüklenemedi. Örnek verilerle devam ediliyor.")
    df = pd.DataFrame({'Mahalle': ['Örnek Mahalle'], 'Oda_Sayisi': ['2+1'], 'Fiyat': [1000000]})
    # st.stop() # Gerçek bir uygulamanın durması için
    

# --- ÖZEL CSS ENJEKSİYONU (YENİ STİLLERİNİZLE GÜNCELLENDİ) ---
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
            --white: #ffffff;
        }}

        .main {{ background: var(--bg-color); }}
        
        /* 2. HEADER VE NAVİGASYON (YENİ STİLE UYGUN) */
        header {{ 
            background: var(--main-dark); 
            color: #fff; 
            padding: 40px 0 20px; /* Yeni Padding: 40px üst, 20px alt */
            text-align: center; 
            border-bottom: 5px solid var(--accent-color); /* Yeni Border */
            /* Streamlit'te border-radius için ekstra dikkat */
            box-shadow: 0 4px 12px rgba(0,0,0,0.15); 
        }}
        
        header h1 {{ 
            font-size: 32px !important; 
            color: #ffffff !important; 
            font-weight: 700 !important; 
            margin: 0 !important; 
            letter-spacing: -0.5px !important; /* Yeni Stil */
        }}
        
        .lead {{ 
            color: var(--main-light); 
            font-size: 18px; 
            font-weight: 300; 
            margin: 10px 0 20px !important; /* Yeni Stil: 20px alt marjin */
        }}
        
        nav {{ 
            margin-top: 20px; 
            display: flex; 
            justify-content: center; 
            flex-wrap: wrap; 
            gap: 15px; /* Yeni Stil: gap 15px */
        }}
        
        nav a {{
            color: var(--main-light) !important;
            margin: 0; /* Gap kullandığımız için margin'i sıfırlıyoruz */
            font-weight: 600;
            text-decoration: none !important;
            transition: all 0.3s;
            text-transform: uppercase;
            font-size: 14px;
            padding: 5px 10px; /* Yeni Stil: padding 5px 10px */
        }}
        
        nav a:hover {{
            color: var(--accent-color) !important;
            /* text-shadow kaldırıldı, sadece renk değişimi bırakıldı */
        }}

        /* 3. FORM VE BUTONLAR (KORUNDU) */
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

        /* 4. BİLGİ KARTLARI (KORUNDU) */
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

        /* 5. FOOTER (KORUNDU) */
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

# --- HEADER BÖLÜMÜ (HTML KISMI KORUNDU) ---
# Streamlit'te bu bölümü değiştirmeye gerek yoktur, çünkü stil yukarıdaki CSS ile kontrol edilmektedir.
st.markdown("""
    <header>
        <div class="wrap">
            <h1>Antalya Gayrimenkul Danışmanı</h1>
            <p class="lead">Güven, Şeffaflık ve Sonuç Odaklı Gayrimenkul Danışmanlığı</p>
            <nav>
                <a href="https://emlakcrm.github.io/emlak/index.html" target="_blank">ANA SAYFA</a>
                <a href="https://emlakcrm.github.io/emlak/hakkimizda.html" target="_blank">HAKKIMIZDA</a>
                <a href="https://emlakcrm.github.io/emlak/ilanlar.html" target="_blank">İLANLAR</a>
                <a href="https://emlakcrm.github.io/emlak/antalya.html" target="_blank">ANTALYA</a>
                <a href="https://emlakcrm.github.io/emlak/form.html" target="_blank">FORM</a>
                <a href="https://emlakcrm.github.io/emlak/resimler.html" target="_blank">FOTO GALERİ</a>
                <a href="https://emlakcrm.github.io/emlak/iletisim.html" target="_blank">İLETİŞİM</a>
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
            # Mahalle seçimi: Veri yüklenemezse varsayılan değer kullanılmalı
            mahalle_options = df['Mahalle'].unique().tolist()
            if not mahalle_options:
                 mahalle_options = ['Veri Yok']
            mahalle = st.selectbox("📍 Mahalle:", mahalle_options)
            
            oda = st.selectbox("🛏️ Oda Sayısı:", ["1+1", "2+1", "3+1", "4+1", "5+1", "Dubleks"])
            m2 = st.number_input("📐 Metrekare (Brüt):", 30, 1000, 100)
        with col2:
            bina_yasi = st.number_input("⏳ Bina Yaşı:", 0, 100, 5)
            kat = st.selectbox("🏢 Kat Durumu:", ["Giriş", "Ara Kat", "En Üst"])
            asansor = st.radio("🛗 Asansör:", ["Var", "Yok"], horizontal=True)

        notlar = st.text_area("📝 Diger Özellikler:", placeholder="Dairenin cephesi, manzara, tadilat durumu,ayrı mutfak,ayrı wc,site içi vb.")
        
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
    
    if min_f > 0:
        # Binlik ayraç için Türkçe format (nokta)
        sonuc = f"₺{min_f:,.0f} - ₺{max_f:,.0f}".replace(',', '.')
    else:
        sonuc = "Bölge Analizi Bekleniyor"

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
    st.markdown('<div class="info-card"><h4>📍 Bölge Analizi</h4><p>Gayrimenkulünüzün çevresindeki benzer mülklerin satış performansını ve eğilimlerini inceliyoruz. Bu derinlemesine inceleme, mülkünüzü pazarda rekabetçi ancak kârlı bir şekilde konumlandırmamızı sağlıyor.</p></div>', unsafe_allow_html=True)
with k2:
    st.markdown('<div class="info-card"><h4>📐 Detaylı Teknik Değerleme</h4><p>Bölge Dinamikleriyle Gerçek Değer. Mülkünüzün fiyatını, mahallenizdeki son satış verilerini, talep ve yatırım potansiyelini analiz ederek belirliyor, size güvenilir bir başlangıç fiyatı sunuyoruz..</p></div>', unsafe_allow_html=True)
with k3:
    st.markdown('<div class="info-card"><h4>🤝 Uzman Desteği</h4><p>Gayrimenkulünüzü piyasada hak ettiği en doğru fiyattan konumlandırıyoruz. Profesyonel analizlerimiz ve geniş pazar bilgimizle, satış sürecinizi şeffaflıkla yönetiyor ve size zaman kazandırıyoruz. Mülkünüz emin ellerde.</p></div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown(f"""
    <div class="footer">
        <h3> Emlak Firması</h3>
        <p>Kepez / Antalya — Sizin İçin En Doğru Değer</p>
        <p style="font-size:13px; opacity:0.8;">© 2025 Tüm Hakları Saklıdır. | İletişim: {WHATSAPP_NUMARASI}</p>
    </div>
    """, unsafe_allow_html=True)


