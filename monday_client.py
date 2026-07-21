import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("MONDAY_API_TOKEN")

HEADERS = {
    "Authorization": API_TOKEN,
    "Content-Type": "application/json"
}

URL = "https://api.monday.com/v2"


def get_board_data(board_id):
    query = f"""
    query {{
      boards(ids: [{board_id}]) {{
        name
        items_page {{
          items {{
            id
            name
            column_values {{
              column {{
                title
              }}
              text
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(
        URL,
        json={"query": query},
        headers=HEADERS
    )

    response.raise_for_status()

    result = response.json()

    if "errors" in result:
        raise Exception(result["errors"])

    board = result["data"]["boards"][0]

    rows = []

    for item in board["items_page"]["items"]:

        row = {
            "Item Name": item["name"]
        }

        for col in item["column_values"]:
            row[col["column"]["title"]] = col["text"]

        rows.append(row)

    return pd.DataFrame(rows)


def load_all_data():

    deals_board = os.getenv("DEALS_BOARD_ID")
    work_board = os.getenv("WORK_ORDERS_BOARD_ID")

    deals_df = get_board_data(deals_board)
    work_df = get_board_data(work_board)

    return deals_df, work_df