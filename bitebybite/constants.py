"""Application-wide constants and demo data for Bite by Bite."""

from __future__ import annotations

APP_NAME = "Bite by Bite"
APP_SUBTITLE = "Pediatric Meal Tracker"
AUTHOR = "Sidra Almoghrabi"
APP_VERSION = "1.0.0"

BRAND_GREEN = "#1E3F2D"
BRAND_CREAM = "#F9F8F4"
BRAND_LIGHT_GREEN = "#E5EEDC"
BRAND_MINT = "#CFE6BE"
BRAND_GRAY = "#6B6B6B"
BRAND_ORANGE = "#D97706"
BRAND_RED = "#B91C1C"

MEAL_NAMES = ["Breakfast", "Morning snack", "Lunch", "Afternoon snack", "Dinner"]
ALLERGY_OPTIONS = [
    "Cow's milk / Dairy",
    "Egg",
    "Peanut",
    "Tree nuts",
    "Soy",
    "Wheat",
    "Fish",
    "Shellfish",
    "Sesame",
]
AMOUNT_EATEN_OPTIONS = ["All", "Most", "Half", "A little", "None"]

DEFAULT_ACCOUNT = {
    "first_name": "Sarah",
    "last_name": "Ahmed",
    "email": "sarah@example.com",
}

DEFAULT_CHILD = {
    "first_name": "Adam",
    "last_name": "Ahmed",
    "date_of_birth": "2020-03-15",
    "dietary_information": "Vegetarian-leaning, prefers mild flavors, avoids spicy food",
    "allergies": ["Cow's milk / Dairy", "Egg", "Peanut"],
}

DEFAULT_MEALS = [
    {
        "id": "breakfast",
        "name": "Breakfast",
        "scheduled": "7:45 AM",
        "logged": True,
        "logged_at": "7:48 AM",
        "food": "Oatmeal with berries; whole milk",
        "amount_eaten": "Most",
        "notes": "Ate well and asked for more berries.",
    },
    {
        "id": "morning_snack",
        "name": "Morning snack",
        "scheduled": "10:15 AM",
        "logged": True,
        "logged_at": "10:15 AM",
        "food": "Apple slices and sunflower-seed butter",
        "amount_eaten": "All",
        "notes": "",
    },
    {
        "id": "lunch",
        "name": "Lunch",
        "scheduled": "12:30 PM",
        "logged": False,
        "logged_at": "",
        "food": "",
        "amount_eaten": "",
        "notes": "",
    },
    {
        "id": "afternoon_snack",
        "name": "Afternoon snack",
        "scheduled": "3:30 PM",
        "logged": False,
        "logged_at": "",
        "food": "",
        "amount_eaten": "",
        "notes": "",
    },
    {
        "id": "dinner",
        "name": "Dinner",
        "scheduled": "6:30 PM",
        "logged": False,
        "logged_at": "",
        "food": "",
        "amount_eaten": "",
        "notes": "",
    },
]

DEFAULT_NUTRIENTS = [
    {"name": "Protein", "actual": 42, "target": 50, "unit": "g", "status": "On track"},
    {"name": "Iron", "actual": 8, "target": 12, "unit": "mg", "status": "Below target"},
    {"name": "Calcium", "actual": 680, "target": 800, "unit": "mg", "status": "On track"},
    {"name": "Vitamin D", "actual": 400, "target": 600, "unit": "IU", "status": "Below target"},
    {"name": "Fiber", "actual": 16, "target": 18, "unit": "g", "status": "On track"},
    {"name": "Vitamin C", "actual": 45, "target": 50, "unit": "mg", "status": "On track"},
]

DEFAULT_CARE_TEAM = [
    {
        "id": "sarah",
        "name": "Sarah Ahmed",
        "role": "Parent / Guardian",
        "access": "Owner",
        "initials": "SA",
    },
    {
        "id": "maria",
        "name": "Maria Santos",
        "role": "Meal logging access",
        "access": "Caregiver",
        "initials": "MS",
    },
]

DEFAULT_SUBSTITUTIONS = [
    {
        "id": 1,
        "original": "Cheese sandwich",
        "replacement": "Chicken wrap",
        "requested_by": "School nurse",
        "reason": "Dairy-free option requested for lunch.",
        "status": "Pending",
    }
]

ROLE_DESCRIPTIONS = [
    (
        "Parent / Guardian",
        "Owns the child profile, manages access, logs meals, and submits requests.",
    ),
    (
        "Caregiver",
        "Can record meals, portions eaten, and factual meal notes. Cannot change health information.",
    ),
    (
        "School Nurse",
        "Can access authorized students and school-relevant nutrition information.",
    ),
    (
        "Pediatrician",
        "Can access authorized patients and the most detailed clinical nutrition view.",
    ),
]
