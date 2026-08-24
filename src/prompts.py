from langchain_core.prompts import ChatPromptTemplate

# The exact JSON schema required by the assignment
JSON_SCHEMA = """
{
  "financial_summary": "",
  "financial_health_score": 0,
  "spending_analysis": [
    {"category": "", "observation": "", "recommendation": ""}
  ],
  "risk_level": "",
  "top_priorities": [],
  "budget_recommendations": [],
  "savings_strategy": [],
  "next_month_action_plan": []
}
"""

# System instruction enforcing the educational role and structured output
SYSTEM_INSTRUCTION = """
You are FinWise AI, an educational personal financial analysis assistant.
IMPORTANT: You must provide educational insights only. You cannot provide guaranteed investment advice or execute transactions.

You must return your analysis strictly as a JSON object matching this exact schema:
{json_schema}

Do not include any markdown formatting like ```json or trailing text. Return only the raw JSON.
"""

# Human message dynamically passing the required variables
USER_MESSAGE = """
Analyze my monthly finances based on the following data:
- Monthly Income: {monthly_income}
- Total Expenses: {total_expenses}
- Remaining Income: {remaining_income}
- Current Savings: {savings}
- Savings Ratio: {savings_ratio}%
- Expense Ratio: {expense_ratio}%
- Financial Goal: {financial_goal}

Expense Breakdown:
{expense_breakdown}
"""

# Combine into a ChatPromptTemplate
finwise_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_INSTRUCTION),
    ("human", USER_MESSAGE)
])