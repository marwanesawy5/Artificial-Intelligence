from flask import Blueprint, request, jsonify, session
from auth.models import db, FinancialData, PlannerHistory

planner_bp = Blueprint("planner", __name__)

# --- NEW ROUTE: Fetch History for the Frontend ---
@planner_bp.route("/api/planner_history", methods=["GET"])
def get_planner_history():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    # Grab all plans for this user, newest first
    history = PlannerHistory.query.filter_by(user_id=session["user_id"]).order_by(PlannerHistory.timestamp.desc()).all()
    
    return jsonify([{
        "date": h.timestamp.strftime("%b %d, %Y - %H:%M"),
        "salary": h.salary,
        "expenses": h.expenses,
        "score": h.score,
        "status": h.status
    } for h in history])

@planner_bp.route("/plan", methods=["POST"])
def generate_plan():
    data = request.get_json()

    # INPUTS
    salary = max(float(data.get("salary", 0)), 0)
    expenses = max(float(data.get("expenses", 0)), 0)
    savings = max(float(data.get("savings", 0)), 0)
    debt = max(float(data.get("debt", 0)), 0)

    risk = data.get("risk", "Medium")
    goal = data.get("goal", "General")

    # CORE CALCULATIONS
    surplus = salary - expenses
    savings_rate = ((savings / salary) * 100 if salary > 0 else 0)
    debt_ratio = ((debt / salary) * 100 if salary > 0 else 0)
    expense_ratio = ((expenses / salary) * 100 if salary > 0 else 0)
    emergency_months = (savings / expenses if expenses > 0 else 0)

    # AI SCORE SYSTEM
    score = 0
    if savings_rate >= 30: score += 40
    elif savings_rate >= 20: score += 35
    elif savings_rate >= 10: score += 25
    else: score += 10

    if surplus >= salary * 0.3: score += 30
    elif surplus >= salary * 0.15: score += 25
    elif surplus > 0: score += 18
    else: score += 5

    if debt == 0: score += 30
    elif debt < savings: score += 25
    elif debt_ratio < 30: score += 18
    else: score += 10

    score = min(score, 100)

    # STATUS CLASSIFICATION
    if score >= 80: status = "Excellent"
    elif score >= 60: status = "Good"
    elif score >= 40: status = "Average"
    else: status = "Risky"
        
    # ... (Keep your calculations at the top) ...

    # SAVE TO SUPABASE (Updated for safety)
    if "user_id" in session:
        try:
            user_id = session["user_id"]
            
            # 1. Update current dashboard totals
            user_finances = FinancialData.query.filter_by(user_id=user_id).first()
            if not user_finances:
                user_finances = FinancialData(user_id=user_id)
                db.session.add(user_finances)
                
            user_finances.expenses = expenses
            user_finances.emergency_fund = savings
            user_finances.monthly_savings = surplus if surplus > 0 else 0
            
            # 2. Save to History
            new_plan = PlannerHistory(
                user_id=user_id,
                salary=salary,
                expenses=expenses,
                score=score,
                status=status
            )
            db.session.add(new_plan)
            db.session.commit()
        except Exception as e:
            print(f"Database Error: {e}")
            db.session.rollback() # Undo the failed save so the app keeps running

    # ... (Keep your advice engine at the bottom) ...

    # AI ADVICE ENGINE
    advice = []
    if surplus <= 0: advice.append("Reduce expenses immediately. You're overspending.")
    elif expense_ratio > 80: advice.append("Your spending is consuming most of your income.")
    if savings_rate < 20: advice.append("Try to save at least 20% of your income.")
    elif savings_rate >= 30: advice.append("Excellent savings discipline.")
    if debt > savings: advice.append("Focus on paying off debt before investing.")
    if debt_ratio > 50: advice.append("Your debt ratio is critically high.")
    elif debt_ratio > 30: advice.append("Consider reducing monthly debt obligations.")
    if emergency_months < 3: advice.append("Build a larger emergency fund for financial safety.")
    elif emergency_months >= 6: advice.append("Your emergency savings are in a healthy range.")
    if risk == "High": advice.append("Consider stocks or ETFs for higher returns.")
    elif risk == "Medium": advice.append("Use a balanced investment approach.")
    else: advice.append("Stick to low-risk savings options.")
    if goal == "Emergency Fund": advice.append("Build 3–6 months of expenses as savings.")
    elif goal == "Invest Growth": advice.append("Invest consistently every month.")
    elif goal == "Debt Freedom": advice.append("Prioritize high-interest debt repayment first.")

    return jsonify({
        "surplus": round(surplus, 2),
        "savings_rate": round(savings_rate, 2),
        "score": score,
        "status": status,
        "advice": advice
    })