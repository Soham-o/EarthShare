"use client";

import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

interface Point {
  date: string;
  carbon_score: number;
  total_kg_co2_month: number;
}

export function WeeklyTrendChart({ points }: { points: Point[] }) {
  const data = points.map((p) => ({
    date: new Date(p.date).toLocaleDateString(undefined, { month: "short", day: "numeric" }),
    kg: p.total_kg_co2_month,
  }));

  return (
    <div>
      <div className="h-56" aria-hidden="true">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 8, right: 8, left: -16, bottom: 0 }}>
            <CartesianGrid stroke="rgba(255,255,255,0.06)" vertical={false} />
            <XAxis dataKey="date" stroke="#9fb3a9" fontSize={12} tickLine={false} axisLine={false} />
            <YAxis stroke="#9fb3a9" fontSize={12} tickLine={false} axisLine={false} width={40} />
            <Tooltip
              contentStyle={{
                background: "#11231c",
                border: "1px solid rgba(255,255,255,0.12)",
                borderRadius: 8,
                color: "#e7efe9",
                fontSize: 13,
              }}
            />
            <Line type="monotone" dataKey="kg" name="kg CO2/month" stroke="#5ec8e0" strokeWidth={2.5} dot={{ r: 3 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <table className="sr-only">
        <caption>Total kg CO2 per month over time</caption>
        <thead>
          <tr>
            <th scope="col">Date</th>
            <th scope="col">kg CO2/month</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={i}>
              <td>{row.date}</td>
              <td>{row.kg}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
