# Monday.com Business Intelligence Agent

## Overview
This project is an AI-powered Business Intelligence chatbot that connects to Monday.com boards containing Deals and Work Orders.

The chatbot answers founder-level business questions by reading live data from Monday.com and generating insights using an LLM.

## Features

- Reads live Monday.com boards
- Handles missing values and inconsistent data
- Answers business questions conversationally
- Generates leadership summaries
- Provides data quality awareness

## Tech Stack

- Python
- Streamlit
- Monday.com GraphQL API
- Pandas
- Groq (Llama 3.3 70B)
- python-dotenv

## Setup

1. Clone the repository.
2. Install requirements.

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with:

```env
MONDAY_API_TOKEN=...
DEALS_BOARD_ID=...
WORK_ORDERS_BOARD_ID=...
GROQ_API_KEY=...
```

4. Run:

```bash
streamlit run app.py
```