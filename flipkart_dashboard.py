import streamlit as st
import pandas as pd
import plotly.express as px

# ---- PAGE SETTINGS ----
st.set_page_config(page_title="Flipkart Analytics Dashboard", layout="wide")

st.title("📊 Flipkart Order Analytics Dashboard")
st.write("Upload your Flipkart order data (CSV) to explore categories, revenue, and delivery times!")

# ---- FILE UPLOAD ----
uploaded_file = st.file_uploader("📁 Upload CSV File", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Convert dates and calculate delivery days
    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    if "delivery_date" in df.columns:
        df["delivery_date"] = pd.to_datetime(df["delivery_date"], errors="coerce")
        df["delivery_days"] = (df["delivery_date"] - df["order_date"]).dt.days

    # Calculate total amount
    if "price" in df.columns and "quantity" in df.columns:
        df["total_amount"] = df["price"] * df["quantity"]

    # ---- METRICS ----
    st.subheader("📈 Summary Metrics")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Orders", len(df))
    c2.metric("Unique Customers", df["customer_id"].nunique() if "customer_id" in df.columns else "-")
    c3.metric("Avg Delivery Days", round(df["delivery_days"].mean(), 2) if "delivery_days" in df.columns else "-")
    c4.metric("Total Revenue (₹)", int(df["total_amount"].sum()) if "total_amount" in df.columns else 0)

    st.divider()

    # ---- VISUALS ----
    if "category" in df.columns:
        st.subheader("📦 Most Ordered Categories")
        cat_counts = df["category"].value_counts().reset_index()
        cat_counts.columns = ["category", "orders"]
        st.plotly_chart(px.bar(cat_counts, x="orders", y="category", orientation="h",
                               title="Most Ordered Categories"), use_container_width=True)

    if "total_amount" in df.columns and "category" in df.columns:
        st.subheader("💰 Revenue by Category")
        rev = df.groupby("category")["total_amount"].sum().reset_index()
        st.plotly_chart(px.bar(rev, x="category", y="total_amount",
                               title="Revenue by Category"), use_container_width=True)

    if "order_date" in df.columns:
        st.subheader("📅 Orders Over Time")
        timeline = df.groupby("order_date").size().reset_index(name="orders")
        st.plotly_chart(px.line(timeline, x="order_date", y="orders", markers=True,
                                title="Orders Over Time"), use_container_width=True)

        if "payment_type" in df.columns:
        st.subheader("💳 Payment Methods Used")
        pay = df["payment_type"].value_counts().reset_index()
        pay.columns = ["Payment Type", "Count"]
        st.plotly_chart(
            px.pie(
                pay,
                names="Payment Type",
                values="Count",
                title="Payment Methods Used"
            ),
            use_container_width=True
        )

    st.divider()
    st.subheader("🧾 Data Preview")
    st.dataframe(df.head(100))
else:
    st.info("👆 Upload a Flipkart CSV file to start analysis.")
