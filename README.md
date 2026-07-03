# Griot

A Streamlit app for grounded AI conversations about African economic reality.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. Push this repository to GitHub.
2. Create a Streamlit Cloud app from the repository.
3. Set the secrets:
   - `GROQ_API_KEY`
   - optionally `GEMINI_API_KEY`
4. Set the main file to `app.py`.
