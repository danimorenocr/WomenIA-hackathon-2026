"use client";

import { useState, useEffect } from "react";
import PageTitle from "../components/PageTitle";


import {
  BarChart,
  Bar,
  LineChart,
  Line,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area,
  Cell,
} from "recharts";

const API_BASE = "http://127.0.0.1:5000/api";

const CAMPUS_COLORS: Record<string, string> = {
  Tunja: "#040959",
  Duitama: "#F28705",
  Sogamoso: "#D09F0A",
  Chiquinquirá: "#FFE66B",
};

interface SedeConsumo {
  sede: string;
  consumo_total_kwh: number;
  consumo_promedio_kwh: number;
}

interface SedeAgua {
  sede: string;
  agua_total_m3: number;
  agua_promedio_litros_hora: number;
}

export default function SedesPage() {
  const [isLoading, setIsLoading] = useState(true);
  const [consumoPorSede, setConsumoPorSede] = useState<SedeConsumo[]>([]);
  const [aguaPorSede, setAguaPorSede] = useState<SedeAgua[]>([]);

  const fetchSedesData = async () => {
    setIsLoading(true);
    try {
      
      const [consumoRes, aguaRes] = await Promise.all([
        fetch(`${API_BASE}/consumo-por-sede`),
        fetch(`${API_BASE}/consumo-agua`)
      ]);

      if (consumoRes.ok) {
        const consumoData = await consumoRes.json();
        if (consumoData.data) {
          setConsumoPorSede(consumoData.data);
        }
      }

      if (aguaRes.ok) {
        const aguaData = await aguaRes.json();
        if (aguaData.data) {
          setAguaPorSede(aguaData.data);
        }
      }
    } catch (error) {
      console.error("Error fetching sedes data:", error);
      // Mantiene los datos simulados si hay error
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchSedesData();
  }, []);

  return (
    <div className="space-y-6">
      <PageTitle
        title="ANÁLISIS ENERGÉTICO POR SEDES"
        subtitle="Comparación del consumo energético y recursos por sede UPTC"
      />

      {isLoading ? (
        <div className="flex justify-center items-center h-64">
          <div className="text-lg text-gray-500">Cargando datos...</div>
        </div>
      ) : consumoPorSede.length === 0 ? (
        <div className="flex justify-center items-center h-64">
          <div className="text-lg text-red-500">Error al cargar datos. Verifica que la API esté corriendo.</div>
        </div>
      ) : (
        <>
          {/* KPIs por sede */}
          <div className="grid grid-cols-4 gap-4 m-10">
            {consumoPorSede.map((sede) => (
              <div
                key={sede.sede}
                className="bg-white p-4 rounded-lg shadow-sm border-l-4"
                style={{ borderLeftColor: CAMPUS_COLORS[sede.sede] }}
              >
                <h3 className="font-semibold mb-2">{sede.sede}</h3>
                <p>⚡ {(sede.consumo_total_kwh / 1000).toFixed(1)} MWh</p>
                <p className="text-gray-600">
                  📊 Promedio: {sede.consumo_promedio_kwh} kWh
                </p>
              </div>
            ))}
          </div>

          {/* Gráficas SOLO por sede */}
          <div className="grid grid-cols-2 gap-6 m-10">

            {/* Consumo total */}
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <h3 className="text-lg font-semibold mb-4">
                🏫 Consumo energético por sede
              </h3>

              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={consumoPorSede}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="sede" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="consumo_total_kwh">
                    {consumoPorSede.map((s) => (
                      <Cell key={s.sede} fill={CAMPUS_COLORS[s.sede]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Agua por sede */}
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <h3 className="text-lg font-semibold mb-4">
                💧 Consumo de agua por sede
              </h3>

              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={aguaPorSede}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="sede" />
                  <YAxis />
                  <Tooltip />
                  <Area
                    type="monotone"
                    dataKey="agua_total_m3"
                    stroke="#2563eb"
                    fill="#2563eb"
                    fillOpacity={0.3}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>

          </div>
        </>
      )}
    </div>
  );
}
