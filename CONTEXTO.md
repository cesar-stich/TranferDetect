# Apuntes del reto: fraude en billetera digital

## 0. De qué trata el reto

Una billetera digital tiene operaciones de enero a junio de 2026. Para algunas de enero a mayo se sabe que fueron fraude, porque el cliente reclamó y la empresa lo confirmó. Para junio no se sabe nada.

Tu trabajo es dar a cada operación de junio un **puntaje de sospecha**: más alto significa más probable que sea fraude. El equipo solo puede revisar **300** operaciones, así que las 300 con mayor puntaje son tus alertas.

**Tú no "confirmas" fraudes.** Confirmar lo hace la empresa cuando el cliente reclama. Tú solo das un puntaje de sospecha.

## 1. Cómo funciona el fraude

### Las dos modalidades

**Tipo 1: cuenta tomada por un tercero.** Un delincuente consigue entrar a la cuenta de otra persona, porque le robó la clave o el celular, y transfiere el dinero. El dueño no hizo la operación; por eso su reclamo dice **"no reconozco la operación"**.

**Tipo 2: cliente engañado.** El propio cliente hace la transferencia desde su celular, porque alguien lo estafó: un premio falso, una inversión, un "trámite urgente". La operación la hizo él, pero bajo engaño; su reclamo dice **"fui engañado"**.

| | Tipo 1: cuenta tomada | Tipo 2: cliente engañado |
|---|---|---|
| Quién hace la operación | El delincuente | El propio cliente, bajo engaño |
| Cómo | Con la clave o el celular robados | Desde su propio celular |
| Motivo del reclamo | "no reconozco la operación" | "fui engañado" |

### La ruta del dinero

El fraude no termina cuando le quitan el dinero a la víctima. Mientras ese dinero siga dentro de la billetera, la empresa todavía puede **congelarlo o revertir la operación**. Por eso el estafador necesita sacarlo, y lo hace en dos pasos:

1. La víctima, o su cuenta tomada, envía el dinero a una cuenta que controla el estafador o un cómplice.
2. Esa cuenta lo **retira casi de inmediato a un banco**, donde la billetera ya no puede recuperarlo.

## 2. Los datos y para qué sirve cada periodo

Tienes tres tablas: `transacciones`, `fraudes_confirmados` y `usuarios`.

**`transacciones`** trae **todas** las operaciones de enero a junio en un solo archivo, sin separar. Ahí están mezcladas las normales y las fraudulentas.

**`fraudes_confirmados`** no trae operaciones nuevas ni es un historial aparte. Es solo una lista de `id_tx` que apuntan a filas que ya están en `transacciones`. Es decir, los fraudes confirmados son operaciones de la misma data.

**No hay una columna que diga "esto es junio".** Lo que distingue los periodos es la columna `fecha_hora`: las de junio son las que tienen fecha de junio de 2026. Separarlas te toca a ti, y es una de las primeras cosas que le dictarás a quien escriba el código.

| Periodo | ¿Está en `transacciones`? | ¿Tienes sus fraudes confirmados? | Para qué sirve | ¿Entra en la entrega? |
|---|---|---|---|---|
| Enero a mayo | Sí | Sí, los que se reclamaron | Aprender cómo se ve un fraude | No |
| Junio | Sí | No, eso es lo que debes predecir | Aplicar lo aprendido y entregar el puntaje | Sí: las 300 alertas salen de aquí |

### La idea del examen

- **Enero a mayo** son los **ejercicios resueltos**: ya sabes cuáles fueron fraude confirmado.
- **Junio** es el **examen**: operaciones sin respuesta.
- **Las 300** son tus **respuestas**: la lista que se manda a revisión con las operaciones más probables de ser fraude.

### Enero a mayo se usa completo, no solo los fraudes

Las operaciones de enero a mayo que **no** son fraude confirmado **no sobran**. El modelo aprende **comparando**: para saber qué tiene de especial un fraude, necesita ver también cómo es una operación normal.

| Lo que ve el modelo | Lo que aprende |
|---|---|
| Solo fraudes | "Los fraudes tienen montos, horas, receptores...", pero no sabe si eso es especial o si **todas** las operaciones son así |
| Fraudes + normales | "Los fraudes se **diferencian** de las normales en esto." Esa diferencia es lo que luego busca en junio |

Por ejemplo: si todos los fraudes se hicieron desde la app, ¿eso es una señal? Si el 99% de las normales también son por app, no dice nada. Eso solo lo sabes si miras las normales.

Las operaciones de enero a mayo sirven para dos cosas:

1. **Entrenar:** son los ejemplos de fraude y de normal.
2. **Historial:** para puntuar una operación de junio puedes usar lo que esa cuenta o ese receptor hizo antes.

### ¿Y si uso solo junio?

Se puede técnicamente, pero solo podrías buscar lo **raro**, y **raro no es lo mismo que fraude**: alguien que paga su alquiler una vez al año es raro y no es fraude. Además estarías dejando de lado los únicos ejemplos reales de fraude que tienes.

## 3. La lista de fraudes está incompleta

Un fraude solo entra a `fraudes_confirmados` si pasan **dos cosas**:

1. el cliente reclama, **y**
2. la empresa lo confirma.

Si el cliente nunca reclama, el fraude existió igual, pero en los datos esa operación se ve como una normal. Por eso la tabla de fraudes está incompleta.

Dentro de enero a mayo, cada operación cae en uno de estos dos casos:

| Caso | Qué significa |
|---|---|
| Su `id_tx` **aparece** en fraudes confirmados | **Seguro** fue fraude, reclamado y confirmado |
| Su `id_tx` **no aparece** | Casi siempre fue normal, pero puede ser un fraude no confirmado. **Desde los datos no puedes distinguir cuál de las dos** |

Hay dos grupos de fraudes escondidos entre las "normales":

**a) Reclamados pero aún no confirmados.** En la vida real existen, pero en tus datos no hay forma de verlos: el archivo solo trae los ya confirmados y no hay una columna de "reclamo en trámite". Para ti son invisibles y se ven igual que una operación normal, así que no puedes usarlos como "sospechosos principales". Esta idea se relaciona con la frase 4 de las bases: los reclamos pueden tardar **hasta 25 días** en llegar.

> **Pregunta:** si una operación ocurrió a fines de mayo, ¿ya habrá llegado su reclamo cuando se armó el archivo?

**b) Fraudes que nadie reclamó.** Existen, como dice la frase 3 de las bases ("no todos los clientes reclaman"), y están escondidos entre las "normales".

### Qué significa esto para el entrenamiento

- Al entrenar, le estás diciendo al modelo que algunos fraudes son "normales". A eso se le llama **ruido en las etiquetas**. Complica un poco el entrenamiento, pero no lo vuelve imposible: los confirmados son ejemplos seguros y las "normales" son casi todas normales de verdad. En la vida real casi siempre es así.
- **Detectar los fraudes escondidos de enero a mayo no es obligatorio.** No dan puntos, porque la entrega es solo de junio. El modelo aprende igual, un poco peor.
- Hacer algo con ellos es una **mejora opcional**, que se decide después de explorar los datos (ver sección 7).

## 4. La regla del tiempo: solo se usa el pasado de cada operación

El modelo se usará **en el instante de la operación**, así que solo puede usar lo que ya se sabía en ese segundo.

### "Tiempo real" es una regla de datos, no un sistema que haya que construir

La frase de las bases no te pide montar un flujo en vivo. Te pide que **cada operación se puntúe como si estuvieras en ese segundo**, sin mirar nada de después.

Todos los datos de junio ya están en la tabla. Se "simula" el tiempo real calculando los datos de cada operación **mirando solo hacia atrás**:

```
Operación del 10 de junio, 15:00
  ✅ lo que hizo esa cuenta antes del 10 de junio, 15:00
  ❌ lo que pasó después (aunque esté en la tabla)
```

Eso se hace para todas las filas a la vez, en un solo script. El resultado es como si el modelo hubiera estado funcionando en vivo durante junio.

Hay dos maneras de romper esta regla sin darte cuenta:

### Trampa 1: usar las filas que vienen después

`transacciones` está completo de enero a junio. Si estás puntuando una operación del 10 de junio, las del 11, 12 y 13 de junio están ahí mismo, unas filas más abajo. Nada te impide mirarlas, pero en el instante real **todavía no existían**.

Un ejemplo con la frase 2 de las bases ("el dinero termina en cuentas que lo retiran rápido"): ese retiro ocurre **después** de la operación fraudulenta. Si calculas "¿el receptor retiró la plata una hora después?", estás usando el futuro, aunque el dato venga de tu propio archivo y no de las respuestas.

### Trampa 2: usar columnas que se llenan después

Algunas columnas describen la operación en el momento en que se hizo, como el monto, el canal o la hora. Otras pueden registrar algo que pasó más tarde y que alguien anotó luego en la misma fila. Se ven como un dato más, pero son futuro. Cuáles son te toca encontrarlo a ti.

> **Pregunta guía:** recorre el diccionario columna por columna y pregúntate: "¿este valor ya existía en el segundo en que se apretó enviar?".

### El receptor sí se puede usar

Quién recibe el dinero es parte de la operación misma: está en la columna `id_receptor` de esa fila y se sabe en el instante. Lo que cambia es **de qué momento** es la información sobre él:

| Sobre el receptor | ¿Vale? |
|---|---|
| Quién es | Sí |
| Todo lo que hizo **antes** de esa operación | Sí |
| Lo que hizo **después** (por ejemplo, retirar la plata) | No |

### La regla aplica a todas las filas, también a las de entrenamiento

- Un dato del 17 de junio para una operación del 10 de junio: **no vale**.
- Un dato del 17 de febrero depende de para qué operación lo uses:
  - para una operación de junio, **sí vale**, porque es pasado;
  - para una operación del 10 de febrero, **no vale**, aunque sea un mes "de entrenamiento".

**¿Por qué?** El modelo tiene que aprender en las mismas condiciones en que luego va a trabajar. Si en febrero le dejas ver lo que pasó una semana después, aprende a apoyarse en esa pista. Cuando llegue a junio, esa pista no estará y fallará.

> **Pregunta:** si una cuenta ya tuvo un fraude confirmado antes, ¿desde qué fecha "se sabe" eso: desde el día de la operación o desde el día del reclamo?

## 5. Qué se entrega y cómo se califica

### Operaciones, no cuentas

**El fraude se marca por operación, no por cuenta.** Cada operación tiene su propio `id_tx`, su propia etiqueta y, en junio, su propio puntaje.

Entregas `predicciones.csv` con un puntaje para **todas** las operaciones de junio, no solo las 300:

- `id_tx`
- `score`: más alto = más sospechosa
- `prioridad` (opcional): el orden de las 300 alertas; si falta, se usa `score`

Las 300 con mayor puntaje son tus alertas. La lista es de **300 operaciones, no de 300 cuentas**, y en ninguna parte de la entrega aparece una cuenta.

Una misma cuenta sí puede aparecer varias veces dentro de esas 300, porque cada una de sus operaciones es una fila distinta. Tres fraudes en la misma cuenta son tres filas, y cada una suma sus propios soles si resulta ser fraude:

| id_tx | Emisor | Monto | ¿Entra en las 300? |
|---|---|---|---|
| T-A | Cuenta X | S/ 900 | Sí |
| T-B | Cuenta X | S/ 1,200 | Sí |
| T-C | Cuenta X | S/ 40 | Puede que no |

Aquí la Cuenta X ocupa dos de tus 300 cupos. La tercera operación puede quedar fuera aunque sea de la misma cuenta, porque se puntúa por separado.

### Cómo se mide la efectividad

Se corre:

```bash
python calificar.py predicciones.csv
```

El script toma tus 300 primeras y las compara con los fraudes reales de junio, que están escondidos. Devuelve tres números:

| Métrica | Qué mide | Peso |
|---|---|---|
| **Soles protegidos** | La suma de los montos de los fraudes reales que cayeron en tus 300 | **Principal** |
| Fraudes atrapados | Cuántos fraudes reales hay en tus 300 | Secundaria |
| PR-AUC | Qué tan bien ordena tu puntaje a **todas** las operaciones de junio, no solo las 300 | Secundaria |

Por ejemplo: si en tus 300 caen 40 fraudes reales que suman S/ 60,000, protegiste S/ 60,000. Las otras 260 alertas fueron falsas alarmas.

Atrapar un fraude de S/ 4,000 vale más que atrapar diez de S/ 20, porque la métrica principal son **soles**, no cantidad de fraudes.

**Dos detalles importantes:**

1. **El puntaje de todas las operaciones importa.** El PR-AUC mira todo el orden, así que las que quedan fuera de las 300 también se califican.
2. **Solo se puede calificar 3 veces en toda la práctica.** No sirve para probar cada idea. Se usa cuando ya tengas un modelo que te convenza.

> **Pregunta:** si solo puedes medirte contra junio 3 veces, ¿cómo vas a saber si un modelo es mejor que otro antes de gastar esos intentos? ¿Qué parte de los datos podrías usar como un "junio de práctica", donde tú sí tienes las respuestas?

### El flujo completo

```
Enero–mayo (fraudes confirmados + el resto)  →  el modelo aprende a diferenciar fraude de normal
                     ↓
Junio (sin respuestas)                       →  pones un puntaje a cada operación
                     ↓
Ordenas de mayor a menor                     →  las 300 primeras son las alertas
                     ↓
calificar.py                                 →  te dice cuántos soles protegiste
```

**En una línea:** entreno con todas las operaciones de enero a mayo, las de fraude confirmado y las demás, que casi todas son normales pero esconden algunos fraudes sin confirmar. El modelo aprende a diferenciar fraude de normal. Luego puntúa cada operación de junio, y las 300 más altas son las alertas que se califican con `calificar.py`.

## 6. Idea propia: dashboard con junio simulado

**Objetivo:** un dashboard donde se vea todo el análisis y que otra persona pueda entrar y usarlo. Reproduce junio en orden, como un tiempo real simulado, y muestra cómo van cambiando las prioridades a medida que llegan operaciones.

**Cómo funciona:**

- **El puntaje de una operación no cambia con el tiempo.** Cada operación se puntúa **una sola vez**, en su instante, con su pasado.
- **Lo que cambia es el ranking.** Van llegando operaciones nuevas, y algunas entran al top 300 y sacan a otras.

```
1 de junio   → top 300 con lo que llegó hasta hoy
15 de junio  → entran operaciones nuevas más sospechosas, salen otras
30 de junio  → top 300 final = lo que se entrega
```

- **La lista final es la misma** que si se calculara todo de una vez. El dashboard no cambia el resultado: es una forma de **mostrarlo**.
- **No hace falta modificar las tablas de Supabase.** La clave es de solo lectura. La simulación se hace en memoria o con un archivo local.
- **El dashboard no puede mostrar "cuántos acerté" en vivo.** Los fraudes de junio solo se usan a través de `calificar.py`, máximo 3 veces.
- **No es parte del reto ni cambia la nota.** Es un extra.

**Cuándo hacerlo (decisión pendiente):**

| Opción | Ventaja | Costo |
|---|---|---|
| **A. Al final, después del modelo** | El reto va primero. El dashboard muestra resultados ya cerrados | Lo ves funcionar recién al final |
| **B. En paralelo desde ahora** | Vas viendo todo desde el inicio | Mucho trabajo extra antes de tener un modelo que mostrar |
| **C. Al final, pero simple** | Una página estática con gráficas y la lista de 300, sin simulación | Menos vistoso que la reproducción de junio |

> **Pregunta:** en la vida real, el 5 de junio el equipo no sabe qué va a pasar el resto del mes. ¿Cómo decide en ese momento si una operación entra o no a las 300?

## 7. Decisión pendiente: qué hacer con los fraudes escondidos

Corregir las etiquetas que crees que están mal se llama **limpiar etiquetas**. Tiene una trampa: para decidir que una operación "probablemente fue fraude" usas tus propias reglas o un modelo. Si luego le dices al modelo "esto es fraude", le enseñas **lo que tú ya creías**, no lo que dicen los datos. Si tu regla estaba equivocada, el modelo aprende tu error y lo repite en junio.

| Opción | Qué haces | Ventaja | Costo |
|---|---|---|---|
| **A. Dejarlas como están** | Todo lo no confirmado cuenta como "normal" | Simple; solo usas lo que la empresa confirmó | El modelo aprende con algo de ruido |
| **B. Quitar las dudosas** | No usas para entrenar las operaciones con la etiqueta más dudosa | No inventas etiquetas; solo dejas fuera lo poco confiable | Pierdes datos; hay que decidir el criterio de "dudosa" |
| **C. Marcar sospechosas como fraude** | Usas reglas o un modelo para cambiar "normal" por "fraude" | Si aciertas, el modelo ve más ejemplos de fraude | Si fallas, el modelo aprende tus errores, y es difícil saber si acertaste |

**Cuándo se decide:** después de explorar los datos, cuando veas cuántos fraudes confirmados hay y cómo se ven. Se puede probar comparando A contra B o C, con la misma partición, la misma métrica y 3 semillas. La decisión final va a `decisiones.md`.

## 8. Preguntas pendientes

1. Si una operación ocurrió a fines de mayo, ¿ya habrá llegado su reclamo cuando se armó el archivo?
2. ¿Qué columnas del diccionario no existían todavía en el segundo en que se apretó enviar?
3. Si una cuenta ya tuvo un fraude confirmado antes, ¿desde qué fecha "se sabe": la de la operación o la del reclamo?
4. De los dos tipos de fraude escondido, ¿cuál podrías ubicar en el calendario sin adivinar? ¿Qué harías con esas operaciones al entrenar?
5. Si le dices al modelo "esta operación fue normal" y en realidad fue un fraude que nadie reclamó, ¿qué aprende el modelo?
6. ¿Para qué te sirven los fraudes confirmados de enero a mayo, si en la entrega solo va junio?
7. En la vida real, el 5 de junio, ¿cómo decide el equipo si una operación entra o no a las 300, sin saber qué pasará el resto del mes?
8. Si solo puedes calificar 3 veces, ¿qué parte de los datos podrías usar como un "junio de práctica" para comparar modelos?
