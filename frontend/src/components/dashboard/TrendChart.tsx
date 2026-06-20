"use client";

import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { FootprintSnapshot } from "@/lib/types";

export function TrendChart({ trend }: { trend: FootprintSnapshot[] }) {
  const data = trend.map((snap) => ({
    date: new Date(snap.created_at).toLocaleDateString(undefined, { month: "short", day: "numeric" }),
    score: snap.carbon_score,
    kg: snap.total_kg_co2_month,
  }));

  return (
    <div>
      <div className="h-64" aria-hidden="true">
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
              labelStyle={{ color: "#9fb3a9" }}
            />
            <Line type="monotone" dataKey="score" name="Carbon Score" stroke="#4ade80" strokeWidth={2.5} dot={{ r: 3 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Accessible alternative for screen reader users, who get little value
          from an SVG line chart even with ARIA labels on it. */}
      <table className="sr-only">
        <caption>Carbon score trend over time</caption>
        <thead>
          <tr>
            <th scope="col">Date</th>
            <th scope="col">Carbon score</th>
            <th scope="col">Total kg CO2 this month</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={i}>
              <td>{row.date}</td>
              <td>{row.score}</td>
              <td>{row.kg}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
