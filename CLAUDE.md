# Datatón de práctica: fraude en billetera digital

Esta carpeta es un ejercicio de aprendizaje con meta de efectividad. La persona que trabaja contigo quiere hacer data science rápido y sencillo, sin programar: tú escribes y ejecutas el código. Lo que ella quiere aprender es el **criterio**: por qué se elige cada columna, cada algoritmo y cada umbral, para poder explicarlo y para poder mejorar el resultado cuando el modelo se estanca.

## Lo que ella quiere aprender (el corazón)

- En datatones anteriores el resultado fue mediocre y no supo explicar ni mejorar las decisiones, porque las tomaba Claude sin que ella entendiera el criterio. Esta práctica es para cambiar eso.
- No le importa de dónde salga el criterio: **díselo directo**. Lo que importa es que lo entienda y lo pueda comprobar.
- Orange es su lupa: ella comprueba ahí lo que tú afirmas. Python es la fábrica: unir tablas, calcular historial, validar, entrenar y entregar.
- La métrica que manda son los **soles**: a más monto, más prioridad.

## Reglas

1. **No abras, leas ni listes nada dentro de `NO_ABRIR/`.** Ahí está la respuesta. Solo se usa de forma indirecta con `python calificar.py predicciones.csv`, y solo cuando la persona lo pida. Máximo 3 calificaciones en toda la práctica.
2. **No actúes sin su permiso.** Primero explica qué vas a hacer y por qué; ejecuta recién cuando diga que sí.
3. **Dile el criterio directo, sin esconder nada.** Si ves un problema en los datos, una columna peligrosa, el algoritmo que conviene o el umbral que sirve, dilo con su evidencia. Recomienda una opción y menciona la alternativa con su ventaja y su costo.
4. **Cada decisión viene con cuatro cosas:** qué se hizo, por qué (la evidencia), cómo comprobarlo ella en Orange (qué widget, qué columna, qué buscar) y, si es un algoritmo o umbral, en qué se basa y por qué ese y no otro.
5. **Explica cada resultado en 5 líneas o menos:** qué significa el número o la gráfica y qué decisión permite tomar.
6. **Las diferencias pequeñas son empate.** Cuando compares opciones usa la misma partición y la misma métrica, y repite con 3 semillas antes de declarar un ganador.
7. Guarda las gráficas como PNG en `graficas/` y el código por misión (`mision_1_explorar.py`, `mision_2_limpiar.py`, ...), con comentarios breves en español. Los CSV para Orange son locales y no se suben al repo.
8. Anota cada decisión y su motivo en `decisiones.md`, escrito para que ella lo pueda explicar en voz alta.

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

Sus apuntes, con las dudas ya resueltas, las decisiones pendientes y las preguntas que aún tiene abiertas, están en `CONTEXTO.md`. Úsalos para no repetir explicaciones y para retomar esas preguntas cuando toque. Ya no hace falta guardar sus respuestas: si una pregunta pendiente se resuelve, explícala y anota la conclusión.

@CONTEXTO.md

## Entrega

`predicciones.csv` con una fila por cada operación de junio:

- `id_tx`
- `score`: más alto = más sospechosa
- `prioridad` (opcional): el número con el que se ordenan las 300 alertas; si falta, se usa `score`
