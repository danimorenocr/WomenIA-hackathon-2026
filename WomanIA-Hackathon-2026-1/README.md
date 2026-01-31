<p align="center">
  <img src="https://img.shields.io/badge/🦅-UPTC_Energy_AI-040959?style=for-the-badge&labelColor=FFE66B" alt="UPTC Energy AI"/>
</p>

<h1 align="center">⚡ EcoUPTC - Backend API</h1>

<p align="center">
  <strong>🌱 Plataforma de Predicción Energética con Inteligencia Artificial Explicable</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-API_REST-000000?style=flat-square&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/XGBoost-ML_Models-FF6600?style=flat-square&logo=xgboost&logoColor=white"/>
  <img src="https://img.shields.io/badge/SHAP-Explicabilidad-2E27B1?style=flat-square"/>
  <img src="https://img.shields.io/badge/Groq-LLM_Chat-F28705?style=flat-square"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/WomenIA-Hackathon_2026-D09F0A?style=for-the-badge"/>
</p>

---

## 🎯 El Problema

> **Las universidades colombianas desperdician hasta un 30% de recursos energéticos** por falta de herramientas predictivas y de monitoreo en tiempo real.

La **UPTC** (Universidad Pedagógica y Tecnológica de Colombia) cuenta con **4 sedes** en Boyacá:
- 🏛️ **Tunja** (Sede Central)
- 🏭 **Duitama**
- ⛏️ **Sogamoso**
- 🏔️ **Chiquinquirá**

Cada sede tiene múltiples sectores (laboratorios, comedores, oficinas, auditorios, salones) con patrones de consumo únicos que necesitan ser optimizados.

---

## 💡 Nuestra Solución

<table>
<tr>
<td width="50%">

### 🤖 IA Predictiva en Cascada
Modelos XGBoost entrenados que predicen en secuencia:
```
Energía (kWh) → Agua (L) → CO₂ (kg)
```
Con precisión superior al **92%** en datos históricos.

</td>
<td width="50%">

### 🧠 Explicabilidad SHAP
No solo predecimos, **explicamos POR QUÉ**:
- Qué factores influyen más
- Cómo reducir el consumo
- Decisiones basadas en datos

</td>
</tr>
<tr>
<td width="50%">

### 💬 Chatbot IA (Groq)
Asistente conversacional que:
- Responde preguntas en lenguaje natural
- Genera predicciones al instante
- Explica resultados de forma amigable

</td>
<td width="50%">

### 📊 API REST Completa
Endpoints para:
- Gráficos de consumo por sede/sector
- Predicciones en tiempo real
- Análisis histórico de datos

</td>
</tr>
</table>

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    🌐 FRONTEND (Next.js)                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    🔌 API REST (Flask)                      │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────────┐│
│  │ /graficos│  │/predecir│  │/chat-groq│ │/generar-shap   ││
│  └─────────┘  └─────────┘  └─────────┘  └─────────────────┘│
└─────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
   │  XGBoost    │    │    SHAP     │    │    Groq     │
   │  Models     │    │  Explainer  │    │  LLM API    │
   │  (3 etapas) │    │  (Waterfall)│    │  (qwen3-32b)│
   └─────────────┘    └─────────────┘    └─────────────┘
```

---

## 🚀 Instalación Rápida

```bash
# 1. Clonar el repositorio
git clone https://github.com/danimorenocr/WomenIA-hackathon-2026.git
cd WomanIA-Hackathon-2026-

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
# Crear archivo .env con:
GROQ_API_KEY=tu_api_key_de_groq

# 5. Ejecutar la API
python api.py
```

**🌐 La API estará disponible en:** `http://localhost:5000`

---

## 📡 Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/graficos` | Datos para todos los gráficos |
| `GET` | `/api/preguntas` | Preguntas predefinidas de predicción |
| `POST` | `/api/chat-groq` | Chat con IA (Groq LLM) |
| `POST` | `/api/predecir` | Predicción ML simple |
| `POST` | `/api/predecir-con-shap` | Predicción + explicabilidad SHAP |
| `POST` | `/api/generar-shap` | Solo gráficos SHAP |
| `POST` | `/api/responder-pregunta` | Responder pregunta predefinida |

---

## 🧪 Ejemplo de Uso

### Predicción con Explicabilidad SHAP:

```bash
curl -X POST http://localhost:5000/api/predecir-con-shap \
  -H "Content-Type: application/json" \
  -d '{
    "sede_id": 1,
    "sector": "Laboratorios",
    "hora": 10,
    "dia_semana": 2,
    "temperatura": 22,
    "ocupacion": 75
  }'
```

### Respuesta:
```json
{
  "energia_kwh": 1847.32,
  "agua_litros": 28450.67,
  "co2_kg": 523.18,
  "shap_graficos": {
    "consumo_energia": { "imagen_base64": "..." },
    "consumo_agua": { "imagen_base64": "..." },
    "emisiones_co2": { "imagen_base64": "..." }
  }
}
```

---

## 📁 Estructura del Proyecto

```
WomanIA-Hackathon-2026-/
├── 📄 api.py                    # API principal Flask
├── 🧠 llm_engine.py             # Motor ML + SHAP
├── 💬 preguntas_predefinidas.py # Lógica de predicciones
├── 📊 generar_graficos.py       # Generación de gráficos
├── 📋 requirements.txt          # Dependencias Python
├── 🔐 .env                      # Variables de entorno
├── 📂 data/
│   └── dataset_energia_limpio_sectores.csv
└── 📂 models/
    ├── modelo_energia.pkl
    ├── modelo_agua.pkl
    └── modelo_co2.pkl
```

---

## 🛠️ Tecnologías

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,flask" alt="Tech Stack"/>
</p>

| Tecnología | Uso |
|------------|-----|
| **Python 3.10+** | Lenguaje principal |
| **Flask** | Framework API REST |
| **XGBoost** | Modelos de Machine Learning |
| **SHAP** | Explicabilidad de predicciones |
| **Pandas** | Procesamiento de datos |
| **Groq API** | LLM para chatbot (GRATIS) |
| **Matplotlib** | Visualizaciones SHAP |

---

## 🌍 Impacto Esperado

<table>
<tr>
<td align="center">
<h3>💰 -25%</h3>
<p>Reducción en costos energéticos</p>
</td>
<td align="center">
<h3>🌱 -30%</h3>
<p>Reducción huella de carbono</p>
</td>
<td align="center">
<h3>💧 -20%</h3>
<p>Ahorro en consumo de agua</p>
</td>
</tr>
</table>

---

## 👩‍💻 Equipo WomenIA

<p align="center">
  <strong>Hackathon WomenIA 2026</strong><br/>
  Desarrollado con 💜 por mujeres en tecnología
</p>

---

<p align="center">
  <img src="https://img.shields.io/badge/Made_with-💜_y_☕-D09F0A?style=for-the-badge"/>
</p>
