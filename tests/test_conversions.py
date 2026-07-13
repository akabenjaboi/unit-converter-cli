import pytest

from unit_converter.conversions import (
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    km_to_miles,
    miles_to_km,
)


def test_celsius_to_fahrenheit_zero():
    assert celsius_to_fahrenheit(0) == 32


def test_celsius_to_fahrenheit_boiling():
    assert celsius_to_fahrenheit(100) == 212


def test_celsius_to_fahrenheit_minus_forty():
    assert celsius_to_fahrenheit(-40) == -40


def test_fahrenheit_to_celsius_zero():
    assert fahrenheit_to_celsius(32) == 0


def test_fahrenheit_to_celsius_boiling():
    assert fahrenheit_to_celsius(212) == 100


def test_fahrenheit_to_celsius_minus_forty():
    assert fahrenheit_to_celsius(-40) == -40


def test_km_to_miles_zero():
    assert km_to_miles(0) == 0


def test_miles_to_km_zero():
    assert miles_to_km(0) == 0


def test_km_miles_roundtrip():
    original = 42.0
    assert miles_to_km(km_to_miles(original)) == pytest.approx(original)


def test_celsius_fahrenheit_roundtrip():
    original = 36.6
    assert fahrenheit_to_celsius(celsius_to_fahrenheit(original)) == pytest.approx(
        original
    )


# --- Casos de borde adicionales ---


def test_km_to_miles_negative_value():
    """Los km negativos no tienen restricción física: deben convertirse igual."""
    assert km_to_miles(-100) == pytest.approx(-62.13711922373339)


def test_miles_to_km_negative_value():
    """Las millas negativas no tienen restricción física: deben convertirse igual."""
    assert miles_to_km(-100) == pytest.approx(-160.9344)


@pytest.mark.parametrize("original", [-100.0, -0.001, 0.0, 0.001, 42.0, 123456.789])
def test_km_miles_roundtrip_parametrized(original):
    assert miles_to_km(km_to_miles(original)) == pytest.approx(original)
    assert km_to_miles(miles_to_km(original)) == pytest.approx(original)


@pytest.mark.parametrize(
    "original", [-273.15, -40.0, -0.001, 0.0, 0.001, 36.6, 100.0, 1000.0]
)
def test_celsius_fahrenheit_roundtrip_parametrized(original):
    assert fahrenheit_to_celsius(celsius_to_fahrenheit(original)) == pytest.approx(
        original
    )
    assert celsius_to_fahrenheit(fahrenheit_to_celsius(original)) == pytest.approx(
        original
    )


def test_celsius_to_fahrenheit_absolute_zero_has_float_rounding_error():
    """Documenta que -273.15°C no produce exactamente -459.67°F por la
    representación binaria de floats: el resultado real es
    -459.66999999999996, ligeramente por encima de -459.67. Esto es
    relevante porque cli.py compara el resultado contra ABSOLUTE_ZERO_F."""
    resultado = celsius_to_fahrenheit(-273.15)
    assert resultado != -459.67
    assert resultado == pytest.approx(-459.67)
    assert resultado > -459.67


def test_km_to_miles_large_value_precision():
    original = 1_000_000.0
    assert km_to_miles(original) == pytest.approx(621371.1922373339)
