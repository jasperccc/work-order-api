from app.security import hash_password, verify_password


def test_hash_password_does_not_return_plaintext() -> None:
    password = "secret"
    password_hash = hash_password(password)

    assert password_hash != password


def test_verify_password_accepts_correct_password() -> None:
    password = "secret"
    password_hash = hash_password(password)
    is_valid = verify_password(password, password_hash)

    assert is_valid is True


def test_verify_password_rejects_incorrect_password() -> None:
    correct_password = "secret"
    wrong_password = "wrong-password"
    correct_password_hash = hash_password(correct_password)
    is_valid = verify_password(wrong_password, correct_password_hash)

    assert is_valid is False


def test_hash_password_uses_random_salt() -> None:
    password = "secret"
    first_password_hash = hash_password(password)
    second_password_hash = hash_password(password)

    assert first_password_hash != second_password_hash
