import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta
from scipy import stats

# ========== KONFIGURASI HALAMAN ==========
st.set_page_config(page_title="Olist Analytics Dashboard", layout="wide")
st.title("📊 Brazilian E‑Commerce Dashboard – Olist")
st.caption("Analisis pesanan, kepuasan pelanggan, dan segmentasi RFM")

# ========== LOAD DATA ==========
@st.cache_data
def load_data():
    # Sesuaikan path dengan lokasi file Anda
    df = pd.read_csv("df_clean.csv", parse_dates=[
        'order_purchase_timestamp',
        'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ])
    # Buat kolom kategori harga jika belum ada
    if 'price_category' not in df.columns:
        bins = [0, 50, 100, 200, 500, 1e7]
        labels = ['Budget (<50)', 'Ekonomis (50-100)', 'Medium (100-200)', 'Premium (200-500)', 'Luxury (>500)']
        df['price_category'] = pd.cut(df['price'], bins=bins, labels=labels)
    return df

df = load_data()

# ========== SIDEBAR FILTER (seperti bike sharing) ==========
with st.sidebar:
    st.header("🔍 Filter Data")

    # Filter Tahun
    tahun_tersedia = sorted(df['order_purchase_timestamp'].dt.year.unique())
    selected_tahun = st.multiselect(
        "Tahun",
        tahun_tersedia,
        default=tahun_tersedia
    )

    # Filter Status Order
    status_options = df['order_status'].unique()
    selected_status = st.multiselect(
        "Status Pesanan",
        status_options,
        default=['delivered']
    )

# ========== APLIKASI FILTER ==========
filtered_df = df[df['order_status'].isin(selected_status)]
if selected_tahun:
    filtered_df = filtered_df[filtered_df['order_purchase_timestamp'].dt.year.isin(selected_tahun)]

if filtered_df.empty:
    st.warning("⚠️ Tidak ada data dengan filter yang dipilih. Ubah filter.")
    st.stop()

# ========== METRIK UTAMA (ukuran kecil rapi) ==========
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Order", f"{len(filtered_df):,}")
col2.metric("Unique Customers", f"{filtered_df['customer_unique_id'].nunique():,}")
col3.metric("Unique Sellers", f"{filtered_df['seller_id'].nunique():,}")
col4.metric("Avg Review Score", f"{filtered_df['review_score'].mean():.2f} / 5")

st.markdown("---")

# ========== FUNGSI BANTU UNTUK PLOT YANG TIDAK TERLALU BESAR ==========
def set_plot_style():
    plt.rcParams['figure.figsize'] = (8, 4)   # ukuran sedang
    plt.rcParams['font.size'] = 10
    sns.set_style("whitegrid")

set_plot_style()

# ========== TAB LAYOUT ==========
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Tren & Review", 
    "🏆 Segmentasi RFM", 
    "🗺️ Lokasi Geografis", 
    "🛒 Kategori Harga"
])

# ---------------------------------------------
# TAB 1: Tren Order & Review (Pertanyaan 1 & 2)
# ---------------------------------------------
with tab1:
    st.subheader("Pertanyaan 1: Tren Order dan Review Score per Bulan")
    
    # Data bulanan
    monthly_orders = filtered_df.groupby(filtered_df['order_purchase_timestamp'].dt.to_period('M')).size().reset_index()
    monthly_orders.columns = ['bulan', 'jumlah_order']
    monthly_orders['bulan_str'] = monthly_orders['bulan'].astype(str)
    
    monthly_review = filtered_df.groupby(filtered_df['order_purchase_timestamp'].dt.to_period('M'))['review_score'].mean().reset_index()
    monthly_review.columns = ['bulan', 'avg_review']
    monthly_review['bulan_str'] = monthly_review['bulan'].astype(str)
    
    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots()
        ax.plot(monthly_orders['bulan_str'], monthly_orders['jumlah_order'], marker='o', color='steelblue', linewidth=2)
        ax.set_title("Jumlah Order per Bulan")
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Jumlah Order")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots()
        ax.plot(monthly_review['bulan_str'], monthly_review['avg_review'], marker='s', color='coral', linewidth=2)
        ax.set_title("Rata-rata Review Score per Bulan")
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Review Score (1-5)")
        ax.set_ylim(0,5)
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
    
    st.markdown("---")
    st.subheader("Pertanyaan 2: Dampak Lonjakan Order (November 2017)")
    
    nov_mask = (filtered_df['order_purchase_timestamp'].dt.year == 2017) & (filtered_df['order_purchase_timestamp'].dt.month == 11)
    nov_data = filtered_df[nov_mask]
    other_data = filtered_df[~nov_mask]
    
    if len(nov_data) > 0 and len(other_data) > 0:
        nov_avg = nov_data['review_score'].mean()
        other_avg = other_data['review_score'].mean()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Review Nov 2017", f"{nov_avg:.2f}")
        c2.metric("Review Bulan Lain", f"{other_avg:.2f}")
        c3.metric("Selisih", f"{nov_avg - other_avg:.2f}")
        
        # Bar chart perbandingan
        fig, ax = plt.subplots()
        bars = ax.bar(['Nov 2017', 'Bulan Lain'], [nov_avg, other_avg], color=['tomato', 'skyblue'])
        ax.set_ylabel("Review Score")
        ax.set_title("Rata-rata Review Score")
        ax.set_ylim(0,5)
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, f"{bar.get_height():.2f}", ha='center')
        st.pyplot(fig)
        
        # Persentase rating rendah vs tinggi
        nov_low = (nov_data['review_score'] <= 2).mean() * 100
        other_low = (other_data['review_score'] <= 2).mean() * 100
        nov_high = (nov_data['review_score'] >= 4).mean() * 100
        other_high = (other_data['review_score'] >= 4).mean() * 100
        
        fig, ax = plt.subplots()
        categories = ['Rating Rendah (1-2)', 'Rating Tinggi (4-5)']
        x = range(len(categories))
        width = 0.35
        ax.bar(x, [nov_low, nov_high], width, label='Nov 2017', color='tomato')
        ax.bar([i+width for i in x], [other_low, other_high], width, label='Bulan Lain', color='skyblue')
        ax.set_ylabel("Persentase (%)")
        ax.set_title("Perbandingan Rating")
        ax.set_xticks([i+width/2 for i in x])
        ax.set_xticklabels(categories)
        ax.legend()
        for i, v in enumerate([nov_low, nov_high]):
            ax.text(i, v+1, f"{v:.1f}%", ha='center')
        for i, v in enumerate([other_low, other_high]):
            ax.text(i+width, v+1, f"{v:.1f}%", ha='center')
        st.pyplot(fig)
        
        # Uji t
        t_stat, p_val = stats.ttest_ind(nov_data['review_score'].dropna(), other_data['review_score'].dropna(), equal_var=False)
        st.info(f"**Uji t independen:** p-value = {p_val:.4f} → {'Penurunan signifikan secara statistik' if p_val < 0.05 else 'Tidak signifikan'}")
    else:
        st.warning("Data November 2017 tidak tersedia setelah filter.")

# ---------------------------------------------
# TAB 2: SEGMENTASI RFM (Pertanyaan 3)
# ---------------------------------------------
with tab2:
    st.subheader("Segmentasi Pelanggan dengan RFM (Recency, Frequency, Monetary)")
    
    rfm_data = filtered_df[filtered_df['order_status'] == 'delivered'].copy()
    if len(rfm_data) == 0:
        st.warning("Tidak ada data delivered. Ubah filter.")
    else:
        ref_date = rfm_data['order_purchase_timestamp'].max() + timedelta(days=1)
        rfm = rfm_data.groupby('customer_unique_id').agg({
            'order_purchase_timestamp': lambda x: (ref_date - x.max()).days,
            'order_id': 'count',
            'price': 'sum'
        }).reset_index()
        rfm.columns = ['customer_unique_id', 'Recency', 'Frequency', 'Monetary']
        rfm = rfm.dropna()
        rfm = rfm[rfm['Recency'] >= 0]
        
        if len(rfm) < 4:
            st.warning("Data tidak cukup untuk quartile segmentation.")
        else:
            try:
                rfm['R_Score'] = pd.qcut(rfm['Recency'], 4, labels=['4','3','2','1'], duplicates='drop')
                rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=['1','2','3','4'], duplicates='drop')
                rfm['M_Score'] = pd.qcut(rfm['Monetary'], 4, labels=['1','2','3','4'], duplicates='drop')
            except Exception as e:
                st.error(f"Error pembuatan skor: {e}")
                rfm['R_Score'] = '2'
                rfm['F_Score'] = '2'
                rfm['M_Score'] = '2'
            
            def seg(row):
                if row['R_Score'] == '4' and row['F_Score'] == '4' and row['M_Score'] == '4':
                    return 'Champion'
                elif row['R_Score'] in ['4','3'] and row['F_Score'] in ['3','4']:
                    return 'Loyal'
                elif row['R_Score'] in ['1','2'] and row['F_Score'] in ['1','2']:
                    return 'At Risk'
                elif row['R_Score'] == '1':
                    return 'Lost'
                else:
                    return 'Regular'
            rfm['Segment'] = rfm.apply(seg, axis=1)
            
            col1, col2 = st.columns(2)
            with col1:
                seg_counts = rfm['Segment'].value_counts()
                fig, ax = plt.subplots()
                seg_counts.plot(kind='bar', color=['green','blue','orange','red','gray'], ax=ax)
                ax.set_title("Jumlah Customer per Segmen")
                ax.set_xlabel("Segment")
                ax.set_ylabel("Jumlah")
                ax.tick_params(axis='x', rotation=45)
                st.pyplot(fig)
            with col2:
                mon_seg = rfm.groupby('Segment')['Monetary'].mean().sort_values(ascending=False)
                fig, ax = plt.subplots()
                mon_seg.plot(kind='bar', color='purple', ax=ax)
                ax.set_title("Rata-rata Pengeluaran (R$) per Segmen")
                ax.set_ylabel("Monetary")
                ax.tick_params(axis='x', rotation=45)
                st.pyplot(fig)
            
            # Lokasi Champion
            cust_seg = rfm[['customer_unique_id', 'Segment']]
            cust_loc = filtered_df[['customer_unique_id', 'customer_state']].drop_duplicates()
            merged = cust_seg.merge(cust_loc, on='customer_unique_id')
            champion_states = merged[merged['Segment'] == 'Champion']['customer_state'].value_counts().head(5)
            st.subheader("📍 Top 5 State Customer Champion")
            fig, ax = plt.subplots()
            champion_states.plot(kind='bar', color='gold', ax=ax)
            ax.set_xlabel("State")
            ax.set_ylabel("Jumlah Champion")
            st.pyplot(fig)

# ---------------------------------------------
# TAB 3: LOKASI GEOGRAFIS
# ---------------------------------------------
with tab3:
    st.subheader("Distribusi Customer dan Seller per State")
    col1, col2 = st.columns(2)
    with col1:
        cust_state = filtered_df['customer_state'].value_counts().head(10)
        fig, ax = plt.subplots()
        cust_state.plot(kind='bar', color='steelblue', ax=ax)
        ax.set_title("Top 10 State Customer")
        ax.set_xlabel("State")
        ax.set_ylabel("Jumlah Customer")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)
    with col2:
        sell_state = filtered_df['seller_state'].value_counts().head(10)
        fig, ax = plt.subplots()
        sell_state.plot(kind='bar', color='darkorange', ax=ax)
        ax.set_title("Top 10 State Seller")
        ax.set_xlabel("State")
        ax.set_ylabel("Jumlah Seller")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)
    
    # Rute pengiriman terpopuler (opsional)
    st.subheader("Top 10 Rute Pengiriman (Seller State → Customer State)")
    df_route = filtered_df[['seller_state', 'customer_state']].dropna()
    route_counts = (df_route['seller_state'] + " → " + df_route['customer_state']).value_counts().head(10)
    fig, ax = plt.subplots()
    route_counts.plot(kind='barh', color='teal', ax=ax)
    ax.set_xlabel("Jumlah Order")
    ax.set_title("Rute Pengiriman Terpadat")
    st.pyplot(fig)

# ---------------------------------------------
# TAB 4: KATEGORI HARGA
# ---------------------------------------------
with tab4:
    st.subheader("Perilaku Belanja Berdasarkan Kategori Harga")
    price_dist = filtered_df['price_category'].value_counts()
    fig, ax = plt.subplots()
    price_dist.plot(kind='bar', color='mediumseagreen', ax=ax)
    ax.set_title("Distribusi Order per Kategori Harga")
    ax.set_xlabel("Kategori")
    ax.set_ylabel("Jumlah Order")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)
    
    st.subheader("Rata-rata Review Score per Kategori Harga")
    rev_price = filtered_df.groupby('price_category', observed=True)['review_score'].mean()
    fig, ax = plt.subplots()
    rev_price.plot(kind='bar', color='coral', ax=ax)
    ax.axhline(y=filtered_df['review_score'].mean(), color='blue', linestyle='--', label='Rata-rata overall')
    ax.set_ylim(0,5)
    ax.set_ylabel("Review Score")
    ax.legend()
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)
    
    # Heatmap (jika RFM tersedia)
    if 'Segment' in locals() and not rfm.empty:
        st.subheader("Heatmap: Kategori Harga vs Segment Customer")
        df_seg = filtered_df.merge(rfm[['customer_unique_id', 'Segment']], on='customer_unique_id', how='left')
        matrix = pd.crosstab(df_seg['price_category'], df_seg['Segment'], normalize='columns') * 100
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(matrix, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax)
        ax.set_title("Persentase (%) Kategori Harga per Segmen")
        st.pyplot(fig)

# ========== FOOTER SUMBER DATA ==========
st.markdown("---")
st.caption("Sumber data: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) | Dashboard dibuat dengan Streamlit")