# Bases del reto: fraude en una billetera digital

Datos ficticios, creados para practicar. Ninguna persona, cuenta u operación es real.

## Contexto

Una billetera digital de Lima tiene unas 5,800 cuentas. Entre enero y junio de 2026 registró cerca de 174,000 operaciones. Los reclamos por fraude vienen subiendo y el equipo de revisión no alcanza a mirar todo.

## Objetivo

Para cada operación de **junio de 2026**, entregar un puntaje de sospecha. El equipo de revisión solo puede revisar **300 operaciones** de junio.

## Qué se entrega

- Todas las operaciones de enero a junio de 2026.
- Los reclamos por fraude confirmados de enero a mayo. Los de junio no se entregan: son lo que hay que predecir.
- La tabla de usuarios.

## Cómo se evalúa

1. Principal: soles protegidos, es decir, la suma de los montos de los fraudes reales que caen dentro de tus 300 alertas.
2. Secundarias: número de fraudes atrapados en las 300 alertas y PR-AUC del puntaje.

## Lo que dice el área de fraude

1. "Vemos dos modalidades: cuentas tomadas por un tercero, y clientes engañados que transfieren por voluntad propia."
2. "El dinero casi siempre termina en cuentas que lo retiran rápido."
3. "No todos los clientes reclaman."
4. "Los reclamos pueden llegar hasta 25 días después de la operación."
5. "La app no permite operaciones mayores a S/ 4,500."
6. "El modelo se usará en el instante de la operación: solo puede usar lo que se sabe hasta ese momento."
7. "Quien revisa necesita entender por qué se marcó cada operación."

## Diccionario de datos

### transacciones.csv

| Columna | Descripción |
| --- | --- |
| id_tx | Identificador de la operación |
| fecha_hora | Fecha y hora de la operación |
| id_emisor | Cuenta que envía el dinero |
| id_receptor | Cuenta que lo recibe; `BANCO` cuando es un retiro a cuenta bancaria |
| tipo | `p2p` (entre cuentas), `pago_comercio`, `retiro_banco` |
| monto | Monto en soles |
| canal | `app` o `web` |
| dispositivo_id | Equipo desde el que se hizo la operación |
| distrito_tx | Distrito desde donde se hizo |
| mensaje | Texto opcional que escribe el emisor |
| fue_revertida | 1 si la operación fue revertida a favor del emisor |

### usuarios.csv

| Columna | Descripción |
| --- | --- |
| id_usuario | Identificador de la cuenta |
| fecha_registro | Fecha de creación de la cuenta |
| tipo_cuenta | `personal` o `negocio` |
| nivel_verificacion | `basico` o `completo` |
| edad | Edad del titular |
| distrito | Distrito de residencia |
| sistema_operativo | `android` o `ios` |
| n_contactos_soporte_2026 | Contactos con soporte en 2026, con corte al 31 de mayo |

### fraudes_confirmados.csv

| Columna | Descripción |
| --- | --- |
| id_tx | Operación reclamada y confirmada como fraude (enero a mayo) |
| fecha_reclamo | Fecha en que el cliente reclamó |
| motivo_reclamo | "no reconozco la operacion" o "fui enganado" |

## Formato de entrega

`predicciones.csv` con una fila por cada operación de junio: `id_tx`, `score` (más alto = más sospechosa) y, opcional, `prioridad` (orden de las 300 alertas).

Para calificar: `python calificar.py predicciones.csv`
