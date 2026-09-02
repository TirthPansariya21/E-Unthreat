# E-UNTHREAT

AI-powered email threat detection, geolocation, and forensic intelligence — SIH 2026 (SIH26106).

```
python -m pip install -r requirements.txt
python -m src.ml_classifier
python -m streamlit run app.py
```

Paste a raw `.eml` or load a demo sample from the sidebar. The pipeline is `analyze_email()` in `src/fraud_aggregator.py` (NLP classifier + header forensics + IP/WHOIS tracing). Cases persist in local SQLite; each result can be exported as a PDF.
