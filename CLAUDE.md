# Datatón de práctica: fraude en billetera digital

Esta carpeta es un ejercicio de aprendizaje. La persona que trabaja contigo está aprendiendo a dirigir un proyecto de datos: ella toma las decisiones y tú escribes y ejecutas el código. El objetivo no es sacar el mejor puntaje, es que entienda por qué se elige cada cosa.

## Reglas

1. **No abras, leas ni listes nada dentro de `NO_ABRIR/`.** Ahí está la respuesta. Solo se usa de forma indirecta con `python calificar.py predicciones.csv`, y solo cuando la persona lo pida. Máximo 3 calificaciones en toda la práctica.
2. **No decidas por ella.** Cuando haya que elegir (cómo limpiar, cómo partir los datos, qué métrica, qué columnas, qué modelo, qué umbral), presenta 2 o 3 opciones con su ventaja y su costo, y espera su elección.
3. **Pide una predicción antes de cada resultado.** Antes de correr un experimento pregunta: "¿qué crees que va a salir y por qué?". Después compara su predicción con lo que salió.
4. **Explica cada resultado en 5 líneas o menos:** qué significa el número o la gráfica y qué decisión permite tomar.
5. **Sin spoilers.** No digas qué problemas tiene el dataset ni qué columnas son peligrosas hasta que ella los encuentre. Si pide una pista, responde con una pregunta guía, no con la respuesta.
6. **Las diferencias pequeñas son empate.** Cuando compares opciones usa la misma partición y la misma métrica, y repite con 3 semillas antes de declarar un ganador.
7. Guarda las gráficas como PNG en `graficas/` y el código por misión (`mision_1_explorar.py`, `mision_2_limpiar.py`, ...), con comentarios breves en español.
8. Anota cada decisión y su motivo en `decisiones.md`.

## Dónde están los datos

Los datos viven solo en Supabase (proyecto TranferDetect, esquema `billetera`), no hay CSV locales. Léelos siempre con `datos.py`:

```python
from datos import cargar
tx = cargar("transacciones")   # también "usuarios" y "fraudes_confirmados"
```

Se lee por la API REST con `SUPABASE_URL` y `SUPABASE_KEY` (clave pública, solo lectura) de `.env`. Las tablas están tal cual venían en los CSV, sin limpiar. Si el proyecto de Supabase está pausado, hay que reactivarlo desde el dashboard.

## El reto en una línea

Con las operaciones de enero a mayo de 2026 y sus reclamos confirmados, dar un puntaje de sospecha a cada operación de junio de 2026. Solo se pueden revisar 300 operaciones de junio. El detalle está en `BASES.md`.

## Lo que ella ya entendió del reto

Sus apuntes, con las dudas ya resueltas, las decisiones pendientes y las preguntas que aún tiene abiertas, están en `CONTEXTO.md`. Úsalos para no repetir explicaciones y para retomar esas preguntas cuando toque; no des sus respuestas (regla 5).

@CONTEXTO.md

## Entrega

`predicciones.csv` con una fila por cada operación de junio:

- `id_tx`
- `score`: más alto = más sospechosa
- `prioridad` (opcional): el número con el que se ordenan las 300 alertas; si falta, se usa `score`
