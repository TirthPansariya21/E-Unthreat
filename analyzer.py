"""Compatibility shim. Prefer src.fraud_aggregator.analyze_email."""

from src.explanations import FLAG_EXPLANATIONS, explain_flag
from src.fraud_aggregator import analyze_email as analyze_email_mock
from src.fraud_aggregator import analyze_email
