"""Interfaz de línea de comandos para unit_converter."""

import argparse
import sys

from unit_converter.conversions import (
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    gallons_to_liters,
    km_to_miles,
    liters_to_gallons,
    miles_to_km,
)

ABSOLUTE_ZERO_C = -273.15
ABSOLUTE_ZERO_F = -459.67

ERROR_ABSOLUTE_ZERO = "Error: temperatura por debajo del cero absoluto"


def _below_absolute_zero(celsius: float, fahrenheit: float) -> bool:
    return celsius < ABSOLUTE_ZERO_C or fahrenheit < ABSOLUTE_ZERO_F


def build_parser() -> argparse.ArgumentParser:
    """Construye el parser de argumentos con sus 6 subcomandos."""
    parser = argparse.ArgumentParser(
        prog="unit-convert",
        description="Convierte unidades de distancia, temperatura y volumen.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    km2mi = subparsers.add_parser("km2mi", help="Kilómetros a millas")
    km2mi.add_argument("valor", type=float)

    mi2km = subparsers.add_parser("mi2km", help="Millas a kilómetros")
    mi2km.add_argument("valor", type=float)

    c2f = subparsers.add_parser("c2f", help="Celsius a Fahrenheit")
    c2f.add_argument("valor", type=float)

    f2c = subparsers.add_parser("f2c", help="Fahrenheit a Celsius")
    f2c.add_argument("valor", type=float)

    l2gal = subparsers.add_parser("l2gal", help="Litros a galones")
    l2gal.add_argument("valor", type=float)

    gal2l = subparsers.add_parser("gal2l", help="Galones a litros")
    gal2l.add_argument("valor", type=float)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Punto de entrada de la CLI. Retorna el código de salida."""
    parser = build_parser()
    args = parser.parse_args(argv)
    valor = args.valor

    if args.command == "km2mi":
        resultado = km_to_miles(valor)
        print(f"{valor:.2f} km = {resultado:.2f} millas")
        return 0

    if args.command == "mi2km":
        resultado = miles_to_km(valor)
        print(f"{valor:.2f} millas = {resultado:.2f} km")
        return 0

    if args.command == "c2f":
        resultado = celsius_to_fahrenheit(valor)
        if _below_absolute_zero(valor, resultado):
            print(ERROR_ABSOLUTE_ZERO, file=sys.stderr)
            return 1
        print(f"{valor:.2f}°C = {resultado:.2f}°F")
        return 0

    if args.command == "f2c":
        resultado = fahrenheit_to_celsius(valor)
        if _below_absolute_zero(resultado, valor):
            print(ERROR_ABSOLUTE_ZERO, file=sys.stderr)
            return 1
        print(f"{valor:.2f}°F = {resultado:.2f}°C")
        return 0

    if args.command == "l2gal":
        resultado = liters_to_gallons(valor)
        print(f"{valor:.2f} litros = {resultado:.2f} galones")
        return 0

    if args.command == "gal2l":
        resultado = gallons_to_liters(valor)
        print(f"{valor:.2f} galones = {resultado:.2f} litros")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
