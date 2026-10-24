"""Califica tus predicciones de junio contra la verdad oculta.

Uso:   python calificar.py predicciones.csv

predicciones.csv debe tener una fila por transaccion de junio de 2026 con:
  id_tx      identificador de la transaccion
  score      numero; mas alto = mas sospechosa
  prioridad  (opcional) numero para ordenar las 300 alertas; si falta, se usa score
"""
import sys, os
import numpy as np, pandas as pd

N_ALERTAS = 300
aqui = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) < 2:
    sys.exit(__doc__)
v = pd.read_csv(os.path.join(aqui, "NO_ABRIR", "verdad_transacciones.csv"))
v = v[v.periodo == "junio"].copy()
p = pd.read_csv(sys.argv[1])
if not {"id_tx", "score"} <= set(p.columns):
    sys.exit("ERROR: predicciones.csv necesita las columnas id_tx y score.")
dup = int(p.id_tx.duplicated().sum())
p = p.sort_values("score", ascending=False).drop_duplicates("id_tx")
fuera = int((~p.id_tx.isin(v.id_tx)).sum())
d = v.merge(p, on="id_tx", how="left")
falt = int(d.score.isna().sum())
d["score"] = d.score.fillna(d.score.min() - 1 if d.score.notna().any() else 0)
if "prioridad" not in d.columns:
    d["prioridad"] = d.score
d["prioridad"] = d.prioridad.fillna(d.prioridad.min() - 1)
y = d.es_fraude.values; m = d.monto_real.values
total_fraudes = int(y.sum()); total_soles = float((y*m).sum())


def pr_auc(y, s):
    o = np.argsort(-s, kind="stable"); yy = y[o]
    prec = np.cumsum(yy)/(np.arange(len(yy)) + 1)
    return float((prec*yy).sum()/yy.sum())


def roc_auc(y, s):
    r = pd.Series(s).rank().values
    n1 = y.sum(); n0 = len(y) - n1
    return float((r[y == 1].sum() - n1*(n1 + 1)/2)/(n1*n0))


def top(orden):
    i = np.argsort(-orden, kind="stable")[:N_ALERTAS]
    return i, int(y[i].sum()), float((y[i]*m[i]).sum())


i_s, f_s, s_s = top(d.score.values)
i_p, f_p, s_p = top(d.prioridad.values)
_, f_m, s_m = top(m)
_, f_x, s_x = top(y*m + y)
rng = np.random.default_rng(0)
az = [top(rng.random(len(y)))[1:] for _ in range(200)]
f_a = float(np.mean([a[0] for a in az])); s_a = float(np.mean([a[1] for a in az]))

print("=" * 66)
print("CALIFICACION - junio 2026")
print("=" * 66)
print(f"Transacciones de junio: {len(d):,} | fraudes reales: {total_fraudes} ({total_fraudes/len(d):.2%}) | soles en fraude: S/ {total_soles:,.0f}")
if dup or fuera or falt:
    print(f"AVISOS: {dup} id_tx duplicados en tu archivo (se uso el score mas alto), {fuera} id_tx que no son de junio (ignorados), "
          f"{falt} transacciones de junio sin score (cuentan como las menos sospechosas).")
print()
print("1) Calidad del ordenamiento (no depende del umbral)")
print(f"   PR-AUC : {pr_auc(y, d.score.values):.3f}   (azar = {total_fraudes/len(d):.3f}, perfecto = 1.000)")
print(f"   ROC-AUC: {roc_auc(y, d.score.values):.3f}   (azar = 0.500)")
print()
print(f"2) Tus {N_ALERTAS} alertas ordenadas por 'score'")
print(f"   Fraudes atrapados : {f_s} de {total_fraudes}")
print(f"   Precision@{N_ALERTAS}     : {f_s/N_ALERTAS:.1%}")
print(f"   Recall@{N_ALERTAS}        : {f_s/total_fraudes:.1%}")
print(f"   Soles protegidos  : S/ {s_s:,.0f}  ({s_s/total_soles:.1%} del total)")
for tf in ["toma_de_cuenta", "estafa"]:
    tot = int((d.tipo_fraude == tf).sum()); cap = int((d.tipo_fraude.values[i_s] == tf).sum())
    print(f"   - {tf:15s}: {cap} de {tot} ({cap/tot:.0%})")
print()
if not np.array_equal(d.prioridad.values, d.score.values):
    print(f"3) Tus {N_ALERTAS} alertas ordenadas por 'prioridad'")
    print(f"   Fraudes atrapados : {f_p} de {total_fraudes}")
    print(f"   Soles protegidos  : S/ {s_p:,.0f}  ({s_p/total_soles:.1%} del total)")
    print()
print("Referencias para comparar (mismas 300 alertas)")
print(f"   Al azar                   : {f_a:5.1f} fraudes | S/ {s_a:>9,.0f}")
print(f"   Solo por monto mas alto   : {f_m:5d} fraudes | S/ {s_m:>9,.0f}")
print(f"   Maximo posible (perfecto) : {f_x:5d} fraudes | S/ {s_x:>9,.0f}")
print("=" * 66)
