<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>BuildAI Pro</title>

<style>
    body {
        font-family: Arial, sans-serif;
        background: #f4f6fb;
        margin: 0;
        padding: 0;
    }

    header {
        background: linear-gradient(to right, #6a6adf, #7a52c7);
        color: white;
        padding: 15px 30px;
        font-size: 22px;
    }

    .container {
        display: flex;
        gap: 20px;
        padding: 20px;
    }

    .card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        width: 50%;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    h2 {
        border-bottom: 2px solid #6a6adf;
        padding-bottom: 8px;
    }

    label {
        display: block;
        margin-top: 10px;
        font-size: 14px;
    }

    input {
        width: 95%;
        padding: 8px;
        margin-top: 4px;
        border-radius: 5px;
        border: 1px solid #ccc;
    }

    button {
        width: 100%;
        padding: 12px;
        background: #6a6adf;
        color: white;
        border: none;
        margin-top: 15px;
        border-radius: 8px;
        font-size: 16px;
        cursor: pointer;
    }

    .result p {
        font-size: 15px;
        margin: 6px 0;
    }

    .highlight {
        font-weight: bold;
        color: #6a6adf;
    }

    .bottom {
        display: flex;
        gap: 20px;
        padding: 20px;
    }

    .small-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        width: 33%;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
</style>
</head>

<body>

<header>
    BuildAI Pro
</header>

<div class="container">

    <div class="card">
        <h2>Project Details</h2>

        <label>Built-up Area (Sq. Yards)</label>
        <input type="number" id="area" value="1000">

        <label>Floors (e.g. G+2)</label>
        <input type="text" id="floors" value="G+2">

        <label>Daily Wage per Worker (₹)</label>
        <input type="number" id="wage" value="500">

        <label>Cost per Sq. Yard (₹)</label>
        <input type="number" id="cost" value="1500">

        <button onclick="calculate()">Calculate Project</button>
    </div>

    <div class="card result">
        <h2>Workers & Labor</h2>
        <p>Total Workers Required: <span class="highlight" id="workers">-</span></p>
        <p>Total Labour Days: <span class="highlight" id="days">-</span></p>
        <p>Masons: <span id="masons">-</span></p>
        <p>Helpers: <span id="helpers">-</span></p>
        <p>Carpenters: <span id="carpenters">-</span></p>
        <p>Steel Workers: <span id="steel">-</span></p>
    </div>

</div>

<div class="bottom">

    <div class="small-card">
        <h3>Timeline</h3>
        <p>Days: <span id="tDays">-</span></p>
        <p>Weeks: <span id="tWeeks">-</span></p>
        <p>Months: <span id="tMonths">-</span></p>
    </div>

    <div class="small-card">
        <h3>Cost Breakdown</h3>
        <p>Labour Cost: ₹<span id="labourCost">-</span></p>
        <p>Material Cost: ₹<span id="materialCost">-</span></p>
        <p>Overhead (10%): ₹<span id="overhead">-</span></p>
        <p><b>Total Cost: ₹<span id="totalCost">-</span></b></p>
    </div>

    <div class="small-card">
        <h3>Materials Required</h3>
        <p>Steel: <span id="steelMat">-</span> tons</p>
        <p>Cement: <span id="cement">-</span> bags</p>
        <p>Sand: <span id="sand">-</span> tons</p>
        <p>Water: <span id="water">-</span> L</p>
    </div>

</div>

<script>
function calculate() {
    let area = parseInt(document.getElementById("area").value);
    let wage = parseInt(document.getElementById("wage").value);
    let cost = parseInt(document.getElementById("cost").value);
    let floorsText = document.getElementById("floors").value;

    // Extract number of floors (G+2 → 3)
    let floors = floorsText.includes("+")
        ? parseInt(floorsText.split("+")[1]) + 1
        : 1;

    let workers = Math.max(6, Math.floor(area / 180));

    // 🔥 Dynamic timeline calculation
    let productivityPerWorker = 12; // sq yards per day
    let days = Math.ceil((area / (workers * productivityPerWorker)) * floors);

    let labourCost = workers * wage * days;
    let materialCost = area * cost;
    let overhead = Math.floor((labourCost + materialCost) * 0.10);
    let totalCost = labourCost + materialCost + overhead;

    document.getElementById("workers").innerText = workers;
    document.getElementById("days").innerText = workers * days;

    document.getElementById("masons").innerText = Math.floor(workers * 0.3);
    document.getElementById("helpers").innerText = Math.floor(workers * 0.4);
    document.getElementById("carpenters").innerText = Math.floor(workers * 0.15);
    document.getElementById("steel").innerText = Math.floor(workers * 0.15);

    // ✅ Timeline now updates correctly
    document.getElementById("tDays").innerText = days;
    document.getElementById("tWeeks").innerText = Math.ceil(days / 7);
    document.getElementById("tMonths").innerText = (days / 30).toFixed(1);

    document.getElementById("labourCost").innerText = labourCost;
    document.getElementById("materialCost").innerText = materialCost;
    document.getElementById("overhead").innerText = overhead;
    document.getElementById("totalCost").innerText = totalCost;

    document.getElementById("steelMat").innerText = (area * 0.0105).toFixed(1);
    document.getElementById("cement").innerText = Math.floor(area * 1.2);
    document.getElementById("sand").innerText = Math.floor(area * 1.8);
    document.getElementById("water").innerText = area * 1500;
}
</script>

</body>
</html>

//backend

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