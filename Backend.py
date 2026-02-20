from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/plan", methods=["POST"])
def generate_plan():
    data = request.json

    area = data["area_sqft"]
    floors = data["floors"]
    material = data["material_type"]
    workers = data["workers"]
    duration = data["duration_months"]

    material_cost = {
        "standard": 1200,
        "premium": 1800
    }

    base_cost = area * material_cost[material]
    labor_cost = workers * 20000 * duration
    total_cost = base_cost + labor_cost

    optimized_cost = total_cost * 0.92

    resource_plan = {
        "engineers": max(1, floors // 2),
        "laborers": workers,
        "machines": max(1, area // 1000)
    }

    schedule = [
        {"task": "Foundation", "months": 1},
        {"task": "Structure", "months": floors},
        {"task": "Finishing", "months": floors}
    ]

    blueprint_insights = [
        "Ensure load distribution is balanced",
        "Use energy-efficient ventilation",
        "Follow seismic safety norms"
    ]

    return jsonify({
        "cost_estimation": total_cost,
        "optimized_cost": optimized_cost,
        "resource_plan": resource_plan,
        "schedule": schedule,
        "blueprint_insights": blueprint_insights
    })

if __name__ == "__main__":
    app.run(debug=True)