from enterprise_data_agent.tools.pii_guard import scan_and_mask_pii


def test_pii_guard_detects_and_masks_sensitive_data():
    raw_payload = (
        "Customer John Doe with email john.doe@enterprise.com and "
        "credit card 4532-1234-5678-9010 requested account deletion."
    )

    result = scan_and_mask_pii(raw_payload)

    assert result.has_pii is True
    assert result.entities_count == 2  # Email and Credit Card
    assert "john.doe@enterprise.com" not in result.sanitized_text
    assert "4532-1234-5678-9010" not in result.sanitized_text
    assert "[EMAIL REDACTED]" in result.sanitized_text
    assert "[CARD REDACTED]" in result.sanitized_text


def test_pii_guard_clean_text_remains_unchanged():
    clean_payload = "System health check normal. Latency P99 is 12 ms."

    result = scan_and_mask_pii(clean_payload)

    assert result.has_pii is False
    assert result.entities_count == 0
    assert result.sanitized_text == clean_payload
