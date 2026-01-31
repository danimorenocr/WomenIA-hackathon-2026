"""
Motor de predicción ML para análisis energético universitario.
Usa modelos XGBoost entrenados para predecir consumo, agua y CO2.
"""

import joblib
import numpy as np
import pandas as pd
import os
import base64
from io import BytesIO

# SHAP se carga de forma lazy para evitar problemas de importación
SHAP_DISPONIBLE = False
shap = None
plt = None

def _cargar_shap():
    """Carga SHAP de forma diferida cuando se necesita"""
    global SHAP_DISPONIBLE, shap, plt
    if shap is None:
        try:
            import shap as _shap
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as _plt
            shap = _shap
            plt = _plt
            SHAP_DISPONIBLE = True
            print("✅ SHAP cargado")
        except ImportError as e:
            print(f"⚠️ SHAP no disponible: {e}")
            SHAP_DISPONIBLE = False
    return SHAP_DISPONIBLE

# =====================================================
# CARGAR MODELOS ML
# =====================================================
modelo_consumo = modelo_agua = modelo_co2 = config_features = None
try:
    print("⏳ Cargando modelos ML...")
    modelo_consumo = joblib.load("models/modelo_consumo.pkl")
    modelo_agua = joblib.load("models/modelo_agua_mejorado.pkl")
    modelo_co2 = joblib.load("models/modelo_co2.pkl")
    config_features = joblib.load("models/config_features.pkl")
    print("✅ Modelos ML cargados")
except Exception as e:
    print(f"⚠️ Modelos ML no disponibles: {e}")

# =====================================================
# CARGAR DATOS CSV
# =====================================================
df_energia = None
try:
    df_energia = pd.read_csv("data/dataset_energia_limpio_sectores.csv")
    print(f"✅ CSV cargado: {len(df_energia)} registros")
except Exception as e:
    print(f"❌ Error cargando CSV: {e}")

# =====================================================
# CONSTANTES
# =====================================================
SEDES = {
    1: "Chiquinquirá",
    2: "Tunja", 
    3: "Duitama",
    4: "Sogamoso"
}

SECTORES = {
    'Comedores': 'comedor',
    'Salones': 'salon',
    'Laboratorios': 'laboratorio',
    'Auditorios': 'auditorio',
    'Oficinas': 'oficina'
}

# =====================================================
# FUNCIÓN PRINCIPAL DE PREDICCIÓN
# =====================================================
def predecir_completo(sede_id, sector, hora, dia_semana, temperatura, ocupacion):
    """
    Predicción completa usando 3 modelos en cascada.
    
    Args:
        sede_id: ID de sede (1-4)
        sector: Nombre del sector (Comedores, Salones, etc.)
        hora: Hora del día (0-23)
        dia_semana: Día de la semana (0=lunes, 6=domingo)
        temperatura: Temperatura exterior en °C
        ocupacion: Porcentaje de ocupación (0-100)
    
    Returns:
        dict con energia_kwh, agua_litros, co2_kg
    """
    try:
        features_consumo = config_features.get("features_stage1", []) if config_features else []
        
        # Preparar features
        X_dict = {
            'ocupacion_pct': ocupacion,
            'temperatura_exterior_c': temperatura,
            'hora': hora,
            'dia_semana': dia_semana,
            'sede_id': sede_id,
        }
        
        # One-hot encoding de sectores
        for sect_name, sect_col in SECTORES.items():
            X_dict[f'sector_{sect_col}'] = 1 if sect_name == sector else 0
        
        # Stage 1: Consumo energético
        X_consumo = [X_dict.get(f, 0) for f in features_consumo]
        X_consumo = np.array([X_consumo])
        pred_consumo = modelo_consumo.predict(X_consumo)[0] if modelo_consumo else 0
        
        # Stage 2: Agua
        features_agua = config_features.get("features_stage2", []) if config_features else []
        X_agua = []
        for feat in features_agua:
            if feat == 'pred_consumo_kwh':
                X_agua.append(pred_consumo)
            else:
                X_agua.append(X_dict.get(feat, 0))
        X_agua = np.array([X_agua])
        pred_agua = modelo_agua.predict(X_agua)[0] if modelo_agua else 0
        
        # Stage 3: CO2
        features_co2 = config_features.get("features_stage3", []) if config_features else []
        X_co2 = []
        for feat in features_co2:
            if feat == 'pred_consumo_kwh':
                X_co2.append(pred_consumo)
            elif feat == 'pred_agua_litros':
                X_co2.append(pred_agua)
            else:
                X_co2.append(X_dict.get(feat, 0))
        X_co2 = np.array([X_co2])
        pred_co2 = modelo_co2.predict(X_co2)[0] if modelo_co2 else 0
        
        return {
            'energia_kwh': float(round(pred_consumo, 2)),
            'agua_litros': float(round(pred_agua, 2)),
            'co2_kg': float(round(pred_co2, 2)),
            'sede': SEDES.get(sede_id, f"Sede {sede_id}"),
            'sector': sector
        }
    
    except Exception as e:
        print(f"⚠️ Error predicción: {e}")
        return {
            'energia_kwh': 0,
            'agua_litros': 0,
            'co2_kg': 0,
            'sede': SEDES.get(sede_id, f"Sede {sede_id}"),
            'sector': sector
        }


# =====================================================
# FUNCIÓN SHAP - GENERAR GRÁFICOS DE IMPORTANCIA
# =====================================================
def generar_shap_graficos(sede_id, sector, hora, dia_semana, temperatura, ocupacion):
    """
    Genera gráficos SHAP para explicar la predicción.
    Retorna imágenes en base64 para cada modelo.
    """
    # Cargar SHAP de forma lazy
    if not _cargar_shap():
        return {"error": "SHAP no disponible", "mensaje": "Instala SHAP con: pip install shap"}
    
    graficos = {}
    
    try:
        # Preparar features
        features_consumo = config_features.get("features_stage1", []) if config_features else []
        
        X_dict = {
            'ocupacion_pct': ocupacion,
            'temperatura_exterior_c': temperatura,
            'hora': hora,
            'dia_semana': dia_semana,
            'sede_id': sede_id,
        }
        
        for sect_name, sect_col in SECTORES.items():
            X_dict[f'sector_{sect_col}'] = 1 if sect_name == sector else 0
        
        # === SHAP para Consumo Energético ===
        if modelo_consumo is not None:
            X_consumo = np.array([[X_dict.get(f, 0) for f in features_consumo]])
            pred_consumo = modelo_consumo.predict(X_consumo)[0]
            
            explainer_consumo = shap.TreeExplainer(modelo_consumo)
            shap_values_consumo = explainer_consumo.shap_values(X_consumo)
            
            # Crear gráfico waterfall
            plt.figure(figsize=(10, 6))
            shap.waterfall_plot(
                shap.Explanation(
                    values=shap_values_consumo[0],
                    base_values=explainer_consumo.expected_value,
                    data=X_consumo[0],
                    feature_names=features_consumo
                ),
                show=False
            )
            plt.title(f"SHAP - Consumo Energético: {pred_consumo:.2f} kWh")
            plt.tight_layout()
            
            # Convertir a base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            graficos['consumo_energia'] = {
                'imagen_base64': base64.b64encode(buffer.getvalue()).decode('utf-8'),
                'prediccion': float(round(pred_consumo, 2)),
                'unidad': 'kWh'
            }
            plt.close()
        
        # === SHAP para Agua ===
        if modelo_agua is not None:
            features_agua = config_features.get("features_stage2", []) if config_features else []
            X_agua = []
            for feat in features_agua:
                if feat == 'pred_consumo_kwh':
                    X_agua.append(pred_consumo)
                else:
                    X_agua.append(X_dict.get(feat, 0))
            X_agua = np.array([X_agua])
            pred_agua = modelo_agua.predict(X_agua)[0]
            
            explainer_agua = shap.TreeExplainer(modelo_agua)
            shap_values_agua = explainer_agua.shap_values(X_agua)
            
            plt.figure(figsize=(10, 6))
            shap.waterfall_plot(
                shap.Explanation(
                    values=shap_values_agua[0],
                    base_values=explainer_agua.expected_value,
                    data=X_agua[0],
                    feature_names=features_agua
                ),
                show=False
            )
            plt.title(f"SHAP - Consumo Agua: {pred_agua:.2f} litros")
            plt.tight_layout()
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            graficos['consumo_agua'] = {
                'imagen_base64': base64.b64encode(buffer.getvalue()).decode('utf-8'),
                'prediccion': float(round(pred_agua, 2)),
                'unidad': 'litros'
            }
            plt.close()
        
        # === SHAP para CO2 ===
        if modelo_co2 is not None:
            features_co2 = config_features.get("features_stage3", []) if config_features else []
            X_co2 = []
            for feat in features_co2:
                if feat == 'pred_consumo_kwh':
                    X_co2.append(pred_consumo)
                elif feat == 'pred_agua_litros':
                    X_co2.append(pred_agua)
                else:
                    X_co2.append(X_dict.get(feat, 0))
            X_co2 = np.array([X_co2])
            pred_co2 = modelo_co2.predict(X_co2)[0]
            
            explainer_co2 = shap.TreeExplainer(modelo_co2)
            shap_values_co2 = explainer_co2.shap_values(X_co2)
            
            plt.figure(figsize=(10, 6))
            shap.waterfall_plot(
                shap.Explanation(
                    values=shap_values_co2[0],
                    base_values=explainer_co2.expected_value,
                    data=X_co2[0],
                    feature_names=features_co2
                ),
                show=False
            )
            plt.title(f"SHAP - Emisiones CO₂: {pred_co2:.2f} kg")
            plt.tight_layout()
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            graficos['emisiones_co2'] = {
                'imagen_base64': base64.b64encode(buffer.getvalue()).decode('utf-8'),
                'prediccion': float(round(pred_co2, 2)),
                'unidad': 'kg'
            }
            plt.close()
        
        return graficos
    
    except Exception as e:
        print(f"⚠️ Error generando SHAP: {e}")
        return {"error": str(e)}
