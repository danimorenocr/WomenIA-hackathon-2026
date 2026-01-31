"""
===============================
TRANSFORMACIÓN DE DATOS POR SECTORES
===============================

Script para transformar el dataset de energía de formato ancho a formato largo,
desagregando el consumo de energía por sectores (comedores, salones, laboratorios, etc.).

Flujo:
1. Cargar dataset limpio
2. Mapear sectores de energía
3. Transformación Melt (formato ancho → largo)
4. Codificar sectores numéricamente
5. Eliminar outliers por percentil
6. Exportar dataset preparado para modelos por sector

Autor: Equipo de Análisis UPTC
Fecha: 2026
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder


# ===============================
# 1. CARGA DEL DATASET LIMPIO
# ===============================
print("📦 Cargando dataset limpio...")

df = pd.read_csv('dataset_energia_limpio.csv')
print(f"  ✓ Cargado: {df.shape[0]} registros × {df.shape[1]} columnas")


# ===============================
# 2. MAPEO DE SECTORES
# ===============================
print("\n🏢 Definiendo sectores...")

# Mapeo de columnas de energía a nombres descriptivos
sectores_map = {
    'energia_comedor_kwh': 'Comedores',
    'energia_salones_kwh': 'Salones',
    'energia_laboratorios_kwh': 'Laboratorios',
    'energia_auditorios_kwh': 'Auditorios',
    'energia_oficinas_kwh': 'Oficinas'
}

print(f"  ✓ Sectores a procesar: {list(sectores_map.values())}")


# ===============================
# 3. DEFINIR VARIABLES DE CONTEXTO
# ===============================
print("\n📊 Seleccionando variables de contexto...")

# Estas columnas se mantienen para cada registro transformado
# (no se "derriten" sino que se replican)
id_vars = [
    'timestamp',                    # Fecha y hora del registro
    'sede_id',                      # ID de la sede
    'temperatura_exterior_c',       # Contexto ambiental
    'ocupacion_pct',                # Contexto de ocupación
    'hora',                         # Hora del día
    'dia_semana',                   # Día de la semana
    'es_festivo',                   # Flag de día festivo
    'es_semana_parciales',          # Flag de semana de parciales
    'es_semana_finales',            # Flag de semana de finales
    'co2_kg',                       # Emisiones de CO2
    'agua_litros'                   # Consumo de agua
]

print(f"  ✓ Variables de contexto: {len(id_vars)}")


# ===============================
# 4. TRANSFORMACIÓN MELT
# ===============================
print("\n🔄 Transformando formato ancho → largo (Melt)...")

# Convertir de formato ancho (una columna por sector)
# a formato largo (una fila por sector-timestamp-sede)
df_global = pd.melt(
    df,
    id_vars=id_vars,
    value_vars=list(sectores_map.keys()),
    var_name='sector_original',      # Nombre de la columna original
    value_name='consumo_kwh'          # Valor de consumo
)

print(f"  ✓ Registros generados: {df_global.shape[0]}")
print(f"  ✓ Columnas: {df_global.shape[1]}")


# ===============================
# 5. NORMALIZAR NOMBRES DE SECTORES
# ===============================
print("\n🏷️  Normalizando nombres de sectores...")

# Mapear nombres técnicos a nombres descriptivos
df_global['sector'] = df_global['sector_original'].map(sectores_map)

# Eliminar columna auxiliar con nombres antiguos
df_global.drop(columns=['sector_original'], inplace=True)

print(f"  ✓ Sectores únicos: {df_global['sector'].unique().tolist()}")


# ===============================
# 6. CODIFICACIÓN NUMÉRICA DE SECTORES
# ===============================
print("\n🔢 Codificando sectores a valores numéricos...")

# Label Encoding: convierte nombres de sectores a números
le_sector = LabelEncoder()
df_global['sector_encoded'] = le_sector.fit_transform(df_global['sector'])

# Mostrar mapeo
mapeo_sector = dict(zip(le_sector.classes_, le_sector.transform(le_sector.classes_)))
print(f"  ✓ Mapeo: {mapeo_sector}")


# ===============================
# 7. ELIMINACIÓN DE OUTLIERS
# ===============================
print("\n📈 Limpiando outliers...")

# Calcular percentil 99 como umbral
q_limit = df_global['consumo_kwh'].quantile(0.99)
registros_antes = df_global.shape[0]

# Limitar valores superiores al percentil 99
df_global['consumo_kwh'] = df_global['consumo_kwh'].clip(upper=q_limit)

print(f"  ✓ Límite de consumo (P99): {q_limit:.2f} kWh")
print(f"  ✓ Registros procesados: {registros_antes}")


# ===============================
# 8. ESTADÍSTICAS POR SECTOR
# ===============================
print("\n📊 Estadísticas de consumo por sector:")

estadisticas = df_global.groupby('sector')['consumo_kwh'].agg([
    ('Promedio', 'mean'),
    ('Mínimo', 'min'),
    ('Máximo', 'max'),
    ('Desv. Est.', 'std'),
    ('Registros', 'count')
]).round(2)

print(estadisticas.to_string())


# ===============================
# 9. VALIDACIONES FINALES
# ===============================
print("\n✅ Validaciones finales...")

# Verificar que no hay nulos en columnas críticas
cols_criticas = ['timestamp', 'sede_id', 'sector', 'consumo_kwh']
nulos = df_global[cols_criticas].isnull().sum()

if nulos.sum() > 0:
    print("  ⚠️  Hay valores nulos detectados:")
    print(nulos[nulos > 0])
else:
    print(f"  ✓ Sin valores nulos en columnas críticas")

# Verificar distribución de sectores
print(f"\n  ✓ Distribución de registros por sector:")
dist = df_global['sector'].value_counts()
for sector, count in dist.items():
    pct = (count / len(df_global) * 100)
    print(f"    • {sector}: {count:,} ({pct:.1f}%)")


# ===============================
# 10. GUARDAR DATASET TRANSFORMADO
# ===============================
print("\n💾 Guardando dataset transformado...")

ruta_salida = "dataset_por_sectores.csv"
df_global.to_csv(ruta_salida, index=False, encoding='utf-8')

print(f"  ✓ Dataset guardado en: {ruta_salida}")


# ===============================
# 11. RESUMEN FINAL
# ===============================
print("\n" + "="*50)
print("✅ TRANSFORMACIÓN COMPLETADA EXITOSAMENTE")
print("="*50)

print(f"""
📋 RESUMEN:
  • Registros originales: {df.shape[0]:,}
  • Registros transformados: {df_global.shape[0]:,}
  • Multiplicador: {df_global.shape[0] / df.shape[0]:.1f}x (por {len(sectores_map)} sectores)
  • Columnas finales: {df_global.shape[1]}
  • Sectores: {len(sectores_map)}
  • Outliers eliminados: Percentil 99

📁 ARCHIVOS GENERADOS:
  1. dataset_por_sectores.csv

🎯 FORMATO LARGO:
  Cada fila representa: [timestamp + sede + contexto + sector + consumo]
  
  Ventajas:
  • Ideal para modelos por sector
  • Facilita análisis comparativo entre sectores
  • Reduce dimensionalidad del problema
  • Permite análisis de patrones por sector-sede

📊 PRÓXIMOS PASOS:
  • Entrenar modelos específicos por sector
  • Analizar patrones de consumo por sector
  • Generar predicciones por sector
  • Comparar desempeño de modelos global vs. por sector
""")

print("="*50)