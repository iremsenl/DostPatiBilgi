import streamlit as st
import streamlit as st
import pandas as pd
import openpyxl
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# VERİYİ YÜKLE (senin dosyanı uygun şekilde oku)
file_path = "./DENEME.xlsx"
df = pd.read_excel(file_path)

# Barınak yoğunluğu = Barınak sayısı / Belediye alanı (km²)

df['BARINAK YOĞUNLUĞU'] = df["BELEDİYE BÜNYESİNDE BULUNAN BARINAK SAYISI"] / df['alan']
print(df['BARINAK YOĞUNLUĞU'])
ortalama_yogunluk = df['BARINAK YOĞUNLUĞU'].mean()
# Fonksiyonlar
def barinak_onerisi(yogunluk):
    if isinstance(yogunluk, pd.Series):
        barinak_yogunlugu = yogunluk.iloc[0]
    if yogunluk < ortalama_yogunluk * 0.0075:
        return 'Barınak sayısı artırılmalı.'
    elif yogunluk > ortalama_yogunluk * 0.150:
        return 'Barınak sayısı yüksek.'
    else:
        return 'Barınak sayısı uygun.'

def veteriner_analizi(row):
    toplam = row['BİRİMDE KAÇ VETERİNER HEKİM BULUNMAKTADIR?']
    dahil = row['SOKAK HAYVANLARI KISIRLAŞTIRMA SÜRECİNE DAHİL OLAN VETERİNER HEKİM SAYISI']
    if toplam == 0:
        return 'Veteriner hekim yok. Acilen personel alınmalı.'
    elif pd.isnull(toplam) or pd.isnull(dahil):
        return 'Veri eksik'
    oran = dahil / toplam
    return 'Veteriner hekimler etkin şekilde görev alıyor.' if oran >= 0.5 else 'Kısırlaştırma sürecine daha fazla dahil olunmalı.'

hizmet_kolonlari = [
    "BELEDİYE BÜNYESİNDE HAYVAN HASTANESİ/BAKIM MERKEZİ VAR MI?",
    "HAYVAN HASTANESİ/BAKIM MERKEZİ BÜNYESİNDE TEDAVİ ODASI VAR MI?",
    "HAYVAN HASTANESİ/BAKIM MERKEZİ BÜNYESİNDE BARINMA ÜNİTESİ VAR MI?",
    "HAYVAN HASTANESİ/BAKIM MERKEZİ BÜNYESİNDE AMELİYATHANE VAR MI?",
    "HAYVAN HASTANESİ/BAKIM MERKEZİ BÜNYESİNDE YOĞUN BAKIM ÜNİTESİ VAR MI?",
    "HAYVAN HASTANESİ/BAKIM MERKEZİ BÜNYESİNDE REHABİLİTASYON MERKEZİ VAR MI?",
    "HAYVAN HASTANESİ/BAKIM MERKEZİ BÜNYESİNDE HAYVAN NAKİL ARACI VAR MI?",
    "HAYVAN HASTANESİ/BAKIM MERKEZİ BÜNYESİNDE HAYVAN AMBULANSI VAR MI?",
    "HAYVAN HASTANESİ/BAKIM MERKEZİ BÜNYESİNDE HAYVAN BARINAĞI VAR MI?",
    "SON 3 YILDA SOKAK HAYVANI SAYISINI TESPİT ETMEYE YÖNELİK ÇALIŞMA YAPILDI MI?",
    "KISIRLAŞTIRMA ÇALIŞMALARI VAR MI?",
    "AŞILAMA ÇALIŞMALARI VAR MI?"
]
print(df[hizmet_kolonlari].head())
# Kolonlardaki 'EVET' değerlerini 1, diğerlerini 0 yapalım
for col in hizmet_kolonlari:
    df[col] = df[col].apply(lambda x: 0 if str(x).strip().upper() == 'HAYIR' else 1 )

# Sonuçları kontrol et
print(df[hizmet_kolonlari].head())  # Sadece hizmet kolonlarını göster

def hizmet_durumu(row, hizmet_kolonlari):
    return "✅ Hizmet alınabilir" if row[hizmet_kolonlari] == 1 else "⚠️ Hizmet alınamaz"

def veteriner_var_mi(sayi):
    if pd.isnull(sayi):
        return "VERİ YOK"
    return "VAR" if sayi > 0 else "YOK"


# Streamlit Arayüzü
st.title("🐾 Belediye Bilgi ve Sokak Hayvanları Hizmet Analizi")
print(df)
# Boş seçenekli belediye listesi
belediye_listesi = sorted(df['BELEDİYE ADI'].dropna().unique().tolist())

# Kullanıcıya açılır kutu sunuluyor
belediye_adi_input = st.selectbox("Bir belediye seçin:", belediye_listesi)

# Seçim yapılmışsa ve geçerli bir belediye ise işlemler başlar
if belediye_adi_input != "👈 Bir belediye seçin":
    belediye_verisi = df[df['BELEDİYE ADI'] == belediye_adi_input]

    if belediye_verisi.empty:
        st.warning("⚠️ Girdiğiniz belediye adına ait veri bulunamadı.")
    else:
        row = belediye_verisi.iloc[0]
        st.subheader(f"📌 {belediye_adi_input.title()} için Analiz ve Öneriler")

        # Veteriner durumu
        veteriner_sayisi = row['BİRİMDE KAÇ VETERİNER HEKİM BULUNMAKTADIR?']
        st.markdown("### 👨‍⚕️ Veteriner Durumu")
        st.write(f"- Mevcut Veteriner Durumu: **{veteriner_var_mi(veteriner_sayisi)}**")
        st.write(f"- Analiz: {veteriner_analizi(row)}")

        # Barınak Yoğunluğu
        barinak_yogunlugu = row["BARINAK YOĞUNLUĞU"]
        st.markdown("### 🏢 Barınak Yoğunluğu")
        st.write(f"- Yoğunluk değeri: `{barinak_yogunlugu:.4f}`")
        st.write(f"- Değerlendirme: {barinak_onerisi(barinak_yogunlugu)}")

        hizmet_kolonlari = {
            "BELEDİYE BÜNYESİNDE HAYVAN HASTANESİ/BAKIM MERKEZİ VAR MI?": "Hayvan Hastanesi/Bakım Merkezi",
            "HAYVAN HASTANESİ/BAKIM MERKEZİ BÜNYESİNDE TEDAVİ ODASI VAR MI?": "Tedavi Odası",
            "HAYVAN HASTANESİ/BAKIM MERKEZİ BÜNYESİNDE BARINMA ÜNİTESİ VAR MI?": "Barınma Ünitesi",
            "HAYVAN HASTANESİ/BAKIM MERKEZİ BÜNYESİNDE AMELİYATHANE VAR MI?": "Ameliyathane",
            "HAYVAN HASTANESİ/BAKIM MERKEZİ BÜNYESİNDE YOĞUN BAKIM ÜNİTESİ VAR MI?": "Yoğun Bakım Ünitesi",
            "HAYVAN HASTANESİ/BAKIM MERKEZİ BÜNYESİNDE REHABİLİTASYON MERKEZİ VAR MI?": "Rehabilitasyon Merkezi",
            "HAYVAN HASTANESİ/BAKIM MERKEZİ BÜNYESİNDE HAYVAN NAKİL ARACI VAR MI?": "Hayvan Nakil Aracı",
            "HAYVAN HASTANESİ/BAKIM MERKEZİ BÜNYESİNDE HAYVAN AMBULANSI VAR MI?": "Hayvan Ambulansı",
            "HAYVAN HASTANESİ/BAKIM MERKEZİ BÜNYESİNDE HAYVAN BARINAĞI VAR MI?": "Hayvan Barınağı",
            "SON 3 YILDA SOKAK HAYVANI SAYISINI TESPİT ETMEYE YÖNELİK ÇALIŞMA YAPILDI MI?": "Sokak Hayvanı Sayımı",
            "KISIRLAŞTIRMA ÇALIŞMALARI VAR MI?": "Kısırlaştırma Çalışmaları",
            "AŞILAMA ÇALIŞMALARI VAR MI?": "Aşılama Çalışmaları"
        }

        # Altyapı hizmetleri
        st.markdown("### 🏥 Altyapı & Hizmetler")
        for hizmet_kolonlari, hizmet_adi in hizmet_kolonlari.items():
            st.write(f"- **{hizmet_adi}**: {hizmet_durumu(row, hizmet_kolonlari)}")

        # Belediye özel faaliyet grafiği
        st.subheader(f"📌 {belediye_adi_input.title()} -Aşı, Kısırlaştırma, Mikroçip faaliyetleri")
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        sns.barplot(x=['Kısırlaştırma', 'Aşılama', 'Mikroçip'],
                    y=[row['SON BİR YILDA KISIRLAŞTIRILAN TOPLAM HAYVAN SAYISI'],
                       row['SON BİR YILDA AŞILANAN SOKAK HAYVANI SAYISI'],
                       row['SON BİR YILDA MİKROÇİP TAKILMIŞ SOKAK HAYVANI SAYISI']],
                    ax=ax1)
        ax1.set_title(f"{belediye_adi_input} - Sokak Hayvanları Faaliyetleri")
        ax1.set_ylabel("Hayvan Sayısı")
        st.pyplot(fig1)

        st.subheader(f"📌 Tüm Belediye Ortalamalarına Göre Faaliyetler")

        ortalama_veriler = {
            'Kısırlaştırma': df['SON BİR YILDA KISIRLAŞTIRILAN TOPLAM HAYVAN SAYISI'].mean(),
            'Aşılama': df['SON BİR YILDA AŞILANAN SOKAK HAYVANI SAYISI'].mean(),
            'Mikroçip': df['SON BİR YILDA MİKROÇİP TAKILMIŞ SOKAK HAYVANI SAYISI'].mean()
        }

        belediye_veriler = {
            'Kısırlaştırma': row['SON BİR YILDA KISIRLAŞTIRILAN TOPLAM HAYVAN SAYISI'],
            'Aşılama': row['SON BİR YILDA AŞILANAN SOKAK HAYVANI SAYISI'],
            'Mikroçip': row['SON BİR YILDA MİKROÇİP TAKILMIŞ SOKAK HAYVANI SAYISI']
        }

        labels = list(ortalama_veriler.keys())
        x = np.arange(len(labels))
        width = 0.35

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(x - width / 2, [belediye_veriler[k] for k in labels], width, label=f'{belediye_adi_input}',
               color='skyblue')
        ax.bar(x + width / 2, [ortalama_veriler[k] for k in labels], width, label='Belediye Ortalaması',
               color='lightgray')

        ax.set_ylabel('Hayvan Sayısı')
        ax.set_title(f"{belediye_adi_input} vs Ortalama Belediye")
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()
        plt.tight_layout()

        # Streamlit ile görselleştirme
        st.pyplot(fig)

        # Dağılım içinde bu belediyeyi gösteren histplot'lar
        st.subheader("📌 Dağılım Oranlarına Göre Mevcut Belediye")
        for col, color, baslik in [
            ('SON BİR YILDA KISIRLAŞTIRILAN TOPLAM HAYVAN SAYISI', 'blue', 'Kısırlaştırma'),
            ('SON BİR YILDA AŞILANAN SOKAK HAYVANI SAYISI', 'green', 'Aşılama'),
            ('SON BİR YILDA MİKROÇİP TAKILMIŞ SOKAK HAYVANI SAYISI', 'orange', 'Mikroçip')
        ]:
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.histplot(df[col], bins=15, kde=True, color=color, ax=ax)
            ax.axvline(x=row[col], color='red', linestyle='--', label=f"{belediye_adi_input}")
            ax.set_title(f'{baslik} Sayısı Dağılımı - {belediye_adi_input} Gösteriliyor')
            ax.set_xlabel(f'{baslik} Sayısı')
            ax.set_ylabel('Belediye Sayısı')
            ax.legend()
            plt.tight_layout()

            # Streamlit ile her bir histogramı görselleştirme
            st.pyplot(fig)

        # İletişim
        st.subheader("📞 İLETİŞİM")
        st.write(f"Belediye İrtibat Numarası: {row['BELEDİYE İRTİBAT NUMARALARI']}")
