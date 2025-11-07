import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# ⚙️ Page Configuration
# -------------------------------
st.set_page_config(page_title="Flipkart Analytics Dashboard", layout="wide")

# -------------------------------
# 🏷️ Title and Description
# -------------------------------
st.title("📊 Flipkart Order Analytics Dashboard")
st.write(
    """
    Upload your Flipkart orders dataset to explore insights like:
    - Most ordered categories  
    - Spending patterns  
    - Average delivery time  
    - Payment methods used  
    - Revenue by category  
    """
)

# -------------------------------
# 📁 File Upload
# -------------------------------
uploaded_file = st.file_uploader("📥 Upload your Flipkart Orders CSV file", type=["csv"])

if uploaded_file is not None:
    # Read CSV
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Convert dates
    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    if "delivery_date" in df.columns:
        df["delivery_date"] = pd.to_datetime(df["delivery_date"], errors="coerce")

    # Calculate delivery days
    if "order_date" in df.columns and "delivery_date" in df.columns:
        df["delivery_days"] = (df["delivery_date"] - df["order_date"]).dt.days

    # Total amount column
    if "price" in df.columns and "quantity" in df.columns:
        df["total_amount"] = df["price"] * df["quantity"]

    # -------------------------------
    # 📈 Summary Metrics
    # -------------------------------
    st.subheader("📌 Key Insights")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Orders", len(df))
    col2.metric("Unique Customers", df["customer_id"].nunique() if "customer_id" in df.columns else "N/A")
    col3.metric("Avg Delivery Days", round(df["delivery_days"].mean(), 2) if "delivery_days" in df.columns else "N/A")
    col4.metric("Total Revenue (₹)", f"{df['total_amount'].sum():,.0f}" if "total_amount" in df.columns else "N/A")

    st.divider()

    # -------------------------------
    # 📊 Visualizations
    # -------------------------------
    if "category" in df.columns:
        st.subheader("📦 Most Ordered Categories")
        cat_count = df["category"].value_counts().reset_index()
        cat_count.columns = ["Category", "Orders"]
        st.plotly_chart(px.bar(cat_count, x="Category", y="Orders", color="Category", title="Orders by Category"), use_container_width=True)

    if "total_amount" in df.columns and "category" in df.columns:
        st.subheader("💰 Revenue by Category")
        revenue = df.groupby("category")["total_amount"].sum().reset_index().sort_values(by="total_amount", ascending=False)
        st.plotly_chart(px.bar(revenue, x="category", y="total_amount", color="category", title="Revenue Distribution by Category"), use_container_width=True)

    if "order_date" in df.columns:
        st.subheader("📅 Orders Over Time")
        orders_over_time = df.groupby("order_date").size().reset_index(name="Orders")
        st.plotly_chart(px.line(orders_over_time, x="order_date", y="Orders", markers=True, title="Order Trend Over Time"), use_container_width=True)

    if "payment_type" in df.columns:
        st.subheader("💳 Payment Methods Used")
        payment_data = df["payment_type"].value_counts().reset_index()
        payment_data.columns = ["Payment Type", "Count"]
        st.plotly_chart(px.pie(payment_data, names="Payment Type", values="Count", title="Preferred Payment Methods"), use_container_width=True)

    st.divider()

    # -------------------------------
    # 🧾 Data Table
    # -------------------------------
    st.subheader("🔍 Data Preview")
    st.dataframe(df.head(20))

else:
    st.info("👆 Please upload a CSV file to start analyzing your Flipkart data.")
