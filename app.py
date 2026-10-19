import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from invention_engine import formulate_concepts, PRESETS, detect_category

load_dotenv()
app = Flask(__name__)

def _money(value):
    try: return max(0, round(float(value), 2))
    except (TypeError, ValueError): return 0

def _fit_to_budget(concept, budget):
    # Recalculate every line item on the server; never trust model arithmetic.
    rows = concept.get("materials") or []
    clean = []
    for row in rows:
        try:
            qty = max(1, int(row.get("quantity", 1)))
            unit = _money(row.get("unit_price", 0))
        except (TypeError, ValueError):
            continue
        clean.append({"name": str(row.get("name", "Material"))[:100],
                      "purpose": str(row.get("purpose", "Used in the prototype"))[:220],
                      "quantity": qty, "unit_price": unit,
                      "subtotal": round(qty * unit, 2),
                      "reusable": bool(row.get("reusable", False))})
    # Prefer low-cost rows and only include rows that fit; show a simplified build if needed.
    clean.sort(key=lambda x: (x["subtotal"], not x["reusable"]))
    picked=[]; total=0.0
    for row in clean:
        if total + row["subtotal"] <= budget + 1e-9:
            picked.append(row); total += row["subtotal"]
    concept["materials"] = picked
    concept["total"] = round(total, 2)
    concept["budget"] = round(budget, 2)
    concept["remaining"] = round(max(0, budget-total), 2)
    if not picked:
        concept["budget_note"] = "No priced material from the proposed list fits this budget. Use only safe items already available, or increase the budget; the site will not claim an unpriced build is complete."
        concept["limits"] = list(concept.get("limits") or []) + ["The entered budget may be too small for a physical prototype. This result is a no-purchase / planning version, not a claim that a complete build costs ₹0."]
    else:
        concept["budget_note"] = "The displayed material items fit within the entered budget. Optional items that did not fit were omitted; check whether the simplified design still meets the goal."
    concept["category"] = str(concept.get("category") or "General")
    concept["needs_manual_review"] = True
    concept["price_note"] = "Prices are AI-generated illustrative estimates, not live-verified shop prices. Verify locally before buying."
    return concept

def _gemini_concept(title, description, category, budget):
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return None
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        prompt = f"""You are GENESIS AI, a practical invention/prototype planner. Create ONE useful, realistic, safe solution to the user's exact problem.
Problem title: {title}
Problem description: {description}
Category: {category}
Hard maximum cash budget in Indian rupees: {budget}. Do not exceed this. Prefer locally available/reused materials and a simpler manual prototype for very small budgets. Never pretend an item is free unless explicitly marked reusable/already available. If a working physical solution is impossible at this budget, propose the smallest useful demonstration or planning prototype and state the limitation clearly. Avoid dangerous mains electricity, medical diagnosis/treatment, structural or other high-risk builds.
Return ONLY valid JSON with keys: name, problem_title, problem_summary, category, tagline, type, complexity, build_time, root_cause, mechanism, materials (array of objects name,purpose,quantity,unit_price,reusable), steps (array of strings), advantages (array), limits (array), safety (array), blueprint (object with input, component, action, result), score_note.
Materials must be relevant to this problem, each quantity positive integer, unit_price numeric in INR, and their sum(quantity*unit_price) <= {budget}. If budget is tiny, use safe household/reused items at 0 only when the user likely already has them, mark reusable true, and explain that they are already available. Make blueprint specific to the generated solution. Do not invent sensors/electronics unless they fit budget."""
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            contents=prompt,
            config={"response_mime_type": "application/json"}
        )
        data = json.loads(response.text)
        required = ["name", "mechanism", "materials", "steps"]
        if not all(k in data for k in required): return None
        data.setdefault("problem_title", title); data.setdefault("problem_summary", description)
        data.setdefault("category", category); data.setdefault("tagline", "A budget-aware prototype concept")
        data.setdefault("type", "GEMINI AI-GENERATED"); data.setdefault("complexity", "Depends on the selected design")
        data.setdefault("build_time", "Estimate only; validate before building")
        data.setdefault("root_cause", "Based on the problem description")
        data.setdefault("advantages", []); data.setdefault("limits", [])
        data.setdefault("safety", ["Check materials and safety before building."])
        data.setdefault("score_note", "AI-generated concept; verify the design, costs, and safety before building.")
        data["mode"] = "GEMINI AI"
        data["pattern_key"] = "ai"
        data["blueprint"] = data.get("blueprint") or {"input": description, "component": ", ".join(str(m.get("name", "")) for m in data.get("materials", [])[:3]), "action": data.get("mechanism", "Follow the build steps"), "result": data.get("tagline", "Intended improvement")}
        return _fit_to_budget(data, budget)
    except Exception as exc:
        app.logger.warning("Gemini generation failed; using offline fallback: %s", exc)
        return None

@app.get("/")
def index():
    return render_template("index.html", presets=PRESETS, ai_configured=bool(os.getenv("GEMINI_API_KEY", "").strip()))

@app.post("/api/formulate")
def formulate():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    description = str(data.get("description", "")).strip()
    # Category is inferred from the problem text, not selected manually.
    category = detect_category(title, description)
    try: budget = float(data.get("budget"))
    except (TypeError, ValueError): return jsonify({"error": "Please enter a valid budget."}), 400
    if len(title) < 3 or len(description) < 8:
        return jsonify({"error": "Enter a title (3+ characters) and description (8+ characters)."}), 400
    if not 1 <= budget <= 1000000:
        return jsonify({"error": "Budget must be between ₹1 and ₹10,00,000."}), 400
    concept = _gemini_concept(title, description, category, budget)
    if concept is None:
        concept = formulate_concepts(title, description, budget, category)[0]
        concept["mode"] = "OFFLINE FALLBACK"
        concept["type"] = "OFFLINE RULE-BASED"
        concept["problem_summary"] = description
        concept["category"] = category
        concept["budget"] = budget
        concept["remaining"] = max(0, budget - float(concept.get("total", 0)))
        concept["fallback_note"] = "Gemini is not configured or temporarily unavailable. Offline mode has a limited set of patterns; for an unknown problem it may provide a general tracking concept rather than a tailored invention."
    return jsonify({"concepts": [concept], "mode": concept.get("mode", "OFFLINE FALLBACK")})

if __name__ == "__main__":
    app.run(debug=True)
