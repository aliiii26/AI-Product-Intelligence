# AI Product Intelligence Agent

## Project Overview
An AI-powered product assistant that helps customers discover and compare smartphones based on their budget and preferences.

The project uses a locally running Qwen3.5 4B language model through Ollama.

## Features

### 1. Product Recommendation
- Accepts a customer's budget.
- Accepts product preferences such as camera, battery, display and 5G.
- Filters products from a sample JSON catalogue.
- Uses an LLM to explain suitable recommendations.

### 2. Product Comparison
- Allows customers to select two products.
- Compares their prices and available features.
- Explains advantages and suitability.
- Uses the provided catalogue information.

## Technology Stack
- Python
- Ollama
- Qwen3.5 4B
- Requests
- JSON
- Visual Studio Code

## Project Structure

```text
AI_Product_Intelligence/
├── .venv/
├── data/
│   └── products.json
├── main.py
└── README.md
```

## How It Works

1. Customer selects recommendation or comparison.
2. Python reads the product catalogue.
3. Python filters or selects the relevant products.
4. The selected product information is sent to Qwen through the Ollama API.
5. Qwen generates recommendations or comparisons.
6. Results are displayed in the terminal.

## How to Run

1. Install Python and Ollama.
2. Download the model:

```powershell
ollama pull qwen3.5:4b
```

3. Install the Python dependency:

```powershell
python -m pip install requests
```

4. Run the application:

```powershell
python main.py
```

## Data Disclaimer

The current product catalogue contains sample testing data. Product prices and specifications are not verified live market listings.

## Project Status

Working prototype with product recommendation and product comparison capabilities.

## Future Improvements
- Review analysis
- Web-based user interface
- Larger product catalogue
- Live product data integration
- More advanced customer preference matching