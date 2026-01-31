"""
===============================
LIMPIEZA Y PREPARACIÓN DE DATOS
===============================

Script para limpiar, procesar y preparar datos de consumo de energía de las sedes de la UPTC.

Flujo:
1. Carga de datos (CSV)
2. Limpieza de columnas y normalización
3. Tratamiento de timestamps
4. Interpolación de valores faltantes
5. Agregaciones temporales (diario, semanal, mensual)
6. Codificación de variables categóricas
7. Manejo completo de valores nulos
8. División temporal (train/test)
9. Entrenamiento de modelo baseline (RandomForest)
10. Análisis de importancia de variables

Autor(as): [Karol Acuña, Daniela Moreno, Sofia Torres, Juliana Garzón]
Fecha: Enero 31 / 2026
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


# ===============================
# 1. CARGA DE DATOS
# ===============================
print("📦 Cargando datos...")
df = pd.read_csv('consumos_uptc.csv')
sedes = pd.read_csv('sedes_uptc.csv')

print(f"  • Consumos: {df.shape}")
print(f"  • Sedes: {sedes.shape}")


# ===============================
# 2. LIMPIEZA DE COLUMNAS
# ===============================
print("\n🧹 Limpiando columnas...")

# Convertir a minúsculas y eliminar espacios
df.columns = df.columns.str.strip().str.lower()
sedes.columns = sedes.columns.str.strip().str.lower()

print(f"  ✓ Columnas normalizadas: {df.columns.tolist()}")


# ===============================
# 3. NORMALIZAR SEDE_ID (CLAVE)
# ===============================
print("\n🔑 Normalizando sede_id...")

df['sede_id'] = df['sede_id'].str.replace('-', '_').str.strip()
sedes['sede_id'] = sedes['sede_id'].str.replace('-', '_').str.strip()

print(f"  ✓ Sedes únicas: {df['sede_id'].nunique()}")


# ===============================
# 4. TIMESTAMP
# ===============================
print("\n⏰ Procesando timestamps...")

df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values(['sede_id', 'timestamp'])

print(f"  ✓ Rango temporal: {df['timestamp'].min()} → {df['timestamp'].max()}")


# ===============================
# 5. COLUMNAS NUMÉRICAS
# ===============================
print("\n🔢 Convirtiendo columnas numéricas...")

cols_interpolar = [
    'energia_total_kwh',
    'energia_comedor_kwh',
    'energia_salones_kwh',
    'energia_laboratorios_kwh',
    'energia_auditorios_kwh',
    'energia_oficinas_kwh',
    'potencia_total_kw',
    'agua_litros',
    'temperatura_exterior_c',
    'ocupacion_pct',
    'co2_kg'
]

df[cols_interpolar] = df[cols_interpolar].apply(
    pd.to_numeric, errors='coerce'
)

print(f"  ✓ {len(cols_interpolar)} columnas convertidas a numérico")


# ===============================
# 6. INTERPOLACIÓN POR SEDE (TIEMPO)
# ===============================
print("\n📈 Interpolando valores faltantes por sede y tiempo...")

df = (
    df
    .set_index('timestamp')
    .groupby('sede_id', group_keys=False)
    .apply(lambda x: x.interpolate(method='time'))
    .reset_index()
)

nulos_antes = df[cols_interpolar].isna().sum().sum()
print(f"  ✓ Nulos interpolados: {nulos_antes}")


# ===============================
# 7. UNIÓN CON SEDES (YA LIMPIO)
# ===============================
print("\n🔗 Uniendo con información de sedes...")

df = df.merge(sedes, on='sede_id', how='left')

print(f"  ✓ Filas: {df.shape[0]}, Columnas: {df.shape[1]}")


# ===============================
# 8. DATASETS AGREGADOS
# ===============================
print("\n📊 Creando agregaciones temporales...")

# Agregación diaria
df_diario = (
    df
    .set_index('timestamp')
    .groupby('sede_id')
    .resample('D')
    .sum(numeric_only=True)
    .reset_index()
)

# Agregación semanal
df_semanal = (
    df
    .set_index('timestamp')
    .groupby('sede_id')
    .resample('W')
    .sum(numeric_only=True)
    .reset_index()
)

# Agregación mensual
df_mensual = (
    df
    .set_index('timestamp')
    .groupby('sede_id')
    .resample('M')
    .sum(numeric_only=True)
    .reset_index()
)

print(f"  • Horario : {df.shape}")
print(f"  • Diario  : {df_diario.shape}")
print(f"  • Semanal : {df_semanal.shape}")
print(f"  • Mensual : {df_mensual.shape}")


# ===============================
# 9. VERIFICACIONES CLAVE
# ===============================
print("\n✅ Verificaciones iniciales...")

print("\nInfo de sedes:")
print(df[['sede_id', 'nombre_completo', 'ciudad']].drop_duplicates())


# ===============================
# 10. ELIMINAR VARIABLES CATEGÓRICAS
# ===============================
print("\n🗑️  Eliminando variables categóricas innecesarias...")

cols_drop = [
    'sede_x',                    # nombre textual de la sede
    'dia_nombre',                # texto
    'periodo_academico'          # texto
]

# Eliminar solo si existen (por seguridad)
df = df.drop(columns=[c for c in cols_drop if c in df.columns])

print(f"  ✓ Columnas eliminadas: {[c for c in cols_drop if c in df.columns]}")


# ===============================
# 11. CODIFICAR sede_id A NUMÉRICO
# ===============================
print("\n🔢 Codificando sede_id a numérico...")

# Normalizar sede_id (mayúsculas, sin espacios, mismo formato)
df['sede_id'] = (
    df['sede_id']
    .astype(str)
    .str.strip()
    .str.upper()
    .str.replace('-', '_')
)

# Mapeo de sedes
sede_map = {
    'UPTC_CHI': 1,
    'UPTC_TUN': 2,
    'UPTC_DUI': 3,
    'UPTC_SOG': 4
}

df['sede_id_num'] = df['sede_id'].map(sede_map)

# Verificar que no haya NaN
if df['sede_id_num'].isna().any():
    raise ValueError("⚠️ Hay sedes sin mapear en sede_id")

# Eliminar sede_id original y renombrar
df = df.drop(columns=['sede_id'])
df = df.rename(columns={'sede_id_num': 'sede_id'})

print(f"  ✓ Valores únicos de sede_id: {sorted(df['sede_id'].unique())}")


# ===============================
# 12. ELIMINAR COLUMNAS INNECESARIAS
# ===============================
print("\n🧹 Eliminando IDs y duplicados...")

if 'reading_id' in df.columns:
    df = df.drop(columns=['reading_id'])

print(f"  ✓ Shape después de limpieza: {df.shape}")


# ===============================
# 13. INSPECCIÓN DE TIPOS DE DATOS
# ===============================
print("\n📋 Tipos de datos:")
print(df.dtypes)

# Mostrar columnas de tipo object
cols_object = df.select_dtypes(include='object').columns
print(f"\nColumnas categóricas (object): {list(cols_object)}")

if len(cols_object) > 0:
    print("\nValores únicos por columna categórica:")
    for col in cols_object:
        print(f"  • {col}: {df[col].nunique()} únicos")
        print(f"    {df[col].unique()[:5]}")


# ===============================
# 14. PROCESAMIENTO DE VARIABLES CATEGÓRICAS
# ===============================
print("\n🏷️  Procesando variables categóricas...")

# Eliminar columnas que no sirven
df = df.drop(columns=['sede_y', 'nombre_completo'] if all(c in df.columns for c in ['sede_y', 'nombre_completo']) else [])

# Label Encoding de ciudad
if 'ciudad' in df.columns:
    ciudad_por_sede = (
        df[['sede_id', 'ciudad']]
        .dropna()
        .drop_duplicates()
        .sort_values('sede_id')
    )
    
    le_ciudad = LabelEncoder()
    le_ciudad.fit(ciudad_por_sede['ciudad'])
    
    df['ciudad_encoded'] = df['ciudad'].map(
        lambda x: le_ciudad.transform([x])[0] if pd.notna(x) else -1
    )
    df = df.drop(columns=['ciudad'])
    print(f"  ✓ Ciudad codificada: {dict(zip(le_ciudad.classes_, le_ciudad.transform(le_ciudad.classes_)))}")

# Mantener booleanos (y rellenar NaN si existen)
if 'tiene_residencias' in df.columns:
    df['tiene_residencias'] = df['tiene_residencias'].fillna(False).astype(bool)

if 'tiene_laboratorios_pesados' in df.columns:
    df['tiene_laboratorios_pesados'] = (
        df['tiene_laboratorios_pesados']
        .fillna(False)
        .astype(bool)
    )

print(f"  ✓ Tipos después de codificación:")
print(df.dtypes)


# ===============================
# 15. MANEJO COMPLETO DE NULOS
# ===============================
print("\n🔍 Analizando valores nulos...")

print(df.isnull().sum())

print("\n✍️  Rellenando valores nulos...")

# 1️⃣ Variables donde NaN significa ausencia de consumo / evento
cero_cols = [
    'energia_auditorios_kwh',
    'ocupacion_pct'
]

cero_cols = [c for c in cero_cols if c in df.columns]
df[cero_cols] = df[cero_cols].fillna(0)
print(f"  ✓ Columnas rellenadas con 0: {cero_cols}")

# 2️⃣ Variables estructurales (rellenar por sede)
estructura_cols = [
    'area_m2',
    'num_estudiantes',
    'num_empleados',
    'num_edificios',
    'altitud_msnm'
]

estructura_cols = [c for c in estructura_cols if c in df.columns]
if estructura_cols:
    df[estructura_cols] = (
        df.groupby('sede_id')[estructura_cols]
          .transform(lambda x: x.fillna(x.median()))
    )
    print(f"  ✓ Columnas estructurales rellenadas por mediana de sede: {estructura_cols}")

# 3️⃣ Variables continuas generales (mediana global)
mediana_cols = [
    'temp_promedio_c',
    'pct_comedores',
    'pct_salones',
    'pct_laboratorios',
    'pct_auditorios',
    'pct_oficinas'
]

mediana_cols = [c for c in mediana_cols if c in df.columns]
if mediana_cols:
    df[mediana_cols] = df[mediana_cols].fillna(df[mediana_cols].median())
    print(f"  ✓ Columnas continuas rellenadas con mediana global: {mediana_cols}")

# 4️⃣ Verificación final
nulos_restantes = df.isna().sum()
print("\n✅ Nulos restantes:")
print(nulos_restantes[nulos_restantes > 0] if (nulos_restantes > 0).any() else "  ✓ Sin valores nulos")

assert df.isna().sum().sum() == 0, "⚠️ Aún hay valores nulos en el dataset"

print(f"\n📈 Shape final: {df.shape}")


# ===============================
# 16. GUARDAR DATASET LIMPIO
# ===============================
print("\n💾 Guardando dataset limpio...")

ruta_salida = "dataset_energia_limpio.csv"
df.to_csv(ruta_salida, index=False, encoding="utf-8")

print(f"  ✓ Dataset guardado en: {ruta_salida}")


# ===============================
# 17. DIVISIÓN TEMPORAL (TRAIN/TEST)
# ===============================
print("\n📊 Dividiendo datos en train/test...")

# Asegurar orden temporal
df = df.sort_values('timestamp').reset_index(drop=True)

# Ver rango de fechas
print(f"  • Rango temporal: {df['timestamp'].min()} → {df['timestamp'].max()}")

# Definir fecha de corte
fecha_corte = "2023-01-01"

# División temporal
df_train = df[df['timestamp'] < fecha_corte]
df_test = df[df['timestamp'] >= fecha_corte]

print(f"  • Train: {df_train.shape[0]} filas")
print(f"  • Test : {df_test.shape[0]} filas")

# Definir target y features
target = "energia_total_kwh"

# Columnas que NO se usan como features
cols_excluir = [
    'timestamp',
    target
]

# Features
X_train = df_train.drop(columns=cols_excluir)
y_train = df_train[target]

X_test = df_test.drop(columns=cols_excluir)
y_test = df_test[target]

print(f"\n  • Features: {X_train.shape[1]}")
print(f"  • Target: {target}")


# ===============================
# 18. MODELO BASELINE - RANDOM FOREST
# ===============================
print("\n🤖 Entrenando modelo Random Forest...")

# Crear modelo
rf = RandomForestRegressor(
    n_estimators=100,
    max_depth=20,
    random_state=42,
    n_jobs=-1
)

# Entrenar
print("  ⏳ Entrenando...")
rf.fit(X_train, y_train)

# Predicciones
y_pred = rf.predict(X_test)

# Métricas
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = rf.score(X_test, y_test)

print("\n📊 RESULTADOS - RandomForest Baseline")
print(f"  • MAE  : {mae:.4f} kWh")
print(f"  • RMSE : {rmse:.4f} kWh")
print(f"  • R²   : {r2:.4f}")


# ===============================
# 19. IMPORTANCIA DE VARIABLES
# ===============================
print("\n🔝 Importancia de variables...")

importancias = pd.DataFrame({
    'feature': X_train.columns,
    'importance': rf.feature_importances_
}).sort_values(by='importance', ascending=False)

print("\nTop 15 variables más importantes:")
print(importancias.head(15).to_string(index=False))

# Guardar importancias
importancias.to_csv('importancias_variables.csv', index=False)
print("\n  ✓ Importancias guardadas en: importancias_variables.csv")


# ===============================
# 20. RESUMEN FINAL
# ===============================
print("\n" + "="*50)
print("✅ PROCESAMIENTO COMPLETADO EXITOSAMENTE")
print("="*50)

print(f"""
📋 RESUMEN:
  • Dataset original: {len(df)} registros
  • Columnas finales: {df.shape[1]}
  • Valores nulos tratados: ✓
  • Agregaciones temporales: 3 (horaria, diaria, semanal, mensual)
  • Modelo entrenado: RandomForest
  • Métrica R²: {r2:.4f}

📁 ARCHIVOS GENERADOS:
  1. dataset_energia_limpio.csv
  2. importancias_variables.csv

🎯 PRÓXIMOS PASOS:
  • Validar predicciones del modelo
  • Ajustar hiperparámetros
  • Probar otros modelos (XGBoost, LightGBM)
  • Análisis de residuos
""")

print("="*50)
