import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { LevelStats } from "@/types/exercise";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";

interface ProgressChartProps {
  stats: LevelStats[];
}

const difficultyColor: Record<string, string> = {
  basic: "#10b981",
  intermediate: "#f59e0b",
  advanced: "#ef4444",
};

export function ProgressChart({ stats }: ProgressChartProps) {
  const data = stats.map((s) => ({
    name: s.level_name,
    accuracy: parseFloat(s.avg_accuracy.toFixed(1)),
    score: parseFloat(s.avg_score.toFixed(1)),
    difficulty: s.difficulty,
  }));

  if (data.length === 0) {
    return (
      <Card>
        <p className="text-center text-sm text-gray-400 py-8">
          Aún no tienes sesiones de práctica. ¡Empieza a leer!
        </p>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Progreso por Nivel</CardTitle>
      </CardHeader>
      <ResponsiveContainer width="100%" height={220}>
        <BarChart data={data} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis dataKey="name" tick={{ fontSize: 12 }} />
          <YAxis domain={[0, 100]} tick={{ fontSize: 12 }} />
          <Tooltip
            formatter={(value, name) => [
              `${value}${name === "accuracy" ? "%" : " pts"}`,
              name === "accuracy" ? "Precisión" : "Puntaje",
            ]}
          />
          <Bar dataKey="accuracy" name="accuracy" radius={[4, 4, 0, 0]}>
            {data.map((entry, index) => (
              <Cell key={index} fill={difficultyColor[entry.difficulty] ?? "#6c3dc7"} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </Card>
  );
}
