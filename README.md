# 📊 Proyek Analisis Data: Brazilian E-Commerce (Olist)

Proyek ini merupakan analisis data end-to-end terhadap dataset e-commerce Olist untuk memahami **tren bisnis, kepuasan pelanggan, dan segmentasi customer bernilai tinggi**.

---

## 📌 Ikhtisar

Analisis ini bertujuan untuk:

* Mengidentifikasi tren pertumbuhan jumlah order.
* Menganalisis dampak lonjakan transaksi terhadap kepuasan pelanggan.
* Mengelompokkan customer berdasarkan nilai bisnis menggunakan **RFM Analysis**.
* Menggali pola geografis dan perilaku pembelian.

---

## 🔍 Alur Analisis Data

Analisis dilakukan secara sistematis untuk memastikan insight yang valid dan dapat diinterpretasikan:

### 1. Data Assessing

* Memahami struktur data dari berbagai tabel (orders, customers, reviews, dll).
* Mengidentifikasi missing values, duplikasi, dan inkonsistensi.

### 2. Data Cleaning

* Menghapus data duplikat.
* Menangani missing values.
* Konversi tipe data (terutama datetime).
* Menggabungkan tabel menjadi dataset utama (`df_clean.csv`).

### 3. Exploratory Data Analysis (EDA)

* Analisis distribusi order, review score, dan harga.
* Identifikasi pola awal dan anomali.
* Eksplorasi hubungan antar variabel.

### 4. Data Visualization & Explanatory Analysis

* Visualisasi tren order per bulan.
* Analisis perubahan review score.
* Perbandingan kondisi normal vs high season.
* Penyajian insight berbasis grafik.

### 5. Analisis Lanjutan

* **RFM Analysis** → segmentasi customer.
* **Geospatial Analysis** → distribusi customer & seller.
* **Behavior Analysis** → pola pembelian berdasarkan harga produk.

---

## 📊 Insight Bisnis

### 1. Tren Pertumbuhan Order (2016–2018)

Platform Olist menunjukkan pertumbuhan transaksi yang konsisten dan berkelanjutan.

* Puncak order: **November 2017 (8.084 order)**
* High season: **Mei – Agustus (puncak Agustus: 11.555 order)**
* Low season: **September**

💡 **Insight:**
Pertumbuhan mencerminkan ekspansi bisnis nyata, bukan hanya faktor musiman.

📌 **Implikasi:**

* Perlu kesiapan stok dan logistik sejak April
* Skalabilitas operasional menjelang akhir tahun

---

### 2. Dampak Lonjakan Order terhadap Kepuasan

Lonjakan order di November 2017 berdampak negatif (namun terbatas):

* Review score turun: **4,09 → 3,91**
* Rating rendah naik: **14,6% → 19,0% (+30%)**
* Uji statistik: **signifikan (p-value = 0,0000)**

💡 **Insight:**
Kualitas layanan tertekan saat demand tinggi.

📌 **Rekomendasi:**

* Tambah kapasitas kurir
* Perkuat customer service
* Optimalkan estimasi pengiriman

---

### 3. Customer Paling Berharga (RFM Analysis)

* **Champion:** 2.030 customer (2,1%)
* Rata-rata spending: **R$ 374,73**

Karakteristik:

* Tidak sering belanja (1–2 transaksi)
* Nilai transaksi tinggi
* Pembelian recent

Lokasi dominan:

* São Paulo, Rio de Janeiro, Minas Gerais, RS, PR

Perilaku:

* Dominan produk **Medium–Premium**
* Minim produk Budget

💡 **Insight:**
Customer bernilai tinggi ditentukan oleh **nilai transaksi, bukan frekuensi**.

📌 **Strategi:**

* Loyalty program bertingkat
* Early access produk premium
* Reaktivasi customer Lost

---

## 📊 Dashboard Interaktif

Dashboard dibuat menggunakan **Streamlit** dan dapat diakses di:

👉 https://braziliandashboard.streamlit.app/

Fitur:

* Tren order & review
* Analisis high season
* Segmentasi RFM
* Analisis geografis
* Kategori harga produk

---

## 📁 Struktur Proyek

```
📁 proyek-analisis-data/
│
├── notebook.ipynb
├── dashboard.py
├── df_clean.csv
├── requirements.txt
└── README.md
```

---

## ⚙️ Teknologi yang Digunakan

* Python
* Pandas & NumPy
* Matplotlib & Seaborn
* SciPy (statistical testing)
* Plotly
* Streamlit

---

## 📚 Sumber Data

Dataset yang digunakan berasal dari:

* [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce?utm_source=chatgpt.com)

Dataset ini berisi sekitar **100.000 transaksi e-commerce (2016–2018)** yang mencakup informasi order, pembayaran, pelanggan, lokasi, hingga review pelanggan, sehingga memungkinkan analisis dari berbagai perspektif bisnis. ([Kaggle][1])

---

## 🚀 Kesimpulan

Analisis ini menunjukkan bahwa:

* Olist mengalami pertumbuhan bisnis yang kuat.
* Lonjakan permintaan dapat menurunkan kualitas layanan jika tidak diantisipasi.
* Customer bernilai tinggi ditentukan oleh nilai transaksi, bukan frekuensi.

Dengan insight ini, bisnis dapat:

* Mengoptimalkan strategi operasional
* Meningkatkan kepuasan pelanggan
* Memaksimalkan customer lifetime value

---

[1]: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce?utm_source=chatgpt.com "Brazilian E-Commerce Public Dataset by Olist"
