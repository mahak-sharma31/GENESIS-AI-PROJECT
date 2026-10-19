"""
GENESIS AI — Invention Engine
Offline, rule-based invention generator.

No API key required.
All material prices are illustrative estimates.
Concepts have not been independently tested.
"""

from copy import deepcopy


# ==================================================
# SAMPLE PROBLEMS
# ==================================================

PRESETS = [
    {
        "title": "Plant Watering Reminder",
        "description": "People forget to water their plants on time.",
        "category": "Agriculture & Environment",
        "budget": 80,
    },
    {
        "title": "Water Tank Overflow",
        "description": "Water gets wasted when an overhead tank overflows.",
        "category": "Water & Sanitation",
        "budget": 150,
    },
    {
        "title": "Unused Room Energy Waste",
        "description": "Lights and fans are sometimes left on in empty rooms.",
        "category": "Energy & Electrical",
        "budget": 120,
    },
    {
        "title": "Plastic Bottle Sorting",
        "description": "Plastic bottles get mixed with other waste.",
        "category": "Waste & Recycling",
        "budget": 200,
    },
    {
        "title": "Tap Leakage Tracking",
        "description": "A leaking tap wastes water and goes unnoticed.",
        "category": "Water & Sanitation",
        "budget": 60,
    },
    {
        "title": "Food Packet Storage",
        "description": "Opened food packets are not sealed properly.",
        "category": "Food & Canteen",
        "budget": 100,
    },
]


# ==================================================
# INVENTION PATTERNS
# Material tuple:
# name, purpose, quantity, unit price, reusable
# ==================================================

PATTERNS = {
    "plant": {
        "title": "Plant Care Reminder System",
        "problem": "People may forget when their plants need watering.",
        "concept": (
            "A simple plant-care reminder using a written schedule "
            "and a visible soil-check indicator."
        ),
        "mechanism": (
            "The user checks the soil and follows a reminder card. "
            "The basic version does not automatically measure moisture."
        ),
        "materials": [
            ("Reused container", "Holds the reminder card", 1, 0, True),
            ("Paper or cardboard", "Creates the reminder card", 1, 0, True),
            ("Marker or pen", "Writes watering dates", 1, 0, True),
            ("Small label", "Identifies the plant", 1, 8, False),
        ],
        "steps": [
            "Clean and dry a small reused container.",
            "Write the plant name on a label.",
            "Create a watering schedule card.",
            "Place the card beside the plant.",
            "Check the soil before watering."
        ],
        "advantages": [
            "Simple and easy to maintain.",
            "Does not need electricity.",
            "Can use reused materials.",
        ],
        "limitations": [
            "Does not automatically detect soil moisture.",
            "The user must check the soil and update the schedule.",
        ],
        "safety": [
            "Keep paper and labels away from direct water contact."
        ],
    },

    "water": {
        "title": "Water Tank Overflow Alert Model",
        "problem": "Water may be wasted when a tank overflows unnoticed.",
        "concept": (
            "A tank-level indicator model demonstrating how rising "
            "water levels can be monitored."
        ),
        "mechanism": (
            "The basic model uses marked water levels and manual "
            "observation. It does not automatically stop a pump."
        ),
        "materials": [
            ("Transparent reused container", "Demonstration tank", 1, 0, True),
            ("Cardboard", "Base and level markings", 1, 0, True),
            ("Marker", "Marks the maximum water level", 1, 8, False),
            ("Tape", "Secures the markings", 1, 12, False),
        ],
        "steps": [
            "Place a transparent container on a stable surface.",
            "Mark low, medium and maximum levels on the outside.",
            "Position the markings so they are easy to see.",
            "Add a small amount of water to demonstrate the levels.",
            "Empty the container safely after the demonstration."
        ],
        "advantages": [
            "Demonstrates tank-level monitoring.",
            "Does not require electricity.",
            "Useful for explaining water conservation.",
        ],
        "limitations": [
            "This is a manual demonstration model.",
            "It does not provide an automatic alarm.",
            "It does not switch off a water pump.",
        ],
        "safety": [
            "Keep water away from electrical devices.",
            "Use a stable container and clean up spills."
        ],
    },

    "lights": {
        "title": "Room Energy Reminder System",
        "problem": "Lights and fans may remain on when a room is empty.",
        "concept": (
            "A door-side reminder prompting people to check lights "
            "and fans before leaving a room."
        ),
        "mechanism": (
            "A visible checklist reminds users to switch off unused "
            "appliances. It does not detect room occupancy."
        ),
        "materials": [
            ("Reused cardboard", "Creates the reminder board", 1, 0, True),
            ("Paper", "Checklist surface", 1, 0, True),
            ("Marker", "Writes reminder messages", 1, 8, False),
            ("Tape", "Attaches the board", 1, 12, False),
        ],
        "steps": [
            "Cut a small piece of clean cardboard.",
            "Write a checklist for lights, fans and appliances.",
            "Add a message such as 'Switch off before leaving'.",
            "Place the reminder near the exit.",
            "Check appliances before leaving the room."
        ],
        "advantages": [
            "Low-cost approach.",
            "Does not need electricity for the reminder.",
            "Encourages energy-saving habits.",
        ],
        "limitations": [
            "Depends on people following the reminder.",
            "Cannot automatically detect an empty room.",
        ],
        "safety": [
            "Do not attach paper or cardboard to hot electrical equipment."
        ],
    },

    "bottle": {
        "title": "Plastic Bottle Sorting Guide",
        "problem": "Plastic bottles may get mixed with other waste.",
        "concept": (
            "A labelled sorting station helping people separate "
            "plastic bottles from other waste."
        ),
        "mechanism": (
            "Users identify and sort items using labels. The model "
            "does not automatically recognise materials."
        ),
        "materials": [
            ("Reused cardboard boxes", "Sorting compartments", 2, 0, True),
            ("Paper", "Category labels", 2, 0, True),
            ("Marker", "Writes sorting instructions", 1, 8, False),
            ("Tape", "Secures labels", 1, 12, False),
        ],
        "steps": [
            "Prepare two clean, dry boxes.",
            "Label one for accepted plastic bottles.",
            "Label the other for other waste.",
            "Add instructions for preparing bottles for collection.",
            "Follow local waste-collection rules."
        ],
        "advantages": [
            "Makes sorting instructions visible.",
            "Can use reused boxes.",
            "Does not require electricity.",
        ],
        "limitations": [
            "Does not use AI or sensors to identify plastic.",
            "The user must follow the sorting labels.",
            "Not every plastic item is accepted by every recycler.",
        ],
        "safety": [
            "Do not handle sharp or contaminated waste with bare hands."
        ],
    },

    "leak": {
        "title": "Tap Leak Observation Tracker",
        "problem": "Small tap leaks may continue because nobody reports them.",
        "concept": (
            "A tracking system recording where a leak occurs "
            "and when it is reported."
        ),
        "mechanism": (
            "A paper tracker records observed leaks. It does not "
            "automatically detect leakage or measure water loss."
        ),
        "materials": [
            ("Reused paper or cardboard", "Tracking sheet", 1, 0, True),
            ("Pen", "Records observations", 1, 0, True),
            ("Tape", "Displays the tracker", 1, 12, False),
            ("Label", "Identifies the location", 1, 8, False),
        ],
        "steps": [
            "Create columns for location, date and report status.",
            "Record the location of the leaking tap.",
            "Inform the responsible person or maintenance team.",
            "Update the record after the repair.",
            "Check whether the leak has stopped."
        ],
        "advantages": [
            "Helps track reported leaks.",
            "Simple and inexpensive.",
            "Supports maintenance follow-up.",
        ],
        "limitations": [
            "Cannot automatically detect leaks.",
            "Does not measure the amount of water wasted.",
            "Repairs may require a qualified person.",
        ],
        "safety": [
            "Do not attempt electrical or plumbing repairs without suitable training."
        ],
    },

    "storage": {
        "title": "Reusable Food Packet Sealing Station",
        "problem": "Opened food packets may not be sealed properly.",
        "concept": (
            "A small station organising opened packets and "
            "providing a place for reusable clips."
        ),
        "mechanism": (
            "Users close suitable packets with clips and follow "
            "the food label's storage instructions."
        ),
        "materials": [
            ("Clean reused box", "Organises packets and clips", 1, 0, True),
            ("Reusable packet clips", "Closes suitable packets", 3, 12, False),
            ("Paper label", "Records opening dates", 1, 0, True),
            ("Marker", "Writes dates or food names", 1, 8, False),
        ],
        "steps": [
            "Clean and dry the storage box.",
            "Place reusable clips in a separate section.",
            "Close each suitable packet securely.",
            "Label opened packets when useful.",
            "Follow the food packaging and storage instructions."
        ],
        "advantages": [
            "Keeps storage supplies organised.",
            "Can reduce accidental packet spills.",
            "Uses reusable clips.",
        ],
        "limitations": [
            "Does not make spoiled food safe.",
            "Does not replace refrigeration where required.",
            "Clips may not provide an airtight seal.",
        ],
        "safety": [
            "Follow food labels for refrigeration and expiry.",
            "Keep the station clean and dry."
        ],
    },

    "food": {
        "title": "Food Waste Observation Tracker",
        "problem": "People may waste food because they do not track unused items.",
        "concept": (
            "A tracker recording food items and relevant dates "
            "to help organise food use."
        ),
        "mechanism": (
            "The user records dates and checks food labels. "
            "The tracker cannot determine whether food is safe to eat."
        ),
        "materials": [
            ("Reused cardboard", "Tracker board", 1, 0, True),
            ("Paper", "Food and date list", 1, 0, True),
            ("Marker", "Records item names and dates", 1, 8, False),
            ("Tape", "Displays the tracker", 1, 12, False),
        ],
        "steps": [
            "Create a list of stored food items.",
            "Record dates according to the packaging.",
            "Place the list near the storage area.",
            "Review the list when planning meals.",
            "Follow food-safety guidance and discard food when necessary."
        ],
        "advantages": [
            "Helps organise food supplies.",
            "Can encourage better meal planning.",
            "Low-cost and easy to update.",
        ],
        "limitations": [
            "The user must maintain the list.",
            "Dates alone cannot guarantee food safety.",
        ],
        "safety": [
            "Never rely only on appearance or smell to determine food safety."
        ],
    },

    "generic": {
        "title": "Problem Tracking and Improvement Board",
        "problem": (
            "A problem may be difficult to solve when observations "
            "and actions are not recorded."
        ),
        "concept": (
            "A reusable board recording the problem, observations, "
            "actions and results."
        ),
        "mechanism": (
            "The user records observations and reviews results. "
            "This is a manual prototype, not an automatic detection system."
        ),
        "materials": [
            ("Reused cardboard", "Board base", 1, 0, True),
            ("Paper", "Observation sheets", 1, 0, True),
            ("Marker", "Writes records", 1, 5, False),
            ("Tape", "Attaches the sheets", 1, 10, False),
        ],
        "steps": [
            "Write the problem in one sentence.",
            "Record when and where it occurs.",
            "List actions that could be tried safely.",
            "Record the action taken and observed result.",
            "Review the records and identify the next improvement."
        ],
        "advantages": [
            "Easy to customise.",
            "Can use reused materials.",
            "Makes observations easier to compare.",
        ],
        "limitations": [
            "Relies on accurate manual records.",
            "Does not automatically solve or detect the problem.",
        ],
        "safety": [
            "Only test changes that are safe and appropriate."
        ],
    },
}


# ==================================================
# TEXT NORMALISATION
# ==================================================

def _normalise(text):
    """Convert input to lowercase searchable text."""
    return " ".join(str(text or "").lower().strip().split())


# ==================================================
# AUTOMATIC CATEGORY DETECTION
# ==================================================

def detect_category(title, description=""):
    """Infer a broad category from the user's problem text."""
    text = _normalise(f"{title} {description}")
    rules = [
        ("Agriculture & Environment", ["plant", "soil", "garden", "farm", "tree", "watering", "environment"]),
        ("Water & Sanitation", ["water", "tank", "tap", "leak", "overflow", "drain", "wash", "pipe"]),
        ("Energy & Electrical", ["electricity", "energy", "light", "fan", "power", "charger", "battery"]),
        ("Waste & Recycling", ["waste", "plastic", "bottle", "recycl", "garbage", "segregat", "litter"]),
        ("Food & Canteen", ["food", "packet", "storage", "canteen", "meal", "expiry", "leftover"]),
        ("Health & Safety", ["safety", "injury", "first aid", "helmet", "health", "hazard", "emergency"]),
        ("Campus & Education", ["classroom", "student", "school", "college", "attendance", "library", "study", "exam"]),
    ]
    for category, words in rules:
        if any(word in text for word in words):
            return category
    return "Daily Life"


# ==================================================
# PATTERN SELECTION
# ==================================================

def choose_pattern(title, description="", category=""):
    """Select an invention pattern using keywords."""

    title_text = _normalise(title)
    description_text = _normalise(description)
    category_text = _normalise(category)

    title_rules = [
        ("plant", [
            "plant", "watering", "water plant", "flower pot",
            "soil moisture", "garden"
        ]),
        ("water", [
            "tank overflow", "water tank", "overhead tank",
            "tank level", "overflow"
        ]),
        ("lights", [
            "energy waste", "unused room", "empty room",
            "lights left", "fan left", "electricity waste",
            "save electricity"
        ]),
        ("bottle", [
            "plastic bottle", "bottle sorting", "waste sorting",
            "plastic sorting", "recycling station"
        ]),
        ("leak", [
            "tap leak", "tap leakage", "leaking tap",
            "water leakage", "pipe leak", "dripping tap"
        ]),
        ("storage", [
            "food packet", "packet storage", "packet sealing",
            "opened packet", "food storage"
        ]),
        ("food", [
            "food waste", "unused food", "food tracking",
            "food expiry", "food dates"
        ]),
    ]

    for key, keywords in title_rules:
        if any(word in title_text for word in keywords):
            return key

    description_rules = [
        ("plant", [
            "plant", "watering", "soil moisture", "garden"
        ]),
        ("water", [
            "tank overflow", "overhead tank", "water tank",
            "tank overflowing"
        ]),
        ("lights", [
            "empty room", "lights left on", "fan left on",
            "electricity waste", "energy waste"
        ]),
        ("bottle", [
            "plastic bottle", "sort plastic", "mixed waste",
            "waste sorting"
        ]),
        ("leak", [
            "leaking tap", "tap leakage", "water leak",
            "dripping tap", "pipe leak"
        ]),
        ("storage", [
            "opened packet", "seal packet", "food packet",
            "packet storage"
        ]),
        ("food", [
            "food waste", "unused food", "expiry date",
            "food dates"
        ]),
    ]

    for key, keywords in description_rules:
        if any(word in description_text for word in keywords):
            return key

    if any(word in category_text for word in ["water", "plumbing"]):
        return "water"

    if any(word in category_text for word in ["energy", "electricity"]):
        return "lights"

    if any(word in category_text for word in ["waste", "recycling", "plastic"]):
        return "bottle"

    if any(word in category_text for word in ["food", "storage"]):
        return "storage"

    if any(word in category_text for word in ["plant", "garden", "environment"]):
        return "plant"

    return "generic"


# ==================================================
# MATERIAL HELPERS
# ==================================================

def _convert_materials(material_rows):
    """Convert material tuples into dictionaries for the frontend."""

    materials = []

    for name, purpose, quantity, unit_price, reusable in material_rows:
        quantity = int(quantity)
        unit_price = float(unit_price)

        materials.append({
            "name": name,
            "purpose": purpose,
            "quantity": quantity,
            "unit_price": unit_price,
            "subtotal": quantity * unit_price,
            "reusable": bool(reusable),
        })

    return materials


def _material_total(materials):
    """Calculate the total illustrative material cost."""

    return sum(
        float(item["subtotal"])
        for item in materials
    )


def _select_materials(pattern, budget):
    """Select the full build if affordable; otherwise offer a clearly labelled
    simplified demo using only listed reused items and affordable essentials.
    Never let the shown total exceed the user's budget.
    """
    materials = _convert_materials(pattern["materials"])
    total = _material_total(materials)
    if total <= budget:
        return materials, total, False

    # Build a reduced proof-of-concept from reusable/free materials first, then
    # add the cheapest priced items that fit. Prices remain estimates.
    reusable = [m for m in materials if m["reusable"] and m["unit_price"] == 0]
    priced = sorted([m for m in materials if m["unit_price"] > 0], key=lambda m: m["subtotal"])
    picked = list(reusable)
    running = _material_total(picked)
    for item in priced:
        if running + item["subtotal"] <= budget:
            picked.append(item)
            running += item["subtotal"]
    # If there are no assumed-already-owned items and no affordable materials,
    # do not fabricate a free complete build.
    if not picked:
        return [], 0.0, True
    return picked, running, True


# ==================================================
# MAIN INVENTION GENERATOR
# ==================================================

def formulate_concepts(
    title,
    description="",
    budget=300,
    category="General",
):
    """
    Generate one offline, rule-based invention concept.

    Returns a list containing one concept to match the frontend.
    """

    title = str(title or "").strip()
    description = str(description or "").strip()
    category = detect_category(title, description)

    try:
        budget = float(budget)
    except (TypeError, ValueError):
        budget = 0.0

    budget = max(0.0, budget)

    pattern_key = choose_pattern(title, description, category)
    pattern = deepcopy(PATTERNS[pattern_key])

    materials, total, using_reuse_fallback = _select_materials(
        pattern,
        budget,
    )

    # Final budget check.
    if total > budget:
        materials = []
        total = 0.0
        using_reuse_fallback = True

    remaining = max(0.0, budget - total)

    actual_problem = description or title

    if using_reuse_fallback and materials:
        # Keep instructions aligned with the reduced demo rather than implying
        # omitted parts are still included.
        available_names = ", ".join(item["name"] for item in materials)
        simplified_steps = [
            f"Use only the materials listed in this simplified build: {available_names}.",
            "Create a small labelled demonstration or tracking aid for the stated problem.",
            "Show how a person would notice the problem and take the intended action.",
            "Test the idea with a safe, small demonstration and record what happens.",
            "Treat this as a proof-of-concept; add omitted parts only after checking the full design and budget.",
        ]
    else:
        simplified_steps = list(pattern["steps"])

    if not actual_problem:
        actual_problem = (
            "A problem that needs a practical, low-cost solution."
        )

    concept = {
        # Main details expected by app.js
        "name": pattern["title"],
        "problem_title": title or pattern["title"],
        "problem_summary": actual_problem,
        "category": category,
        "tagline": (pattern["concept"] + " Simplified proof-of-concept because of the entered budget.") if using_reuse_fallback and materials else pattern["concept"],
        "type": "OFFLINE RULE-BASED",
        "complexity": "Beginner-friendly prototype",
        "build_time": "Approximately 30–60 minutes",

        # Problem and mechanism
        "root_cause": pattern["problem"],
        "mechanism": pattern["mechanism"],

        # Budget
        "materials": materials,
        "total": total,
        "budget": budget,
        "remaining": remaining,

        # Instructions and safety
        "steps": simplified_steps,
        "advantages": list(pattern["advantages"]),
        "limits": list(pattern["limitations"]),
        "limitations": list(pattern["limitations"]),
        "safety": list(pattern["safety"]),

        # Honest feasibility explanation
        "score_note": (
            "This concept was selected using predefined rules and "
            "a matching pattern. Its practical feasibility has not "
            "been independently tested. Review the materials, estimated "
            "prices, safety requirements and build instructions before "
            "constructing a prototype."
        ),

        # Extra metadata
        "pattern_key": pattern_key,
        "mode": "OFFLINE RULE-BASED",
        "price_note": (
            "Non-zero prices are illustrative estimates, not "
            "live-verified shop prices."
        ),
        "budget_note": (
            "No listed material from this pattern fits the entered budget; increase the budget or use a different, safe design."
            if not materials
            else ("A simplified proof-of-concept is shown because the full material list exceeds the budget. Check that it still demonstrates the intended idea." if using_reuse_fallback else "The displayed estimated materials total fits within the entered budget.")
        ),
        "reuse_note": (
            "No material list fits this budget; no complete build is claimed."
            if not materials
            else ("Only listed reusable items and affordable parts are included; any omitted component is not part of this simplified demo." if using_reuse_fallback else "The standard illustrative materials list fits the entered budget.")
        ),
        "is_reuse_fallback": using_reuse_fallback,
        "simplified_build": using_reuse_fallback and bool(materials),
        "needs_manual_review": True,
    }

    return [concept]


# ==================================================
# OPTIONAL HELPER
# ==================================================

def get_sample_problems():
    """Return a copy of the preset problem list."""
    return deepcopy(PRESETS)