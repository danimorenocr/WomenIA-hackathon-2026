<p align="center">
  <img src="https://img.shields.io/badge/🦅-UPTC_Energy_Dashboard-040959?style=for-the-badge&labelColor=FFE66B" alt="UPTC Dashboard"/>
</p>

<h1 align="center">🎨 EcoUPTC - Frontend Dashboard</h1>

<p align="center">
  <strong>📊 Panel de Control Inteligente para la Gestión Energética Universitaria</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Next.js-15-000000?style=flat-square&logo=nextdotjs&logoColor=white"/>
  <img src="https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black"/>
  <img src="https://img.shields.io/badge/TypeScript-5.0-3178C6?style=flat-square&logo=typescript&logoColor=white"/>
  <img src="https://img.shields.io/badge/Tailwind-CSS-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white"/>
  <img src="https://img.shields.io/badge/Recharts-Visualización-FF6B6B?style=flat-square"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/WomenIA-Hackathon_2026-D09F0A?style=for-the-badge"/>
</p>

---

## ✨ Vista Previa

<table>
<tr>
<td align="center" width="50%">

### 📊 Dashboard Principal
Panel con KPIs en tiempo real, gráficos de consumo y tendencias energéticas.

</td>
<td align="center" width="50%">

### 🦅 Chatbot IA
Asistente inteligente con predicciones y explicabilidad SHAP visual.

</td>
</tr>
<tr>
<td align="center">

### 🏛️ Vista por Sedes
Análisis detallado por cada sede de la UPTC (Tunja, Duitama, Sogamoso, Chiquinquirá).

</td>
<td align="center">

### 🏢 Vista por Sectores
Comparativa entre Laboratorios, Comedores, Oficinas, Auditorios y Salones.

</td>
</tr>
</table>

---

## 🎯 Características Principales

<table>
<tr>
<td width="33%" align="center">
<h3>📈</h3>
<strong>Gráficos Interactivos</strong>
<p>Visualizaciones dinámicas con Recharts que responden en tiempo real</p>
</td>
<td width="33%" align="center">
<h3>🤖</h3>
<strong>Chatbot Inteligente</strong>
<p>Predicciones instantáneas con explicabilidad SHAP integrada</p>
</td>
<td width="33%" align="center">
<h3>📱</h3>
<strong>Diseño Responsivo</strong>
<p>Adaptable a cualquier dispositivo: desktop, tablet y móvil</p>
</td>
</tr>
<tr>
<td width="33%" align="center">
<h3>⚡</h3>
<strong>KPIs en Vivo</strong>
<p>Métricas clave actualizadas desde la API del backend</p>
</td>
<td width="33%" align="center">
<h3>🧠</h3>
<strong>IA Explicable</strong>
<p>Gráficos SHAP que muestran POR QUÉ la IA predice lo que predice</p>
</td>
<td width="33%" align="center">
<h3>🎨</h3>
<strong>UI/UX Moderno</strong>
<p>Paleta de colores institucional UPTC con glassmorphism</p>
</td>
</tr>
</table>

---

## 🖥️ Páginas del Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│  🏠 /                    Dashboard Principal                │
│  ├── KPIs: Consumo total, Agua, CO₂, Eficiencia            │
│  ├── Gráfico: Consumo por hora del día                     │
│  ├── Gráfico: Distribución por sector                      │
│  └── Gráfico: Tendencia semanal                            │
├─────────────────────────────────────────────────────────────┤
│  🏛️ /sedes              Análisis por Sedes                 │
│  ├── Tunja (Central) | Duitama | Sogamoso | Chiquinquirá   │
│  ├── Consumo energético por sede                           │
│  └── Consumo de agua por sede                              │
├─────────────────────────────────────────────────────────────┤
│  🏢 /sectores           Análisis por Sectores              │
│  ├── Laboratorios | Comedores | Oficinas                   │
│  ├── Auditorios | Salones                                  │
│  └── Comparativa de eficiencia                             │
├─────────────────────────────────────────────────────────────┤
│  🧠 /inteligencia       Predicciones IA                    │
│  └── Formulario de predicción con SHAP                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🦅 Chatbot con SHAP

El chatbot incluye:

1. **💬 Chat libre** con Groq LLM (qwen3-32b)
2. **🔮 Preguntas predefinidas** para predicciones rápidas
3. **📊 Gráficos SHAP** que explican cada predicción
4. **🔍 Modal de ampliación** para ver detalles

```
┌─────────────────────────────────────┐
│  🦅 CHATBOT UPTC                    │
├─────────────────────────────────────┤
│  Usuario: ¿Cuánta energía          │
│  consumirá el laboratorio de        │
│  la sede 3 mañana a las 5pm?       │
├─────────────────────────────────────┤
│  Bot: ⚡ Predicción para            │
│  Laboratorios en Sogamoso:          │
│                                     │
│  💡 Energía: 1,847.32 kWh          │
│  💧 Agua: 28,450 litros            │
│  🌱 CO₂: 523.18 kg                 │
│                                     │
│  🧠 Generando explicabilidad...    │
│  [████████████░░░░░░]              │
│                                     │
│  📊 SHAP - Factores:               │
│  ┌─────────────────────┐           │
│  │ [Gráfico Waterfall] │  ← Click  │
│  └─────────────────────┘    para   │
│                             ampliar │
└─────────────────────────────────────┘
```

---

## 🎨 Paleta de Colores UPTC

```css
/* Colores institucionales */
--azul-oscuro:   #040959;  /* Fondos principales */
--azul-medio:    #2E27B1;  /* Acentos */
--naranja:       #F28705;  /* CTAs, alertas */
--dorado:        #D09F0A;  /* Badges, destacados */
--amarillo:      #FFE66B;  /* Backgrounds claros */
--lila:          #BCBEDA;  /* Bordes suaves */
```

---

## 🚀 Instalación Rápida

```bash
# 1. Navegar a la carpeta frontend
cd -WomanIA-Hackathon-2026-frontend

# 2. Instalar dependencias
npm install

# 3. Ejecutar en desarrollo
npm run dev

# 4. Abrir en navegador
# → http://localhost:3000
```

> ⚠️ **Importante:** Asegúrate de que el backend esté corriendo en `http://localhost:5000`

---

## 📁 Estructura del Proyecto

```
-WomanIA-Hackathon-2026-frontend/
├── 📂 app/
│   ├── 🎨 globals.css           # Estilos globales + Tailwind
│   ├── 📄 layout.tsx            # Layout principal
│   ├── 📄 page.tsx              # Dashboard principal
│   ├── 📂 components/
│   │   ├── 🦅 ChatBot.jsx       # Chatbot con SHAP
│   │   ├── 📊 KPIBox.jsx        # Componente de KPI
│   │   └── 📝 PageTitle.jsx     # Títulos de página
│   ├── 📂 sedes/
│   │   └── page.tsx             # Vista por sedes
│   ├── 📂 sectores/
│   │   └── page.tsx             # Vista por sectores
│   └── 📂 inteligencia/
│       └── page.jsx             # Predicciones IA
├── 📂 public/
│   ├── 🦅 eagle-mascot.png      # Mascota UPTC
│   └── 💬 chat-icon.png         # Icono del chat
├── 📄 package.json
├── 📄 tailwind.config.js
├── 📄 tsconfig.json
└── 📄 next.config.ts
```

---

## 🛠️ Tecnologías

<p align="center">
  <img src="https://skillicons.dev/icons?i=nextjs,react,typescript,tailwind" alt="Tech Stack"/>
</p>

| Tecnología | Versión | Uso |
|------------|---------|-----|
| **Next.js** | 15.x | Framework React con SSR |
| **React** | 19.x | Librería UI |
| **TypeScript** | 5.x | Tipado estático |
| **Tailwind CSS** | 4.x | Estilos utilitarios |
| **Recharts** | 2.x | Gráficos interactivos |
| **Lucide React** | - | Iconos modernos |

---

## 🔗 Conexión con Backend

El frontend se comunica con la API a través de:

```javascript
const API_BASE = "http://localhost:5000/api";

// Endpoints consumidos:
fetch(`${API_BASE}/graficos`)         // Datos de gráficos
fetch(`${API_BASE}/preguntas`)        // Preguntas predefinidas
fetch(`${API_BASE}/chat-groq`)        // Chat IA
fetch(`${API_BASE}/responder-pregunta`) // Predicciones
fetch(`${API_BASE}/generar-shap`)     // Gráficos SHAP
```

---

## 📱 Responsive Design

<table>
<tr>
<td align="center">
<h3>🖥️ Desktop</h3>
<p>Grids de 3-4 columnas<br/>Sidebar expandido</p>
</td>
<td align="center">
<h3>📱 Tablet</h3>
<p>Grids de 2 columnas<br/>Sidebar colapsable</p>
</td>
<td align="center">
<h3>📲 Mobile</h3>
<p>Stack vertical<br/>Navegación hamburguesa</p>
</td>
</tr>
</table>

---

## 🎯 Características Destacadas

### ⚡ Predicción Asíncrona
```
1. Usuario hace pregunta
2. ✅ Predicción aparece INSTANTÁNEAMENTE
3. 🔄 "Generando explicabilidad SHAP..."
4. ✅ Gráficos SHAP aparecen sin bloquear
```

### 🔍 Modal de SHAP
- Click en cualquier gráfico para ampliar
- Explicación de colores (rojo↑ / azul↓)
- Visualización de factores más influyentes

---

## 👩‍💻 Equipo WomenIA

<p align="center">
  <strong>Hackathon WomenIA 2026</strong><br/>
  Desarrollado con 💜 por mujeres en tecnología
</p>

<p align="center">
  <a href="https://github.com/danimorenocr/WomenIA-hackathon-2026">
    <img src="https://img.shields.io/badge/GitHub-Repositorio-181717?style=for-the-badge&logo=github"/>
  </a>
</p>

---

<p align="center">
  <img src="https://img.shields.io/badge/Hecho_con-💜_Next.js_y_☕-D09F0A?style=for-the-badge"/>
</p>
