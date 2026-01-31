"""
================================================================================
🚨 DETECCIÓN DE ANOMALÍAS ROBUSTA (SIN REENTRENAR MODELOS)
================================================================================

Este módulo implementa un sistema de detección de anomalías para datos de
consumo de energía, agua y emisiones de CO2. Utiliza técnicas estadísticas
robustas basadas en mediana e IQR (rango intercuartílico) para identificar
comportamientos anómalos sin necesidad de reentrenar modelos de machine learning.

Características principales:
  - Detección contextual por hora del día
  - Normalización robusta usando mediana e IQR
  - Clasificación en tres niveles: Normal, Alerta, Crítica
  - Función de detección para eventos individuales (chatbot)
  - Explicabilidad de anomalías detectadas

Dependencias:
  - numpy: Operaciones numéricas
  - pandas: Manipulación de datos

Autor(as): [Karol Acuña, Daniela Moreno, Sofia Torres, Juliana Garzón]
Fecha: Enero 31 / 2026
================================================================================
"""

import numpy as np
import pandas as pd

print("\n" + "=" * 70)
print("🚨 DETECCIÓN DE ANOMALÍAS ROBUSTA")
print("=" * 70)

# ================================================================
# SECCIÓN 1: PREPARACIÓN DE DATOS Y VARIABLES BASE
# ================================================================
# Este bloque copia el dataframe global y define las variables a analizar
# Se utiliza una copia para evitar modificaciones indeseadas en df_global

results = df_global.copy()
# DataFrame que contendrá todas las métricas de anomalía
# DataFrame que contendrá todas las métricas de anomalía

# Diccionario de variables a analizar con sus descripciones
variables = {
    'consumo_kwh': '⚡ Energía',      # Consumo de energía en kilovatios-hora
    'agua_litros': '💧 Agua',        # Consumo de agua en litros
    'co2_kg': '🌱 CO2'               # Emisiones de CO2 en kilogramos
}

# ================================================================
# SECCIÓN 2: CÁLCULO DE SCORES ROBUSTOS POR VARIABLE
# ================================================================
# Se calcula el Z-score robusto usando mediana e IQR, agrupado por hora
# Esta normalización es resistente a outliers, a diferencia de Z-score clásico
# Fórmula: Z_robusto = |valor - mediana| / IQR

for var in variables.keys():
    # Mediana por hora (medida de tendencia central resistente a outliers)
    mediana = results.groupby('hora')[var].transform('median')
    
    # Q3 y Q1 por hora (percentiles 75% y 25%)
    q75 = results.groupby('hora')[var].transform(lambda x: x.quantile(0.75))
    q25 = results.groupby('hora')[var].transform(lambda x: x.quantile(0.25))
    
    # Rango intercuartílico (IQR) - medida de dispersión robusta
    # Se añade 1e-6 para evitar división por cero
    iqr = (q75 - q25).replace(0, np.nan)
    
    # Z-score robusto: desviación del valor respecto a la mediana, 
    # normalizada por el IQR
    results[f'{var}_z'] = np.abs(results[var] - mediana) / (iqr + 1e-6)

# ================================================================
# SECCIÓN 3: CÁLCULO DEL SCORE GLOBAL DE ANOMALÍA
# ================================================================
# Se combinan los tres scores individuales con pesos que reflejan su importancia
# Pesos: Energía (40%) > Agua (35%) > CO2 (25%)

results['anomalia_score_raw'] = (
    0.4 * results['consumo_kwh_z'] +    # 40%: Z-score de energía
    0.35 * results['agua_litros_z'] +   # 35%: Z-score de agua
    0.25 * results['co2_kg_z']          # 25%: Z-score de CO2
)
# Score combinado que representa la magnitud general de la anomalía

# ================================================================
# SECCIÓN 4: NORMALIZACIÓN ROBUSTA CON LOGARITMO
# ================================================================
# Se aplica log1p (log(1+x)) para comprimir la escala de los scores
# Esto reduce el impacto de outliers extremos y facilita la interpretación

results['anomalia_score'] = np.log1p(results['anomalia_score_raw'])
# anomalia_score es más homogéneo que anomalia_score_raw

# ================================================================
# SECCIÓN 5: CÁLCULO DEL PERCENTIL POR CONTEXTO HORARIO
# ================================================================
# ELEMENTO CLAVE: Compara cada evento con su contexto histórico de la MISMA HORA
# Esto permite detectar anomalías que varían según la hora del día
# Ejemplo: consumo de 5000 kWh es normal a las 12:00 pero anómalo a las 3:00

results['anomalia_percentil'] = (
    results
    .groupby('hora')['anomalia_score']
    .rank(pct=True)  # Ranking normalizado (0.0 a 1.0) dentro de cada hora
)
# anomalia_percentil: porcentaje de eventos por hora más anomalosos que este

# ================================================================
# SECCIÓN 6: CLASIFICACIÓN FINAL EN TRES NIVELES
# ================================================================
# Basada en percentiles dentro del contexto horario:
#   - Normal: < 90 percentil (comportamiento típico)
#   - Alerta: 90-97 percentil (inusual pero no crítico)
#   - Crítica: > 97 percentil (muy anómalo, requiere atención)

def clasificar_anomalia(p):
    """
    Clasifica el nivel de anomalía basándose en el percentil.
    
    Args:
        p (float): Percentil del evento (0.0 a 1.0)
        
    Returns:
        str: Nivel de clasificación ('Normal', 'Alerta' o 'Crítica')
    """
    if p < 0.90:
        return 'Normal'
    elif p < 0.97:
        return 'Alerta'
    else:
        return 'Crítica'

results['nivel_anomalia'] = results['anomalia_percentil'].apply(clasificar_anomalia)
# nivel_anomalia: clasificación final de cada evento

# ================================================================
# SECCIÓN 7: RESUMEN ESTADÍSTICO DE ANOMALÍAS DETECTADAS
# ================================================================
# Genera un informe general sobre la distribución de anomalías
# y el comportamiento de las variables por nivel de severidad

print("\n📊 Resumen de anomalías (%)")
# Distribución porcentual de eventos por nivel de severidad
print(
    results['nivel_anomalia']
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

# Valores promedio de cada variable por nivel de severidad
for var, label in variables.items():
    print(f"\n{label} promedio")
    print(
        results
        .groupby('nivel_anomalia')[var]
        .mean()
    )

# ================================================================
# SECCIÓN 8: IDENTIFICACIÓN DE TOP 10 EVENTOS CRÍTICOS
# ================================================================
# Extrae y visualiza los 10 eventos más anómalos del dataset
# Útil para investigación manual y auditoría

print("\n🔥 Top 10 eventos críticos")

# Extrae eventos críticos ordenados por severidad
top_criticos = (
    results[results['nivel_anomalia'] == 'Crítica']
    .sort_values('anomalia_score_raw', ascending=False)
    .head(10)[[
        'timestamp',
        'hora',
        'consumo_kwh',
        'agua_litros',
        'anomalia_score_raw',
        'anomalia_percentil',
        'co2_kg'
    ]]
)

# Mostrar tabla con los eventos más críticos
print(top_criticos.to_string())

# ================================================================
# SECCIÓN 9: GUARDADO OPCIONAL DE RESULTADOS
# ================================================================
# Se puede guardar el dataframe con todas las métricas de anomalía en CSV
# Descomenta la siguiente línea para activar el guardado

# results.to_csv("anomalias_detectadas.csv", index=False)
# Salida: archivo CSV con timestamp, variables, scores y clasificaciones

print("\n" + "=" * 70)
print("✅ DETECCIÓN DE ANOMALÍAS FINALIZADA CORRECTAMENTE")
print("   ✔ Robusta (mediana + IQR)")
print("   ✔ Contextual (por hora del día)")
print("   ✔ Sin reentrenar modelos")
print("=" * 70)


# ================================================================
# PARTE 2: FUNCIONES PARA DETECCIÓN DE ANOMALÍAS EN CHATBOT
# ================================================================
# Módulo separado para integración con chatbots que necesitan evaluar
# eventos individuales en tiempo real sin recalcular todo el dataset

import numpy as np
import pandas as pd

# ================================================================
# SECCIÓN 1: FUNCIÓN PRINCIPAL - DETECTAR ANOMALÍA DE UN EVENTO
# ================================================================

def detectar_anomalia_evento(
    df_ref,
    timestamp,
    hora,
    consumo_kwh,
    agua_litros,
    co2_kg
):
    """
    Detecta si un evento puntual es anómalo comparándolo contra el histórico
    de la MISMA HORA del día.
    
    Algoritmo:
    1. Filtra datos históricos de la misma hora
    2. Calcula Z-scores robustos para cada variable
    3. Combina scores con pesos predefinidos
    4. Normaliza con logaritmo
    5. Calcula percentil respecto al histórico
    6. Clasifica como Normal/Alerta/Crítica
    7. Identifica variables causantes de la anomalía
    
    Args:
        df_ref (pd.DataFrame): DataFrame histórico con columnas 
                              'hora', 'consumo_kwh', 'agua_litros', 'co2_kg'
        timestamp (str): Timestamp del evento a evaluar (formato libre, solo informativo)
        hora (int): Hora del día (0-23)
        consumo_kwh (float): Consumo de energía en kWh
        agua_litros (float): Consumo de agua en litros
        co2_kg (float): Emisiones de CO2 en kg
        
    Returns:
        dict: Diccionario con claves:
              - 'timestamp': Timestamp del evento
              - 'nivel': Clasificación ('Normal', 'Alerta', 'Crítica')
              - 'percentil': Percentil del evento (0-100)
              - 'score': Score numérico de anomalía
              - 'explicacion': Lista de causas identificadas
              - 'mensaje': Mensaje opcional (si datos insuficientes)
    """

    # Filtra datos históricos de la misma hora del día
    contexto = df_ref[df_ref['hora'] == hora]

    # Validación: se requieren mínimo 50 eventos para hacer una evaluación confiable
    if len(contexto) < 50:
        return {
            "nivel": "Normal",
            "mensaje": "No hay suficientes datos históricos para evaluar anomalías."
        }

    def score_robusto(valor, serie):
        """
        Calcula Z-score robusto para un valor individual.
        Resistente a outliers usando mediana e IQR.
        
        Args:
            valor (float): Valor individual a evaluar
            serie (pd.Series): Serie histórica de referencia
            
        Returns:
            float: Z-score robusto normalizado
        """
        med = serie.median()
        iqr = serie.quantile(0.75) - serie.quantile(0.25)
        return abs(valor - med) / (iqr + 1e-6)

    # Calcula Z-scores robustos para cada variable
    z_consumo = score_robusto(consumo_kwh, contexto['consumo_kwh'])
    z_agua = score_robusto(agua_litros, contexto['agua_litros'])
    z_co2 = score_robusto(co2_kg, contexto['co2_kg'])

    # Score combinado ponderado
    score_raw = 0.4 * z_consumo + 0.35 * z_agua + 0.25 * z_co2
    # Normalización con log1p para comprimir escala
    score_final = np.log1p(score_raw)

    # Calcula los scores históricos usando la misma fórmula ponderada
    # para comparar el evento actual con la distribución histórica
    scores_hist = (
        0.4 * abs(contexto['consumo_kwh'] - contexto['consumo_kwh'].median()) /
        (contexto['consumo_kwh'].quantile(0.75) - contexto['consumo_kwh'].quantile(0.25) + 1e-6)
        +
        0.35 * abs(contexto['agua_litros'] - contexto['agua_litros'].median()) /
        (contexto['agua_litros'].quantile(0.75) - contexto['agua_litros'].quantile(0.25) + 1e-6)
        +
        0.25 * abs(contexto['co2_kg'] - contexto['co2_kg'].median()) /
        (contexto['co2_kg'].quantile(0.75) - contexto['co2_kg'].quantile(0.25) + 1e-6)
    )

    # Percentil: porcentaje de eventos históricos menos anómalos que el evento actual
    percentil = (scores_hist < score_raw).mean()

    # Clasificación basada en percentiles (mismo umbral que en análisis batch)
    if percentil < 0.90:
        nivel = "Normal"
    elif percentil < 0.97:
        nivel = "Alerta"
    else:
        nivel = "Crítica"

    # Identificación de causas: examina qué variables provocaron la anomalía
    # Un Z-score > 3 indica desviación significativa
    causas = []
    if z_consumo > 3:
        causas.append("consumo energético inusualmente alto")
    if z_agua > 3:
        causas.append("consumo de agua fuera de lo normal")
    if z_co2 > 3:
        causas.append("emisiones de CO₂ elevadas")

    # Si no hay causas individuales significativas, la anomalía es por combinación
    if not causas:
        causas.append("comportamiento combinado atípico")

    return {
        "timestamp": timestamp,
        "nivel": nivel,
        "percentil": round(percentil * 100, 2),  # Convertir a escala 0-100
        "score": round(score_final, 2),           # Score normalizado
        "explicacion": causas                      # Causas de la anomalía
    }

# ================================================================
# SECCIÓN 2: SIMULACIÓN DE ENTRADA DE USUARIO (EJEMPLO CHATBOT)
# ================================================================
# Ejemplo de datos que un usuario podría proporcionar al chatbot
# para verificar si un evento específico es anómalo

evento_usuario = {
    "timestamp": "2025-06-24 12:00",    # Timestamp del evento a analizar
    "hora": 12,                         # Hora del día (para filtrar contexto)
    "consumo_kwh": 7200,                # Consumo de energía
    "agua_litros": 180000,              # Consumo de agua
    "co2_kg": 1600                      # Emisiones de CO2
}

# Ejecuta la detección de anomalía para el evento del usuario
resultado = detectar_anomalia_evento(
    df_ref=df_global,
    timestamp=evento_usuario["timestamp"],
    hora=evento_usuario["hora"],
    consumo_kwh=evento_usuario["consumo_kwh"],
    agua_litros=evento_usuario["agua_litros"],
    co2_kg=evento_usuario["co2_kg"]
)

# ================================================================
# SECCIÓN 3: FUNCIÓN DE RESPUESTA DEL CHATBOT (GENERACIÓN DE TEXTO)
# ================================================================
# Convierte el resultado técnico en un mensaje natural para el usuario
# Adapta el tono según el nivel de severidad

def respuesta_chatbot(resultado):
    """
    Genera una respuesta natural en lenguaje conversacional para el usuario
    basada en los resultados de detección de anomalía.
    
    Args:
        resultado (dict): Diccionario retornado por detectar_anomalia_evento()
        
    Returns:
        str: Mensaje natural explicando si hay anomalía y sus causas
    """
    # Caso Normal: consumo dentro de los parámetros esperados
    if resultado["nivel"] == "Normal":
        return (
            f"✅ El consumo registrado a las {resultado['timestamp']} "
            f"se encuentra dentro de los valores normales para esa hora."
        )

    # Prepara la lista de causas para incluir en el mensaje
    causas = ", ".join(resultado["explicacion"])

    # Caso Alerta: comportamiento inusual pero no crítico
    if resultado["nivel"] == "Alerta":
        return (
            f"⚠️ Atención: el evento de las {resultado['timestamp']} "
            f"presenta un comportamiento inusual ({causas}). "
            f"Se encuentra en el percentil {resultado['percentil']}."
        )

    # Caso Crítica: anomalía severa que requiere atención inmediata
    return (
        f"🚨 ALERTA CRÍTICA\n"
        f"El evento registrado a las {resultado['timestamp']} es altamente anómalo.\n"
        f"Motivos detectados: {causas}.\n"
        f"Nivel de severidad: percentil {resultado['percentil']}."
    )

# ================================================================
# SECCIÓN 4: EJECUCIÓN DEL EJEMPLO - RESPUESTA AL USUARIO
# ================================================================
# Genera y muestra la respuesta natural del chatbot para el evento de ejemplo

print("\n🤖 Respuesta del chatbot:\n")
print(respuesta_chatbot(resultado))

# ================================================================
# FIN DEL MÓDULO
# ================================================================
# Este script proporciona dos flujos de trabajo principales:
#
# 1. ANÁLISIS BATCH (Secciones 1-9 de la Parte 1):
#    - Procesa todo df_global de una vez
#    - Identifica tendencias generales de anomalías
#    - Genera reportes de top 10 eventos críticos
#
# 2. DETECCIÓN EN TIEMPO REAL (Parte 2):
#    - Evalúa eventos individuales contra contexto histórico
#    - Ideal para integración con chatbots
#    - Proporciona explicaciones naturales
#
# Características técnicas:
# - Robusto frente a outliers (mediana + IQR)
# - Sensible al contexto (análisis por hora)
# - Sin dependencia de modelos ML reentrenables
# - Interpretable y explicable
