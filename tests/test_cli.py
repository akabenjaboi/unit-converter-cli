import re

import pytest

from unit_converter.cli import main

_ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;]*m")


def _strip_ansi(text: str) -> str:
    """Quita códigos de color ANSI que argparse (Python 3.13+) puede
    inyectar en la ayuda según la terminal/entorno."""
    return _ANSI_ESCAPE_RE.sub("", text)


def test_km2mi(capsys):
    code = main(["km2mi", "10"])
    captured = capsys.readouterr()
    assert code == 0
    assert captured.out == "10.00 km = 6.21 millas\n"


def test_mi2km(capsys):
    code = main(["mi2km", "10"])
    captured = capsys.readouterr()
    assert code == 0
    assert captured.out == "10.00 millas = 16.09 km\n"


def test_c2f(capsys):
    code = main(["c2f", "100"])
    captured = capsys.readouterr()
    assert code == 0
    assert captured.out == "100.00°C = 212.00°F\n"


def test_f2c(capsys):
    code = main(["f2c", "212"])
    captured = capsys.readouterr()
    assert code == 0
    assert captured.out == "212.00°F = 100.00°C\n"


def test_non_numeric_argument_exits_with_code_2():
    with pytest.raises(SystemExit) as exc_info:
        main(["km2mi", "no-es-un-numero"])
    assert exc_info.value.code == 2


def test_no_subcommand_exits_with_code_2():
    with pytest.raises(SystemExit) as exc_info:
        main([])
    assert exc_info.value.code == 2


def test_c2f_below_absolute_zero(capsys):
    code = main(["c2f", "-300"])
    captured = capsys.readouterr()
    assert code == 1
    assert "cero absoluto" in captured.err


def test_f2c_below_absolute_zero(capsys):
    code = main(["f2c", "-500"])
    captured = capsys.readouterr()
    assert code == 1
    assert "cero absoluto" in captured.err


# --- Casos de borde adicionales ---


def test_km2mi_negative_value(capsys):
    """Los km negativos no tienen restricción física y deben funcionar."""
    code = main(["km2mi", "-100"])
    captured = capsys.readouterr()
    assert code == 0
    assert captured.out == "-100.00 km = -62.14 millas\n"


def test_mi2km_negative_value(capsys):
    """Las millas negativas no tienen restricción física y deben funcionar."""
    code = main(["mi2km", "-100"])
    captured = capsys.readouterr()
    assert code == 0
    assert captured.out == "-100.00 millas = -160.93 km\n"


def test_c2f_below_absolute_zero_exact_message(capsys):
    """Verifica el mensaje exacto de error en stderr (no solo una subcadena)."""
    code = main(["c2f", "-300"])
    captured = capsys.readouterr()
    assert code == 1
    assert captured.err == "Error: temperatura por debajo del cero absoluto\n"
    assert captured.out == ""


def test_f2c_below_absolute_zero_exact_message(capsys):
    """Verifica el mensaje exacto de error en stderr (no solo una subcadena)."""
    code = main(["f2c", "-500"])
    captured = capsys.readouterr()
    assert code == 1
    assert captured.err == "Error: temperatura por debajo del cero absoluto\n"
    assert captured.out == ""


def test_c2f_at_absolute_zero_boundary_succeeds(capsys):
    """-273.15°C es exactamente el cero absoluto: debe aceptarse (código 0),
    no rechazarse. Debido a redondeo binario, el resultado interno es
    -459.66999999999996°F (ligeramente por encima del límite), por lo que
    la validación de cli.py no debería marcarlo como error."""
    code = main(["c2f", "-273.15"])
    captured = capsys.readouterr()
    assert code == 0
    assert captured.out == "-273.15°C = -459.67°F\n"
    assert captured.err == ""


def test_f2c_at_absolute_zero_boundary_succeeds(capsys):
    """-459.67°F es exactamente el cero absoluto: debe aceptarse (código 0)."""
    code = main(["f2c", "-459.67"])
    captured = capsys.readouterr()
    assert code == 0
    assert captured.out == "-459.67°F = -273.15°C\n"
    assert captured.err == ""


def test_c2f_just_below_absolute_zero_boundary_fails(capsys):
    """Un centésimo por debajo del cero absoluto debe seguir rechazándose."""
    code = main(["c2f", "-273.16"])
    captured = capsys.readouterr()
    assert code == 1
    assert captured.err == "Error: temperatura por debajo del cero absoluto\n"


def test_f2c_just_below_absolute_zero_boundary_fails(capsys):
    """Un centésimo por debajo del cero absoluto debe seguir rechazándose."""
    code = main(["f2c", "-459.68"])
    captured = capsys.readouterr()
    assert code == 1
    assert captured.err == "Error: temperatura por debajo del cero absoluto\n"


def test_rounding_edge_case_two_decimals(capsys):
    """2.005 no se representa exactamente en binario (es ligeramente menor
    a 2.005), por lo que :.2f redondea hacia abajo a 2.00 en vez de 2.01.
    Se documenta el comportamiento real, no el ingenuamente esperado."""
    code = main(["km2mi", "2.005"])
    captured = capsys.readouterr()
    assert code == 0
    assert captured.out == "2.00 km = 1.25 millas\n"


def test_help_flag_main_exits_zero(capsys):
    """--help debe salir con SystemExit(0), no debe tratarse como error."""
    with pytest.raises(SystemExit) as exc_info:
        main(["--help"])
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "usage:" in _strip_ansi(captured.out)
    assert captured.err == ""


def test_help_flag_subcommand_exits_zero(capsys):
    """km2mi --help también debe salir con SystemExit(0)."""
    with pytest.raises(SystemExit) as exc_info:
        main(["km2mi", "--help"])
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "usage: unit-convert km2mi" in _strip_ansi(captured.out)
    assert captured.err == ""


def test_invalid_subcommand_exits_with_code_2():
    with pytest.raises(SystemExit) as exc_info:
        main(["km2millas", "10"])
    assert exc_info.value.code == 2
