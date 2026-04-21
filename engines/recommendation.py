"""
Recommendation engine – returns 3 options based on goal + context + predicted food.
"""

RECOMMENDATIONS_DB = {
    # junk foods → healthier alternatives
    "pizza": {
        "healthier_alternative": ("Multigrain Veggie Wrap", "Whole grain wrap with roasted veggies & hummus", 320, "🌯"),
        "improved_version": ("Whole Wheat Pizza", "Same pizza on whole wheat base, less cheese", 480, "🍕"),
        "quick_prep": ("Oats Upma", "Quick savory oats with veggies, ready in 10 min", 260, "🥣"),
    },
    "burger": {
        "healthier_alternative": ("Grilled Chicken Lettuce Wrap", "High protein, low carb wrap", 300, "🥗"),
        "improved_version": ("Whole Wheat Burger", "Same patty, multigrain bun, extra greens", 420, "🍔"),
        "quick_prep": ("Boiled Egg Sandwich", "2 eggs + brown bread, 5 min prep", 280, "🥚"),
    },
    "chips": {
        "healthier_alternative": ("Makhana (Fox Nuts)", "Roasted, light, high protein snack", 120, "🌰"),
        "improved_version": ("Baked Veggie Chips", "Baked version with less oil", 160, "🥔"),
        "quick_prep": ("Mixed Nuts", "Handful of almonds + walnuts", 180, "🥜"),
    },
    "ice cream": {
        "healthier_alternative": ("Greek Yogurt Bowl", "With fresh berries and honey", 180, "🫐"),
        "improved_version": ("Banana Nice Cream", "Frozen banana blended – same creamy texture", 140, "🍌"),
        "quick_prep": ("Chilled Fruit Bowl", "Chop whatever fruit is available", 100, "🍇"),
    },
    "noodles": {
        "healthier_alternative": ("Zucchini Noodles", "Same texture, much fewer calories", 120, "🥒"),
        "improved_version": ("Whole Wheat Noodles", "Switch to whole grain, add veggies", 320, "🍜"),
        "quick_prep": ("Oats Khichdi", "Quick, filling, healthy – 10 min", 260, "🥣"),
    },
    "default": {
        "healthier_alternative": ("Fresh Fruit Bowl", "Seasonal fruits with chia seeds", 150, "🍱"),
        "improved_version": ("Lighter Version", "Reduce portion size by 30% and add salad", 250, "🥗"),
        "quick_prep": ("Sprouts Salad", "Boiled sprouts + lemon + spices – 5 min", 180, "🌱"),
    },
}

# Goal-based calorie adjustment
GOAL_CALORIE_FACTOR = {
    "lose": 0.8,
    "maintain": 1.0,
    "gain": 1.2,
}


def get_recommendations(predicted_food: str, goal: str, context: str) -> list[dict]:
    key = predicted_food.lower()
    template = RECOMMENDATIONS_DB.get(key, RECOMMENDATIONS_DB["default"])
    factor = GOAL_CALORIE_FACTOR.get(goal, 1.0)

    options = []
    type_map = ["healthier_alternative", "improved_version", "quick_prep"]

    for opt_type in type_map:
        name, desc, cals, emoji = template[opt_type]
        options.append({
            "type": opt_type,
            "name": name,
            "description": desc,
            "calories_approx": int(cals * factor),
            "emoji": emoji,
        })

    return options
