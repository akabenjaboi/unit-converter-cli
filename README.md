# unit-converter-cli

CLI simple para convertir unidades de distancia (kilómetros / millas),
temperatura (Celsius / Fahrenheit) y volumen (litros / galones). Escrito en
Python puro, sin dependencias en tiempo de ejecución.

## Requisitos

- Python 3.11+

## Instalación

Crea un entorno virtual e instala el paquete en modo editable junto con las
dependencias de desarrollo (`black`, `ruff`, `pytest`).

### PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

### bash

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Uso

El comando instalado es `unit-convert`, con 6 subcomandos: `km2mi`, `mi2km`,
`c2f`, `f2c`, `l2gal` y `gal2l`.

```console
$ unit-convert km2mi 10
10.00 km = 6.21 millas

$ unit-convert mi2km 10
10.00 millas = 16.09 km

$ unit-convert c2f 100
100.00°C = 212.00°F

$ unit-convert f2c 212
212.00°F = 100.00°C

$ unit-convert l2gal 10
10.00 litros = 2.64 galones

$ unit-convert gal2l 10
10.00 galones = 37.85 litros
```

Si el valor de temperatura ingresado (o el resultado) está por debajo del
cero absoluto (-273.15°C / -459.67°F), el comando falla:

```console
$ unit-convert c2f -300
Error: temperatura por debajo del cero absoluto
$ echo $?
1
```

## Desarrollo

```bash
black .
ruff check .
pytest -q
```
