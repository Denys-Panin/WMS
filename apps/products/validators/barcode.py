from django.core.exceptions import ValidationError


def _validate_gtin(
    value: str,
    *,
    expected_length: int,
    barcode_name: str,
) -> None:
    if len(value) != expected_length or not value.isascii() or not value.isdecimal():
        raise ValidationError(
            f"{barcode_name} must contain exactly {expected_length} ASCII digits."
        )

    digits = [int(digit) for digit in value]

    total = sum(
        digit * (3 if index % 2 == 0 else 1)
        for index, digit in enumerate(reversed(digits[:-1]))
    )

    check_digit = (10 - (total % 10)) % 10

    if digits[-1] != check_digit:
        raise ValidationError(f"Invalid {barcode_name} check digit.")


def validate_ean13(value: str) -> None:
    _validate_gtin(
        value,
        expected_length=13,
        barcode_name="EAN-13",
    )


def validate_upca(value: str) -> None:
    _validate_gtin(
        value,
        expected_length=12,
        barcode_name="UPC-A",
    )
