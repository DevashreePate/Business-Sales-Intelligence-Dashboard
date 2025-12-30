import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ===============================
# PAGE CONFIGURATION
# ===============================
st.set_page_config(
    page_title="Sales Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# ===============================
# CUSTOM CSS FOR UI/UX
# ===============================
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}

.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
    text-align: center;
}

.metric-title {
    font-size: 18px;
    color: #6c757d;
}

.metric-value {
    font-size: 28px;
    font-weight: bold;
    color: #0d6efd;
}

.section {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# LOAD DATA
# ===============================
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_sales_data.csv")
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

df = load_data()

# ===============================
# TITLE
# ===============================
st.title("📊 Business Sales Intelligence Dashboard")
st.markdown("Gain insights into revenue, profit, products, and regional performance.")

# ===============================
# SIDEBAR FILTERS
# ===============================
st.sidebar.title("🔍 Dashboard Filters")
st.sidebar.markdown("Use filters to analyze sales data dynamically.")

year_filter = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df['Year'].unique()),
    default=sorted(df['Year'].unique())
)

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df['Region'].unique()),
    default=sorted(df['Region'].unique())
)

filtered_df = df[
    (df['Year'].isin(year_filter)) &
    (df['Region'].isin(region_filter))
]

# ===============================
# KPI CALCULATIONS
# ===============================
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_orders = filtered_df['Order ID'].nunique()

# ===============================
# KPI CARDS
# ===============================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">💰 Total Revenue</div>
        <div class="metric-value">₹ {total_sales:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">📈 Total Profit</div>
        <div class="metric-value">₹ {total_profit:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">🧾 Total Orders</div>
        <div class="metric-value">{total_orders}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ===============================
# SALES TREND SECTION
# ===============================
st.markdown("## 📅 Yearly Sales Trend")
with st.container():
    yearly_sales = filtered_df.groupby('Year')['Sales'].sum()

    fig1, ax1 = plt.subplots(figsize=(10,4))
    sns.lineplot(
        x=yearly_sales.index,
        y=yearly_sales.values,
        marker="o",
        linewidth=3,
        color="#0d6efd",
        ax=ax1
    )
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Sales")
    ax1.set_title("Year-wise Sales Performance")
    ax1.grid(alpha=0.3)
    st.pyplot(fig1)

# ===============================
# TOP PRODUCTS SECTION
# ===============================
st.markdown("## 🏆 Top 10 Products by Sales")
with st.container():
    top_products = (
        filtered_df.groupby('Product Name')['Sales']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig2, ax2 = plt.subplots(figsize=(10,4))
    sns.barplot(
        x=top_products.values,
        y=top_products.index,
        color="#0d6efd",
        ax=ax2
    )
    ax2.set_xlabel("Sales")
    ax2.set_ylabel("Product")
    ax2.set_title("Top Performing Products")
    st.pyplot(fig2)

# ===============================
# REGION DISTRIBUTION
# ===============================
st.markdown("## 🌍 Region-wise Sales Distribution")
with st.container():
    region_sales = filtered_df.groupby('Region')['Sales'].sum()

    fig3, ax3 = plt.subplots(figsize=(6,6))
    ax3.pie(
        region_sales.values,
        labels=region_sales.index,
        autopct='%1.1f%%',
        startangle=90
    )
    ax3.set_title("Sales Share by Region")
    st.pyplot(fig3)

# ===============================
# DATA TABLE
# ===============================
st.markdown("## 📋 Sales Data Preview")
st.dataframe(filtered_df)

# ===============================
# INSIGHTS SECTION
# ===============================
st.markdown("""
<div style="background-color:#e9f2ff; padding:20px; border-radius:10px;">
<b>📌 Key Business Insights</b><br><br>
• Identifies top-performing products and regions<br>
• Highlights yearly revenue growth trends<br>
• Enables data-driven strategic decisions
</div>
""", unsafe_allow_html=True)

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.markdown(
    "📊 **Business Sales Intelligence Dashboard** | Built using Python & Streamlit"
)
