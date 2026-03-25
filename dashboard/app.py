import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ================================
# 🔧 PAGE CONFIG
# ================================
st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="🚨",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

# ================================
# 🎯 HEADER
# ================================
st.title("🚨 AI-Powered Fraud Detection System")
st.markdown("Detect suspicious financial transactions in real-time using Machine Learning")
st.divider()

# ================================
# 🎛️ SIDEBAR INPUTS
# ================================
with st.sidebar:
    st.header("⚙️ Transaction Details")
    step = st.number_input("Step (Hours)", min_value=1, value=1)
    type_tx = st.selectbox("Transaction Type", ["CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"])
    amount = st.number_input("Transaction Amount", min_value=0.0, value=1000.0)
    oldbalanceOrg = st.number_input("Old Balance (Sender)", value=5000.0)
    newbalanceOrig = st.number_input("New Balance (Sender)", value=4000.0)
    oldbalanceDest = st.number_input("Old Balance (Receiver)", value=0.0)
    newbalanceDest = st.number_input("New Balance (Receiver)", value=1000.0)

    predict_btn = st.button("🚀 Detect Fraud", type="primary", use_container_width=True)

# ================================
# 🚀 PREDICTION & DASHBOARD
# ================================
if predict_btn:
    payload = {
        "step": step,
        "type": type_tx,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest
    }
    
    with st.spinner("Analyzing risk..."):
        try:
            res = requests.post(f"{API_URL}/predict", json=payload)
            if res.status_code == 200:
                data = res.json()
                prob = data["probability"]
                is_fraud = data["is_fraud"]
                risk_score = data["risk_score"]

                # ================================
                # 💡 INSIGHTS / REAL-TIME ALERTS
                # ================================
                if prob > 0.7:
                    st.error("🚨 HIGH-RISK FRAUD DETECTED: Immediate investigation recommended.")
                elif prob > 0.4:
                    st.warning("⚠️ MODERATE RISK: Monitor transaction closely.")
                else:
                    st.success("✅ Transaction appears safe.")
                
                # ================================
                # 📊 KPI CARDS
                # ================================
                c1, c2, c3 = st.columns(3)
                c1.metric("Fraud Probability", f"{prob*100:.2f}%")
                
                risk_level = "HIGH 🚨" if prob > 0.7 else "MEDIUM ⚠️" if prob > 0.4 else "LOW ✅"
                c2.metric("Risk Level", risk_level)
                
                c3.metric("Prediction", "FRAUD" if is_fraud else "SAFE")
                st.divider()

                col_left, col_right = st.columns(2)
                
                with col_left:
                    # ================================
                    # 📈 VISUALIZATION
                    # ================================
                    st.subheader("📊 Risk Score Visualization")
                    fig1, ax1 = plt.subplots(figsize=(6,3))
                    ax1.bar(["Fraud Risk"], [prob], color="red" if prob > 0.5 else "green", width=0.4)
                    ax1.set_ylim(0, 1)
                    ax1.set_ylabel("Probability")
                    st.pyplot(fig1)
                    
                    # ================================
                    # 🔄 WHAT-IF ANALYSIS
                    # ================================
                    st.subheader("🔄 What-if Analysis (Amount Variance)")
                    st.caption("Simulating varied transaction amounts while proportionately adjusting final balances to maintain structural reality.")
                    scenarios = []
                    
                    # Original structural offset logic
                    error_orig_offset = newbalanceOrig + amount - oldbalanceOrg
                    error_dest_offset = oldbalanceDest + amount - newbalanceDest
                    
                    for amt in [amount * 0.5, amount, amount * 1.5]:
                        temp_payload = payload.copy()
                        temp_payload["amount"] = amt
                        
                        # Adjust mathematically so we don't accidentally manufacture an accounting error
                        temp_payload["newbalanceOrig"] = max(0.0, oldbalanceOrg - amt + error_orig_offset)
                        temp_payload["newbalanceDest"] = max(0.0, oldbalanceDest + amt - error_dest_offset)
                        
                        temp_res = requests.post(f"{API_URL}/predict", json=temp_payload).json()
                        scenarios.append({
                            "Amount": str(amt),
                            "Raw_Amt": amt,
                            "Fraud Probability": round(temp_res["probability"] * 100, 2)
                        })
                    
                    scenario_df = pd.DataFrame(scenarios)
                    st.dataframe(scenario_df[["Amount", "Fraud Probability"]])
                    
                    st.subheader("📊 Scenario Risk Comparison")
                    fig2, ax2 = plt.subplots(figsize=(6,3))
                    ax2.bar(scenario_df["Amount"], scenario_df["Fraud Probability"], width=0.4, color="orange")
                    ax2.set_xlabel("Transaction Amount ($)")
                    ax2.set_ylabel("Fraud %")
                    st.pyplot(fig2)

                with col_right:
                    # ================================
                    # 🔥 SHAP EXPLAINABILITY
                    # ================================
                    st.subheader("🔍 SHAP Explainability")
                    explain_res = requests.post(f"{API_URL}/explain", json=payload)
                    if explain_res.status_code == 200:
                        exp_data = explain_res.json()
                        df_shap = pd.DataFrame(exp_data["shap_values"])
                        
                        st.markdown("Positive SHAP values actively push the model toward **Fraud**. Negative values push it toward **Safe**.")
                        
                        top_features = df_shap.head(5).copy()
                        # Sort to make graph ordered
                        top_features = top_features.sort_values(by="value", ascending=True)

                        fig_shap, ax_shap = plt.subplots(figsize=(6,4))
                        colors = ['red' if val > 0 else 'green' for val in top_features["value"]]
                        ax_shap.barh(top_features["feature"], top_features["value"], color=colors)
                        ax_shap.set_xlabel("SHAP Value (Impact)")
                        st.pyplot(fig_shap)
                        
                        # ================================
                        # 🤖 CHATBOT ("Why is this fraud?")
                        # ================================
                        st.subheader("🤖 Chatbot: \"Why is this fraud?\"")
                        
                        # Rule-based natural language generator
                        top_driver = df_shap.iloc[0]
                        second_driver = df_shap.iloc[1]
                        
                        explain_text = f"**AI Diagnostic:** I categorized this as **HIGH RISK** primarily because the `{top_driver['feature']}` is abnormal. " if is_fraud else f"**AI Diagnostic:** I categorized this as **SAFE** primarily because the `{top_driver['feature']}` appears normal. "
                        
                        if top_driver["value"] > 0:
                            explain_text += f"This specific feature dramatically increased the probability of fraud (+{top_driver['value']:.2f} log-odds). "
                        else:
                            explain_text += f"This feature decreased the fraud risk (-{abs(top_driver['value']):.2f} log-odds). "
                        
                        if is_fraud and "errorBalance" in top_driver["feature"]:
                            explain_text += "\n\n*Explanation:* Our internal accounting checks show a massive discrepancy between what the user had, what they transferred, and what their final balance was recorded as. This is a massive red flag for bypassing accounting rules during a cash-out!"
                        
                        explain_text += f"\n\nA secondary factor was the `{second_driver['feature']}`."

                        if is_fraud:
                            st.error(explain_text)
                        else:
                            st.info(explain_text)
            else:
                st.error("API did not return a valid response. Check backend logs.")
        except Exception as e:
            st.error(f"Could not connect to Prediction API. Ensure it is running! Error: {e}")

# ================================
# 📋 FOOTER
# ================================
st.divider()
st.caption("Built with Machine Learning • Fraud Detection System")
