def calculate_financials(monthly_income: float, expenses: dict, current_savings: float) -> dict:
    """Computes basic financial ratios and a preliminary health score."""
    
    total_expenses = sum(expenses.values())
    remaining_income = monthly_income - total_expenses
    
    # Guard against divide-by-zero
    if monthly_income > 0:
        savings_ratio = (current_savings / monthly_income) * 100
        expense_ratio = (total_expenses / monthly_income) * 100
    else:
        savings_ratio = 0.0
        expense_ratio = 0.0 if total_expenses == 0 else 100.0

    # Calculate preliminary score (0-100 heuristic)
    score = 50 # Base score
    
    # Reward healthy savings
    if savings_ratio >= 20:
        score += 30
    elif savings_ratio >= 10:
        score += 15
        
    # Penalize high expenses
    if expense_ratio >= 90:
        score -= 30
    elif expense_ratio >= 75:
        score -= 15
        
    # Ensure score stays strictly within 0-100 bounds
    preliminary_score = max(0, min(100, int(score)))

    return {
        "total_expenses": total_expenses,
        "remaining_income": remaining_income,
        "savings_ratio": round(savings_ratio, 2),
        "expense_ratio": round(expense_ratio, 2),
        "preliminary_score": preliminary_score
    }