"""
Honda Car India Limited — Dataset Generator
Based on KPIs from service analytics dashboards.
Run: python generate_data.py
"""

import pandas as pd
import numpy as np
import os

np.random.seed(77)
os.makedirs("data", exist_ok=True)

# ── 1. REGIONAL SERVICE PERFORMANCE ───────────────────────────
regional = pd.DataFrame([
    {
        "zone": "South",
        "sr_target": 572000, "sr_actual": 557300, "sr_achievement": 97.4,
        "pm_target": 328000, "pm_actual": 319500, "pm_achievement": 97.4,
        "rsa_target": 18400, "rsa_actual": 43100, "rsa_achievement": 234.2,
        "ew_deliveries": 19400, "ew_actual": 11780, "ew_penetration": 60.7,
        "atw_target": 5950, "atw_actual": 5440, "atw_achievement": 91.4,
        "dssi_score": 963,
        "zone_rank": 1
    },
    {
        "zone": "North",
        "sr_target": 634000, "sr_actual": 609800, "sr_achievement": 96.2,
        "pm_target": 317000, "pm_actual": 300200, "pm_achievement": 94.7,
        "rsa_target": 20500, "rsa_actual": 38900, "rsa_achievement": 189.8,
        "ew_deliveries": 21500, "ew_actual": 12180, "ew_penetration": 56.6,
        "atw_target": 6250, "atw_actual": 5270, "atw_achievement": 84.3,
        "dssi_score": 956,
        "zone_rank": 2
    },
    {
        "zone": "West",
        "sr_target": 522000, "sr_actual": 498000, "sr_achievement": 95.4,
        "pm_target": 286000, "pm_actual": 267900, "pm_achievement": 93.7,
        "rsa_target": 16400, "rsa_actual": 35800, "rsa_achievement": 218.3,
        "ew_deliveries": 16400, "ew_actual": 9300, "ew_penetration": 56.7,
        "atw_target": 5020, "atw_actual": 4190, "atw_achievement": 83.5,
        "dssi_score": 953,
        "zone_rank": 3
    },
    {
        "zone": "East",
        "sr_target": 598000, "sr_actual": 402300, "sr_achievement": 67.3,
        "pm_target": 239000, "pm_actual": 231400, "pm_achievement": 96.8,
        "rsa_target": 13160, "rsa_actual": 28190, "rsa_achievement": 214.2,
        "ew_deliveries": 11100, "ew_actual": 6060, "ew_penetration": 54.6,
        "atw_target": 4240, "atw_actual": 3620, "atw_achievement": 85.4,
        "dssi_score": 949,
        "zone_rank": 4
    },
])
regional.to_csv("data/regional_performance.csv", index=False)
print("✅ data/regional_performance.csv")

# ── 2. DEALER PERFORMANCE ──────────────────────────────────────
dealers_raw = [
    ("Divine Honda",       "Dehradun",    "Uttarakhand", "North", "DD049"),
    ("Deep Honda",         "Muktsar",     "Punjab",      "North", "DD243"),
    ("Deep Honda",         "Bhatinda",    "Punjab",      "North", "DD165"),
    ("Deep Honda",         "Amritsar",    "Punjab",      "North", "DD288"),
    ("Crown Honda",        "Vaishali",    "UP",          "North", "DD382"),
    ("Crown Honda",        "Noida",       "UP",          "North", "DD162"),
    ("Crown Honda",        "Ghaziabad",   "UP",          "North", "DD249"),
    ("Crown Honda",        "Delhi",       "Delhi",       "North", "DD341"),
    ("Courtesy Honda N2",  "Panipat",     "Haryana",     "North", "DD266"),
    ("Courtesy Honda N2",  "Karnal",      "Haryana",     "North", "DD357"),
    ("Courtesy Honda N1",  "Delhi",       "Delhi",       "North", "DD368"),
    ("Classic Honda",      "Faridabad",   "Haryana",     "North", "DD068"),
    ("Cherish Honda",      "Delhi",       "Delhi",       "North", "DD307"),
    ("Sango Honda",        "Itanagar",    "Arunachal",   "East",  "DD343"),
    ("Shree Honda",        "Chennai",     "Tamil Nadu",  "South", "DD201"),
    ("Indus Honda",        "Bangalore",   "Karnataka",   "South", "DD215"),
    ("Sundaram Honda",     "Chennai",     "Tamil Nadu",  "South", "DD188"),
    ("Popular Honda",      "Kochi",       "Kerala",      "South", "DD174"),
    ("Navnit Honda",       "Mumbai",      "Maharashtra", "West",  "DD091"),
    ("Rohan Honda",        "Pune",        "Maharashtra", "West",  "DD103"),
]

sr_zone_base = {"North": 49100, "South": 44000, "West": 38800, "East": 28600}
pm_zone_base = {"North": 24500, "South": 25000, "West": 21500, "East": 17900}
ew_zone_pen  = {"North": 56.6,  "South": 60.7,  "West": 56.7,  "East": 54.6}

rows = []
for i, (name, city, state, zone, code) in enumerate(dealers_raw):
    rng = np.random.default_rng(i * 23)
    sr_t = int(sr_zone_base[zone] * rng.uniform(0.7, 1.3))
    sr_a = int(sr_t * rng.uniform(0.82, 1.08))
    pm_t = int(pm_zone_base[zone] * rng.uniform(0.7, 1.3))
    pm_a = int(pm_t * rng.uniform(0.80, 1.05))
    deliveries = int(rng.uniform(185, 430))
    ew_pen = ew_zone_pen[zone] + rng.uniform(-8, 8)
    ew_a   = int(deliveries * ew_pen / 100)
    rsa_t  = int(rng.uniform(820, 2250))
    rsa_a  = int(rsa_t * rng.uniform(1.8, 2.4))
    atw_t  = int(rng.uniform(310, 820))
    atw_a  = int(atw_t * rng.uniform(0.75, 1.05))
    dssi   = int(rng.uniform(934, 977))

    sr_ach   = round(sr_a / sr_t * 100, 1)
    pm_ach   = round(pm_a / pm_t * 100, 1)
    rsa_ach  = round(rsa_a / rsa_t * 100, 1)
    ew_pen_r = round(ew_a / deliveries * 100, 1)
    atw_ach  = round(atw_a / atw_t * 100, 1)

    score = round(
        sr_ach  * 0.25 +
        pm_ach  * 0.20 +
        min(rsa_ach, 250) / 250 * 100 * 0.20 +
        ew_pen_r * 0.20 +
        atw_ach * 0.15,
        1
    )

    rows.append({
        "dealer_code": code,
        "dealer_name": name,
        "city": city,
        "state": state,
        "zone": zone,
        "sr_target": sr_t,  "sr_actual": sr_a,  "sr_achievement": sr_ach,
        "pm_target": pm_t,  "pm_actual": pm_a,  "pm_achievement": pm_ach,
        "deliveries": deliveries,
        "ew_actual": ew_a,  "ew_penetration": ew_pen_r,
        "rsa_target": rsa_t, "rsa_actual": rsa_a, "rsa_achievement": rsa_ach,
        "atw_target": atw_t, "atw_actual": atw_a, "atw_achievement": atw_ach,
        "dssi_score": dssi,
        "composite_score": score,
    })

dealers_df = pd.DataFrame(rows).sort_values("composite_score", ascending=False).reset_index(drop=True)
dealers_df["rank"] = dealers_df.index + 1
dealers_df.to_csv("data/dealer_performance.csv", index=False)
print("✅ data/dealer_performance.csv")

# ── 3. MONTHLY TREND DATA ──────────────────────────────────────
months = pd.date_range("2024-04-01", "2025-03-01", freq="MS")
month_labels = [m.strftime("%b-%Y") for m in months]

sr_monthly_base  = [172400,175800,168600,181900,163500,158400,173700,171600,178900,186000,189000,148300]
pm_monthly_base  = [94400, 97100, 92000, 98100, 89900, 86900, 95100, 93000, 96100,100100,102200, 83900]
rsa_monthly_base = [11250, 11750, 11050, 12470, 10730, 10330, 12070, 11450, 12270, 12780, 13290, 10910]

monthly_rows = []
for i, (m, lbl) in enumerate(zip(months, month_labels)):
    rng2 = np.random.default_rng(i * 41)
    sr_a  = int(sr_monthly_base[i]  * rng2.uniform(0.93, 1.03))
    pm_a  = int(pm_monthly_base[i]  * rng2.uniform(0.92, 1.04))
    rsa_a = int(rsa_monthly_base[i] * rng2.uniform(0.95, 1.05))
    monthly_rows.append({
        "month": lbl, "month_num": i+1,
        "sr_actual": sr_a, "sr_target": sr_monthly_base[i],
        "pm_actual": pm_a, "pm_target": pm_monthly_base[i],
        "rsa_actual": rsa_a,
    })

monthly_rows.append({
    "month": "Jan-2026", "month_num": 13,
    "sr_actual": 27840, "sr_target": 172400,
    "pm_actual": 15940, "pm_target": 94400,
    "rsa_actual": 5930,
})

monthly_df = pd.DataFrame(monthly_rows)
monthly_df.to_csv("data/monthly_trends.csv", index=False)
print("✅ data/monthly_trends.csv")

# ── 4. CORPORATE SALES ────────────────────────────────────────
corp_sales = pd.DataFrame([
    {"zone": "East",  "delivery_target": 793,  "delivery_actual": 596,  "achievement_pct": 75.2},
    {"zone": "North", "delivery_target": 2482, "delivery_actual": 1690, "achievement_pct": 68.1},
    {"zone": "South", "delivery_target": 2404, "delivery_actual": 1677, "achievement_pct": 69.8},
    {"zone": "West",  "delivery_target": 1714, "delivery_actual": 1164, "achievement_pct": 67.9},
])
corp_sales["gap"] = corp_sales["delivery_target"] - corp_sales["delivery_actual"]
corp_sales.to_csv("data/corporate_sales.csv", index=False)
print("✅ data/corporate_sales.csv")

# ── 5. RSA MODEL-WISE ─────────────────────────────────────────
rsa_models = pd.DataFrame([
    {"model": "Amaze",   "rsa_count": 43900, "segment": "Sedan"},
    {"model": "City",    "rsa_count": 32700, "segment": "Sedan"},
    {"model": "WR-V",    "rsa_count": 15300, "segment": "SUV"},
    {"model": "Elevate", "rsa_count": 13300, "segment": "SUV"},
    {"model": "BR-V",    "rsa_count": 10200, "segment": "SUV"},
    {"model": "BRIO",    "rsa_count":  9200, "segment": "Hatchback"},
])
rsa_models["share_pct"] = (rsa_models["rsa_count"] / rsa_models["rsa_count"].sum() * 100).round(1)
rsa_models.to_csv("data/rsa_models.csv", index=False)
print("✅ data/rsa_models.csv")

# ── 6. IT LICENSE / VENDOR DATA ────────────────────────────────
it_licenses = pd.DataFrame([
    {"application": "H-Connect",                     "partner": "Agranya",           "contract_type": "Agreement", "criticality": "High",    "systems_count": 1},
    {"application": "Helpdesk, Network",              "partner": "NTT",               "contract_type": "MSA",       "criticality": "High",    "systems_count": 2},
    {"application": "HSCP",                           "partner": "Tech Mahindra",     "contract_type": "Contract",  "criticality": "Medium",  "systems_count": 1},
    {"application": "WMS",                            "partner": "NEC Corporation",   "contract_type": "Contract",  "criticality": "High",    "systems_count": 1},
    {"application": "iTraining",                      "partner": "Stratbeans",        "contract_type": "Agreement", "criticality": "Low",     "systems_count": 1},
    {"application": "BOT",                            "partner": "Automation Edge",   "contract_type": "Agreement", "criticality": "Medium",  "systems_count": 1},
    {"application": "iWorkshop",                      "partner": "Bosch Ltd",         "contract_type": "MSA",       "criticality": "Medium",  "systems_count": 1},
    {"application": "Dlite, HLife, H-Connect, OBIEE", "partner": "IBM India Pvt Ltd", "contract_type": "MSA",       "criticality": "Critical","systems_count": 4},
    {"application": "Infrastructure",                 "partner": "Kyndryl Solutions", "contract_type": "MSA",       "criticality": "Critical","systems_count": 1},
    {"application": "HDMPS, QICS, FET, HEMS, F3",    "partner": "Infosys",           "contract_type": "MSA",       "criticality": "Critical","systems_count": 5},
    {"application": "MPS",                            "partner": "HP",                "contract_type": "Contract",  "criticality": "Medium",  "systems_count": 1},
    {"application": "NDC",                            "partner": "Panasonic",         "contract_type": "Agreement", "criticality": "Medium",  "systems_count": 1},
    {"application": "BOT",                            "partner": "Exela (Source HOV)","contract_type": "Agreement", "criticality": "Low",     "systems_count": 1},
    {"application": "NDC",                            "partner": "Artificial Reality","contract_type": "Agreement", "criticality": "Low",     "systems_count": 1},
    {"application": "SMAART",                         "partner": "GainInsight",       "contract_type": "Contract",  "criticality": "Medium",  "systems_count": 1},
    {"application": "SPEAR",                          "partner": "Girnarsoft",        "contract_type": "Contract",  "criticality": "Medium",  "systems_count": 1},
])
it_licenses["concentration_risk"] = it_licenses["systems_count"].apply(
    lambda x: "HIGH RISK" if x >= 4 else "MODERATE" if x >= 2 else "Normal"
)
it_licenses.to_csv("data/it_licenses.csv", index=False)
print("✅ data/it_licenses.csv")

# ── 7. HSQS COMPLAINT RATE ────────────────────────────────────
hsqs = pd.DataFrame([
    {"parameter": "Refreshment",                  "complaint_rate_pct": 7.8, "survey_type": "WI"},
    {"parameter": "Clean & Comfortable Facility", "complaint_rate_pct": 3.9, "survey_type": "WI"},
    {"parameter": "Courteousness",                "complaint_rate_pct": 3.8, "survey_type": "WI"},
    {"parameter": "Car Features Explanation",     "complaint_rate_pct": 1.9, "survey_type": "WI"},
    {"parameter": "Safety & Handling Explanation","complaint_rate_pct": 1.8, "survey_type": "WI"},
    {"parameter": "Explanation",                  "complaint_rate_pct": 0.0, "survey_type": "WI"},
    {"parameter": "Test Drive",                   "complaint_rate_pct": 0.0, "survey_type": "WI"},
])
hsqs.to_csv("data/hsqs_complaints.csv", index=False)
print("✅ data/hsqs_complaints.csv")

print("\n✅ All 7 datasets generated in data/ folder")
print(f"   Dealers: {len(dealers_df)}")
print(f"   Regions: {len(regional)}")
print(f"   Monthly rows: {len(monthly_df)}")
print(f"   IT Vendors: {len(it_licenses)}")
