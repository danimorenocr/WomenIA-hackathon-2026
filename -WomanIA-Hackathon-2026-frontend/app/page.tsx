"use client";

import { useEffect, useState } from "react";
import PageTitle from "./components/PageTitle";
import Image from "next/image";

const API_BASE = "http://localhost:5000/api";

interface ConsumoSede {
  sede: string;
  consumo_total_kwh: number;
  consumo_promedio_kwh: number;
}

interface AguaSede {
  sede: string;
  agua_total_m3: number;
  agua_promedio_litros_hora: number;
}

interface EmisionSede {
  sede: string;
  co2_total_toneladas: number;
  co2_promedio_kg_hora: number;
}

interface CostoSector {
  sector: string;
  costo_total_cop: number;
  costo_promedio_kwh_cop: number;
}

interface DistribucionSector {
  sector: string;
  consumo_kwh: number;
  porcentaje: number;
}

export default function Home() {
  const [consumoSede, setConsumoSede] = useState<ConsumoSede[]>([]);
  const [aguaSede, setAguaSede] = useState<AguaSede[]>([]);
  const [emisionesSede, setEmisionesSede] = useState<EmisionSede[]>([]);
  const [costosSector, setCostosSector] = useState<CostoSector[]>([]);
  const [distribucionSector, setDistribucionSector] = useState<DistribucionSector[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function cargarDatos() {
      try {
        setLoading(true);
        const [consumoRes, aguaRes, emisionesRes, costosRes, distribucionRes] = await Promise.all([
          fetch(`${API_BASE}/consumo-por-sede`),
          fetch(`${API_BASE}/consumo-agua`),
          fetch(`${API_BASE}/emisiones-co2`),
          fetch(`${API_BASE}/costos-operacionales`),
          fetch(`${API_BASE}/distribucion-por-sector`),
        ]);

        if (!consumoRes.ok || !aguaRes.ok || !emisionesRes.ok || !costosRes.ok || !distribucionRes.ok) {
          throw new Error("Error al cargar datos del dashboard");
        }

        const consumoData = await consumoRes.json();
        const aguaData = await aguaRes.json();
        const emisionesData = await emisionesRes.json();
        const costosData = await costosRes.json();
        const distribucionData = await distribucionRes.json();

        setConsumoSede(consumoData.data || []);
        setAguaSede(aguaData.data || []);
        setEmisionesSede(emisionesData.data || []);
        setCostosSector(costosData.data || []);
        setDistribucionSector(distribucionData.data || []);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Error desconocido");
      } finally {
        setLoading(false);
      }
    }

    cargarDatos();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando indicadores...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center text-red-600">
          <p className="text-xl font-semibold">Error</p>
          <p>{error}</p>
          <p className="text-sm text-gray-500 mt-2">Verifica que la API esté corriendo en localhost:5000</p>
        </div>
      </div>
    );
  }

  // 📊 KPIs globales
  const totalEnergia = consumoSede.reduce(
    (acc, s) => acc + s.consumo_total_kwh,
    0,
  );

  const totalAgua = aguaSede.reduce(
    (acc, s) => acc + s.agua_total_m3,
    0,
  );

  const totalCO2 = emisionesSede.reduce(
    (acc, s) => acc + s.co2_total_toneladas,
    0,
  );

  const totalCosto = costosSector.reduce(
    (acc, s) => acc + s.costo_total_cop,
    0,
  );

  const sedeMayorConsumo = consumoSede.length > 0
    ? consumoSede.reduce((max, curr) =>
        curr.consumo_total_kwh > max.consumo_total_kwh ? curr : max
      )
    : { sede: "N/A", consumo_total_kwh: 0 };

  const sectorMayorConsumo = distribucionSector.length > 0
    ? distribucionSector.reduce((max, curr) =>
        curr.consumo_kwh > max.consumo_kwh ? curr : max
      )
    : { sector: "N/A", consumo_kwh: 0 };

  return (
    <div className="space-y-8 p-6">
      <PageTitle
        title="VISIÓN GENERAL"
        subtitle="Estado global del consumo y la sostenibilidad energética de la UPTC"
      />

      <div className="flex flex-col lg:flex-row gap-8 items-start">
        {/* KPIs principales */}
        <div className="flex-1 space-y-6">
          {/* Fila de KPIs principales */}
          <div className="grid grid-cols-2 xl:grid-cols-4 gap-4">
            <div className="bg-[#BCBEDA] rounded-2xl p-5 shadow-md text-center">
              <p className="text-xs text-slate-600 mb-1">⚡ Energía total</p>
              <h2 className="text-3xl font-bold text-[#040959]">{(totalEnergia / 1000).toFixed(1)}</h2>
              <p className="text-sm text-slate-700">MWh</p>
            </div>
            
            <div className="bg-[#BCBEDA] rounded-2xl p-5 shadow-md text-center">
              <p className="text-xs text-slate-600 mb-1">💧 Agua total</p>
              <h2 className="text-3xl font-bold text-[#040959]">{totalAgua.toFixed(0)}</h2>
              <p className="text-sm text-slate-700">m³</p>
            </div>
            
            <div className="bg-[#BCBEDA] rounded-2xl p-5 shadow-md text-center">
              <p className="text-xs text-slate-600 mb-1">🌱 CO₂ total</p>
              <h2 className="text-3xl font-bold text-[#040959]">{totalCO2.toFixed(1)}</h2>
              <p className="text-sm text-slate-700">toneladas</p>
            </div>
            
            <div className="bg-[#BCBEDA] rounded-2xl p-5 shadow-md text-center">
              <p className="text-xs text-slate-600 mb-1">💰 Costo total</p>
              <h2 className="text-3xl font-bold text-[#040959]">${(totalCosto / 1_000_000).toFixed(1)}M</h2>
              <p className="text-sm text-slate-700">COP</p>
            </div>
          </div>

          {/* Alertas / Destacados */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-white rounded-2xl p-6 shadow-md border-l-4 border-[#F28705]">
              <div className="flex items-center gap-3">
                <span className="text-3xl">🏛️</span>
                <div>
                  <p className="text-xs text-slate-500 uppercase tracking-wide">Sede con mayor consumo</p>
                  <h3 className="text-2xl font-bold text-[#040959]">{sedeMayorConsumo.sede}</h3>
                  <p className="text-sm text-[#F28705]">{sedeMayorConsumo.consumo_total_kwh.toLocaleString()} kWh</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white rounded-2xl p-6 shadow-md border-l-4 border-[#D09F0A]">
              <div className="flex items-center gap-3">
                <span className="text-3xl">⚠️</span>
                <div>
                  <p className="text-xs text-slate-500 uppercase tracking-wide">Sector crítico</p>
                  <h3 className="text-2xl font-bold text-[#040959]">{sectorMayorConsumo.sector}</h3>
                  <p className="text-sm text-[#D09F0A]">{sectorMayorConsumo.consumo_kwh.toLocaleString()} kWh</p>
                </div>
              </div>
            </div>
          </div>

          {/* Resumen rápido */}
          <div className="bg-[#BCBEDA] rounded-2xl p-6 shadow-xl text-white">
            <h3 className="text-lg font-bold mb-4 text-[#040959]">📊 Resumen de sedes</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {consumoSede.map((sede) => (
                <div key={sede.sede} className="bg-white rounded-xl p-3 backdrop-blur-sm">
                  <p className="text-xs text-[#040959]">{sede.sede}</p>
                  <p className="text-lg font-bold text-[#040959]">{(sede.consumo_total_kwh / 1000).toFixed(1)} MWh</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Mascota */}
        <div className="hidden lg:flex flex-col items-center">
          <div className="relative">
            <Image 
              src="/eagle-mascot.png" 
              width={220} 
              height={280} 
              alt="Mascota UPTC"
              className="drop-shadow-2xl"
            />
            <div className="absolute -bottom-4 left-1/2 transform -translate-x-1/2 bg-[#F28705] text-white px-4 py-2 rounded-full text-sm font-bold shadow-lg">
              🦅 UPTC 
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
