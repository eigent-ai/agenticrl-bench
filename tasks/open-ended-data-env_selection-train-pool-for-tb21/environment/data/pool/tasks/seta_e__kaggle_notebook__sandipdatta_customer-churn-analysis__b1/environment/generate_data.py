#!/usr/bin/env python3
"""Generate synthetic employee attrition dataset with strong, realistic correlations."""
import random
import csv
import math
import os

random.seed(42)

N = 1470

departments = ["Sales", "Research & Development", "Human Resources"]
dept_weights = [0.30, 0.55, 0.15]

job_roles = {
    "Sales": ["Sales Executive", "Sales Representative"],
    "Research & Development": ["Research Scientist", "Laboratory Technician",
                               "Manufacturing Director", "Research Director"],
    "Human Resources": ["Human Resources", "Manager", "Healthcare Representative"],
}

marital_options = ["Single", "Married", "Divorced"]


def weighted_choice(options, weights):
    r = random.random()
    cumulative = 0
    for opt, w in zip(options, weights):
        cumulative += w
        if r <= cumulative:
            return opt
    return options[-1]


rows = []
for i in range(1, N + 1):
    age = random.randint(18, 60)
    daily_rate = random.randint(100, 1500)
    dept = weighted_choice(departments, dept_weights)
    job_role = random.choice(job_roles[dept])
    distance_from_home = random.randint(1, 30)
    education = random.randint(1, 5)
    environment_satisfaction = random.randint(1, 4)
    gender = random.choice(["Male", "Female"])
    job_involvement = random.randint(1, 4)
    job_level = random.randint(1, 5)
    job_satisfaction = random.randint(1, 4)
    marital_status = random.choice(marital_options)
    base_income = 1000 + job_level * 3000 + age * 50
    monthly_income = max(1000, min(20000, int(base_income + random.gauss(0, 1500))))
    num_companies_worked = random.randint(0, 9)
    over_time = random.choice(["Yes", "No"])
    percent_salary_hike = random.randint(10, 25)
    performance_rating = random.choice([3, 3, 3, 4])
    relationship_satisfaction = random.randint(1, 4)
    total_working_years = max(0, min(40, age - 18 + random.randint(-3, 3)))
    training_times_last_year = random.randint(0, 6)
    work_life_balance = random.randint(1, 4)
    years_at_company = max(0, min(40, random.randint(0, total_working_years)))
    years_in_current_role = max(0, min(18, random.randint(0, years_at_company)))
    years_since_last_promotion = max(0, min(15, random.randint(0, years_at_company)))
    years_with_curr_manager = max(0, min(17, random.randint(0, years_at_company)))

    # Compute attrition probability — STRONG correlations for ML learnability
    logit = -7.5

    # Over_time is the strongest predictor
    if over_time == "Yes":
        logit += 2.8

    # Job satisfaction: very low => high attrition
    if job_satisfaction == 1:
        logit += 2.0
    elif job_satisfaction == 2:
        logit += 0.8

    # Environment satisfaction
    if environment_satisfaction == 1:
        logit += 1.5
    elif environment_satisfaction == 2:
        logit += 0.5

    # Monthly income: low income => attrition
    if monthly_income < 3000:
        logit += 1.8
    elif monthly_income < 5000:
        logit += 0.8

    # Distance from home
    if distance_from_home > 20:
        logit += 1.0
    elif distance_from_home > 10:
        logit += 0.4

    # Marital status
    if marital_status == "Single":
        logit += 0.8

    # Years at company
    if years_at_company <= 1:
        logit += 1.2
    elif years_at_company <= 3:
        logit += 0.5

    # Total working years
    if total_working_years <= 3:
        logit += 0.8

    # Num companies worked
    if num_companies_worked >= 7:
        logit += 0.8

    # Work life balance
    if work_life_balance == 1:
        logit += 1.2

    # Job involvement
    if job_involvement == 1:
        logit += 1.0

    # Age
    if age < 25:
        logit += 0.6

    prob = 1.0 / (1.0 + math.exp(-logit))
    attrition = "Yes" if random.random() < prob else "No"

    rows.append({
        "employee_id": i,
        "age": age,
        "daily_rate": daily_rate,
        "department": dept,
        "distance_from_home": distance_from_home,
        "education": education,
        "environment_satisfaction": environment_satisfaction,
        "gender": gender,
        "job_involvement": job_involvement,
        "job_level": job_level,
        "job_role": job_role,
        "job_satisfaction": job_satisfaction,
        "marital_status": marital_status,
        "monthly_income": monthly_income,
        "num_companies_worked": num_companies_worked,
        "over_time": over_time,
        "percent_salary_hike": percent_salary_hike,
        "performance_rating": performance_rating,
        "relationship_satisfaction": relationship_satisfaction,
        "total_working_years": total_working_years,
        "training_times_last_year": training_times_last_year,
        "work_life_balance": work_life_balance,
        "years_at_company": years_at_company,
        "years_in_current_role": years_in_current_role,
        "years_since_last_promotion": years_since_last_promotion,
        "years_with_curr_manager": years_with_curr_manager,
        "attrition": attrition,
    })

attrition_count = sum(1 for r in rows if r["attrition"] == "Yes")
actual_rate = attrition_count / len(rows)
print(f"Generated {len(rows)} rows, attrition rate: {actual_rate:.3f} ({attrition_count}/{len(rows)})")

fieldnames = list(rows[0].keys())
output_path = os.environ.get("OUTPUT_PATH", "/tmp/employee_attrition.csv")
with open(output_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Dataset written to {output_path}")
