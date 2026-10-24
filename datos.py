# Lee las tablas del reto desde Supabase (esquema "billetera") por la API REST.
# Usa SUPABASE_URL y SUPABASE_KEY (clave pública, solo lectura) de .env.
# Uso en cualquier misión:
#   from datos import cargar
#   tx = cargar("transacciones")
import os

import pandas as pd
import requests

aqui = os.path.dirname(os.path.abspath(__file__))

# Lee .env si existe (no se sube al repo)
ruta_env = os.path.join(aqui, ".env")
if os.path.exists(ruta_env):
    for linea in open(ruta_env, encoding="utf-8"):
        if "=" in linea and not linea.startswith("#"):
            k, v = linea.strip().split("=", 1)
            os.environ.setdefault(k, v)

TABLAS = ("usuarios", "transacciones", "fraudes_confirmados")
PAGINA = 1000  # máximo de filas que Supabase entrega por pedido
# Columnas que en la base son fecha y se devuelven como datetime
FECHAS = {"transacciones": ["fecha_hora"], "fraudes_confirmados": ["fecha_reclamo"]}


def cargar(tabla):
    """Devuelve la tabla completa como DataFrame, sin la columna de carga 'fila'."""
    if tabla not in TABLAS:
        raise ValueError(f"Tabla desconocida: {tabla}. Opciones: {TABLAS}")
    url = f"{os.environ['SUPABASE_URL'].rstrip('/')}/rest/v1/{tabla}"
    key = os.environ["SUPABASE_KEY"]
    cabeceras = {"apikey": key, "Authorization": f"Bearer {key}", "Accept-Profile": "billetera"}

    filas, desde = [], 0
    with requests.Session() as s:
        while True:
            r = s.get(url, headers={**cabeceras, "Range": f"{desde}-{desde + PAGINA - 1}"},
                      params={"select": "*", "order": "fila"}, timeout=60)
            r.raise_for_status()
            lote = r.json()
            filas.extend(lote)
            if len(lote) < PAGINA:
                break
            desde += PAGINA

    df = pd.DataFrame(filas).drop(columns="fila")
    for col in FECHAS.get(tabla, []):
        df[col] = pd.to_datetime(df[col])
    return df


if __name__ == "__main__":
    for t in TABLAS:
        print(t, cargar(t).shape)
