import streamlit as st
st.set_page_config(
    page_title="Fraud Detection Dashboard",
    page_icon="💳",
    layout="wide"
)
import pandas as pd
import joblib
st.markdown("""
<style>
.main {
    background-color: #0e1117;
    color: white;
}
.stMetric {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("💳 Explainable Fraud Detection System")
st.markdown("### 🚀 Real-time Transaction Risk Analysis Dashboard")

# Load model safely
@st.cache_resource
def load_model():
    return joblib.load("../model/model.pkl")

model = load_model()

# Upload file
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)

        # FIX: remove target column
        if "Class" in data.columns:
            data = data.drop("Class", axis=1)

        st.subheader("📊 Data Preview")
        st.write(data.head())

        # Prediction
        preds = model.predict(data)
        probs = model.predict_proba(data)[:, 1]

        data["Fraud Prediction"] = preds
        data["Status"] = data["Fraud Prediction"].apply(
        lambda x: "🔴 Fraud" if x == 1 else "🟢 Safe"
        )

        st.subheader("📊 Key Metrics")

        col1, col2 , col3 = st.columns(3)

        with col1:
            st.metric("Total Transactions", len(data))

        with col2:
            st.metric("Fraud Detected", int(sum(preds)))
        
        with col3:
            fraud_rate = (sum(preds) / len(data)) * 100
            st.metric("Fraud Rate (%)", f"{fraud_rate:.2f}%")
            
        st.markdown("---")
        st.subheader("📈 Transaction Analysis (Highlighted)")
        def highlight_fraud(row):
            if row["Fraud Prediction"] == 1:
                return ['background-color: #ffcccc'] * len(row)  # light red
            else:
                return [''] * len(row)

        styled_df = data.head(100).style.apply(highlight_fraud, axis=1)

        st.dataframe(styled_df)

        st.success("✅ Predictions generated successfully!")

    except Exception as e:
        st.error(f"Error: {e}")

    st.subheader("🔍 Feature Importance (SHAP)")
    st.image("E:\Explainable-Fraud-Detection-System\images\shap_summary.png")

st.markdown("---")
st.markdown("Built with ❤️ using Machine Learning, SHAP & Streamlit")