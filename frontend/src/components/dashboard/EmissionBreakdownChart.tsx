"use client";

import { Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { CategoryBreakdown } from "@/lib/types";
import { CATEGORY_META } from "@/lib/category-meta";

export function EmissionBreakdownChart({ breakdown }: { breakdown: CategoryBreakdown[] }) {
  const data = [...breakdown].sort((a, b) => b.kg_co2_month - a.kg_co2_month);

  return (
    <div>
      <div className="h-64" aria-hidden="true">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ top: 8, right: 16, left: 8, bottom: 0 }}>
            <CartesianGrid stroke="rgba(255,255,255,0.06)" horizontal={false} />
            <XAxis type="number" stroke="#9fb3a9" fontSize={12} tickLine={false} axisLine={false} />
            <YAxis
              type="category"
              dataKey="category"
              stroke="#9fb3a9"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              width={110}
              tickFormatter={(value: string) => CATEGORY_META[value]?.label ?? value}
            />
            <Tooltip
              formatter={(value) => [`${value} kg CO2/month`, ""]}
              labelFormatter={(label) => CATEGORY_META[String(label)]?.label ?? String(label)}
              contentStyle={{
                background: "#11231c",
                border: "1px solid rgba(255,255,255,0.12)",
                borderRadius: 8,
                color: "#e7efe9",
                fontSize: 13,
              }}
            />
            <Bar dataKey="kg_co2_month" radius={[0, 6, 6, 0]} barSize={18}>
              {data.map((entry) => (
                <Cell key={entry.category} fill={CATEGORY_META[entry.category]?.barColor ?? "#9fb3a9"} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <table className="sr-only">
        <caption>Carbon footprint by category, kilograms of CO2 per month</caption>
        <thead>
          <tr>
            <th scope="col">Category</th>
            <th scope="col">kg CO2/month</th>
            <th scope="col">% of total</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <tr key={row.category}>
              <td>{CATEGORY_META[row.category]?.label ?? row.category}</td>
              <td>{row.kg_co2_month}</td>
              <td>{row.percent_of_total}%</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Visible legend doubles as the non-color-dependent key for sighted users */}
      <ul className="mt-3 flex flex-wrap gap-3" aria-hidden="true">
        {data.map((row) => {
          const meta = CATEGORY_META[row.category];
          const Icon = meta?.icon;
          return (
            <li key={row.category} className="flex items-center gap-1.5 text-xs text-mist-dim">
              <span className="h-2.5 w-2.5 rounded-full" style={{ background: meta?.barColor }} />
              {Icon && <Icon className="h-3.5 w-3.5" />}
              {meta?.label ?? row.category}
            </li>
          );
        })}
      </ul>
    </div>
  );
}
