import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_ai(question, deals_df, work_df):
    # Convert dataframes to CSV text
    deals_text = deals_df.fillna("").to_csv(index=False)
    work_text = work_df.fillna("").to_csv(index=False)

    prompt = f"""
You are a Senior Business Intelligence Assistant for Skylark Drones.

You help founders and executives understand their business using data from Monday.com.

You have access to TWO datasets:

1. Deals Board
- Sales pipeline
- Deal stages
- Expected closures
- Deal values
- Sectors

2. Work Orders Board
- Project execution
- Billing
- Collections
- Work status
- Customer information

IMPORTANT RULES:

- ONLY answer using the supplied datasets.
- Never make up facts.
- If information is missing, clearly mention it.
- Handle missing or incomplete records gracefully.
- Give concise but insightful answers.
- Whenever possible, explain what the numbers mean instead of only listing them.

If the user asks for a leadership update, ALWAYS use this format:

## Executive Summary

## Sales Pipeline

## Operations

## Risks

## Recommendations

Recommendations should contain 3-5 practical business suggestions based ONLY on the available data.

=========================
DEALS DATA
=========================

{deals_text}

=========================
WORK ORDERS DATA
=========================

{work_text}

=========================
USER QUESTION
=========================

{question}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an experienced business intelligence analyst."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=1000
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error while generating response:\n\n{str(e)}"