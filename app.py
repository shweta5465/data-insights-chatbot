import streamlit as st
import pandas as pd
import plotly.express as px
from chatbot import ask_chatbot
from data_handler import load_data

st.set_page_config(
    page_title="Data Insights Chatbot",
    page_icon="📊",
    layout="wide"
)

df = load_data()

# ✅ Smart Chart Function - Works for ALL questions
def show_smart_chart(user_question):
    question = user_question.lower()

    try:
        # Region related
        if "region" in question:
            col = "Region"
            metric = "Profit" if "profit" in question else "Sales"
            chart_data = df.groupby(col)[metric].sum().reset_index()
            fig = px.bar(chart_data, x=col, y=metric,
                        title=f"📊 {metric} by Region",
                        color=col, text_auto=True)

        # Category related
        elif "category" in question and "sub" not in question:
            metric = "Profit" if "profit" in question else "Sales"
            chart_data = df.groupby("Category")[metric].sum().reset_index()
            fig = px.pie(chart_data, names="Category", values=metric,
                        title=f"📊 {metric} by Category")

        # Sub category
        elif "sub" in question or "sub-category" in question:
            metric = "Profit" if "profit" in question else "Sales"
            chart_data = df.groupby("Sub-Category")[metric].sum().reset_index()
            chart_data = chart_data.sort_values(metric, ascending=False)
            fig = px.bar(chart_data, x="Sub-Category", y=metric,
                        title=f"📊 {metric} by Sub-Category",
                        color=metric, text_auto=True)

        # Top products
        elif "product" in question or "top" in question:
            metric = "Profit" if "profit" in question else "Sales"
            n = 10 if "10" in question else 5
            chart_data = df.groupby("Product Name")[metric].sum().reset_index()
            chart_data = chart_data.sort_values(metric, ascending=False).head(n)
            fig = px.bar(chart_data, x=metric, y="Product Name",
                        orientation="h",
                        title=f"🏆 Top {n} Products by {metric}",
                        color=metric, text_auto=True)

        # Monthly or trend
        elif "month" in question or "trend" in question or "time" in question:
            df["Order Date"] = pd.to_datetime(df["Order Date"])
            df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
            chart_data = df.groupby("Month")["Sales"].sum().reset_index()
            fig = px.line(chart_data, x="Month", y="Sales",
                         title="📈 Monthly Sales Trend", markers=True)

        # Yearly
        elif "year" in question or "annual" in question:
            df["Order Date"] = pd.to_datetime(df["Order Date"])
            df["Year"] = df["Order Date"].dt.year
            chart_data = df.groupby("Year")["Sales"].sum().reset_index()
            fig = px.bar(chart_data, x="Year", y="Sales",
                        title="📊 Yearly Sales", color="Year", text_auto=True)

        # Segment
        elif "segment" in question or "customer" in question:
            metric = "Profit" if "profit" in question else "Sales"
            chart_data = df.groupby("Segment")[metric].sum().reset_index()
            fig = px.pie(chart_data, names="Segment", values=metric,
                        title=f"📊 {metric} by Customer Segment")

        # Ship mode
        elif "ship" in question or "shipping" in question:
            chart_data = df.groupby("Ship Mode")["Sales"].sum().reset_index()
            fig = px.bar(chart_data, x="Ship Mode", y="Sales",
                        title="🚚 Sales by Ship Mode",
                        color="Ship Mode", text_auto=True)

        # State or city
        elif "state" in question:
            chart_data = df.groupby("State")["Sales"].sum().reset_index()
            chart_data = chart_data.sort_values("Sales", ascending=False).head(10)
            fig = px.bar(chart_data, x="State", y="Sales",
                        title="📊 Top 10 States by Sales",
                        color="Sales", text_auto=True)

        elif "city" in question:
            chart_data = df.groupby("City")["Sales"].sum().reset_index()
            chart_data = chart_data.sort_values("Sales", ascending=False).head(10)
            fig = px.bar(chart_data, x="City", y="Sales",
                        title="📊 Top 10 Cities by Sales",
                        color="Sales", text_auto=True)

        # Profit general
        elif "profit" in question:
            chart_data = df.groupby("Category")["Profit"].sum().reset_index()
            fig = px.bar(chart_data, x="Category", y="Profit",
                        title="💰 Profit by Category",
                        color="Category", text_auto=True)

        # Discount
        elif "discount" in question:
            chart_data = df.groupby("Category")["Discount"].mean().reset_index()
            fig = px.bar(chart_data, x="Category", y="Discount",
                        title="🏷️ Average Discount by Category",
                        color="Category", text_auto=True)

        # Quantity
        elif "quantity" in question or "units" in question:
            chart_data = df.groupby("Category")["Quantity"].sum().reset_index()
            fig = px.bar(chart_data, x="Category", y="Quantity",
                        title="📦 Quantity Sold by Category",
                        color="Category", text_auto=True)

        # DEFAULT - show for ALL other questions
        else:
            chart_data = df.groupby("Category")["Sales"].sum().reset_index()
            fig = px.pie(chart_data, names="Category", values="Sales",
                        title="📊 Overall Sales by Category")

        # Show the chart
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        # If any error, always show default chart
        chart_data = df.groupby("Region")["Sales"].sum().reset_index()
        fig = px.bar(chart_data, x="Region", y="Sales",
                    title="📊 Sales by Region",
                    color="Region", text_auto=True)
        st.plotly_chart(fig, use_container_width=True)


# Title
st.title("📊 Data Insights Chatbot")
st.markdown("Ask me anything about your sales data!")

# Sidebar
with st.sidebar:
    st.header("📁 Dataset Info")
    st.write(f"**Rows:** {len(df)}")
    st.write(f"**Columns:** {len(df.columns)}")
    st.write("**Column Names:**")
    for col in df.columns:
        st.write(f"  - {col}")
    if st.checkbox("Show Raw Data"):
        st.dataframe(df.head(20))

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
user_input = st.chat_input("Ask about the data... e.g. What is the total sales by region?")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("assistant"):
        with st.spinner("Analyzing data..."):
            response = ask_chatbot(user_input, st.session_state.chat_history)
            st.write(response)
            # ✅ ALWAYS show a chart for every question
            show_smart_chart(user_input)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "assistant", "content": response})

# Quick buttons
st.markdown("---")
st.markdown("### 💡 Try these questions:")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📈 Sales by region"):
        st.info("Type: What is the total sales by region?")
with col2:
    if st.button("🏆 Top 5 products"):
        st.info("Type: What are the top 5 products by sales?")
with col3:
    if st.button("📅 Monthly trend"):
        st.info("Type: Show me the monthly sales trend")