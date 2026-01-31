"use client";

import { useState, useEffect } from "react";
import PageTitle from "../components/PageTitle";

import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

const API_BASE = "http://localhost:5000/api";

interface ConsumoSector {
  sector: string;
  consumo_total_kwh: number;
}

interface DistribucionSector {
  sector: string;
  consumo_kwh: number;
  porcentaje: number;
}

interface ImpactoSector {
  sector: string;
  co2_total_toneladas: number;
  agua_total_m3: number;
  consumo_energia_kwh: number;
  equivalente_arboles: number;
}

interface TendenciaDia {
  fecha: string;
  consumo_kwh: number;
}

type TendenciasSector = Record<string, TendenciaDia[]>;

const COLORS: Record<string, string> = {
  Laboratorios: "#2E27B1",
  Oficinas: "#040959",
  Salones: "#F28705",
  Comedores: "#D09F0A",
  Auditorios: "#FFE66B",
};

export default function SectoresPage() {
  const [consumoSector, setConsumoSector] = useState<ConsumoSector[]>([]);
  const [distribucion, setDistribucion] = useState<DistribucionSector[]>([]);
  const [impacto, setImpacto] = useState<ImpactoSector[]>([]);
  const [tendencias, setTendencias] = useState<TendenciasSector>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [consumoRes, distribucionRes, impactoRes, tendenciasRes] = await Promise.all([
          fetch(`${API_BASE}/consumo-por-sector`),
          fetch(`${API_BASE}/distribucion-por-sector`),
          fetch(`${API_BASE}/impacto-ambiental`),
          fetch(`${API_BASE}/tendencias-sector`),
        ]);

        if (!consumoRes.ok || !distribucionRes.ok || !impactoRes.ok || !tendenciasRes.ok) {
          throw new Error("Error al cargar datos de sectores");
        }

        const consumoData = await consumoRes.json();
        const distribucionData = await distribucionRes.json();
        const impactoData = await impactoRes.json();
        const tendenciasData = await tendenciasRes.json();

        setConsumoSector(consumoData.data || []);
        setDistribucion(distribucionData.data || []);
        setImpacto(impactoData.data || []);
        setTendencias(tendenciasData.data || {});
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Error desconocido");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando datos de sectores...</p>
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

  return (
    <div className="space-y-10 p-6">
      <PageTitle
        title="Consumo energético por sectores"
        subtitle="Análisis inteligente por áreas de la UPTC"
      />

      {/* KPIs */}
      <div className="grid grid-cols-5 gap-4">
        {impacto.map((s) => (
          <div
            key={s.sector}
            className="bg-white p-4 rounded-xl shadow border-l-4"
            style={{ borderColor: COLORS[s.sector] }}
          >
            <h3 className="font-semibold">{s.sector}</h3>
            <p>⚡ {s.consumo_energia_kwh.toLocaleString()} kWh</p>
            <p className="text-red-600">🌫 {s.co2_total_toneladas} ton CO₂</p>
            <p className="text-blue-600">💧 {s.agua_total_m3} m³</p>
          </div>
        ))}
      </div>

      {/* Barras */}
      <div className="bg-white p-6 rounded-xl shadow">
        <h2 className="font-semibold mb-4">Consumo por sector</h2>

        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={consumoSector}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="sector" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="consumo_total_kwh">
              {consumoSector.map((s) => (
                <Cell key={s.sector} fill={COLORS[s.sector]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Pie */}
      <div className="bg-white p-6 rounded-xl shadow">
        <h2 className="font-semibold mb-4">Distribución del consumo</h2>

        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={distribucion}
              dataKey="consumo_kwh"
              nameKey="sector"
              outerRadius={110}
              label={({ sector, porcentaje }) =>
                `${sector} ${porcentaje}%`
              }
            >
              {distribucion.map((s) => (
                <Cell key={s.sector} fill={COLORS[s.sector]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Líneas */}
      <div className="bg-white p-6 rounded-xl shadow">
        <h2 className="font-semibold mb-4">Tendencias por sector</h2>

        <ResponsiveContainer width="100%" height={320}>
          <LineChart>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="fecha" />
            <YAxis />
            <Tooltip />
            <Legend />

            {Object.entries(tendencias).map(([sector, data]) => (
              <Line
                key={sector}
                data={data}
                dataKey="consumo_kwh"
                name={sector}
                stroke={COLORS[sector]}
                dot={false}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
