TRANSPORT_FACTORS = {
    "Car": 0.21,
    "Bus": 0.08,
    "Train": 0.04,
    "Bike": 0.0,
    "Walk": 0.0
}


def calculate_impact(distance, vehicle, electricity, water, meals, meat_meals, plastic_bottles):
    transport_impact = distance * TRANSPORT_FACTORS[vehicle]
    electricity_impact = electricity * 0.4
    water_impact = water * 0.0003
    food_impact = meals * 1.5 + meat_meals * 2.5
    waste_impact = plastic_bottles * 0.08

    total = (
        transport_impact
        + electricity_impact
        + water_impact
        + food_impact
        + waste_impact
    )

    return {
        "transport": transport_impact,
        "electricity": electricity_impact,
        "water": water_impact,
        "food": food_impact,
        "waste": waste_impact,
        "total": total
    }