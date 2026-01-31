from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import random
from generar_graficos import (
    generar_consumo_total_por_sede,
    generar_tendencias_consumo_por_sede,
    generar_eficiencia_por_estudiante,
    generar_emisiones_co2_por_sede,
    generar_consumo_agua_por_sede,
    generar_temperatura_vs_consumo,
    generar_consumo_por_sector,
    generar_distribucion_consumo_por_sector,
    generar_tendencias_consumo_por_sector,
    generar_eficiencia_por_sector_y_sede,
    generar_correlacion_ocupacion_consumo,
    generar_costos_operacionales_por_sector,
    generar_impacto_ambiental_por_sector,
    generar_todos_los_graficos
)
from llm_engine import predecir_completo, SEDES, generar_shap_graficos
import os
from groq import Groq
from dotenv import load_dotenv
from preguntas_predefinidas import obtener_preguntas, responder_pregunta as responder_pregunta_predefinida

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)

# =====================================================
# RUTAS PRINCIPALES
# =====================================================

@app.route('/')
def home():
    return jsonify({
        "message": "API de Análisis Energético Universitario",
        "version": "2.0",
        "endpoints": {
            "Chat IA": "/api/chat-groq (GET/POST)",
            "Gráficos": "/api/graficos",
            "Predicción": "/api/predecir (POST)"
        }
    })

# =====================================================
# ENDPOINT PRINCIPAL: CHAT CON GROQ (GRATIS)
# =====================================================
@app.route('/api/chat-groq', methods=['GET', 'POST'])
def chat_groq():
    """
    Endpoint para conversar con Groq (GRATIS y muy rápido)
    
    GET: /api/chat-groq?mensaje=Hola
    POST Body: {"mensaje": "Hola, ¿cómo estás?"}
    """
    try:
        # Soportar GET y POST
        if request.method == 'GET':
            mensaje = request.args.get('mensaje', '')
        else:
            data = request.get_json()
            mensaje = data.get('mensaje', '') if data else ''
        
        if not mensaje:
            return jsonify({"error": "Mensaje requerido"}), 400
        
        # Configurar Groq
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        
        if not GROQ_API_KEY:
            return jsonify({
                "error": "API de Groq no configurada. Agrega GROQ_API_KEY en .env"
            }), 500
        
        client = Groq(api_key=GROQ_API_KEY)
        
        chat_completion = client.chat.completions.create(
            model="qwen/qwen3-32b",
            messages=[
                {
                    "role": "system",
                    "content": """Eres un asistente amigable especializado en análisis energético de la UPTC (Universidad Pedagógica y Tecnológica de Colombia).

La UPTC tiene 4 sedes principales:
- Tunja (sede central, Boyacá)
- Duitama (Boyacá)
- Sogamoso (Boyacá)  
- Chiquinquirá (Boyacá)

Tu rol es ayudar con consultas sobre consumo energético, agua, emisiones de CO2 y sostenibilidad en estas sedes universitarias.

Si te piden predicciones específicas de consumo, menciona que pueden usar los botones de 'Predicciones rápidas' disponibles en el chat.

Responde siempre en español de forma concisa y útil. NO inventes datos de personas ni información personal."""
                },
                {
                    "role": "user",
                    "content": mensaje
                }
            ],
            temperature=0.6,
            max_completion_tokens=1500,
            top_p=0.95
        )
        
        respuesta = chat_completion.choices[0].message.content
        
        # Limpiar la respuesta: quitar el bloque <think>...</think>
        if "<think>" in respuesta and "</think>" in respuesta:
            respuesta = respuesta.split("</think>")[-1].strip()
        
        return jsonify({
            "respuesta": respuesta,
            "modelo": "qwen/qwen3-32b"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =====================================================
# ENDPOINTS DE GRÁFICOS
# =====================================================

@app.route('/api/graficos')
def todos_graficos():
    """Retorna todos los gráficos en un solo JSON"""
    return jsonify(generar_todos_los_graficos())

@app.route('/api/consumo-por-sede')
def consumo_por_sede():
    return jsonify(generar_consumo_total_por_sede())

@app.route('/api/tendencias-consumo')
def tendencias_consumo():
    return jsonify(generar_tendencias_consumo_por_sede())

@app.route('/api/eficiencia-estudiante')
def eficiencia_estudiante():
    return jsonify(generar_eficiencia_por_estudiante())

@app.route('/api/emisiones-co2')
def emisiones_co2():
    return jsonify(generar_emisiones_co2_por_sede())

@app.route('/api/consumo-agua')
def consumo_agua():
    return jsonify(generar_consumo_agua_por_sede())

@app.route('/api/temperatura-consumo')
def temperatura_consumo():
    return jsonify(generar_temperatura_vs_consumo())

@app.route('/api/consumo-por-sector')
def consumo_por_sector():
    return jsonify(generar_consumo_por_sector())

@app.route('/api/distribucion-por-sector')
def distribucion_por_sector():
    return jsonify(generar_distribucion_consumo_por_sector())

@app.route('/api/tendencias-sector')
def tendencias_sector():
    return jsonify(generar_tendencias_consumo_por_sector())

@app.route('/api/eficiencia-sector-sede')
def eficiencia_sector_sede():
    return jsonify(generar_eficiencia_por_sector_y_sede())

@app.route('/api/correlacion-ocupacion')
def correlacion_ocupacion():
    return jsonify(generar_correlacion_ocupacion_consumo())

@app.route('/api/costos-operacionales')
def costos_operacionales():
    return jsonify(generar_costos_operacionales_por_sector())

@app.route('/api/impacto-ambiental')
def impacto_ambiental():
    return jsonify(generar_impacto_ambiental_por_sector())

# =====================================================
# ENDPOINTS INTERACTIVOS
# =====================================================

@app.route('/api/preguntas', methods=['GET'])
def preguntas():
    return jsonify({
        "preguntas": obtener_preguntas(),
        "total": len(obtener_preguntas())
    })

@app.route('/api/responder-pregunta', methods=['POST'])
def responder_pregunta_api():
    try:
        data = request.get_json()
        print(f"\n🔮 [responder-pregunta] Data recibida: {data}")
        
        if 'pregunta_id' in data:
            pregunta_id = data['pregunta_id']
            print(f"🔮 [responder-pregunta] Buscando pregunta_id: {pregunta_id}")
            preguntas_list = obtener_preguntas()
            print(f"🔮 [responder-pregunta] Preguntas disponibles: {[p['id'] for p in preguntas_list]}")
            pregunta_obj = next((p for p in preguntas_list if p['id'] == pregunta_id), None)
            
            if not pregunta_obj:
                print(f"❌ [responder-pregunta] Pregunta ID {pregunta_id} NO encontrada")
                return jsonify({"error": f"Pregunta con ID {pregunta_id} no encontrada"}), 404
            
            pregunta_texto = pregunta_obj['pregunta']
            print(f"✅ [responder-pregunta] Pregunta encontrada: {pregunta_texto}")
        elif 'pregunta' in data:
            pregunta_texto = data['pregunta']
            print(f"🔮 [responder-pregunta] Pregunta directa: {pregunta_texto}")
        else:
            print(f"❌ [responder-pregunta] No se encontró pregunta_id ni pregunta en data")
            return jsonify({"error": "Se requiere 'pregunta_id' o 'pregunta'"}), 400
        
        print(f"🔮 [responder-pregunta] Llamando a responder_pregunta_predefinida...")
        resultado = responder_pregunta_predefinida(pregunta_texto)
        print(f"✅ [responder-pregunta] Resultado: {resultado}")
        return jsonify(resultado)
    
    except Exception as e:
        import traceback
        print(f"❌ [responder-pregunta] ERROR: {str(e)}")
        print(f"❌ [responder-pregunta] Traceback:\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint de chat para predicciones energéticas"""
    try:
        data = request.get_json()
        pregunta = data.get('pregunta', '')
        
        if not pregunta:
            return jsonify({"error": "Pregunta requerida"}), 400
        
        resultado = responder_pregunta_predefinida(pregunta)
        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/predecir', methods=['POST'])
def predecir():
    """Endpoint de predicción ML completa"""
    try:
        data = request.get_json()
        
        required = ['sede_id', 'sector', 'hora', 'dia_semana', 'temperatura', 'ocupacion']
        for param in required:
            if param not in data:
                return jsonify({"error": f"Parámetro '{param}' requerido"}), 400
        
        resultado = predecir_completo(
            sede_id=data['sede_id'],
            sector=data['sector'],
            hora=data['hora'],
            dia_semana=data['dia_semana'],
            temperatura=data['temperatura'],
            ocupacion=data['ocupacion']
        )
        
        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/predecir-con-shap', methods=['POST'])
def predecir_con_shap():
    """Endpoint de predicción ML con gráficos SHAP de explicabilidad"""
    try:
        data = request.get_json()
        
        required = ['sede_id', 'sector', 'hora', 'dia_semana', 'temperatura', 'ocupacion']
        for param in required:
            if param not in data:
                return jsonify({"error": f"Parámetro '{param}' requerido"}), 400
        
        # Obtener predicción
        resultado = predecir_completo(
            sede_id=data['sede_id'],
            sector=data['sector'],
            hora=data['hora'],
            dia_semana=data['dia_semana'],
            temperatura=data['temperatura'],
            ocupacion=data['ocupacion']
        )
        
        # Generar gráficos SHAP
        shap_graficos = generar_shap_graficos(
            sede_id=data['sede_id'],
            sector=data['sector'],
            hora=data['hora'],
            dia_semana=data['dia_semana'],
            temperatura=data['temperatura'],
            ocupacion=data['ocupacion']
        )
        
        # Combinar resultados
        resultado['shap_graficos'] = shap_graficos
        
        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/generar-shap', methods=['POST'])
def generar_shap_endpoint():
    """Endpoint para generar SOLO los gráficos SHAP (se llama después de la predicción)"""
    try:
        data = request.get_json()
        print(f"🎨 [generar-shap] Generando gráficos SHAP...")
        
        required = ['sede_id', 'sector', 'hora', 'dia_semana', 'temperatura', 'ocupacion']
        for param in required:
            if param not in data:
                return jsonify({"error": f"Parámetro '{param}' requerido"}), 400
        
        # Generar solo los gráficos SHAP
        shap_graficos = generar_shap_graficos(
            sede_id=data['sede_id'],
            sector=data['sector'],
            hora=data['hora'],
            dia_semana=data['dia_semana'],
            temperatura=data['temperatura'],
            ocupacion=data['ocupacion']
        )
        
        print(f"✅ [generar-shap] Gráficos SHAP generados correctamente")
        return jsonify({"shap_graficos": shap_graficos})
    
    except Exception as e:
        print(f"❌ [generar-shap] Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# =====================================================
# INICIAR SERVIDOR
# =====================================================
if __name__ == '__main__':
    print("=" * 50)
    print("🚀 API DE ANÁLISIS ENERGÉTICO v2.0")
    print("=" * 50)
    print("\n📡 Servidor: http://localhost:5000")
    print("\n🤖 Chat IA (Groq): /api/chat-groq")
    print("📊 Gráficos: /api/graficos")
    print("🔮 Predicción: /api/predecir")
    print("📈 Predicción + SHAP: /api/predecir-con-shap")
    print("\n" + "=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
