
import requests
import json
from pathlib import Path

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3.5:4b"

DATA_FILE = Path(__file__).parent / "data" / "products.json"

with open(DATA_FILE, "r", encoding="utf-8") as file:
    products = json.load(file)


def ask_qwen(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "think": False,
                "options": {
                    "num_predict": 300,
                    "temperature": 0.3
                }
            },
            timeout=300
        )

        response.raise_for_status()
        return response.json()["response"]

    except requests.exceptions.RequestException as error:
        return f"Connection error: {error}"


def recommend_products(budget, preference):

    matching_products = [
        p for p in products
        if p["category"].lower() == "smartphone"
        and p["price"] <= budget
        and any(
            preference.lower() in feature.lower()
            for feature in p["features"]
        )
    ]

    if not matching_products:
        print("\nNo matching products found.")
        return

    prompt = f"""
    You are an AI Product Recommendation Agent.

    Customer budget: Rs. {budget}
    Customer preference: {preference}

    Available products:
    {json.dumps(matching_products, indent=2)}

    Recommend suitable products.
    Explain why they match the customer's needs.
    Use only the provided information.
    Do not invent specifications or prices.
    """

    print("\nGenerating recommendations...")
    print(ask_qwen(prompt))


def compare_products(product1, product2):

    selected = []

    for name in [product1, product2]:
        matches = [
            p for p in products
            if p["name"].lower() == name.lower()
        ]

        if not matches:
            print(f"\nProduct not found: {name}")
            return

        selected.append(matches[0])

    prompt = f"""
    Compare these two products using only the supplied data:

    {json.dumps(selected, indent=2)}

    Show:
    1. Price comparison
    2. Feature comparison
    3. Advantages of each product
    4. Which customer needs each product suits best

    Do not invent missing specifications.
    Clearly mention when information is unavailable.
    """

    print("\nGenerating product comparison...")
    print(ask_qwen(prompt))


print("=" * 45)
print("AI PRODUCT INTELLIGENCE AGENT")
print("=" * 45)

print("\n1. Recommend a product")
print("2. Compare two products")

choice = input("\nChoose an option (1 or 2): ")

if choice == "1":

    budget = int(input("\nEnter your budget (Rs.): "))
    preference = input("Enter your preference (camera/battery/display/5G): ")

    recommend_products(budget, preference)

elif choice == "2":

    print("\nAvailable products:")

    for p in products:
        print("-", p["name"])

    product1 = input("\nEnter first product name: ")
    product2 = input("Enter second product name: ")

    compare_products(product1, product2)

else:
    print("\nInvalid option. Please choose 1 or 2.")


