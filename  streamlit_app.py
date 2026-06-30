# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Infra TCO Calculator", page_icon="💰", layout="wide")

# --- SIDEBAR INPUTS ---
st.sidebar.header("🎛️ Workload Parameters")
num_gpus = st.sidebar.slider("Number of GPUs", min_value=10, max_value=1000, value=100, step=10)
training_hours = st.sidebar.slider("Training Duration (Hours)", min_value=100, max_value=2000, value=720, step=50)

st.sidebar.markdown("---")
st.sidebar.header("💲 Pricing Inputs ($/GPU/hr)")
on_demand_price = st.sidebar.number_input("Legacy On-Demand Price", value=2.50, step=0.10)
raw_spot_price = st.sidebar.number_input("Raw Spot Price", value=0.80, step=0.10)
managed_spot_price = st.sidebar.number_input("Proposed Managed Spot Price", value=1.00, step=0.10)

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Efficiency & Overhead")
idle_waste_pct = st.sidebar.slider("On-Demand Idle Waste (%)", 0.0, 50.0, 20.0) / 100
interruption_overhead_pct = st.sidebar.slider("Raw Spot Interruption Overhead (%)", 0.0, 50.0, 15.0) / 100
manual_eng_overhead = st.sidebar.number_input("Manual Spot Eng. Overhead ($)", value=6000, step=500)

# --- CALCULATIONS ---
# 1. Legacy On-Demand
legacy_ondemand_compute = num_gpus * training_hours * on_demand_price
legacy_ondemand_tco = legacy_ondemand_compute # Waste is baked into the high rate

# 2. Legacy Raw Spot
raw_spot_effective_hours = training_hours / (1 - interruption_overhead_pct)
legacy_rawspot_compute = num_gpus * raw_spot_effective_hours * raw_spot_price
legacy_rawspot_tco = legacy_rawspot_compute + manual_eng_overhead

# 3. Proposed Managed Spot (Tier 3)
proposed_managed_compute = num_gpus * training_hours * managed_spot_price
proposed_managed_tco = proposed_managed_compute

# Savings
savings_vs_ondemand = legacy_ondemand_tco - proposed_managed_tco
savings_pct = (savings_vs_ondemand / legacy_ondemand_tco) * 100 if legacy_ondemand_tco > 0 else 0

# --- MAIN UI ---
st.title("💰 AI Infrastructure TCO & ROI Calculator")
st.markdown("Proving that **Efficiency-Aligned Pricing** (Managed Spot) beats Legacy Compute pricing by eliminating idle waste and manual overhead.")

# Metric Cards
col1, col2, col3 = st.columns(3)
col1.metric("Legacy On-Demand TCO", f"${legacy_ondemand_tco:,.0f}", delta=f"{idle_waste_pct*100}% idle waste", delta_color="inverse")
col2.metric("Legacy Raw Spot TCO", f"${legacy_rawspot_tco:,.0f}", delta=f"${manual_eng_overhead:,.0f} eng. overhead", delta_color="inverse")
col3.metric("Proposed Managed Spot TCO", f"${proposed_managed_tco:,.0f}", delta="0% waste / 0 eng. overhead", delta_color="normal")

st.markdown("---")

# The "Aha" Moment
st.success(f"### 🚀 The 'Aha' Moment: Switch to Managed Spot to save **${savings_vs_ondemand:,.0f}** ({savings_pct:.1f}% reduction in TCO)!")

# Charts
st.subheader("📊 TCO Breakdown Comparison")

# Prepare data for Plotly
df_chart = pd.DataFrame({
    'Pricing Model': ['Legacy On-Demand', 'Legacy Raw Spot', 'Proposed Managed Spot'],
    'Compute Cost': [legacy_ondemand_compute, legacy_rawspot_compute, proposed_managed_compute],
    'Hidden Costs/Waste': [legacy_ondemand_compute * idle_waste_pct, manual_eng_overhead, 0]
})

fig = px.bar(df_chart, x='Pricing Model', y=['Compute Cost', 'Hidden Costs/Waste'],
             title="Total Cost of Ownership (TCO) Breakdown",
             labels={'value': 'Cost ($)', 'variable': 'Cost Component'},
             color_discrete_sequence=['#1f77b4', '#ff7f0e'])
fig.update_layout(barmode='stack', xaxis_tickangle=-45, height=500)
st.plotly_chart(fig, use_container_width=True)

# Data Table & Download
st.subheader("📋 Detailed Financial Model")
df_table = pd.DataFrame({
    'Metric': ['Base Price ($/GPU/hr)', 'Total GPU Hours Billed', 'Compute Cost ($)', 'Hidden Costs ($)', 'TOTAL TCO ($)'],
    'Legacy On-Demand': [f"${on_demand_price:.2f}", f"{num_gpus * training_hours:,}", f"${legacy_ondemand_compute:,.2f}", f"${legacy_ondemand_compute * idle_waste_pct:,.2f}", f"${legacy_ondemand_tco:,.2f}"],
    'Legacy Raw Spot': [f"${raw_spot_price:.2f}", f"{num_gpus * raw_spot_effective_hours:,.0f}", f"${legacy_rawspot_compute:,.2f}", f"${manual_eng_overhead:,.2f}", f"${legacy_rawspot_tco:,.2f}"],
    'Proposed Managed Spot': [f"${managed_spot_price:.2f}", f"{num_gpus * training_hours:,}", f"${proposed_managed_compute:,.2f}", "$0.00", f"${proposed_managed_tco:,.2f}"]
})
st.dataframe(df_table, use_container_width=True, hide_index=True)

# Download button
csv = df_table.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Financial Model (CSV)",
    data=csv,
    file_name='ai_tco_comparison.csv',
    mime='text/csv',
)

# Footer
st.markdown("---")
st.caption("Built for Project 1: Value-Based Pricing & Packaging for AI Platforms. | Powered by Streamlit.")