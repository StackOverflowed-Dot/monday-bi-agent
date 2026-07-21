# Decision Log

## Assumptions

- Monday.com boards are the single source of truth.
- The agent reads data in real time rather than using local CSVs.
- Missing values are expected and should not prevent analysis.

## Trade-offs

- Used Groq instead of OpenAI due to free API availability and fast inference.
- Chose Streamlit for rapid prototyping.
- Sent board data directly to the LLM since the dataset is relatively small (~524 rows), simplifying implementation within the assignment timeline.

## Leadership Updates

The agent interprets leadership updates as executive summaries including:
- Pipeline health
- Sector performance
- Work order status
- Risks caused by missing or incomplete data

## Future Improvements

- Smarter filtering before sending data to the LLM.
- Charts and dashboards.
- Authentication and role-based access.
- Conversation memory.
- Caching to reduce API calls.