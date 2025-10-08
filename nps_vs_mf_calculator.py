import streamlit as st
import math

st.set_page_config(page_title="NPS vs Mutual Fund Calculator", layout="centered")

st.title("🏦 NPS vs Mutual Fund - Retirement Comparison Calculator")

st.markdown("""
Adjust the parameters below to see how **NPS** and **Mutual Fund** investments compare
for long-term retirement planning.  
The model assumes systematic investment for the pre-retirement phase and systematic withdrawal post-retirement.
""")

# ---------------------- Inputs -----------------------
st.sidebar.header("🔧 Input Parameters")

monthly_invest = st.sidebar.number_input("Monthly Pre-Tax Investable Amount (₹)", min_value=100.0, value=100.0, step=10.0)
years_invest = st.sidebar.slider("Years to Retirement", 10, 40, 20)
years_retire = st.sidebar.slider("Years in Retirement", 10, 40, 30)

tax_pre = st.sidebar.slider("Pre-Retirement Tax Rate (%)", 0, 50, 33)
tax_post = st.sidebar.slider("Post-Retirement Tax Rate (%)", 0, 50, 30)

nps_return = st.sidebar.number_input("NPS Return Before Retirement (%)", value=10.0, step=0.1)
mf_return_pre = st.sidebar.number_input("MF Return Before Retirement (%)", value=11.5, step=0.1)
mf_return_post = st.sidebar.number_input("MF Return After Retirement (%)", value=11.5, step=0.1)

annuity_rate = st.sidebar.number_input("Annuity Rate (%)", value=6.0, step=0.1)
ltcg_effective_tax = st.sidebar.slider("Effective MF Withdrawal Tax (%)", 0, 20, 5)

st.sidebar.markdown("---")
st.sidebar.markdown("Made by 💼 Abhinav Tripathi")

# ---------------------- Helper Functions -----------------------
def fv(p, r, n):
    """Future value of monthly investment."""
    return p * ((1 + r/12)**(12*n) - 1) / (r/12)

def annual_withdrawal(corpus, r, n):
    """Annual withdrawal for given return and duration to deplete corpus."""
    r_annual = r / 100
    return corpus * (r_annual / (1 - (1 + r_annual)**(-n)))

# ---------------------- Core Calculations -----------------------
# Post-tax MF invest
mf_invest = monthly_invest * (1 - tax_pre / 100)

# 20-year corpus
nps_corpus = fv(monthly_invest, nps_return / 100, years_invest)
mf_corpus = fv(mf_invest, mf_return_pre / 100, years_invest)

# NPS splits
nps_mf = nps_corpus * 0.6
nps_annuity = nps_corpus * 0.4

# Post-retirement withdrawals
nps_annuity_income = nps_annuity * annuity_rate / 100 * (1 - tax_post / 100)
nps_mf_income = annual_withdrawal(nps_mf, mf_return_post, years_retire) * (1 - ltcg_effective_tax / 100)
mf_income = annual_withdrawal(mf_corpus, mf_return_post, years_retire) * (1 - ltcg_effective_tax / 100)

# ---------------------- Display Results -----------------------
st.subheader("📊 Results Summary")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 🏦 NPS Route")
    st.metric("20-Year Corpus (₹)", f"{nps_corpus:,.0f}")
    st.metric("Post-tax Annual Income (₹)", f"{nps_annuity_income + nps_mf_income:,.0f}")
with col2:
    st.markdown("### 📈 Mutual Fund Route")
    st.metric("20-Year Corpus (₹)", f"{mf_corpus:,.0f}")
    st.metric("Post-tax Annual Income (₹)", f"{mf_income:,.0f}")

# Comparative summary
st.markdown("---")
if (nps_annuity_income + nps_mf_income) > mf_income:
    diff = ((nps_annuity_income + nps_mf_income) / mf_income - 1) * 100
    st.success(f"✅ **NPS is better** by {diff:.1f}% in annual post-tax retirement income.")
else:
    diff = ((mf_income / (nps_annuity_income + nps_mf_income)) - 1) * 100
    st.warning(f"✅ **Mutual Fund is better** by {diff:.1f}% in annual post-tax retirement income.")

st.markdown("---")
st.caption("📘 This tool assumes consistent returns and simplified taxation (flat LTCG on withdrawals). For financial planning, always consider inflation, market risk, and changing tax laws.")
