from questions import questions

emission_factors = {
    "phone_calls": 0.19,
    "sms": 0.000014,
    "emails": 0.004,
    "spam_emails": 0.00003,
    "emails_with_attachments": 0.05,

    "water_usage": 1.052,

    "flight_economy": 0.08378,
    "flight_first_class": 0.12565,
    "taxi": 0.21863,

    "petrol_car": 0.1949,
    "diesel_car": 0.171,
    "cng_car": 0.165,
    "motorbike": 0.11662,
    "train": 0.04678,
    "bus": 0.12259,

    "electricity": 0.39,
    "heating": 0.215,
    "gas": 2.09672,

    "paper_waste": 0.5,
    "plastic_waste": 1.5,
    "glass_waste": 0.2,
    "general_waste": 2.0
}

def calculate_footprint(answers: dict) -> dict:
    total_footprint = 0
    category_breakdown = {}

    for question in questions:
        question_id = question["id"]
        value = answers.get(question_id, question.get("default_value", 0))

        # Handle ranges (e.g., "100-200") as average
        if isinstance(value, str) and '-' in value:
            low, high = map(float, value.split('-'))
            value = (low + high) / 2

        emission = float(value) * emission_factors.get(question_id, 0)
        category_breakdown.setdefault(question["category"], 0)
        category_breakdown[question["category"]] += emission
        total_footprint += emission

    return {
        "total_carbon_footprint_kg": round(total_footprint, 2),
        "category_breakdown": category_breakdown
    }