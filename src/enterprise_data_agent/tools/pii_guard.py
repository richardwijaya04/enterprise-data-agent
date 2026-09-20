import re

from enterprise_data_agent.core.models import PIIEntity, PIIScanResult

EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")
CARD_PATTERN = re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b")
PHONE_PATTERN = re.compile(
    r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
)


def scan_and_mask_pii(text: str) -> PIIScanResult:
    """Scans the input text for PII entities and masks them."""
    detected: list[PIIEntity] = []
    sanitized = text

    # Scan for credit card numbers
    for match in CARD_PATTERN.finditer(text):
        original = match.group()
        masked = "[CARD REDACTED]"
        detected.append(
            PIIEntity(
                entity_type="Credit Card", original_value=original, masked_value=masked
            )
        )
        sanitized = sanitized.replace(original, masked)

    # Scan for email addresses
    for match in EMAIL_PATTERN.finditer(text):
        original = match.group()
        masked = "[EMAIL REDACTED]"
        detected.append(
            PIIEntity(
                entity_type="EMAIL_ADDRESS",
                original_value=original,
                masked_value=masked,
            )
        )
        sanitized = sanitized.replace(original, masked)

    return PIIScanResult(
        has_pii=len(detected) > 0,
        entities_count=len(detected),
        detected_entities=detected,
        sanitized_text=sanitized,
    )
