
import streamlit as st
import requests
import json
from pathlib import Path

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="ProductPilot",
    page_icon="✈️",
    layout="wide"
)

# ==========================================
# 2. LOAD PRODUCT CATALOGUE
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
PRODUCT_FILE = BASE_DIR / "data" / "products.json"

with open(PRODUCT_FILE, "r", encoding="utf-8") as file:
    products = json.load(file)


# ==========================================
# 3. OLLAMA CONFIGURATION
# ==========================================

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


# ==========================================
# 4. SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("✈️ ProductPilot")

st.sidebar.caption("Your guide to better purchases.")

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Explore Products",
        "AI Assistant"
    ]
)

st.sidebar.divider()

st.sidebar.markdown("### Technology Stack")

st.sidebar.caption(
    "Python • Streamlit • Ollama • Qwen 3.5 4B"
)


# ==========================================
# 5. HOME DASHBOARD
# ==========================================

if page == "Home":

    st.title("✈️ Welcome to ProductPilot")

    st.subheader("Your guide to better purchases.")

    st.write(
        "Discover products, compare features and get "
        "intelligent shopping recommendations powered by AI."
    )

    st.divider()

    # Dashboard statistics

    total_products = len(products)

    total_brands = len(set(
        p["brand"] for p in products
    ))

    total_categories = len(set(
        p["category"] for p in products
    ))

    average_price = (
        sum(p["price"] for p in products) / total_products
        if total_products > 0 else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Products",
        total_products
    )

    col2.metric(
        "Available Brands",
        total_brands
    )

    col3.metric(
        "Categories",
        total_categories
    )

    col4.metric(
        "Average Price",
        f"₹{average_price:,.0f}"
    )

    st.divider()

    # Featured products

    st.subheader("⭐ Budget-Friendly Picks")

    featured_products = sorted(
        products,
        key=lambda p: p["price"]
    )[:3]

    columns = st.columns(3)

    for index, product in enumerate(featured_products):

        with columns[index]:

            with st.container(border=True):

                st.subheader(product["name"])

                st.caption(product["brand"])

                st.markdown(
                    f"### ₹{product['price']:,}"
                )

                st.write("**Key Features**")

                for feature in product["features"]:

                    st.write(f"• {feature}")

    st.divider()

    # About ProductPilot

    st.subheader("🚀 Explore ProductPilot")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 🛒 Explore Products")

        st.write(
            "Browse the product catalogue and filter "
            "products by brand, price, category and features."
        )

        if st.button(
            "Explore Products",
            use_container_width=True
        ):

            st.session_state.selected_page = "Explore Products"
            st.rerun()

    with col2:

        st.markdown("### 🤖 AI Shopping Assistant")

        st.write(
            "Get intelligent recommendations and compare "
            "products using our local AI model."
        )

        if st.button(
            "Open AI Assistant",
            use_container_width=True
        ):

            st.session_state.selected_page = "AI Assistant"
            st.rerun()


# ==========================================
# 6. EXPLORE PRODUCTS PAGE
# ==========================================

elif page == "Explore Products":

    st.title("🛒 Explore Products")

    st.caption(
        "Find the products that match your requirements."
    )

    st.sidebar.subheader("🔍 Product Filters")

    # Category filter

    categories = ["All"] + sorted(set(
        p["category"] for p in products
    ))

    selected_category = st.sidebar.selectbox(
        "Category",
        categories
    )

    # Brand filter

    brands = sorted(set(
        p["brand"] for p in products
    ))

    selected_brands = st.sidebar.multiselect(
        "Select Brands",
        brands,
        default=brands
    )

    # Price filter

    max_price = max(
        (p["price"] for p in products),
        default=1000
    )

    price_range = st.sidebar.slider(
        "Price Range (₹)",
        min_value=0,
        max_value=max_price,
        value=(0, max_price),
        step=500
    )

    # Feature filter

    all_features = sorted(set(
        feature
        for p in products
        for feature in p["features"]
    ))

    selected_features = st.sidebar.multiselect(
        "Select Features",
        all_features
    )

    # Apply filters

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

    st.metric(
        "Matching Products",
        len(filtered_products)
    )

    st.divider()

    # Display product cards

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

                    st.write(
                        "**Category:**",
                        product["category"]
                    )

                    st.write("**Features:**")

                    for feature in product["features"]:

                        st.write(f"• {feature}")

    else:

        st.warning(
            "No products found. Try changing your filters."
        )


# ==========================================
# 7. AI ASSISTANT PAGE
# ==========================================

elif page == "AI Assistant":

    st.title("🤖 ProductPilot AI Assistant")

    st.caption(
        "Your personal shopping assistant, powered by Qwen 3.5 4B."
    )

    # Initialize chat history

    if "messages" not in st.session_state:

        st.session_state.messages = []

    # Clear chat

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()

    # Display chat history

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # Chat input

    user_input = st.chat_input(
        "Ask ProductPilot about products, prices or recommendations..."
    )

    if user_input:

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):

            st.markdown(user_input)

        with st.chat_message("assistant"):

            with st.spinner("ProductPilot is thinking..."):

                prompt = f"""
You are ProductPilot, an AI Product Intelligence Assistant.

Your tagline is: Your guide to better purchases.

Available product catalogue:

{json.dumps(products, indent=2)}

User question:

{user_input}

Instructions:

1. Recommend products based on the user's requirements.
2. Compare products when requested.
3. Respect the user's budget.
4. Only use products from the provided catalogue.
5. Never invent prices or product specifications.
6. Explain recommendations in simple language.
7. Always show complete prices.
8. Use bullet points instead of Markdown tables.
9. Clearly mention when information is unavailable.
10. Help users make informed purchasing decisions.
"""

                try:

                    answer = ask_qwen(prompt)

                except requests.exceptions.ConnectionError:

                    answer = (
                        "Unable to connect to Ollama. "
                        "Please make sure Ollama is running."
                    )

                except requests.exceptions.Timeout:

                    answer = (
                        "Qwen took too long to respond. "
                        "Please try again."
                    )

                except requests.exceptions.RequestException as error:

                    answer = f"An error occurred: {error}"

                st.markdown(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })


        
