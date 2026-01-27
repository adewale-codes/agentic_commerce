import re
from typing import List, Tuple
from app.agent.schemas import Constraints, ClarifyingQuestion

def extract_constraints(text: str) -> Constraints:
    t = text.lower()

    c = Constraints()

    m = re.search(r"(?:under|below|<=)\s*£?\s*(\d{2,5})", t)
    if m:
        c.max_price_gbp = float(m.group(1))
    m2 = re.search(r"£\s*(\d{2,5})", t)
    if c.max_price_gbp is None and m2:
        c.max_price_gbp = float(m2.group(1))

    m = re.search(r"(\d{1,2})\s*gb\s*ram", t)
    if m:
        c.min_ram_gb = int(m.group(1))

    if "1tb" in t or "1024gb" in t:
        c.min_storage_gb = 1024
    else:
        m = re.search(r"(\d{3,4})\s*gb\s*(?:ssd|storage)?", t)
        if m:
            c.min_storage_gb = int(m.group(1))

    m = re.search(r"(\d{1,2}(?:\.\d)?)\s*h(?:ours)?\s*battery", t)
    if m:
        c.min_battery_hours = float(m.group(1))
    elif "good battery" in t or "long battery" in t:
        c.min_battery_hours = 10.0

    m = re.search(r"under\s*(\d(?:\.\d)?)\s*kg", t)
    if m:
        c.max_weight_kg = float(m.group(1))

    if "mac" in t or "macos" in t:
        c.os = "macOS"
    elif "chromeos" in t or "chromebook" in t:
        c.os = "ChromeOS"
    elif "windows" in t:
        c.os = "Windows 11"

    m = re.search(r"deliver(?:y)?\s*(?:in|within)\s*(\d{1,2})\s*day", t)
    if m:
        c.shipping_days_max = int(m.group(1))

    return c

def clarifying_questions(c: Constraints) -> List[ClarifyingQuestion]:
    qs: List[ClarifyingQuestion] = []

    if c.max_price_gbp is None:
        qs.append(ClarifyingQuestion(
            question="What’s your budget (max price in £)?",
            choices=["£400", "£650", "£900", "No limit"]
        ))

    if c.min_ram_gb is None:
        qs.append(ClarifyingQuestion(
            question="How much RAM do you want?",
            choices=["8GB", "16GB", "32GB"]
        ))

    if c.os is None:
        qs.append(ClarifyingQuestion(
            question="Which OS do you prefer?",
            choices=["Windows 11", "macOS", "ChromeOS", "No preference"]
        ))

    return qs
