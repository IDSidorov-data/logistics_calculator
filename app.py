import streamlit as st

# --- ЯДРО ЛОГИКИ ("СКЕЛЕТ") ---
def calculate_logistics_metrics(client_rate, carrier_rate, additional_costs=0):
    """Рассчитывает метрики для одной логистической операции."""
    if client_rate is None or carrier_rate is None:
        return None
    if client_rate <= 0:
        return None
    
    if additional_costs is None:
        additional_costs = 0

    gross_profit = client_rate - carrier_rate - additional_costs
    profitability = (gross_profit / client_rate) * 100

    return {
        "profit_rub": gross_profit,
        "profitability_pct": profitability
    }

# --- ИНТЕРФЕЙС ("МЫШЦЫ" + "КОЖА") v1.0 ---

st.set_page_config(
    page_title="Калькулятор маржинальности",
    page_icon="🚚",
    layout="centered"
)

st.title("Калькулятор маржинальности экспедитора 🚚")
st.write("Введите данные по рейсу, чтобы мгновенно рассчитать его эффективность.")

st.header("Входные данные")

col1, col2 = st.columns(2)

with col1:
    client_rate = st.number_input(
        "1. Ставка клиента, ₽", 
        step=1000.0, 
        placeholder="Сумма от заказчика",
        value=None 
    )

with col2:
    carrier_rate = st.number_input(
        "2. Ставка перевозчика, ₽", 
        step=1000.0, 
        placeholder="Сумма для исполнителя",
        value=None
    )

additional_costs = st.number_input(
    "3. Дополнительные расходы (опционально), ₽", 
    step=100.0, 
    placeholder="Платные дороги, стоянки...",
    value=None
)

results = calculate_logistics_metrics(client_rate, carrier_rate, additional_costs)

st.header("Результаты расчета")

if results:
    profit = results["profit_rub"]
    profitability = results["profitability_pct"]

    res_col1, res_col2 = st.columns(2)

    with res_col1:
        st.metric(label="Прибыль (маржа)", value=f"{profit:,.0f}".replace(',', ' ') + " ₽")

    with res_col2:
        st.metric(label="Маржинальность", value=f"{profitability:.1f} %")
    
    st.markdown("---")

    if profit > 0:
        st.success("### ✅ ВЫГОДНО")
    else:
        st.error("### ❌ УБЫТОЧНО")
else:
    st.info("Введите ставки клиента и перевозчика для начала расчета.")

st.markdown("---")
st.write("Прототип v1.0")