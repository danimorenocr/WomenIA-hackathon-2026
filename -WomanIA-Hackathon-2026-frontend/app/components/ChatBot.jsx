'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';

const API_BASE = "http://localhost:5000/api";

export default function ChatBot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [preguntasPredefinidas, setPreguntasPredefinidas] = useState([]);
  const [imagenAmpliada, setImagenAmpliada] = useState(null);

  // Cargar preguntas predefinidas al abrir el chat
  useEffect(() => {
    if (isOpen && preguntasPredefinidas.length === 0) {
      fetch(`${API_BASE}/preguntas`)
        .then(res => res.json())
        .then(data => {
          if (data.preguntas) {
            setPreguntasPredefinidas(data.preguntas);
          }
        })
        .catch(err => console.error('Error cargando preguntas:', err));
    }
  }, [isOpen]);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  // Enviar pregunta predefinida (predicción primero, SHAP después)
  const sendPredefinedQuestion = async (pregunta) => {
    if (isLoading) return;
    
    setMessages(prev => [...prev, { text: pregunta.pregunta, sender: 'user' }]);
    setIsLoading(true);
    
    try {
      const response = await fetch(`${API_BASE}/responder-pregunta`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ pregunta_id: pregunta.id }),
      });

      const data = await response.json();

      if (response.ok && data.respuesta) {
        // Primero mostrar la predicción SIN SHAP
        const messageIndex = messages.length + 1; // índice del nuevo mensaje
        setMessages(prev => [...prev, { 
          text: data.respuesta, 
          sender: 'bot',
          prediccion: data.prediccion || null,
          shap_graficos: null,  // inicialmente null
          cargandoShap: true    // indicador de carga SHAP
        }]);
        
        setIsLoading(false); // Liberar el loading para que usuario pueda seguir
        
        // Luego cargar SHAP en background
        if (data.sede_id && data.sector && data.hora !== undefined) {
          try {
            const shapResponse = await fetch(`${API_BASE}/generar-shap`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                sede_id: data.sede_id,
                sector: data.sector,
                hora: data.hora,
                dia_semana: data.dia_semana,
                temperatura: data.temperatura,
                ocupacion: data.ocupacion
              }),
            });
            
            const shapData = await shapResponse.json();
            
            if (shapResponse.ok && shapData.shap_graficos) {
              // Actualizar el mensaje con los gráficos SHAP
              setMessages(prev => prev.map((msg, idx) => 
                idx === messageIndex 
                  ? { ...msg, shap_graficos: shapData.shap_graficos, cargandoShap: false }
                  : msg
              ));
            } else {
              // Quitar el indicador de carga si falla
              setMessages(prev => prev.map((msg, idx) => 
                idx === messageIndex 
                  ? { ...msg, cargandoShap: false }
                  : msg
              ));
            }
          } catch (shapError) {
            console.error('Error cargando SHAP:', shapError);
            setMessages(prev => prev.map((msg, idx) => 
              idx === messageIndex 
                ? { ...msg, cargandoShap: false }
                : msg
            ));
          }
        }
      } else {
        setMessages(prev => [...prev, { 
          text: data.error || 'Error al obtener predicción.', 
          sender: 'bot' 
        }]);
        setIsLoading(false);
      }
    } catch (error) {
      setMessages(prev => [...prev, { 
        text: 'Error de conexión. Verifica que la API esté corriendo en localhost:5000', 
        sender: 'bot' 
      }]);
      setIsLoading(false);
    }
  };

  const sendMessage = async () => {
    if (inputMessage.trim() && !isLoading) {
      const userMessage = inputMessage.trim();
      setMessages(prev => [...prev, { text: userMessage, sender: 'user' }]);
      setInputMessage('');
      setIsLoading(true);
      
      try {
        const response = await fetch(`${API_BASE}/chat-groq`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ mensaje: userMessage }),
        });

        const data = await response.json();

        if (response.ok && data.respuesta) {
          setMessages(prev => [...prev, { 
            text: data.respuesta, 
            sender: 'bot' 
          }]);
        } else {
          setMessages(prev => [...prev, { 
            text: data.error || 'Error al obtener respuesta del servidor.', 
            sender: 'bot' 
          }]);
        }
      } catch (error) {
        setMessages(prev => [...prev, { 
          text: 'Error de conexión. Verifica que la API esté corriendo en localhost:5000', 
          sender: 'bot' 
        }]);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <>
      {/* Botón flotante del chatbot con mascota águila */}
      <button
        onClick={toggleChat}
        className="fixed bottom-6 right-6 z-50 bg-gradient-to-br from-yellow-200 to-yellow-300 hover:from-yellow-300 hover:to-yellow-400 text-gray-800 rounded-full  shadow-xl transition-all duration-300 hover:scale-110 border-2 border-yellow-400"
        aria-label="Abrir chat"
      >
        <div className="relative">
          <Image
            src="/chat-icon.png"
            alt="Chatbot UPTC"
            width={60}
            height={60}
            className="rounded-full"
          />
          <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-400 rounded-full border-2 border-white animate-pulse"></div>
        </div>
      </button>

      {/* Ventana del chat */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 z-50 w-96 h-[600px] bg-gradient-to-b from-yellow-50 to-white rounded-[2.5rem] shadow-2xl flex flex-col border-2 border-yellow-200 backdrop-blur-sm">
          {/* Header del chat */}
          <div className="bg-gradient-to-r from-yellow-200 to-yellow-300 text-gray-800 p-6 rounded-t-[2.5rem] flex justify-between items-center border-b-2 border-yellow-300">
            <div className="flex items-center gap-3">
              <div className="relative">
                <Image
                  src="/chat-icon.png"
                  alt="Chatbot UPTC"
                  width={40}
                  height={40}
                  className="rounded-full border-2 border-white shadow-md"
                />
                <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-400 rounded-full border-2 border-white"></div>
              </div>
              <div>
                <h3 className="font-bold text-xl text-gray-800">CHATBOT</h3>
                <p className="text-xs text-gray-600">Asistente UPTC 🦅</p>
              </div>
            </div>
            <button
              onClick={toggleChat}
              className="w-8 h-8 bg-white/80 hover:bg-white rounded-full flex items-center justify-center text-gray-700 hover:text-gray-900 transition-all duration-200 shadow-md"
              aria-label="Cerrar chat"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Mensajes */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gradient-to-b from-transparent to-yellow-50/30">
            {messages.length === 0 ? (
              <div className="flex flex-col items-center text-center">
                <div className="mb-3 relative">
                  <Image
                    src="/eagle-mascot.png"
                    alt="Mascota UPTC"
                    width={80}
                    height={80}
                    className="rounded-2xl shadow-lg"
                  />
                  <div className="absolute -top-2 -right-2 bg-yellow-400 text-white text-xs px-2 py-1 rounded-full font-bold">
                    UPTC
                  </div>
                </div>
                <div className="bg-gradient-to-r from-yellow-100 to-yellow-200 rounded-2xl p-3 max-w-xs border-2 border-yellow-300 shadow-md mb-4">
                  <p className="text-sm font-bold text-gray-800 mb-1">¡Hola! 👋</p>
                  <p className="text-gray-700 text-xs leading-relaxed">
                    Soy tu asistente energético. ¡Pregúntame lo que quieras o elige una predicción! 🦅⚡
                  </p>
                </div>
                
                {/* Preguntas predefinidas */}
                {preguntasPredefinidas.length > 0 && (
                  <div className="w-full space-y-2">
                    <p className="text-xs font-semibold text-gray-600 mb-2">📊 Predicciones rápidas:</p>
                    {preguntasPredefinidas.map((pregunta) => (
                      <button
                        key={pregunta.id}
                        onClick={() => sendPredefinedQuestion(pregunta)}
                        disabled={isLoading}
                        className="w-full text-left px-3 py-2 bg-white hover:bg-yellow-50 border-2 border-yellow-200 hover:border-yellow-400 rounded-xl text-xs text-gray-700 transition-all duration-200 shadow-sm hover:shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        🔮 {pregunta.pregunta}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            ) : (
              messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex items-end gap-3 ${
                    message.sender === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  {/* Foto del emisor para mensajes del bot */}
                  {message.sender === 'bot' && (
                    <div className="relative">
                      <Image
                        src="/eagle-mascot.png"
                        alt="Bot UPTC"
                        width={36}
                        height={36}
                        className="rounded-2xl shadow-md border-2 border-yellow-300"
                      />
                      <div className="absolute -bottom-1 -right-1 text-xs bg-yellow-400 text-white rounded-full w-5 h-5 flex items-center justify-center font-bold">
                        U
                      </div>
                    </div>
                  )}
                  
                  {/* Burbuja del mensaje */}
                  <div
                    className={`max-w-[85%] px-5 py-4 rounded-3xl shadow-md border-2 ${
                      message.sender === 'user'
                        ? 'bg-gradient-to-br from-yellow-300 to-yellow-400 text-gray-800 rounded-br-md border-yellow-400'
                        : 'bg-gradient-to-br from-white to-yellow-50 text-gray-800 rounded-bl-md border-yellow-200'
                    }`}
                  >
                    <div 
                      className="text-sm leading-relaxed font-medium whitespace-pre-line"
                      dangerouslySetInnerHTML={{
                        __html: message.text
                          .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                          .replace(/\n/g, '<br/>')
                      }}
                    />
                    
                    {/* Indicador de carga SHAP */}
                    {message.cargandoShap && (
                      <div className="mt-4 pt-4 border-t border-yellow-200">
                        <div className="flex items-center gap-2 text-xs text-gray-500">
                          <div className="flex gap-1">
                            <span className="w-1.5 h-1.5 bg-[#2E27B1] rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                            <span className="w-1.5 h-1.5 bg-[#2E27B1] rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                            <span className="w-1.5 h-1.5 bg-[#2E27B1] rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                          </div>
                          <span className="font-medium">🧠 Generando explicabilidad SHAP...</span>
                        </div>
                      </div>
                    )}
                    
                    {/* Gráficas SHAP de explicabilidad */}
                    {message.shap_graficos && !message.shap_graficos.error && (
                      <div className="mt-4 pt-4 border-t border-yellow-200">
                        <p className="text-xs font-bold text-gray-600 mb-2">🧠 Explicabilidad IA (SHAP)</p>
                        <div className="space-y-3">
                          {message.shap_graficos.consumo_energia?.imagen_base64 && (
                            <div>
                              <p className="text-xs text-gray-500 mb-1">⚡ Factores del consumo energético:</p>
                              <img 
                                src={`data:image/png;base64,${message.shap_graficos.consumo_energia.imagen_base64}`} 
                                alt="SHAP Energía" 
                                className="w-full rounded-lg shadow-sm cursor-pointer hover:opacity-80 transition-opacity"
                                onClick={() => setImagenAmpliada({
                                  src: `data:image/png;base64,${message.shap_graficos.consumo_energia.imagen_base64}`,
                                  titulo: '⚡ SHAP - Consumo Energético'
                                })}
                              />
                            </div>
                          )}
                          {message.shap_graficos.consumo_agua?.imagen_base64 && (
                            <div>
                              <p className="text-xs text-gray-500 mb-1">💧 Factores del consumo de agua:</p>
                              <img 
                                src={`data:image/png;base64,${message.shap_graficos.consumo_agua.imagen_base64}`} 
                                alt="SHAP Agua" 
                                className="w-full rounded-lg shadow-sm cursor-pointer hover:opacity-80 transition-opacity"
                                onClick={() => setImagenAmpliada({
                                  src: `data:image/png;base64,${message.shap_graficos.consumo_agua.imagen_base64}`,
                                  titulo: '💧 SHAP - Consumo de Agua'
                                })}
                              />
                            </div>
                          )}
                          {message.shap_graficos.emisiones_co2?.imagen_base64 && (
                            <div>
                              <p className="text-xs text-gray-500 mb-1">🌱 Factores de emisiones CO₂:</p>
                              <img 
                                src={`data:image/png;base64,${message.shap_graficos.emisiones_co2.imagen_base64}`} 
                                alt="SHAP CO2" 
                                className="w-full rounded-lg shadow-sm cursor-pointer hover:opacity-80 transition-opacity"
                                onClick={() => setImagenAmpliada({
                                  src: `data:image/png;base64,${message.shap_graficos.emisiones_co2.imagen_base64}`,
                                  titulo: '🌱 SHAP - Emisiones CO₂'
                                })}
                              />
                            </div>
                          )}
                        </div>
                        <p className="text-xs text-gray-400 mt-2 text-center">Haz clic en una gráfica para ampliar</p>
                      </div>
                    )}
                  </div>

                </div>
              ))
            )}
            {/* Indicador de escribiendo */}
            {isLoading && (
              <div className="flex items-end gap-3 justify-start">
                <div className="relative">
                  <Image
                    src="/eagle-mascot.png"
                    alt="Bot UPTC"
                    width={36}
                    height={36}
                    className="rounded-2xl shadow-md border-2 border-yellow-300"
                  />
                </div>
                <div className="bg-gradient-to-br from-white to-yellow-50 text-gray-800 rounded-3xl rounded-bl-md border-2 border-yellow-200 px-5 py-4 shadow-md">
                  <div className="flex gap-1">
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Input de mensaje */}
          <div className="bg-gradient-to-r from-yellow-100 to-yellow-200 border-t-2 border-yellow-300 p-4 rounded-b-[2.5rem]">
            <div className="flex gap-2 items-center">
              <div className="relative flex-1">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder={isLoading ? "Esperando respuesta..." : "Escribe tu mensaje..."}
                  disabled={isLoading}
                  className="w-full px-5 py-4 pr-12 border-2 border-yellow-300 rounded-full focus:outline-none focus:border-yellow-400 bg-white text-gray-800 placeholder-gray-500 shadow-inner font-medium disabled:bg-gray-100 disabled:cursor-not-allowed"
                />
               
              </div>
              <button
                onClick={sendMessage}
                disabled={isLoading || !inputMessage.trim()}
                className="bg-gradient-to-br from-yellow-400 to-yellow-500 hover:from-yellow-500 hover:to-yellow-600 text-gray-800 px-5 py-4 rounded-full transition-all duration-200 flex items-center justify-center shadow-lg hover:shadow-xl transform hover:scale-105 border-2 border-yellow-400 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal para imagen ampliada */}
      {imagenAmpliada && (
        <div 
          className="fixed inset-0 z-[100] bg-black/80 flex items-center justify-center p-4"
          onClick={() => setImagenAmpliada(null)}
        >
          <div 
            className="bg-white rounded-2xl max-w-4xl max-h-[90vh] overflow-auto shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="sticky top-0 bg-gradient-to-r from-[#040959] to-[#2E27B1] text-white p-4 rounded-t-2xl flex justify-between items-center">
              <h3 className="font-bold">{imagenAmpliada.titulo}</h3>
              <button 
                onClick={() => setImagenAmpliada(null)}
                className="w-8 h-8 bg-white/20 hover:bg-white/30 rounded-full flex items-center justify-center transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="p-4">
              <img 
                src={imagenAmpliada.src} 
                alt={imagenAmpliada.titulo}
                className="w-full h-auto rounded-lg"
              />
              <p className="text-xs text-gray-500 mt-3 text-center">
                Los valores positivos (rojos) aumentan la predicción, los negativos (azules) la disminuyen.
              </p>
            </div>
          </div>
        </div>
      )}
    </>
  );
}