import streamlit as st
import pandas as pd
import locale

# --- CONFIGURAÇÕES DA PÁGINA ---
st.set_page_config(
    page_title="Simulador de Investimento GA4 360 - Proposta com Desconto",
    page_icon="📊",
    layout="centered"
)

# --- FUNÇÕES DE CÁLCULO ---

def format_currency(value):
    """Formata um número como moeda (R$)."""
    try:
        # Tenta configurar o locale para PT-BR, caso falhe usa formatação manual
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        return locale.currency(value, grouping=True, symbol=True)
    except locale.Error:
        return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def calculate_ga4_cost(events):
    """
    Calcula o investimento no GA4 360 com base na proposta com desconto.
    """
    if events <= 0:
        return 0, "N/A"
    
    if events <= 25:
        cost = 12525.09
        tier_label = "Nível A"
    elif events <= 500:
        base_cost = 12525.09
        overage_events = events - 25
        cost = base_cost + (overage_events * 52.73)
        tier_label = "Nível A"
    elif events <= 2500:
        base_cost = 37571.84
        overage_events = events - 500
        cost = base_cost + (overage_events * 11.44)
        tier_label = "Nível B"
    elif events <= 10000:
        base_cost = 60451.84
        overage_events = events - 2500
        cost = base_cost + (overage_events * 3.22)
        tier_label = "Nível C"
    elif events <= 25000:
        base_cost = 84601.84
        overage_events = events - 10000
        cost = base_cost + (overage_events * 2.45)
        tier_label = "Nível D"
    else:
        base_cost = 121351.84
        overage_events = events - 25000
        cost = base_cost + (overage_events * 2.45)
        tier_label = "Nível E"
        
    return cost, tier_label

# --- INTERFACE DA APLICAÇÃO ---

st.title("📊 Simulador de Investimento GA4 360")
st.subheader("Simulação com Proposta Comercial Aplicada")

with st.sidebar:
    st.header("⚙️ Insira seus dados")
    monthly_events_input = st.number_input(
        label="Volume de eventos mensais (em milhões)",
        min_value=0.0,
        value=0.0,
        step=10.0,
        help="Informe a quantidade total de eventos (em milhões) por mês."
    )

st.divider()

if monthly_events_input > 0:
    monthly_cost, reference_tier = calculate_ga4_cost(monthly_events_input)
    annual_cost = monthly_cost * 12

    st.subheader("📈 Sua Estimativa de Investimento")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Nível de Referência", value=reference_tier)
    with col2:
        st.metric(label="Valor Mensal Estimado", value=format_currency(monthly_cost))
    with col3:
        st.metric(label="Valor Anual Estimado", value=format_currency(annual_cost))

    st.info(f"Para **{monthly_events_input:,.0f} milhões** de eventos, seu investimento é calculado usando o **{reference_tier}** como base.".replace(',', '.'))
else:
    st.warning("Por favor, insira um volume de eventos maior que zero na barra lateral para calcular.")

with st.expander("Clique para ver os detalhes da proposta (Tabela de Preços)"):
    st.markdown("""
    A tabela abaixo reflete os valores da proposta com desconto. O cálculo considera o custo fixo do tier anterior somado ao volume excedente de milhões de eventos.
    """)
    
    price_data = {
        "Nível": ["A", "B", "C", "D", "E", "F"],
        "Faixa (Milhões)": ["0-25", "25-500", "500-2.500", "2.500-10.000", "10.000-25.000", "> 25.000"],
        "Valor por Milhão Excedente": ["-", "R$ 52,73", "R$ 11,44", "R$ 3,22", "R$ 2,45", "R$ 2,45"],
        "Cálculo do Investimento Mensal": [
            "Valor Fixo de R$ 12.525,09",
            "R$ 12.525,09 + (Eventos - 25M) * R$ 52,73",
            "R$ 37.571,84 + (Eventos - 500M) * R$ 11,44",
            "R$ 60.451,84 + (Eventos - 2.500M) * R$ 3,22",
            "R$ 84.601,84 + (Eventos - 10.000M) * R$ 2,45",
            "R$ 121.351,84 + (Eventos - 25.000M) * R$ 2,45"
        ]
    }
    price_df = pd.DataFrame(price_data)
    st.dataframe(price_df, use_container_width=True, hide_index=True)

st.divider()
st.caption("Esta é uma ferramenta de simulação baseada em uma proposta específica. Os valores devem ser validados formalmente.")