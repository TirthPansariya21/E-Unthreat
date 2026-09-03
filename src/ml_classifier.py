"""TF-IDF + Logistic Regression phishing classifier plus rule-based NLP signals (FR2)."""

from __future__ import annotations

import csv
import re
from html.parser import HTMLParser
from pathlib import Path

from src.email_parser import ParsedEmail
from src.paths import MODEL_PATH, MODELS_DIR, TRAINING_CSV

BRANDS = [
    "paypal",
    "microsoft",
    "apple",
    "amazon",
    "google",
    "facebook",
    "instagram",
    "netflix",
    "linkedin",
    "github",
    "wellsfargo",
    "chase",
    "bankofamerica",
    "dhl",
    "fedex",
    "ups",
    "adobe",
    "dropbox",
    "whatsapp",
]

URGENCY_RE = re.compile(
    r"\b(urgent|immediately|within\s+\d+\s+hours?|act now|last chance|"
    r"account (will be )?(locked|suspended|closed)|verify (your )?account|"
    r"confirm (your )?(identity|password)|limited time|failure to|"
    r"unusual (sign[- ]?in|activity)|unauthorized)\b",
    re.I,
)
CREDENTIAL_RE = re.compile(
    r"\b(password|otp|one[- ]time (code|password)|ssn|social security|"
    r"cvv|pin|login here|reset your password|update (your )?billing|"
    r"confirm (your )?details)\b",
    re.I,
)
SHORT_LINK_RE = re.compile(
    r"https?://(bit\.ly|tinyurl\.com|t\.co|goo\.gl|ow\.ly|is\.gd|buff\.ly|cutt\.ly)/",
    re.I,
)
PAYMENT_RE = re.compile(
    r"\b(gift card|itunes|steam card|wire transfer|bitcoin|crypto|urgent payment|"
    r"purchase \d+ cards)\b",
    re.I,
)
BRAND_DISPLAY_RE = re.compile(
    r"\b(paypal|microsoft|apple|amazon|google|netflix|wells fargo|bank of america|"
    r"it support|helpdesk|ceo|cfo|human resources|dhl|fedex)\b",
    re.I,
)
ATTACHMENT_RE = re.compile(
    r"\b(invoice attached|see attached|voicemail|\.html attachment|enable macros|"
    r"shipment (label|notification)|document enclosed)\b",
    re.I,
)
IP_URL_RE = re.compile(r"https?://(?:\d{1,3}\.){3}\d{1,3}", re.I)
HREF_RE = re.compile(r"""href\s*=\s*['"]([^'"]+)['"]""", re.I)


class _LinkTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.pairs: list[tuple[str, str]] = []
        self._href: str | None = None
        self._buf: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self._href = href
                self._buf = []

    def handle_data(self, data):
        if self._href is not None:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._href is not None:
            self.pairs.append(("".join(self._buf).strip(), self._href))
            self._href = None
            self._buf = []


def _levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        curr = [i]
        for j, cb in enumerate(b, 1):
            ins, delete, sub = curr[j - 1] + 1, prev[j] + 1, prev[j - 1] + (ca != cb)
            curr.append(min(ins, delete, sub))
        prev = curr
    return prev[-1]


def _normalize_label(value: str) -> str:
    table = str.maketrans({"0": "o", "1": "l", "3": "e", "4": "a", "5": "s", "7": "t"})
    return value.lower().replace("-", "").replace("_", "").translate(table)


def lookalike_brand(domain: str) -> str | None:
    if not domain:
        return None
    label = domain.split(".")[0].lower()
    bait = {"secure", "login", "account", "verify", "support", "alert", "security", "notify", "signin"}
    parts = [label, label.replace("-", "")] + [p for p in re.split(r"[-_]", label) if p]
    for part in parts:
        compact = part.replace("-", "").replace("_", "")
        normalized = _normalize_label(part)
        for brand in BRANDS:
            if compact == brand:
                continue
            if normalized == brand:
                return brand
            if len(compact) >= 4 and _levenshtein(compact, brand) <= 2:
                return brand
            if compact.startswith(brand) and any(token in compact for token in bait):
                return brand
    return None


def _training_rows() -> list[tuple[str, str]]:
    phishing = [
        "Your PayPal account will be locked in 12 hours. Verify your account immediately and confirm your identity at this link.",
        "Dear Customer, unusual activity on your Microsoft account. Reset your password now or it will be suspended.",
        "Urgent wire transfer required before close of business. Purchase gift cards and send the codes. Do not discuss on Slack.",
        "Invoice attached outstanding customs fee. Confirm your details so we can release the package. Dear Customer.",
        "Click here to update your billing and confirm your password. Failure to act now will close the account.",
        "Amazon order on hold. Login here with your password to avoid cancellation. Limited time.",
        "IT support: your mailbox is full. Confirm your identity and password immediately via http://bit.ly/reset-now",
        "Wells Fargo security alert. Unauthorized transaction. Verify your account within 24 hours.",
        "CEO requesting urgent payment. Process this wire and buy itunes gift cards today.",
        "DHL parcel on hold. Confirm your details or the shipment will be returned. Dear Customer.",
        "Apple ID locked. Confirm your identity and update billing at http://apple-secure-login.tk",
        "Netflix payment failed. Update your billing and password or the subscription ends today.",
        "Document enclosed.enable macros to view the voicemail invoice attached.",
        "Your package from FedEx needs a customs payment in bitcoin. Act now.",
        "Dear user, we detected unusual activity. Login here to keep your account.",
        "Paypa1 security: account will be locked. Verify account immediately https://bit.ly/pp-alert",
        "Human resources: update payroll bank details today or you will not be paid.",
        "Crypto wallet verification required. Send bitcoin to release the funds immediately.",
        "Bank of America: confirm your details and SSN or the account will be closed.",
        "Helpdesk ticket: unusual sign-in. Reset your password using the attached html.",
        "Last chance to confirm your identity for the tax refund wire transfer.",
        "Google Drive voicemail: see attached invoice.html and enable macros.",
        "LinkedIn: confirm your password after unusual activity or we suspend the profile.",
        "UPS delivery failed. Pay the outstanding fee with gift cards. Dear Customer.",
        "Adobe license expired. Confirm your details and credit card CVV immediately.",
        "Dropbox shared a confidential file. Login here to view. Account will be locked.",
        "WhatsApp verification OTP requested. Send the one time password to continue.",
        "Your mailbox will be closed within 6 hours unless you verify your account now.",
        "Supplier invoice: urgent payment to a new bank account. Do not call the office.",
        "Security team: unauthorized login. Confirm your identity at this shortened link.",
    ]
    legitimate = [
        "A new sign-in to your GitHub account from Chrome on Windows. If this was you, no action is required.",
        "Your package was delivered today. Track it on the official carrier site. Thank you for shopping with us.",
        "Open enrolment reminder. No action required yet. Benefits questions can wait until next week.",
        "Meeting: product review Thursday 3pm. Calendar invite attached. See you then.",
        "Your monthly statement is ready in online banking. No password is requested in this email.",
        "GitHub: we noticed a new sign-in. Review sessions at github.com/settings/sessions.",
        "Thanks for your order. Receipt for invoice 18422 is available in your account.",
        "Project standup notes from this morning. Action items are in the tracker.",
        "Password changed successfully on your account. If you did this, no further action is needed.",
        "Newsletter: three articles we liked this week. Unsubscribe anytime.",
        "Your flight is confirmed. Check-in opens 24 hours before departure.",
        "Welcome to the team. HR orientation is Monday. Reply if you have dietary notes.",
        "The pull request was merged. CI is green. Nice work.",
        "Reminder: library book due next Friday. Renew online if you need more time.",
        "Your electricity bill is available. Pay by the date on the statement.",
        "Concert tickets are in your wallet app. Doors at 7. Enjoy the show.",
        "Doctor appointment confirmed for 10:30. Arrive 10 minutes early.",
        "Classroom assignment posted. Submit before Friday. Let me know if you have questions.",
        "Backup completed successfully. 42 GB stored. No action required.",
        "Subscription renewed. Thank you for being a customer. Manage billing in settings.",
        "Conference talk accepted. Travel booking link is on the speaker portal.",
        "Happy birthday. The team chipped in for coffee. See you at lunch.",
        "Weather alert: rain this afternoon. No office closure expected.",
        "Your table reservation is confirmed for two at 19:00.",
        "Code of conduct acknowledgement received. Thank you.",
        "The server maintenance window finished. Services are back to normal.",
        "Timesheet submitted. Your manager will approve it this week.",
        "Welcome email: verify the address by visiting our official site when convenient.",
        "Family photo album shared. View when you have a moment. No rush.",
        "Invoice 90210 from your accountant. Payment terms net 30 as agreed.",
    ]
    # Light paraphrases so TF-IDF has more n-grams.
    extra_phish = [t.replace("account", "profile") for t in phishing[:10]]
    extra_legit = [t.replace("your", "the") for t in legitimate[:10]]
    rows = [(t, "phishing") for t in phishing + extra_phish]
    rows += [(t, "legitimate") for t in legitimate + extra_legit]
    return rows


def ensure_training_csv(path: Path = TRAINING_CSV) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["text", "label"])
            writer.writerows(_training_rows())
    return path


def load_dataset(path: Path | None = None) -> tuple[list[str], list[str]]:
    csv_path = ensure_training_csv(path or TRAINING_CSV)
    texts, labels = [], []
    with csv_path.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            texts.append(row["text"])
            labels.append(row["label"])
    return texts, labels


def train_and_save(path: Path = MODEL_PATH) -> dict:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline
    import joblib

    texts, labels = load_dataset()
    x_train, x_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.25, random_state=42, stratify=labels
    )
    pipe = Pipeline(
        [
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, max_features=8000)),
            ("clf", LogisticRegression(max_iter=500, class_weight="balanced")),
        ]
    )
    pipe.fit(x_train, y_train)
    acc = float(accuracy_score(y_test, pipe.predict(x_test)))
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"pipeline": pipe, "accuracy": acc}, path)
    return {"accuracy": acc, "n_train": len(x_train), "n_test": len(x_test), "path": str(path)}


def _load_model():
    try:
        import joblib
    except Exception:
        return None
    if not MODEL_PATH.exists():
        try:
            train_and_save()
        except Exception:
            return None
    try:
        import joblib as jb
        return jb.load(MODEL_PATH)
    except Exception:
        return None


def predict_text(text: str) -> dict:
    """Return {label, confidence 0-100, accuracy} using the saved model, or a safe fallback."""
    bundle = _load_model()
    if bundle is None:
        return {"label": "Suspicious", "confidence": 50, "accuracy": None, "available": False}
    pipe = bundle["pipeline"]
    proba = pipe.predict_proba([text])[0]
    classes = list(pipe.classes_)
    phish_idx = classes.index("phishing") if "phishing" in classes else 0
    p_phish = float(proba[phish_idx])
    if p_phish >= 0.70:
        label = "Phishing"
        confidence = round(p_phish * 100)
    elif p_phish >= 0.40:
        label = "Suspicious"
        confidence = round(p_phish * 100)
    else:
        label = "Legitimate"
        confidence = round((1 - p_phish) * 100)
    return {
        "label": label,
        "confidence": int(confidence),
        "p_phishing": p_phish,
        "accuracy": bundle.get("accuracy"),
        "available": True,
    }


def rule_based_signals(parsed: ParsedEmail) -> list[str]:
    flags: list[str] = []
    combined = f"{parsed.subject}\n{parsed.body}\n{parsed.from_name} {parsed.from_addr}"
    if URGENCY_RE.search(combined):
        flags.append("Urgency language detected")
    if SHORT_LINK_RE.search(combined):
        flags.append("Suspicious shortened link found")
    brand = lookalike_brand(parsed.domain)
    if brand:
        flags.append("Lookalike domain detected")
    if CREDENTIAL_RE.search(combined):
        flags.append("Credential harvesting language")
    display = parsed.from_name or parsed.from_addr
    match = BRAND_DISPLAY_RE.search(display)
    if match:
        token = match.group(0).lower().replace(" ", "")
        if token and token not in parsed.domain.replace("-", ""):
            flags.append("Brand impersonation in display name")
    if re.search(r"dear (customer|user|member|client|valued)", combined, re.I) and (
        CREDENTIAL_RE.search(combined) or URGENCY_RE.search(combined)
    ):
        flags.append("Generic greeting with sensitive ask")
    if PAYMENT_RE.search(combined):
        flags.append("Request for payment / gift cards")
    if ATTACHMENT_RE.search(combined):
        flags.append("Suspicious attachment reference")
    if IP_URL_RE.search(combined):
        flags.append("IP-based URL in body")
    if parsed.html_body:
        parser = _LinkTextParser()
        try:
            parser.feed(parsed.html_body)
        except Exception:
            parser.pairs = []
        for text, href in parser.pairs:
            if text and href and "://" in href:
                host = re.sub(r"^https?://", "", href, flags=re.I).split("/")[0].lower()
                if text.lower() not in href.lower() and any(b in text.lower() for b in BRANDS):
                    if not any(b in host for b in BRANDS):
                        flags.append("Link display text does not match URL")
                        break
    for name in parsed.attachments:
        flags.append(f"Attachment listed: {name}")
    return list(dict.fromkeys(flags))


def classify_content(parsed: ParsedEmail) -> dict:
    rules = rule_based_signals(parsed)
    ml = predict_text(parsed.combined_text)
    content_flags = list(rules)
    if ml.get("available") and ml["label"] == "Phishing" and ml["confidence"] >= 70:
        content_flags.insert(0, f"ML classifier: phishing ({ml['confidence']}% confidence)")
    if not content_flags and ml["label"] == "Legitimate":
        content_flags = ["No content anomalies detected"]
    return {
        "content_flags": content_flags,
        "ml_label": ml["label"],
        "ml_confidence": ml["confidence"],
        "ml_p_phishing": ml.get("p_phishing", 0.5),
        "ml_available": bool(ml.get("available")),
        "ml_accuracy": ml.get("accuracy"),
    }


if __name__ == "__main__":
    stats = train_and_save()
    print(f"Trained TF-IDF + Logistic Regression  accuracy={stats['accuracy']:.3f}  "
          f"n_train={stats['n_train']} n_test={stats['n_test']}")
    print(f"Saved {stats['path']}")
