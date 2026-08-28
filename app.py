import streamlit as st
from src.config import GOALS, CURRENCIES
from src.financial_calculator import calculate_financials
from src.chains import get_llm, stream_recommendations
from src.cache_manager import configure_llm_cache
from src.utils import parse_llm_json

import streamlit as st

# 1. Check if the user has already entered their API key in this session
if 'api_key_entered' not in st.session_state:
    st.session_state.api_key_entered = False

if not st.session_state.api_key_entered:
    # --- BEAUTIFUL AUTHENTICATION SCREEN FOR FINWISE ---
    
    # Center-aligned headers for FinWise
    st.markdown(
        """
        <h1 style='text-align: center;'>📈 FinWise AI</h1>
        <p style='text-align: center; color: #666666; font-size: 18px;'>
            AI-Powered Personal Financial Analysis and Smart Budget Assistant
        </p>
        <br><br>
        """, 
        unsafe_allow_html=True
    )
    
    left_spacer, center_column, right_spacer = st.columns([1, 1.5, 1])
    
    with center_column:
        st.markdown("### 🔐 Enter OpenAI API Key")
        
        # The input field
        user_key = st.text_input(
            label="OpenAI API Key",
            type="password",
            placeholder="sk-...",
            label_visibility="collapsed"
        )
        
        st.caption("Your API key is used strictly for this session and is not saved.")
        
        # The continue button
        if st.button("Continue ➔", type="primary", use_container_width=True):
            if user_key.startswith("sk-"): 
                # Save it as 'user_api_key' to match your FinWise code
                st.session_state.user_api_key = user_key 
                st.session_state.api_key_entered = True
                st.rerun() 
            else:
                st.error("Please enter a valid OpenAI API key (starts with 'sk-').")
                
    # Stop the rest of the app from running until this screen is passed
    st.stop()

# ==========================================
# --- MAIN FINWISE DASHBOARD STARTS HERE ---
# ==========================================


with st.sidebar:
    st.title("📈 FinWise AI")
    # ... your markdown and disclaimers ...
    
    st.divider()
    
    # REPLACED LINE: Pull the key directly from the landing page
    user_api_key = st.session_state.user_api_key
    
    cache_option = st.radio("Cache Strategy", ["Memory (Fastest)", "SQLite (Persistent)"])
if not user_api_key:
    st.info("👈 Please enter your OpenAI API Key in the sidebar to access the dashboard.")
    st.stop()

# 3. Main Dashboard UI
st.title("Financial Analysis Dashboard")
display_disclaimer()

# Form for user inputs
with st.form("financial_form"):
    st.subheader("Monthly Financial Data")
    
    col1, col2 = st.columns(2)
    with col1:
        currency = st.selectbox("Currency", CURRENCIES)
        monthly_income = st.number_input("Monthly Income", min_value=0, value=5000, step=100)
        current_savings = st.number_input("Current Monthly Savings", min_value=0, value=1000, step=100)
        financial_goal = st.selectbox("Primary Financial Goal", GOALS)
        
    with col2:
        st.markdown("**Monthly Expenses**")
        ex_housing = st.number_input("Housing / Rent", min_value=0, value=0)
        ex_food = st.number_input("Food", min_value=0, value=0)
        ex_transport = st.number_input("Transportation", min_value=0, value=0)
        ex_utilities = st.number_input("Utilities", min_value=0, value=0)
        
    with st.expander("Additional Expense Categories"):
        col3, col4 = st.columns(2)
        with col3:
            ex_edu = st.number_input("Education", min_value=0, value=0)
            ex_health = st.number_input("Healthcare", min_value=0, value=0)
            ex_debt = st.number_input("Loan / Debt Payments", min_value=0, value=0)
        with col4:
            ex_entertainment = st.number_input("Entertainment", min_value=0, value=0)
            ex_personal = st.number_input("Personal Care", min_value=0, value=0)
            ex_other = st.number_input("Other", min_value=0, value=0)

    submitted = st.form_submit_button("Analyze Finances")

# 4. Processing and Output
if submitted:
    # 1. Validation to stop execution if the key is missing
    if not user_api_key:
        st.error("Please enter your OpenAI API Key in the sidebar before analyzing finances.")
        st.stop()

    expenses_dict = {
        "Housing/Rent": ex_housing, "Food": ex_food, "Transportation": ex_transport,
        "Utilities": ex_utilities, "Education": ex_edu, "Healthcare": ex_health,
        "Loan/Debt": ex_debt, "Entertainment": ex_entertainment, 
        "Personal Care": ex_personal, "Other": ex_other
    }
    
    # Run deterministic calculations
    calcs = calculate_financials(monthly_income, expenses_dict, current_savings)
    
    st.divider()
    st.subheader("1. Financial Overview (Calculated)")
    
    # Display calculated metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Income", f"{monthly_income:,.2f}")
    m2.metric("Total Expenses", f"{calcs['total_expenses']:,.2f}")
    m3.metric("Remaining Income", f"{calcs['remaining_income']:,.2f}")
    m4.metric("Savings Ratio", f"{calcs['savings_ratio']}%")
    
    # THIS WAS MISSING: Prepare LLM Inputs
    expense_breakdown_str = "\n".join([f"{k}: {v}" for k, v in expenses_dict.items()])
    llm_inputs = {
        "monthly_income": monthly_income,
        "total_expenses": calcs["total_expenses"],
        "remaining_income": calcs["remaining_income"],
        "savings": current_savings,
        "savings_ratio": calcs["savings_ratio"],
        "expense_ratio": calcs["expense_ratio"],
        "financial_goal": financial_goal,
        "expense_breakdown": expense_breakdown_str
    }
    
    st.divider()
    st.subheader("2. AI Analysis Generation")
    
    # Pass the user's key into your function
    llm = get_llm(user_api_key)
    
    # Stream the raw generation 
    with st.expander("View Raw AI Streaming Data", expanded=True):
        st.write("Streaming AI insights...")
        raw_response = st.write_stream(stream_recommendations(llm, llm_inputs))
    
    # Parse the streamed JSON
    parsed_data = parse_llm_json(raw_response)
    
    # Render the structured dashboard
    st.subheader("3. FinWise AI Insights")
    
    colA, colB = st.columns(2)
    with colA:
        st.metric("AI Financial Health Score", f"{parsed_data.get('financial_health_score', 0)} / 100")
        st.progress(parsed_data.get('financial_health_score', 0) / 100)
    with colB:
        st.info(f"**Risk Level:** {parsed_data.get('risk_level', 'N/A')}")
        
    st.markdown(f"**Summary:** {parsed_data.get('financial_summary', 'N/A')}")
    
    tab1, tab2, tab3 = st.tabs(["Spending Analysis", "Action Plan", "Recommendations"])
    
    with tab1:
        for item in parsed_data.get("spending_analysis", []):
            st.markdown(f"- **{item.get('category')}**: {item.get('observation')} -> *{item.get('recommendation')}*")
            
    with tab2:
        st.markdown("### Top Priorities")
        for priority in parsed_data.get("top_priorities", []):
            st.markdown(f"- {priority}")
        st.markdown("### Next Month's Plan")
        for plan in parsed_data.get("next_month_action_plan", []):
            st.markdown(f"- {plan}")
            
    with tab3:
        st.markdown("### Budget Strategy")
        for rec in parsed_data.get("budget_recommendations", []):
            st.markdown(f"- {rec}")
        st.markdown("### Savings Strategy")
        for strat in parsed_data.get("savings_strategy", []):
            st.markdown(f"- {strat}")