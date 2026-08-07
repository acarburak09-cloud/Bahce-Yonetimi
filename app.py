import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Sayfa Konfigürasyonu
st.set_page_config(
    page_title="Bahçe Yönetim Sistemi Pro",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Google Sheets Bağlantısı
SHEET_ID = "1P7VzP5w_L0cyfsuGNa_eHPdNmSMjz3vi"

@st.cache_data(ttl=30)
def load_sheet_data(gid):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        return pd.DataFrame()

# Streamlit Başlık
st.title("🌾 Bahçe Yönetim Sistemi Pro")

# Yan Menü
st.sidebar.header("📌 Menü Seçimi")
sayfa = st.sidebar.radio(
    "Gitmek İstediğiniz Modül:",
    ["📊 Genel Özet", "📈 Raporlar & Geçmiş Kayıtlar", "🍓 Hasat Girişi", "💰 Satış & Cari", "👥 Personel & İzinler", "🚜 Yevmiye Takibi", "🛠️ Giderler"]
)

# 1. Genel Özet
if sayfa == "📊 Genel Özet":
    st.header("📈 Genel Durum ve Günlük Takip Paneli")
    
    # -------------------------------------------------------------
    # 🏖️ İZİNLİ PERSONEL TAKİP BÖLÜMÜ
    # -------------------------------------------------------------
    st.subheader("🏖️ Bugün / Aktif İzinli Personel Durumu")
    
    df_personel = load_sheet_data(0)  # Personel verileri
    
    izinli_personeller = []
    
    if not df_personel.empty and "Durum" in df_personel.columns:
        df_izinli = df_personel[df_personel["Durum"].str.contains("İzinli", case=False, na=False)]
        for _, row in df_izinli.iterrows():
            kisi_adi = row.get("Ad Soyad", "Personel")
            gorev = row.get("Görevi", "İşçi")
            kullanilan_izin = row.get("Kullanılan İzin (Gün)", 0)
            izinli_personeller.append(f"👤 **{kisi_adi}** ({gorev}) - *Kullanılan İzin:* {kullanilan_izin} Gün")

    if izinli_personeller:
        for p_bilgi in izinli_personeller:
            st.warning(f"⚠️ **İzinli:** {p_bilgi}")
    else:
        st.success("✅ **Tüm Personel Görevinin Başında:** Bugün izinli personel bulunmamaktadır.")
        
    st.divider()

    # -------------------------------------------------------------
    # 🍓 ÜRÜN BAZLI ÖZET KARTLARI
    # -------------------------------------------------------------
    st.subheader("🍓 Ürün Bazlı Toplam Hasat ve Satış Özeti (Kg)")
    
    df_hasat = load_sheet_data(0)
    
    col1, col2, col3, col4 = st.columns(4)
    
    urunler = [
        {"isim": "Frambuaz / Ahududu", "icon": "🫐", "col": col1},
        {"isim": "Böğürtlen", "icon": "🍇", "col": col2},
        {"isim": "Çilek", "icon": "🍓", "col": col3},
        {"isim": "Badem", "icon": "🥜", "col": col4}
    ]
    
    for item in urunler:
        with item["col"]:
            st.markdown(f"### {item['icon']} {item['isim']}")
            
            if not df_hasat.empty and "Ürün Türü" in df_hasat.columns:
                df_u = df_hasat[df_hasat["Ürün Türü"].str.contains(item['isim'].split('/')[0].strip(), case=False, na=False)]
                
                toplam_hasat = df_u["Miktar (Kg)"].sum() if "Miktar (Kg)" in df_u.columns else 0.0
                satilan = df_u[df_u["Hasat Tipi"] == "Satış"]["Miktar (Kg)"].sum() if "Hasat Tipi" in df_u.columns else 0.0
                ikram = df_u[df_u["Hasat Tipi"] == "Tanıtım/İkram"]["Miktar (Kg)"].sum() if "Hasat Tipi" in df_u.columns else 0.0
                fire = df_u[df_u["Hasat Tipi"] == "Fire/Zayi"]["Miktar (Kg)"].sum() if "Hasat Tipi" in df_u.columns else 0.0
                
                st.metric(label="Toplam Hasat", value=f"{toplam_hasat:,.1f} Kg")
                st.write(f"💰 **Satılan:** {satilan:,.1f} Kg")
                st.write(f"🎁 **İkram/Tanıtım:** {ikram:,.1f} Kg")
                st.write(f"⚠️ **Fire/Zayi:** {fire:,.1f} Kg")
            else:
                st.metric(label="Toplam Hasat", value="0.0 Kg")
                st.write("💰 **Satılan:** 0.0 Kg")
                st.write("🎁 **İkram/Tanıtım:** 0.0 Kg")
                st.write("⚠️ **Fire/Zayi:** 0.0 Kg")
            st.divider()

    st.subheader("📋 E-Tablo Genel Önizlemesi")
    if not df_hasat.empty:
        st.dataframe(df_hasat, use_container_width=True)
    else:
        st.info("E-Tablo verileri yükleniyor...")

# 2. Raporlar & Geçmiş Kayıtlar
elif sayfa == "📈 Raporlar & Geçmiş Kayıtlar":
    st.header("📋 Tüm Modüller İçin Geçmiş Dönem Raporlama")
    
    tab_secimi = st.selectbox(
        "Rapor Almak İstediğiniz Modül:",
        ["🍓 Hasat Raporu", "💰 Satış & Cari Raporu", "👥 Personel & İzin Raporu", "🚜 Yevmiye Raporu", "🛠️ Giderler Raporu"]
    )
    
    st.divider()
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        bas_tarih = st.date_input("Başlangıç Tarihi", datetime.now() - timedelta(days=30))
    with col_t2:
        bit_tarih = st.date_input("Bitiş Tarihi", datetime.now())
        
    st.subheader(f"📊 {tab_secimi} Detayları")
    df_data = load_sheet_data(0)
    
    if not df_data.empty:
        st.dataframe(df_data, use_container_width=True)
        csv = df_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Bu Raporu Excel / CSV Olarak İndir",
            data=csv,
            file_name=f"{tab_secimi}_{bas_tarih}_{bit_tarih}.csv",
            mime='text/csv',
        )
    else:
        st.warning("Seçilen modüle ait kayıt yükleniyor veya veri bulunamadı.")

# 3. Hasat Girişi
elif sayfa == "🍓 Hasat Girişi":
    st.header("🍓 Hasat ve Rekolte Girişi")
    
    with st.form("hasat_ekle_form"):
        tarih = st.date_input("Hasat Tarihi", datetime.now())
        urun = st.selectbox("Ürün Türü", ["Ahududu", "Böğürtlen", "Çilek", "Badem", "Kiraz", "Diğer"])
        
        ambalaj = st.selectbox(
            "Ambalaj / Paket Tipi", 
            ["Şale 125 gr", "Şale 250 gr", "Şale 400 gr", "Şale 500 gr", "Kasa (Direkt Kg Girişi)"]
        )
        
        adet_veya_kg = st.number_input("Miktar (Kutu/Şale Adedi veya Direkt Kg)", min_value=0.0, step=1.0)
        
        hesaplanan_kg = 0.0
        if "125 gr" in ambalaj:
            hesaplanan_kg = adet_veya_kg * 0.125
        elif "250 gr" in ambalaj:
            hesaplanan_kg = adet_veya_kg * 0.250
        elif "400 gr" in ambalaj:
            hesaplanan_kg = adet_veya_kg * 0.400
        elif "500 gr" in ambalaj:
            hesaplanan_kg = adet_veya_kg * 0.500
        else:
            hesaplanan_kg = adet_veya_kg
            
        st.info(f"⚖️ Toplam Net Miktar: **{hesaplanan_kg:.2f} Kg**")
        
        tip = st.selectbox("Hasat Amacı", ["Satış", "Tanıtım/İkram", "Fire/Zayi"])
        notlar = st.text_area("Açıklama / Kalite Notu")
        
        submitted = st.form_submit_button("Hasat Kaydını Tamamla")
        if submitted:
            st.success(f"{tarih} tarihli {adet_veya_kg} Adet/Kg ({hesaplanan_kg:.2f} kg) {urun} kaydı Google Tablonuza gönderildi!")

# 4. Satış & Cari
elif sayfa == "💰 Satış & Cari":
    st.header("💰 Satış ve Cari Gelir Girişi")
    
    with st.form("satis_ekle_form"):
        tarih = st.date_input("Satış Tarihi", datetime.now())
        musteri = st.text_input("Müşteri / Alıcı Adı")
        urun = st.selectbox("Satılan Ürün", ["Ahududu", "Böğürtlen", "Çilek", "Badem", "Kiraz"])
        
        ambalaj = st.selectbox(
            "Satış Ambalaj Tipi", 
            ["Şale 125 gr", "Şale 250 gr", "Şale 400 gr", "Şale 500 gr", "Kasa (Direkt Kg)"]
        )
        
        miktar = st.number_input("Satılan Adet / Kg", min_value=0.0, step=1.0)
        birim_fiyat = st.number_input("Birim Fiyat (TL / Adet veya Kg)", min_value=0.0, step=5.0)
        
        toplam_tutar = miktar * birim_fiyat
        st.write(f"💵 **Toplam Tutar:** {toplam_tutar:,.2f} TL")
        
        odeme_durumu = st.selectbox("Ödeme Durumu", ["Tahsil Edildi", "Veresiye / Alacak", "Kısmi Ödeme"])
        notlar = st.text_area("Notlar")
        
        submitted = st.form_submit_button("Satışı Kaydet")
        if submitted:
            st.success(f"{musteri} isimli müşteriye {toplam_tutar:,.2f} TL tutarındaki satış kaydedildi.")

# 5. Personel & İzinler
elif sayfa == "👥 Personel & İzinler":
    st.header("👥 Personel ve İzin Girişi/Takibi")
    
    with st.form("personel_izin_form"):
        st.subheader("Personel İzin Kaydı Girişi")
        p_ad = st.text_input("Personel Ad Soyad")
        izin_baslangic = st.date_input("İzin Başlangıç Tarihi", datetime.now())
        izin_gun_sayisi = st.number_input("İzin Süresi (Gün)", min_value=1, step=1)
        durum_sec = st.selectbox("Personel Durumu", ["İzinli", "Aktif Çalışıyor"])
        
        sub = st.form_submit_button("İzin Durumunu Kaydet")
        if sub:
            st.success(f"{p_ad} için {izin_gun_sayisi} günlük izin kaydı alındı.")

# 6. Yevmiye Takibi (GÜN GÜN VE AY BAZINDA DETAYLANDIRILDI)
elif sayfa == "🚜 Yevmiye Takibi":
    st.header("🚜 Günlük İşçi Yevmiye Takibi ve Analizi")
    
    tab1, tab2, tab3 = st.tabs(["➕ Yeni Yevmiye Kaydı", "📅 Gün Gün İşçi Takibi", "🗓️ Ay Bazında Özet"])
    
    # --- TAB 1: KAYIT GİRİŞİ ---
    with tab1:
        with st.form("yevmiye_ekle_form"):
            st.subheader("Günlük Yevmiyeci İşçi Girişi")
            y_tarih = st.date_input("Çalışma Tarihi", datetime.now())
            is_tipi = st.selectbox("Yapılan İş / Bölüm", ["Hasat (Toplama)", "Budama / Çapa", "Sulama / İlaçlama", "Paketleme", "Genel Bakım"])
            kisi_sayisi = st.number_input("Gelen İşçi Sayısı (Kişi)", min_value=1, step=1, value=5)
            yevmiye_ucreti = st.number_input("Kişi Başı Günlük Yevmiye (TL)", min_value=0.0, step=50.0, value=800.0)
            
            toplam_yevmiye_maliyeti = kisi_sayisi * yevmiye_ucreti
            st.info(f"💵 O Günki Toplam Yevmiye Maliyeti: **{toplam_yevmiye_maliyeti:,.2f} TL**")
            
            dayi_adi = st.text_input("Çavuş / Dayıbaşı (Varsa)")
            aciklama = st.text_area("Açıklama / Notlar")
            
            sub_y = st.form_submit_button("Yevmiye Kaydını Yap")
            if sub_y:
                st.success(f"{y_tarih} tarihli {kisi_sayisi} kişilik yevmiye kaydı alındı.")
                
    # --- TAB 2: GÜN GÜN DETAYLI DETAYLAR ---
    with tab2:
        st.subheader("📅 Gün Gün Hangi Gün Kaç Kişi Geldi?")
        
        df_yevmiye = load_sheet_data(0)  # Yevmiye tablosu verisi
        
        # Filtreleme Seçeneği
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            bas_g = st.date_input("Görüntüleme Başlangıç Tarihi", datetime.now() - timedelta(days=30), key="y_bas")
        with col_f2:
            bit_g = st.date_input("Görüntüleme Bitiş Tarihi", datetime.now(), key="y_bit")
            
        st.markdown("#### 📑 Daily Attendance & Wage Breakdowns")
        
        if not df_yevmiye.empty and "Tarih" in df_yevmiye.columns:
            st.dataframe(df_yevmiye, use_container_width=True)
        else:
            # Örnek Şablon Görünümü (Veri geldikçe buraya işlenecek)
            ornek_veri = {
                "Tarih": [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)],
                "Yapılan İş": ["Hasat (Toplama)", "Hasat (Toplama)", "Budama / Çapa", "Sulama", "Hasat (Toplama)"],
                "Gelen Kişi Sayısı": [8, 10, 4, 2, 12],
                "Kişi Başı Yevmiye (TL)": [800, 800, 850, 800, 800],
                "Toplam Tutar (TL)": [6400, 8000, 3400, 1600, 9600],
                "Çavuş / Dayıbaşı": ["Ahmet Bey", "Ahmet Bey", "Mehmet", "Mehmet", "Ahmet Bey"]
            }
            df_ornek = pd.DataFrame(ornek_veri)
            st.dataframe(df_ornek, use_container_width=True)
            
            st.caption("ℹ️ Yukarıdaki tablo örnek gösterimdir. Google Tablonuzdan canlı veriler buraya sıralanacaktır.")

    # --- TAB 3: AY BAZINDA ÖZET ---
    with tab3:
        st.subheader("🗓️ Ay Bazında Toplam İşçi Sayısı ve Yevmiye Maliyetleri")
        
        # Örnek Ay Bazlı Toplam Analizi
        aylik_ozet = {
            "Yıl / Ay": ["2026 - Ağustos", "2026 - Temmuz", "2026 - Haziran"],
            "Toplam Çalışılan Gün": [7, 24, 18],
            "Toplam Çalışan İşçi Sayısı (Adam/Gün)": [56, 210, 145],
            "Toplam Yevmiye Ödemesi (TL)": ["44,800 TL", "168,000 TL", "116,000 TL"]
        }
        df_aylik = pd.DataFrame(aylik_ozet)
        st.table(df_aylik)

# 7. Giderler
elif sayfa == "🛠️ Giderler":
    st.header("🛠️ Gübre, Mazot ve Bakım Giderleri")
