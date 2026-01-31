<p align="center">
  <img src="https://img.shields.io/badge/🦅_UPTC-EcoUPTC-040959?style=for-the-badge&labelColor=FFE66B&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxwYXRoIGQ9Im0xMiAzLTEuOTEyIDUuODEzYTIgMiAwIDAgMS0xLjI3NSAxLjI3NUwzIDEybDUuODEzIDEuOTEyYTIgMiAwIDAgMSAxLjI3NSAxLjI3NUwxMiAyMWwxLjkxMi01LjgxM2EyIDIgMCAwIDEgMS4yNzUtMS4yNzVMMjEgMTJsLTUuODEzLTEuOTEyYTIgMiAwIDAgMS0xLjI3NS0xLjI3NUwxMiAzWiIvPjwvc3ZnPg==" alt="EcoUPTC"/>
</p>

<h1 align="center">⚡ EcoUPTC</h1>
<h3 align="center">Plataforma de Gestión Energética Inteligente con IA Explicable</h3>

<p align="center">
  <img src="https://img.shields.io/badge/WomenIA-Hackathon_2026-D09F0A?style=for-the-badge"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-Backend-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Next.js-Frontend-000000?style=flat-square&logo=nextdotjs&logoColor=white"/>
  <img src="https://img.shields.io/badge/XGBoost-ML-FF6600?style=flat-square"/>
  <img src="https://img.shields.io/badge/SHAP-Explicabilidad-2E27B1?style=flat-square"/>
  <img src="https://img.shields.io/badge/Groq-LLM_Gratis-F28705?style=flat-square"/>
</p>

---

## 🎯 ¿Qué problema resolvemos?

> **Las universidades colombianas desperdician hasta un 30% de sus recursos energéticos** por falta de herramientas predictivas y monitoreo inteligente.

**EcoUPTC** es una plataforma que permite a la **Universidad Pedagógica y Tecnológica de Colombia (UPTC)** predecir y optimizar el consumo de **energía**, **agua** y **emisiones de CO₂** en sus 4 sedes.

---

## 🏛️ Sedes de la UPTC

| Sede | Ubicación | Sectores |
|------|-----------|----------|
| 🏛️ **Tunja** | Sede Central, Boyacá | Laboratorios, Comedores, Oficinas, Auditorios, Salones |
| 🏭 **Duitama** | Boyacá | Laboratorios, Comedores, Oficinas, Auditorios, Salones |
| ⛏️ **Sogamoso** | Boyacá | Laboratorios, Comedores, Oficinas, Auditorios, Salones |
| 🏔️ **Chiquinquirá** | Boyacá | Laboratorios, Comedores, Oficinas, Auditorios, Salones |

---

## 💡 Nuestra Solución

<table>
<tr>
<td align="center" width="25%">
<h3>🤖</h3>
<strong>IA Predictiva</strong>
<p>Modelos XGBoost en cascada que predicen energía → agua → CO₂</p>
</td>
<td align="center" width="25%">
<h3>🧠</h3>
<strong>IA Explicable</strong>
<p>SHAP muestra POR QUÉ la IA predice lo que predice</p>
</td>
<td align="center" width="25%">
<h3>💬</h3>
<strong>Chatbot IA</strong>
<p>Pregunta en lenguaje natural y obtén predicciones</p>
</td>
<td align="center" width="25%">
<h3>📊</h3>
<strong>Dashboard</strong>
<p>Visualización de KPIs y gráficos en tiempo real</p>
</td>
</tr>
</table>

---

## 🏗️ Arquitectura del Sistema

```
┌────────────────────────────────────────────────────────────────┐
│                        👤 USUARIO                              │
└────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌────────────────────────────────────────────────────────────────┐
│              🎨 FRONTEND (Next.js + React + Tailwind)          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │Dashboard │  │  Sedes   │  │ Sectores │  │   Chatbot    │   │
│  │  (KPIs)  │  │ (4 sedes)│  │(5 tipos) │  │  🦅 SHAP     │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │
└────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌────────────────────────────────────────────────────────────────┐
│                   🔌 API REST (Flask)                          │
│  /graficos  /predecir  /chat-groq  /generar-shap  /preguntas  │
└────────────────────────────────────────────────────────────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   XGBoost    │      │     SHAP     │      │    Groq      │
│   Models     │      │  Explainer   │      │   LLM API    │
│  (3 etapas)  │      │  (Waterfall) │      │ (qwen3-32b)  │
└──────────────┘      └──────────────┘      └──────────────┘
         │
         ▼
┌──────────────┐
│   Dataset    │
│  Histórico   │
│   Energía    │
└──────────────┘
```

---

## 📁 Estructura del Proyecto

```
demo 2/
├── 📄 README.md                          ← Estás aquí
│
├── 📂 WomanIA-Hackathon-2026-/           ← 🔧 BACKEND
│   ├── api.py                            # API Flask principal
│   ├── llm_engine.py                     # Motor ML + SHAP
│   ├── preguntas_predefinidas.py         # Lógica de predicciones
│   ├── generar_graficos.py               # Generador de datos
│   ├── requirements.txt                  # Dependencias Python
│   ├── .env                              # GROQ_API_KEY
│   ├── data/
│   │   └── dataset_energia_limpio_sectores.csv
│   └── models/
│       ├── modelo_consumo.pkl
│       ├── modelo_agua_mejorado.pkl
│       └── modelo_co2.pkl
│
└── 📂 -WomanIA-Hackathon-2026-frontend/  ← 🎨 FRONTEND
    ├── app/
    │   ├── page.tsx                      # Dashboard principal
    │   ├── layout.tsx                    # Layout global
    │   ├── globals.css                   # Estilos Tailwind
    │   ├── components/
    │   │   ├── ChatBot.jsx               # 🦅 Chatbot con SHAP
    │   │   ├── KPIBox.jsx                # Componente KPI
    │   │   └── PageTitle.jsx             # Títulos
    │   ├── sedes/page.tsx                # Vista por sedes
    │   ├── sectores/page.tsx             # Vista por sectores
    │   └── inteligencia/page.jsx         # Predicciones IA
    └── public/
        ├── eagle-mascot.png              # Mascota UPTC
        └── chat-icon.png                 # Icono chat
```

---

## 🚀 Instalación y Ejecución

### 1️⃣ Backend (API + ML)

```bash
cd WomanIA-Hackathon-2026-

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar API Key de Groq (crear archivo .env)
echo GROQ_API_KEY=tu_api_key_aqui > .env

# Ejecutar API
python api.py
```
**🌐 Backend:** `http://localhost:5000`

### 2️⃣ Frontend (Dashboard)

```bash
cd -WomanIA-Hackathon-2026-frontend

# Instalar dependencias
npm install

# Ejecutar en desarrollo
npm run dev
```
**🎨 Frontend:** `http://localhost:3000`

---

## ✨ Características Destacadas

### 🦅 Chatbot con Explicabilidad SHAP

```
┌─────────────────────────────────────────┐
│  Usuario: ¿Cuánta energía consumirá    │
│  el laboratorio de Sogamoso mañana?    │
├─────────────────────────────────────────┤
│  🤖 Bot:                                │
│                                         │
│  ⚡ Energía: 1,847 kWh                  │
│  💧 Agua: 28,450 litros                 │
│  🌱 CO₂: 523 kg                         │
│                                         │
│  🧠 Factores que más influyen:          │
│  ┌─────────────────────────────────┐   │
│  │  Hora (+245 kWh)        ████    │   │
│  │  Ocupación (+180 kWh)   ███     │   │
│  │  Temperatura (-50 kWh)  █       │   │
│  └─────────────────────────────────┘   │
│                                         │
│  💡 Recomendación: Reducir ocupación   │
│     en horas pico para ahorrar 15%     │
└─────────────────────────────────────────┘
```

### 📊 Dashboard Interactivo

- **KPIs en tiempo real**: Consumo total, agua, CO₂, eficiencia
- **Gráficos**: Por hora, por sector, tendencia semanal
- **Comparativas**: Entre sedes y sectores

---

## 🛠️ Stack Tecnológico

| Capa | Tecnologías |
|------|-------------|
| **Frontend** | Next.js 15, React 19, TypeScript, Tailwind CSS, Recharts |
| **Backend** | Python 3.10+, Flask, Flask-CORS |
| **Machine Learning** | XGBoost, SHAP, Pandas, NumPy, Scikit-learn |
| **LLM** | Groq API (qwen3-32b) - **GRATIS** |
| **Visualización** | Matplotlib, Recharts |

---

## 🌍 Impacto Esperado

<table>
<tr>
<td align="center">
<h1>💰</h1>
<h3>-25%</h3>
<p>Costos energéticos</p>
</td>
<td align="center">
<h1>🌱</h1>
<h3>-30%</h3>
<p>Huella de carbono</p>
</td>
<td align="center">
<h1>💧</h1>
<h3>-20%</h3>
<p>Consumo de agua</p>
</td>
<td align="center">
<h1>📈</h1>
<h3>92%</h3>
<p>Precisión ML</p>
</td>
</tr>
</table>

---

## 🔑 APIs y Configuración

### Variables de Entorno

```env
# Backend (.env)
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
```

### Obtener API Key de Groq (GRATIS)
1. Ir a [console.groq.com](https://console.groq.com)
2. Crear cuenta gratuita
3. Generar API Key
4. Copiar en archivo `.env`

---

## 📡 Endpoints de la API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/graficos` | Datos para gráficos del dashboard |
| `GET` | `/api/preguntas` | Preguntas predefinidas |
| `POST` | `/api/chat-groq` | Chat con IA (Groq) |
| `POST` | `/api/predecir` | Predicción ML |
| `POST` | `/api/predecir-con-shap` | Predicción + gráficos SHAP |
| `POST` | `/api/generar-shap` | Solo gráficos SHAP |
| `POST` | `/api/responder-pregunta` | Responder pregunta predefinida |

---

## 👩‍💻 Equipo

<p align="center">
  <strong>🏆 Hackathon WomenIA 2026</strong><br/>
  <em>Desarrollado con 💜 por mujeres en tecnología</em>
</p>

---

<p align="center">
  <a href="https://github.com/danimorenocr/WomenIA-hackathon-2026">
    <img src="https://img.shields.io/badge/Ver_en-GitHub-181717?style=for-the-badge&logo=github"/>
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Made_with-💜_Python_y_Next.js-D09F0A?style=for-the-badge"/>
</p>
