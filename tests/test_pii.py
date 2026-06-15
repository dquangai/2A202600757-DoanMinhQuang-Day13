from app.pii import hash_user_id, scrub_text, scrub_value


def test_scrub_email() -> None:
    out = scrub_text("Email me at student@vinuni.edu.vn")
    assert "student@" not in out
    assert "REDACTED_EMAIL" in out


def test_scrub_common_sensitive_fields() -> None:
    text = (
        "Phone 0987654321, CCCD 001234567890, card 4111 1111 1111 1111, "
        "passport B1234567, address số 12 đường Lê Lợi"
    )
    out = scrub_text(text)
    assert "0987654321" not in out
    assert "001234567890" not in out
    assert "4111" not in out
    assert "B1234567" not in out
    assert "đường" not in out.lower()


def test_scrub_nested_values() -> None:
    out = scrub_value({"payload": {"items": ["student@vinuni.edu.vn", {"card": "4111-1111-1111-1111"}]}})
    assert out == {
        "payload": {
            "items": ["[REDACTED_EMAIL]", {"card": "[REDACTED_CREDIT_CARD]"}],
        }
    }


def test_hash_user_id_is_stable_and_not_raw() -> None:
    first = hash_user_id("u01")
    assert first == hash_user_id("u01")
    assert first != "u01"
    assert len(first) == 12
