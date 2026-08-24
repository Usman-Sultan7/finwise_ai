import json
import re

def parse_llm_json(response_text: str) -> dict:
    """Safely parses the JSON output from the LLM."""
    try:
        # First, try to parse it directly
        return json.loads(response_text)
    except json.JSONDecodeError:
        # If that fails, try to extract the JSON block using regex 
        match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Fallback empty structure matching the schema if parsing fails completely
        return {
            "financial_summary": "Error parsing AI response.",
            "financial_health_score": 0,
            "spending_analysis": [],
            "risk_level": "Unknown",
            "top_priorities": [],
            "budget_recommendations": [],
            "savings_strategy": [],
            "next_month_action_plan": []
        }