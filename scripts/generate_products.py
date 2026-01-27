import json
import random
from pathlib import Path

random.seed(42)

BRANDS = {
    "Lenovo": ["IdeaPad", "ThinkPad", "Yoga Slim"],
    "Dell": ["Inspiron", "Vostro", "XPS"],
    "HP": ["Pavilion", "Envy", "ProBook"],
    "Acer": ["Aspire", "Swift"],
    "ASUS": ["VivoBook", "ZenBook", "TUF Gaming"],
    "MSI": ["Modern", "GF Series"],
    "LG": ["UltraLight"],
    "Apple": ["MacBook Air"]
}

CPUS = [
    ("Intel i3-1115G4", 0.9),
    ("Intel i5-1135G7", 1.0),
    ("Intel i5-1235U", 1.15),
    ("Intel i7-1255U", 1.35),
    ("Intel i7-1360P", 1.55),
    ("Ryzen 3 5300U", 0.95),
    ("Ryzen 5 5500U", 1.10),
    ("Ryzen 5 7530U", 1.25),
    ("Ryzen 7 5700U", 1.35),
    ("Ryzen 7 7840U", 1.65),
    ("Apple M1", 1.45),
    ("Apple M2", 1.75),
]

RAM_OPTIONS = [4, 8, 16, 32]
STORAGE_OPTIONS = [128, 256, 512, 1024]
SCREEN_OPTIONS = [13.3, 14.0, 15.6, 16.0]
RES_BY_SCREEN = {
    13.3: ["2560x1600", "1920x1080"],
    14.0: ["1920x1080", "1920x1200", "2880x1800"],
    15.6: ["1920x1080"],
    16.0: ["1920x1200", "2560x1600"]
}
OS_BY_BRAND = {"Apple": "macOS"}

PORT_SETS = [
    ["USB-C", "USB-A", "HDMI"],
    ["USB-C", "USB-A"],
    ["USB-A", "HDMI"],
    ["USB-C", "USB-A", "HDMI", "Ethernet"]
]

def weighted_choice(options, weights):
    return random.choices(options, weights=weights, k=1)[0]

def price_estimate(brand, cpu_mult, ram_gb, storage_gb, screen_inches, battery_hours, weight_kg):
    base = 260
    base *= cpu_mult
    base += (ram_gb - 4) * 18
    base += (storage_gb / 256) * 35
    base += (screen_inches - 13) * 20
    base += (battery_hours - 6) * 10
    base -= max(0, (weight_kg - 1.2)) * 25

    if brand == "Apple":
        base *= 1.35
    elif brand in ["Dell", "Lenovo", "HP", "ASUS", "LG"]:
        base *= 1.10
    else:
        base *= 1.00

    base = max(179, min(base, 2499))
    return round(base / 10) * 10 - 0.99

def generate_one(idx: int):
    brand = random.choice(list(BRANDS.keys()))
    family = random.choice(BRANDS[brand])

    cpu, cpu_mult = random.choice(CPUS)

    ram = weighted_choice(RAM_OPTIONS, weights=[0.05, 0.45, 0.42, 0.08])

    storage = weighted_choice(STORAGE_OPTIONS, weights=[0.06, 0.42, 0.40, 0.12])

    screen = weighted_choice(SCREEN_OPTIONS, weights=[0.25, 0.40, 0.30, 0.05])
    resolution = random.choice(RES_BY_SCREEN[screen])

    battery = round(random.uniform(6.0, 16.5), 1)
    weight = round(random.uniform(0.95, 2.45), 2)

    gpu = None
    if brand in ["ASUS", "MSI"] and random.random() < 0.18:
        gpu = random.choice(["NVIDIA RTX 3050", "NVIDIA RTX 4050"])

    ports = random.choice(PORT_SETS)
    os = OS_BY_BRAND.get(brand, random.choice(["Windows 11", "Windows 11", "Windows 11", "ChromeOS"]))

    rating = round(random.uniform(3.6, 4.8), 1)
    reviews = int(random.uniform(80, 6500))
    shipping_days = random.randint(1, 8)
    in_stock = random.random() < 0.88

    price = price_estimate(brand, cpu_mult, ram, storage, screen, battery, weight)
    title = f"{brand} {family} {screen:g} ({cpu.split()[1]}, {ram}GB, {storage}GB SSD)"

    item = {
        "id": f"lap_{idx:04d}",
        "title": title,
        "brand": brand,
        "category": "laptop",
        "price_gbp": price,
        "rating": rating,
        "review_count": reviews,
        "shipping_days": shipping_days,
        "in_stock": in_stock,
        "attributes": {
            "cpu": cpu,
            "ram_gb": ram,
            "storage_gb": storage,
            "battery_hours": battery,
            "weight_kg": weight,
            "screen_inches": screen,
            "resolution": resolution,
            "os": os,
            "ports": ports
        },
        "url": f"https://example.com/{f'lap_{idx:04d}'}"
    }

    if gpu:
        item["attributes"]["gpu"] = gpu

    return item

def main(n=800):
    data = [generate_one(i) for i in range(1, n + 1)]
    out_path = Path("data/products.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, indent=2))
    print(f"Wrote {n} products to {out_path}")

if __name__ == "__main__":
    main(800)
