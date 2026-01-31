# 🌿 API de Análisis Energético Universitario

Sistema de predicción y análisis energético para universidades usando Machine Learning y LLM.

## 📁 Estructura del Proyecto

```
WomanIA-Hackathon-2026/
├── api.py                    # API Flask principal
├── llm_engine.py             # Motor de predicción ML
├── generar_graficos.py       # Generador de datos para gráficos
├── preguntas_predefinidas.py # Sistema de preguntas naturales
├── requirements.txt          # Dependencias Python
├── .env                      # Variables de entorno (API keys)
├── data/
│   └── dataset_energia_limpio_sectores.csv
└── models/
    ├── modelo_consumo.pkl
    ├── modelo_agua_mejorado.pkl
    ├── modelo_co2.pkl
    └── config_features.pkl
```

## 🚀 Instalación

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## ▶️ Ejecutar

```bash
python api.py
```

Servidor: `http://localhost:5000`

---

## 📡 ENDPOINTS DE LA API

### 🤖 Chat con IA (Groq - GRATIS)

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/chat-groq?mensaje=Hola` | Chat con query param |
| POST | `/api/chat-groq` | Chat con body JSON |

**Ejemplo POST:**
```json
{"mensaje": "¿Cómo puedo ahorrar energía?"}
```

**Respuesta:**
```json
{
    "respuesta": "¡Hola! Para ahorrar energía te recomiendo...",
    "modelo": "qwen/qwen3-32b"
}
```

---

### 📊 Gráficos y Análisis

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/graficos` | **Todos los gráficos en JSON** |
| GET | `/api/consumo-por-sede` | Consumo total por sede |
| GET | `/api/tendencias-consumo` | Tendencias últimos 30 días |
| GET | `/api/eficiencia-estudiante` | Eficiencia por estudiante |
| GET | `/api/emisiones-co2` | Emisiones CO₂ por sede |
| GET | `/api/consumo-agua` | Consumo de agua por sede |
| GET | `/api/temperatura-consumo` | Temperatura vs consumo |
| GET | `/api/consumo-por-sector` | Consumo por sector |
| GET | `/api/distribucion-por-sector` | Distribución % por sector |
| GET | `/api/tendencias-sector` | Tendencias por sector |
| GET | `/api/eficiencia-sector-sede` | Eficiencia sector × sede |
| GET | `/api/correlacion-ocupacion` | Ocupación vs consumo |
| GET | `/api/costos-operacionales` | Costos COP por sector |
| GET | `/api/impacto-ambiental` | CO₂ + agua + árboles |

---

### 🔮 Predicción ML

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/predecir` | Predicción completa |
| POST | `/api/predecir-con-shap` | Predicción + gráficos SHAP |

**Body (para ambos endpoints):**
```json
{
    "sede_id": 2,
    "sector": "Laboratorios",
    "hora": 14,
    "dia_semana": 2,
    "temperatura": 25,
    "ocupacion": 75
}
```

**Respuesta `/api/predecir`:**
```json
{
    "energia_kwh": 1250.45,
    "agua_litros": 3500.20,
    "co2_kg": 425.30,
    "sede": "Tunja",
    "sector": "Laboratorios"
}
```

**Respuesta `/api/predecir-con-shap`:**
```json
{
    "energia_kwh": 1250.45,
    "agua_litros": 3500.20,
    "co2_kg": 425.30,
    "sede": "Tunja",
    "sector": "Laboratorios",
    "shap_graficos": {
        "consumo_energia": {
            "imagen_base64": "iVBORw0KGgo...",
            "prediccion": 1250.45,
            "unidad": "kWh"
        },
        "consumo_agua": {
            "imagen_base64": "iVBORw0KGgo...",
            "prediccion": 3500.20,
            "unidad": "litros"
        },
        "emisiones_co2": {
            "imagen_base64": "iVBORw0KGgo...",
            "prediccion": 425.30,
            "unidad": "kg"
        }
    }
}
```

#### 📈 ¿Qué son los gráficos SHAP?

Los gráficos **SHAP (SHapley Additive exPlanations)** muestran:
- **Importancia de cada variable** en la predicción
- **Dirección del impacto** (positivo/negativo)
- **Magnitud de la contribución** de cada feature

Cada `imagen_base64` es un gráfico waterfall que puedes mostrar en el frontend así:
```html
<img src="data:image/png;base64,{imagen_base64}" alt="SHAP Chart">
```

---

### 💬 Preguntas Naturales

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/preguntas` | Lista de preguntas predefinidas |
| POST | `/api/responder-pregunta` | Responder por ID |
| POST | `/api/chat` | Chat para predicciones |

**Ejemplo:**
```json
{"pregunta": "¿Cuánta energía consumirá el laboratorio de la sede 3 mañana a las 5pm?"}
```

---

## 🏢 Sedes

| ID | Nombre |
|----|--------|
| 1 | Chiquinquirá |
| 2 | Tunja |
| 3 | Duitama |
| 4 | Sogamoso |

## 🏗️ Sectores

- Comedores
- Salones
- Laboratorios
- Auditorios
- Oficinas

---

## 🔑 Configuración (.env)

```env
GROQ_API_KEY=tu-groq-api-key-aqui
```

Obtén tu API key gratis: https://console.groq.com/keys

## 📊 Tecnologías

- **Backend**: Flask + Flask-CORS
- **ML**: XGBoost, Scikit-learn
- **Explicabilidad**: SHAP (SHapley Additive exPlanations)
- **LLM**: Groq (Qwen3-32B) - Gratis
- **Data**: Pandas, NumPy
- **Visualización**: Matplotlib

---

## 📋 Parámetros de Predicción

| Parámetro | Tipo | Descripción | Rango/Valores |
|-----------|------|-------------|---------------|
| `sede_id` | int | ID de la sede | 1-4 |
| `sector` | string | Nombre del sector | Ver lista de sectores |
| `hora` | int | Hora del día | 0-23 |
| `dia_semana` | int | Día de la semana | 0=Lun, 6=Dom |
| `temperatura` | float | Temperatura exterior °C | Típico: 15-35 |
| `ocupacion` | float | Porcentaje de ocupación | 0-100 |

---

## 🧪 Ejemplos de Uso

### cURL - Predicción simple
```bash
curl -X POST "http://localhost:5000/api/predecir" \
  -H "Content-Type: application/json" \
  -d '{"sede_id":1,"sector":"Aulas","hora":10,"dia_semana":2,"temperatura":25,"ocupacion":75}'
```

### cURL - Predicción con SHAP
```bash
curl -X POST "http://localhost:5000/api/predecir-con-shap" \
  -H "Content-Type: application/json" \
  -d '{"sede_id":1,"sector":"Aulas","hora":10,"dia_semana":2,"temperatura":25,"ocupacion":75}'
```

### PowerShell
```powershell
$body = @{sede_id=1; sector="Aulas"; hora=10; dia_semana=2; temperatura=25; ocupacion=75} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/api/predecir-con-shap" -Method POST -ContentType "application/json" -Body $body
```

### Python
```python
import requests

data = {
    "sede_id": 1,
    "sector": "Aulas",
    "hora": 10,
    "dia_semana": 2,
    "temperatura": 25,
    "ocupacion": 75
}

# Predicción simple
response = requests.post("http://localhost:5000/api/predecir", json=data)
print(response.json())

# Predicción con SHAP
response = requests.post("http://localhost:5000/api/predecir-con-shap", json=data)
result = response.json()

# Mostrar imagen SHAP (guardar como archivo)
import base64
with open("shap_energia.png", "wb") as f:
    f.write(base64.b64decode(result["shap_graficos"]["consumo_energia"]["imagen_base64"]))
```

### JavaScript (Frontend)
```javascript
const data = {
    sede_id: 1,
    sector: "Aulas",
    hora: 10,
    dia_semana: 2,
    temperatura: 25,
    ocupacion: 75
};

fetch("http://localhost:5000/api/predecir-con-shap", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
})
.then(res => res.json())
.then(result => {
    // Mostrar imagen SHAP en el HTML
    const img = document.createElement("img");
    img.src = `data:image/png;base64,${result.shap_graficos.consumo_energia.imagen_base64}`;
    document.body.appendChild(img);
});
```
