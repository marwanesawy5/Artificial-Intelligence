from flask import Blueprint, request, jsonify

planner_bp = Blueprint("planner", __name__)

@planner_bp.route("/plan", methods=["POST"])
def generate_plan():
    data = request.get_json()

    salary = float(data.get("salary", 0))
    expenses = float(data.get("expenses", 0))
    savings = float(data.get("savings", 0))
    debt = float(data.get("debt", 0))
    risk = data.get("risk", "Medium")
    goal = data.get("goal", "General")

    # -----------------------
    # CALCULATIONS
    # -----------------------
    surplus = salary - expenses
    savings_rate = (savings / salary) * 100 if salary > 0 else 0

    score = 0
    if savings_rate > 20:
        score += 40
    elif savings_rate > 10:
        score += 25
    else:
        score += 10

    if surplus > 0:
        score += 30
    else:
        score += 5

    if debt < savings:
        score += 30
    else:
        score += 10

    # -----------------------
    # ADVICE
    # -----------------------
    advice = []

    if surplus <= 0:
        advice.append("Reduce expenses immediately. You're overspending.")

    if savings_rate < 20:
        advice.append("Try to save at least 20% of your income.")

    if debt > savings:
        advice.append("Focus on paying off debt before investing.")

    if risk == "High":
        advice.append("Consider stocks or ETFs for higher returns.")
    elif risk == "Medium":
        advice.append("Use a balanced investment approach.")
    else:
        advice.append("Stick to low-risk savings options.")

    if goal == "Emergency Fund":
        advice.append("Build 3–6 months of expenses as savings.")
    elif goal == "Investment":
        advice.append("Invest consistently every month.")

    return jsonify({
        "surplus": round(surplus, 2),
        "savings_rate": round(savings_rate, 2),
        "score": score,
        "advice": advice
    })