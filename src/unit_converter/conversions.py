"""Funciones puras de conversión de unidades."""

KM_PER_MILE = 1.609344
LITERS_PER_GALLON = 3.785411784


def km_to_miles(km: float) -> float:
    """Convierte kilómetros a millas."""
    return km / KM_PER_MILE


def miles_to_km(miles: float) -> float:
    """Convierte millas a kilómetros."""
    return miles * KM_PER_MILE


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convierte grados Celsius a grados Fahrenheit."""
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convierte grados Fahrenheit a grados Celsius."""
    return (fahrenheit - 32) * 5 / 9


def liters_to_gallons(liters: float) -> float:
    """Convierte litros a galones."""
    return liters / LITERS_PER_GALLON


def gallons_to_liters(gallons: float) -> float:
    """Convierte galones a litros."""
    return gallons * LITERS_PER_GALLON
