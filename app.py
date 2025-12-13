import streamlit as st
import pandas as pd
import smtplib
import urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import socket

# --- 1. AYARLAR VE GÜVENLİK (SECRETS) ---
def ayar_getir(anahtar, varsayilan):
    """st.secrets'tan ayarı alır, yoksa varsayilanı kullanır."""
    try: 
        return st.secrets.get(anahtar, varsayilan)
    except: 
        return varsayilan

# Uygulama Ayarları
# GÖNDEREN_EMAIL: Burası Selman Bey'in analizleri alacağı mail adresidir.
GÖNDEREN_EMAIL = ayar_getir("GÖNDEREN_EMAIL", "piyazsosu@gmail.com") 
UYGULAMA_SIFRESI = ayar_getir("UYGULAMA_SIFRESI", "ikafvsebounnuhng") 
WHATSAPP_NUMARASI = ayar_getir("WHATSAPP_NUMARASI", "905355739260") # Burası Selman Bey'in WhatsApp numarasıdır.
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


# --- 2. FONKSİYONLAR ---

@st.cache_data
def veri_yukle(dosya_adi):
    """Veri dosyasını yükler ve önbelleğe alır."""
    try:
        df_cache = pd.read_csv(dosya_adi, sep=None, engine='python', encoding='utf-8-sig')
        df_cache.columns = df_cache.columns.str.strip()
        return df_cache
    except FileNotFoundError:
        return pd.DataFrame({'Mahalle': ['Örnek Mahalle'], 'Oda_Sayisi': ['2+1'], 'Fiyat': [1000000]})
    except Exception as e:
        st.error(f"Veri yüklenirken kritik bir hata oluştu: {e}")
        return pd.DataFrame({'Mahalle': ['Örnek Mahalle'], 'Oda_Sayisi': ['2+1'], 'Fiyat': [1000000]})

def mail_gonder(alici_mail, konu, icerik):
    """SMTP kullanarak belirtilen alıcıya e-posta gönderir."""
    try:
        mesaj = MIMEMultipart()
        mesaj['From'] = GÖNDEREN_EMAIL
        mesaj['To'] = alici_mail
        mesaj['Subject'] = konu
        mesaj.attach(MIMEText(icerik, 'plain'))

        sunucu = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
        sunucu.starttls()
        sunucu.login(GÖNDEREN_EMAIL, UYGULAMA_SIFRESI)
        
        sunucu.sendmail(GÖNDEREN_EMAIL, alici_mail, mesaj.as_string())
        sunucu.quit()
        return True, "Başarılı"
    except smtplib.SMTPAuthenticationError:
        return False, "E-posta gönderimi başarısız: Kimlik doğrulama hatası (Uygulama Şifresi veya E-posta adresini kontrol edin)."
    except socket.timeout:
        return False, "E-posta gönderimi başarısız: Ağ zaman aşımı hatası."
    except Exception as e:
        return False, f"E-posta gönderimi başarısız: Genel Hata: {e}"

# --- 3. VERİ YÜKLEME ---
df = veri_yukle('emlak_verileri.csv')
veriler_mevcut = not df.empty and 'Fiyat' in df.columns and 'Mahalle' in df.columns and 'Oda_Sayisi' in df.columns

# --- 4. SAYFA AYARLARI VE ÖZEL CSS ENJEKSİYONU ---
st.set_page_config(page_title="Ekspertiz | Selman Güneş", page_icon="🏡", layout="wide")

st.markdown(f"""
    <style>
        /* CSS Kodları (Değişmedi) */
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
        header {{ background: var(--main-dark); color: #fff; padding: 40px 0 20px; text-align: center; border-bottom: 5px solid var(--accent-color); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }}
        header h1 {{ font-size: 32px !important; color: #ffffff !important; font-weight: 700 !important; margin: 0 !important; letter-spacing: -0.5px !important; }}
        .lead {{ color: var(--main-light); font-size: 18px; font-weight: 300; margin: 10px 0 20px !important; }}
        nav {{ margin-top: 20px; display: flex; justify-content: center; flex-wrap: wrap; gap: 15px; }}
        nav a {{ color: var(--main-light) !important; margin: 0; font-weight: 600; text-decoration: none !important; transition: all 0.3s; text-transform: uppercase; font-size: 14px; padding: 5px 10px; }}
        nav a:hover {{ color: var(--accent-color) !important; }}
        .stForm {{ background: white !important; border: 1px solid var(--main-light) !important; border-radius: 15px !important; padding: 40px !important; box-shadow: 0 8px 24px rgba(26, 67, 57, 0.08) !important; }}
        .stButton>button {{ background-color: var(--main-dark) !important; color: white !important; border-radius: 6px !important; font-weight: 700 !important; border: none !important; transition: 0.3s !important; height: 3.5em !important; }}
        .stButton>button:hover {{ background-color: var(--cta-dark) !important; color: white !important; transform: translateY(-2px); box-shadow: 0 5px 15px rgba(212, 91, 37, 0.3); }}
        .info-card {{ background: #fff; padding: 25px; border-radius: 12px; border-left: 5px solid var(--accent-color); box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center; height: 100%; }}
        .info-card h4 {{ color: var(--main-dark); font-weight: 700; }}
        .footer {{ background: var(--main-dark); color: var(--main-light); text-align: center; padding: 40px 0; margin-top: 50px; border-radius: 20px 20px 0 0; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. HEADER BÖLÜMÜ (UI) ---
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

# --- 6. ANA FORM ALANI ---
st.markdown("<br>", unsafe_allow_html=True)
c_left, c_mid, c_right = st.columns([1, 6, 1])

with c_mid:
    st.markdown("<h2 style='text-align:center; color:#1A4339;'>Gayrimenkul Analiz & Değerleme</h2>", unsafe_allow_html=True)
    
    with st.form("main_form"):
        col1, col2 = st.columns(2)
        
        # Mahalle Seçimi Yönetimi
        mahalle_options = df['Mahalle'].unique().tolist() if veriler_mevcut else ['Veri Yok']
        if not veriler_mevcut:
            st.warning("Veri Analizi için 'emlak_verileri.csv' dosyası gereklidir.")
        
        with col1:
            mahalle = st.selectbox("📍 Mahalle:", mahalle_options, disabled=not veriler_mevcut)
            oda = st.selectbox("🛏️ Oda Sayısı:", ["1+1", "2+1", "3+1", "4+1", "5+1", "Dubleks"])
            m2 = st.number_input("📐 Metrekare (Brüt):", 30, 1000, 100)
        with col2:
            bina_yasi = st.number_input("⏳ Bina Yaşı:", 0, 100, 5)
            kat = st.selectbox("🏢 Kat Durumu:", ["Giriş", "Ara Kat", "En Üst"])
            asansor = st.radio("🛗 Asansör:", ["Var", "Yok"], horizontal=True)

        notlar = st.text_area("📝 Diger Özellikler:", placeholder="Dairenin cephesi, manzara, tadilat durumu,ayrı mutfak,ayrı wc,site içi vb.")
        
        st.markdown("<hr style='border: 0.5px solid #C4D8BF;'>", unsafe_allow_html=True)
        
        # Müşteri E-posta alanı kaldırıldı
        ad = st.text_input("Adınız Soyadınız:")
        tel = st.text_input("Telefon Numaranız:")
        
        btn_mail, btn_wa = st.columns(2)
        # Buton metni daha net hale getirildi
        s_mail = btn_mail.form_submit_button("📩 ANALİZİ BANA MAİL AT")
        s_wa = btn_wa.form_submit_button("💬 WHATSAPP İLE BANA SOR")

# --- 7. ANALİZ VE İŞLEM SONUCU ---
if (s_mail or s_wa):
    
    # 7.1 TEMEL KONTROL
    # Sadece Ad ve Telefon zorunlu tutuluyor
    if not ad or not tel:
        st.error("Lütfen Adınız ve Telefon Numaranızı tam giriniz.")
        st.stop()

    # 7.2 BÖLGE ANALİZİ (Min/Max Fiyat Hesaplama)
    if veriler_mevcut and mahalle != 'Veri Yok':
        filtre = df[(df['Mahalle'] == mahalle) & (df['Oda_Sayisi'] == oda)]
        min_f = int(filtre['Fiyat'].min()) if not filtre.empty else 0
        max_f = int(filtre['Fiyat'].max()) if not filtre.empty else 0
        
        if min_f > 0:
            sonuc = f"₺{min_f:,.0f} - ₺{max_f:,.0f}".replace(',', '.')
        else:
            sonuc = "Bölge Analizi Bekleniyor (Yeterli Eşleşen Veri Yok)"
    else:
        sonuc = "Veri Kaynağına Erişilemiyor"

    # 7.3 DETAYLI MESAJ İÇERİĞİ OLUŞTURMA
    analiz_mesaji = f"""Selman Bey Merhaba, 
{ad} ({tel}) {mahalle} mahallesindeki {oda} dairesi için BÖLGE ANALİZİ ve EKSPERTİZ talebinde bulundu.

**-- GAYRİMENKUL DETAYLARI --**
- Müşteri Adı: {ad}
- Müşteri Tel: {tel}
- Mahalle / Oda: {mahalle} / {oda}
- Metrekare (Brüt): {m2} m²
- Bina Yaşı: {bina_yasi} yıl
- Kat Durumu: {kat}
- Asansör: {asansor}
- Ek Özellikler/Notlar: {notlar if notlar else 'Belirtilmedi'}

**-- BÖLGE TAHMİNİ --**
- Tahmini Değer Aralığı: {sonuc}
"""

    # 7.4 İŞLEM ADIMLARI
    
    # A) E-POSTA GÖNDERME (Sadece Selman Bey'e)
    if s_mail:
        konu = f"YENİ EKSPERTİZ TALEBİ: {mahalle} - {oda} ({ad})"
        
        # Analiz, GÖNDEREN_EMAIL (Sizin adresinize) gönderiliyor.
        gonderim_basarili, hata_mesaji = mail_gonder(GÖNDEREN_EMAIL, konu, analiz_mesaji)

        if gonderim_basarili:
            st.success("Analiz detayları E-posta adresinize (Selman Bey) başarıyla iletildi. En kısa sürede müşteriyle iletişime geçilecektir.")
        else:
            st.error(f"Analiz talebiniz E-posta ile tarafınıza iletilemedi. Lütfen WhatsApp'tan kontrol ediniz. Hata: {hata_mesaji}")
    
    # B) WHATSAPP GÖNDERME (Sadece Selman Bey'e)
    if s_wa:
        wa_mesaj = analiz_mesaji 
        st.link_button("📲 WHATSAPP İLE ANALİZİ İLET", f"https://wa.me/{WHATSAPP_NUMARASI}?text={urllib.parse.quote(wa_mesaj)}", type="primary", use_container_width=True)
        st.success("Analiz detayları WhatsApp üzerinden iletilmeye hazır. Lütfen çıkan butona tıklayınız.")


    # 7.5 KULLANICIYA SONUCU GÖSTERME
    st.markdown(f"""
        <div style="background:var(--main-light); padding:25px; border-radius:10px; border:2px solid var(--main-dark); text-align:center; margin-top:20px;">
            <h4 style="color:var(--main-dark); margin:0;">Tahmini Piyasa Değer Aralığı</h4>
            <h1 style="color:var(--cta-dark); margin:10px 0;">{sonuc}</h1>
            <p style="color:var(--text-color); margin:0; font-weight: 500;">*Bu aralık, sadece bölgenizdeki genel ilan fiyatlarına dayanır. Detaylı ekspertiz için en kısa sürede sizinle iletişime geçilecektir.</p>
        </div>
    """, unsafe_allow_html=True)

# --- 8. ÖZELLİK KARTLARI (UI) ---
st.markdown("<br>", unsafe_allow_html=True)
k1, k2, k3 = st.columns(3)
with k1:
    st.markdown('<div class="info-card"><h4>📍 Bölge Analizi</h4><p>Gayrimenkulünüzün çevresindeki benzer mülklerin satış performansını ve eğilimlerini inceliyoruz. Bu derinlemesine inceleme, mülkünüzü pazarda rekabetçi ancak kârlı bir şekilde konumlandırmamızı sağlıyor.</p></div>', unsafe_allow_html=True)
with k2:
    st.markdown('<div class="info-card"><h4>📐 Detaylı Teknik Değerleme</h4><p>Bölge Dinamikleriyle Gerçek Değer. Mülkünüzün fiyatını, mahallenizdeki son satış verilerini, talep ve yatırım potansiyelini analiz ederek belirliyor, size güvenilir bir başlangıç fiyatı sunuyoruz..</p></div>', unsafe_allow_html=True)
with k3:
    st.markdown('<div class="info-card"><h4>🤝 Uzman Desteği</h4><p>Gayrimenkulünüzü piyasada hak ettiği en doğru fiyattan konumlandırıyoruz. Profesyonel analizlerimiz ve geniş pazar bilgimizle, satış sürecinizi şeffaflıkla yönetiyor ve size zaman kazandırıyoruz. Mülkünüz emin ellerde.</p></div>', unsafe_allow_html=True)

# --- 9. FOOTER (UI) ---
st.markdown(f"""
    <div class="footer">
        <h3> Emlak Firması</h3>
        <p>Kepez / Antalya — Sizin İçin En Doğru Değer</p>
        <p style="font-size:13px; opacity:0.8;">© 2025 Tüm Hakları Saklıdır. | İletişim: {WHATSAPP_NUMARASI}</p>
    </div>
    """, unsafe_allow_html=True)
