import streamlit as st
from engine.registry import load_tariffs
from engine.compare import compare_two_tariffs, find_lowest_cost_tariff
from engine.defaults import DEFAULT_TOU_SPLITS

st.set_page_config(layout="wide")
st.title("SCE Tariff Comparison & Recommendation Tool")

tariffs = load_tariffs()

tariff_names = [t['tariff'] for t in tariffs]

st.sidebar.header("Tariff Selection")
t1_name = st.sidebar.selectbox("Tariff A", tariff_names, index=0)
t2_name = st.sidebar.selectbox("Tariff B", tariff_names, index=1)

st.sidebar.header("Usage Inputs")nbilling_days = st.sidebar.number_input("Billing Days", value=30)
total_kwh = st.sidebar.number_input("Total Monthly kWh", value=1200)
peak_kw = st.sidebar.number_input("Peak Demand (kW)", value=6.5)
rider = st.sidebar.number_input("Riders ($/kWh)", value=0.03)
tax = st.sidebar.number_input("Tax Rate", value=0.08)

tariff_a = next(t for t in tariffs if t['tariff'] == t1_name)
tariff_b = next(t for t in tariffs if t['tariff'] == t2_name)

st.subheader("Estimated TOU Allocation (No Interval Data)")

usage_split = {}
remaining = 1.0
for p in tariff_a['tou_periods']:
    default = DEFAULT_TOU_SPLITS.get(p, 1/len(tariff_a['tou_periods']))
    usage_split[p] = st.slider(p.replace('_',' ').title(), 0.0, remaining, default)
    remaining -= usage_split[p]

usage_kwh = {p: usage_split[p] * total_kwh for p in usage_split}

if st.button("Compare Tariffs"):
    result = compare_two_tariffs(tariff_a, tariff_b, usage_kwh, peak_kw, nbilling_days, rider, tax)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(result['tariff_a']['tariff'])
        for li in result['tariff_a']['line_items']:
            st.write(f"{li['name']}: ${li['amount']}")
        st.write(f"**Total: ${result['tariff_a']['total']}**")

    with col2:
        st.subheader(result['tariff_b']['tariff'])
        for li in result['tariff_b']['line_items']:
            st.write(f"{li['name']}: ${li['amount']}")
        st.write(f"**Total: ${result['tariff_b']['total']}**")

    st.markdown("---")
    st.subheader("Estimated Lowest Cost Eligible Tariff")
    ranked = find_lowest_cost_tariff(tariffs, usage_kwh, peak_kw, nbilling_days, rider, tax)
    for i, (name, total) in enumerate(ranked):
        st.write(f"{i+1}. {name}: ${total}")
