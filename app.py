
import streamlit as st
import requests
import json
from pathlib import Path

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="AI Product Intelligence",
    page_icon="🛍️",
    layout="wide"
)

st.title("🛍️ AI Product Intelligence Agent")
st.caption("Your personal AI shopping assistant")

# -----------------------------
# LOAD PRODUCT CATALOGUE
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent
PRODUCT_FILE = BASE_DIR / "data" / "products.json"

with open(PRODUCT_FILE, "r", encoding="utf-8") as file:
    products = json.load(file)

# -----------------------------
# SIDEBAR PRODUCT FILTERS
# -----------------------------

st.sidebar.title("🔍 Product Filters")

categories = ["All"] + sorted(set(
    p["category"] for p in products
))

selected_category = st.sidebar.selectbox(
    "Category",
    categories
)

brands = sorted(set(p["brand"] for p in products))

selected_brands = st.sidebar.multiselect(
    "Select Brands",
    brands,
    default=brands
)

max_price = max(p["price"] for p in products)

price_range = st.sidebar.slider(
    "Price Range (₹)",
    min_value=0,
    max_value=max_price,
    value=(0, max_price),
    step=500
)

all_features = sorted(set(
    feature
    for p in products
    for feature in p["features"]
))

selected_features = st.sidebar.multiselect(
    "Features",
    all_features
)

# -----------------------------
# FILTER PRODUCTS
# -----------------------------

filtered_products = [
    p for p in products
    if (
        (selected_category == "All"
         or p["category"] == selected_category)
        and p["brand"] in selected_brands
        and price_range[0] <= p["price"] <= price_range[1]
        and (
            not selected_features
            or all(
                feature in p["features"]
                for feature in selected_features
            )
        )
    )
]

st.sidebar.divider()

st.sidebar.metric(
    "Matching Products",
    len(filtered_products)
)

if st.sidebar.button("Reset Filters"):
    st.rerun()

# -----------------------------
# DISPLAY PRODUCT CARDS
# -----------------------------

st.subheader("🛒 Product Catalogue")

if filtered_products:
    columns = st.columns(3)

    for index, product in enumerate(filtered_products):
        with columns[index % 3]:
            with st.container(border=True):
                st.subheader(product["name"])
                st.caption(product["brand"])

                st.markdown(
                    f"### ₹{product['price']:,}"
                )

                st.write("**Category:**", product["category"])

                st.write("**Features:**")

                for feature in product["features"]:
                    st.write(f"• {feature}")

else:
    st.warning("No products match your selected filters.")

# -----------------------------
# OLLAMA CONFIGURATION
# -----------------------------

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3.5:4b"


def ask_qwen(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "think": False,
            "options": {
                "num_predict": 400,
                "temperature": 0.3
            }
        },
        timeout=300
    )

    response.raise_for_status()

    return response.json()["response"]


# -----------------------------
# AI CHAT SECTION
# -----------------------------

st.divider()
st.subheader("🤖 Ask Your AI Shopping Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Display chat history

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input

user_input = st.chat_input(
    "Ask about products, prices or recommendations..."
)

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        with st.spinner("Qwen is thinking..."):

            if not filtered_products:
                answer = (
                    "No products currently match your sidebar filters. "
                    "Please adjust the filters and try again."
                )

            else:
                prompt = f"""
You are an AI Product Intelligence and Shopping Assistant.

Here is the available product catalogue:
{json.dumps(filtered_products, indent=2)}

User question:
{user_input}

Instructions:
1. Recommend products based on the user's requirements.
2. Compare products when requested.
3. Respect the available product prices and catalogue.
4. Use only the products provided above.
5. Never invent prices, features or specifications.
6. Explain recommendations in simple language.
7. Always write complete prices with all digits.
8. Use bullet points instead of Markdown tables.
9. If the catalogue does not contain enough information,
   clearly explain that.
10. Remember that the available catalogue is already filtered
    according to the user's sidebar selections.
"""

                try:
                    answer = ask_qwen(prompt)

                except requests.exceptions.RequestException as error:
                    answer = (
                        f"Could not connect to Ollama: {error}"
                    )

            st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
