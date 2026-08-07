import streamlit as st
import pandas as pd
from datetime import datetime

# Mobil Uyumlu Sayfa Düzeni
st.set_page_config(page_title="Bahçe Yönetim Sistemi Pro", page_icon="🌾", layout="centered")

# Başlık
st.title("🌾 Bahçe Yönetim Sistemi Pro")
st.caption("Meyve, Fidan, Yevmiye, Personel İzin, Tanıtım/Fire ve Detaylı Analiz Paneli")

# --- ANA MENÜ ---
menu = st.sidebar.radio(
    "📌 ANA MENÜ",
    [
        "📊 Ana Panel / Özet", 
        "🌾 Hasat & Ay Ay Rekolte", 
        "🎁 Tanıtım & Fire / Zayi",
        "💰 Satış & Cari Takip", 
        "👤 Personel & İzin Takibi", 
        "👥 Yevmiyeciler", 
        "🚜 Giderler & Ekipman Bakım", 
        "🌱 Fidan Stok/Satış"
    ]
)

# 1. ANA PANEL / ÖZET
if menu == "📊 Ana Panel / Özet":
    st.subheader("📈 Genel Durum ve Özet Göstergeleri")
    
    # Rekolte hesaplaması: Satılan Hasat + Tanıtım + Fire/Zayi Toplamı
    satılan_hasat_kg = 12850.0
    tanıtım_kg = 350.0
    fire_zayi_kg = 200.0
    toplam_üretilen_hasat_kg = satılan_hasat_kg + tanıtım_kg + fire_zayi_kg
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Toplam Üretilen Hasat (Brüt)", value=f"{toplam_üretilen_hasat_kg:,.0f} kg", help="Satış + Tanıtım + Fire/Zayi Toplamı")
        st.metric(label="Toplam Meyve Geliri", value="485,000 TL")
        st.metric(label="Aktif Personel Sayısı", value="4 Kişi")
    with col2:
        st.metric(label="Tanıtım & Fire Toplamı", value=f"{tanıtım_kg + fire_zayi_kg:,.0f} kg", help="350 kg Tanıtım / 200 kg Fire")
        st.metric(label="Toplam Giderler", value="142,500 TL")
        st.metric(label="Net Kasa / Kâr", value="342,500 TL")
        
    st.info("💡 **Bilgi:** Tanıtım amaçlı verilen meyveler ve zayi olan ürünler toplam üretilen rekolteye otomatik olarak eklenmektedir.")

# 2. HASAT & AY AY REKOLTE
elif menu == "🌾 Hasat & Ay Ay Rekolte":
    st.subheader("🌾 Hasat Kayıtları ve Aylık Rekolte Analizi")
    secim = st.radio("İşlem Seçin", ["➕ Yeni Hasat Ekle", "📅 Ay Ay Rekolte Analizi & Grafikler"], horizontal=True)
    
    if secim == "➕ Yeni Hasat Ekle":
        with st.form("detayli_hasat", clear_on_submit=True):
            tarih = st.date_input("Hasat Tarihi", datetime.now())
            urun = st.selectbox("Ürün Türü", ["Ahududu", "Böğürtlen", "Çilek", "Badem", "Diğer"])
            parsel = st.selectbox("Saha / Parsel", ["1. Parsel Ahududu", "2. Parsel Böğürtlen", "Çileklik", "Bademlik", "Sera"])
            miktar = st.number_input("Toplanan Miktar (Kg)", min_value=0.0, step=0.5)
            ambalaj = st.text_input("Ambalaj Detayı", placeholder="Örn: 250gr x 40 Kutu / Şale")
            notlar = st.text_area("Notlar / Kalite Detayı")
            
            if st.form_submit_button("💾 Hasat Kaydını İşle"):
                st.success("✅ Hasat kaydı başarıyla eklendi!")
    else:
        st.write("### 📈 2026 Yılı Ay Ay Hasat Dağılımı (Kg)")
        aylik_veri = pd.DataFrame({
            "Ay": ["Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim"],
            "Ahududu (Kg)": [150, 600, 1200, 850, 300, 0],
            "Böğürtlen (Kg)": [0, 120, 450, 700, 250, 0],
            "Çilek (Kg)": [300, 450, 350, 150, 80, 0],
            "Badem (Kg)": [0, 0, 0, 0, 1500, 950]
        })
        st.dataframe(aylik_veri, use_container_width=True)
        st.bar_chart(aylik_veri.set_index("Ay"))

# 3. TANITIM & FİRE / ZAYİ
elif menu == "🎁 Tanıtım & Fire / Zayi":
    st.subheader("🎁 Tanıtım Meyvesi ve Fire/Zayi Takip Modülü")
    
    tab_t1, tab_t2 = st.tabs(["🎁 Tanıtım / İkram Meyvesi Ekle", "🗑️ Fire / Zayi Meyve Ekle"])
    
    with tab_t1:
        st.caption("Tanıtım, ikram veya numune olarak verilen meyveleri buradan girebilirsiniz.")
        with st.form("tanitim_formu", clear_on_submit=True):
            tarih = st.date_input("Tarih", datetime.now())
            urun = st.selectbox("Ürün Türü ", ["Ahududu", "Böğürtlen", "Çilek", "Badem", "Diğer"])
            miktar = st.number_input("Verilen Miktar (Kg)", min_value=0.0, step=0.5)
            verilen_yer = st.text_input("Verilen Kişi / Kurum / Yürütülen Tanıtım", placeholder="Örn: Halil Bey / Numune Dağıtımı")
            tahmini_deger = st.number_input("Tahmini Değeri (TL)", min_value=0.0, step=10.0, help="Muhasebe analizi için opsiyoneldir.")
            notlar = st.text_area("Notlar")
            
            if st.form_submit_button("🎁 Tanıtım Kaydını İşle"):
                st.success(f"✅ {miktar} kg {urun} tanıtım kaydı eklendi. Bu miktar toplam üretilen rekolteye dahil edildi!")

    with tab_t2:
        st.caption("Sıcak, ezilme veya saklama koşulları nedeniyle zayi olan meyveleri buradan girebilirsiniz.")
        with st.form("fire_formu", clear_on_submit=True):
            tarih = st.date_input("Tarih ", datetime.now())
            urun = st.selectbox("Ürün Türü  ", ["Ahududu", "Böğürtlen", "Çilek", "Badem", "Diğer"])
            miktar = st.number_input("Zayi Miktarı (Kg)", min_value=0.0, step=0.5)
            neden = st.text_input("Zayi Nedeni", placeholder="Örn: Nakliye ezilmesi, aşırı sıcak bozulması")
            tahmini_kayip = st.number_input("Tahmini Kayıp Değeri (TL)", min_value=0.0, step=10.0)
            notlar = st.text_area("Notlar ")
            
            if st.form_submit_button("🗑️ Fire Kaydını İşle"):
                st.warning(f"⚠️ {miktar} kg {urun} fire/zayi olarak kaydedildi. Toplam üretilen meyve miktarına eklendi.")

# 4. SATIŞ & CARİ
elif menu == "💰 Satış & Cari Takip":
    st.subheader("💰 Satış Kaydı ve Müşteri Cari Hesabı")
    with st.form("satis_formu", clear_on_submit=True):
        tarih = st.date_input("Satış Tarihi", datetime.now())
        satis_tipi = st.selectbox("Satış Tipi", ["Meyve Satışı", "Fidan / Fide Satışı", "Diğer"])
        musteri = st.text_input("Müşteri / Alıcı Adı")
        urun = st.text_input("Satılan Ürün / Detay")
        miktar = st.number_input("Miktar (Kg veya Adet)", min_value=0.0, step=1.0)
        birim_fiyat = st.number_input("Birim Fiyat (TL)", min_value=0.0, step=1.0)
        odeme_durumu = st.radio("Ödeme Durumu", ["Tahsil Edildi (Kasa/Banka)", "Veresiye / Açık Hesap (Alacak)"])
        if st.form_submit_button("💾 Satışı Kaydet"):
            st.success("✅ Satış başarıyla kaydedildi!")

# 5. PERSONEL & İZİN TAKİBİ
elif menu == "👤 Personel & İzin Takibi":
    st.subheader("👤 Sabit Personel Kartları ve Yıllık İzin Takibi")
    tab1, tab2, tab3 = st.tabs(["📋 Personel Kartları & İzin Bakiyeleri", "➕ Yeni Personel Tanımla", "📅 İzin Kullanımı Gir"])
    with tab1:
        with st.expander("👤 Burak Acar — Saha & Operasyon Sorumlusu", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**İşe Başlama Tarihi:** 01.01.2024")
                st.write("**Görevi:** Saha Sorumlusu & Operatör")
                st.write("**Aylık Maaş:** 45,000 TL")
            with col2:
                st.write("**Yıllık İzin Hakkı:** 14 Gün")
                st.write("**Kullanılan İzin:** 4 Gün")
                st.metric("Kalan İzin Bakiyesi", "10 Gün")
            st.write("---")
            st.caption("• 12/05/2026 - 16/05/2026 | 4 Gün | Yıllık İzin")
    with tab2:
        with st.form("yeni_personel", clear_on_submit=True):
            ad_soyad = st.text_input("Ad Soyad")
            gorev = st.text_input("Görevi")
            maas = st.number_input("Aylık Net Maaş (TL)", min_value=0.0)
            izin_hak = st.number_input("Yıllık İzin Hakkı (Gün)", min_value=0, value=14)
            if st.form_submit_button("💾 Personel Kartı Oluştur"):
                st.success("✅ Personel kartı oluşturuldu!")
    with tab3:
        with st.form("izin_giris_formu", clear_on_submit=True):
            personel = st.selectbox("Personel Seçiniz", ["Burak Acar", "Ahmet Yılmaz"])
            gun = st.number_input("Kullanılan Gün Sayısı", min_value=1, step=1)
            tur = st.selectbox("İzin Türü", ["Yıllık İzin", "Ücretsiz İzin", "Sağlık / Rapor", "Mazeret İzni"])
            if st.form_submit_button("📅 İzni İşe ve Düş"):
                st.success("✅ İzin kaydı işlendi ve bakiyeden düşüldü.")

# 6. YEVMİYECİLER
elif menu == "👥 Yevmiyeciler":
    st.subheader("👥 Günlük Yevmiyeci ve İşçilik Takibi")
    with st.form("yevmiye_formu", clear_on_submit=True):
        tarih = st.date_input("Tarih", datetime.now())
        is_adi = st.text_input("Yapılan İş", placeholder="Örn: Ahududu Toplama, Çapalama")
        kisi = st.number_input("Çalışan Kişi Sayısı", min_value=1, step=1)
        yevmiye = st.number_input("Kişi Başı Yevmiye (TL)", min_value=0.0, step=50.0)
        odenen = st.number_input("O Gün Ödenen Tutar (TL)", min_value=0.0, step=100.0)
        if st.form_submit_button("👥 Yevmiye Kaydet"):
            st.success("✅ Yevmiyeci kaydı eklendi!")

# 7. GİDERLER & BAKIM
elif menu == "🚜 Giderler & Ekipman Bakım":
    st.subheader("🚜 Gider Kaydı ve Traktör/Ekipman Bakım Defteri")
    tab_g1, tab_g2 = st.tabs(["💸 Genel Gider Ekle", "🔧 Traktör & Ekipman Bakım Kaydı"])
    with tab_g1:
        with st.form("gider_formu", clear_on_submit=True):
            kategori = st.selectbox("Gider Kategorisi", ["Mazot / Yakıt", "Gübre / İlaç", "Ambalaj / Kasa", "Diğer"])
            aciklama = st.text_input("Açıklama")
            tutar = st.number_input("Tutar (TL)", min_value=0.0)
            if st.form_submit_button("💸 Gider Kaydet"):
                st.success("✅ Gider işlendi!")
    with tab_g2:
        with st.form("bakim_formu", clear_on_submit=True):
            arac = st.selectbox("Araç / Ekipman", ["Traktör", "4x4 Pickup", "Çapa Makinesi", "İlaçlama Motoru"])
            yapilan_islem = st.text_input("Yapılan İşlem / Değişen Parça")
            maliyet = st.number_input("Bakım Maliyeti (TL)", min_value=0.0)
            if st.form_submit_button("🔧 Bakım Kaydet"):
                st.success("✅ Bakım kaydı işlendi!")

# 8. FİDAN STOK/SATIŞ
elif menu == "🌱 Fidan Stok/Satış":
    st.subheader("🌱 Fidan/Fide Stok ve Satış Modülü")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.info("• Ahududu Fidanı: 1,200 Adet\n• Böğürtlen Fidanı: 850 Adet\n• Çilek Fidesi: 5,000 Adet")
    with col_f2:
        with st.form("fidan_satis", clear_on_submit=True):
            fidan_turu = st.selectbox("Fidan Türü", ["Ahududu Fidanı", "Böğürtlen Fidanı", "Çilek Fidesi"])
            adet = st.number_input("Satılan Adet", min_value=1, step=10)
            fiyat = st.number_input("Birim Fiyat (TL)", min_value=0.0)
            if st.form_submit_button("🌱 Fidan Satışını Kaydet"):
                st.success("✅ Fidan satışı kaydedildi!")
