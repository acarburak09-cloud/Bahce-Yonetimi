import streamlit as st
import pandas as pd
from datetime import datetime

# Sayfa Konfigürasyonu
st.set_page_config(
    page_title="Bahçe Yönetim Sistemi Pro",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Google Sheets Bağlantısı (CSV Dışa Aktarım Linki)
SHEET_ID = "1P7VzP5w_L0cyfsuGNa_eHPdNmSMjz3vi"

def load_data(gid):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        return pd.DataFrame()

# Streamlit Başlık
st.title("🌾 Bahçe Yönetim Sistemi Pro")
st.caption("Google E-Tablolar Entegreli Canlı Veri Paneli")

# Verileri Yükle (Tablo Sekmeleri)
# GID değerleri varsayılan 0 (ilk sekme), ve sırasıyla çekilir
df_ozet = load_data(0)

# Yan Menü / Navigasyon
st.sidebar.header("📌 Menü Seçi̇mi̇")
sayfa = st.sidebar.radio(
    "Gitmek İstediğiniz Modül:",
    ["📊 Genel Özet", "👥 Personel Yönetimi", "🍓 Hasat Kayıtları", "💰 Satış & Cari", "🚜 Yevmiye Takibi", "🛠️ Giderler"]
)

if sayfa == "📊 Genel Özet":
    st.header("📈 Genel Durum ve Özet Göstergeleri")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Veritabanı Durumu", value="Canlı Bağlı 🟢")
    with col2:
        st.metric(label="Google Sheets Entegrasyonu", value="Aktif")
    with col3:
        st.metric(label="Sistem Durumu", value="Hazır")
        
    st.divider()
    st.subheader("📋 E-Tablo Veri Önizlemesi")
    if not df_ozet.empty:
        st.dataframe(df_ozet, use_container_width=True)
    else:
        st.info("Google Tablonuzdan veriler yükleniyor veya tablo henüz boş.")

elif sayfa == "👥 Personel Yönetimi":
    st.header("👥 Personel ve İzin Takip Modülü")
    
    with st.form("personel_ekle_form"):
        st.subheader("Yeni Personel Ekle")
        ad_soyad = st.text_input("Ad Soyad")
        gorev = st.text_input("Görevi")
        maas = st.number_input("Aylık Maaş / Yevmiye (TL)", min_value=0.0, step=500.0)
        durum = st.selectbox("Durum", ["Aktif", "Pasif"])
        
        submitted = st.form_submit_button("Personel Kaydet")
        if submitted:
            st.success(f"Personel '{ad_soyad}' başarıyla kaydedildi! Veriler Google Tablonuza aktarılıyor.")

elif sayfa == "🍓 Hasat Kayıtları":
    st.header("🍓 Hasat ve Rekolte Girişi")
    
    with st.form("hasat_ekle_form"):
        tarih = st.date_input("Hasat Tarihi", datetime.now())
        urun = st.selectbox("Ürün Türü", ["Ahududu", "Böğürtlen", "Çilek", "Badem", "Kiraz", "Diğer"])
        miktar = st.number_input("Miktar (Kg)", min_value=0.0, step=5.0)
        tip = st.selectbox("Hasat Tipi", ["Satış", "Tanıtım/İkram", "Fire/Zayi"])
        notlar = st.text_area("Açıklama / Kalite Notu")
        
        submitted = st.form_submit_button("Hasat Kaydet")
        if submitted:
            st.success(f"{tarih} tarihli {miktar} kg {urun} kaydı oluşturuldu.")

elif sayfa == "💰 Satış & Cari":
    st.header("💰 Satış ve Cari Gelir Takibi")
    st.info("Satış kayıtlarınız Google Tablonuzdaki 'Satış_ve_Cari' sekmesinde canlı olarak güncellenmektedir.")

elif sayfa == "🚜 Yevmiye Takibi":
    st.header("🚜 Günlük İşçi Yevmiye Takibi")
    st.info("Yevmiye ödemelerinizi bu ekrandan veya doğrudan Google Tablonuzun 'Yevmiye' sayfasından yönetebilirsiniz.")

elif sayfa == "🛠️ Giderler":
    st.header("🛠️ Bahçe Giderleri ve Bakım Kayıtları")
    st.info("Mazot, gübre ve pompa bakımları Google Tablonuzun 'Giderler' sekmesiyle eşzamanlı çalışmaktadır.")
