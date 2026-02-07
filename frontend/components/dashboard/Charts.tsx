'use client';

import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

interface ChartProps {
  data: Array<{ date: string; value: number; [key: string]: any }>;
  dataKey?: string;
  color?: string;
  height?: number;
  showGrid?: boolean;
  type?: 'line' | 'area';
}

export function TrendChart({ 
  data, 
  dataKey = 'value', 
  color = 'rgb(96, 165, 250)', 
  height = 300,
  showGrid = true,
  type = 'line'
}: ChartProps) {
  const ChartComponent = type === 'area' ? AreaChart : LineChart;
  const DataComponent = type === 'area' ? Area : Line;

  return (
    <ResponsiveContainer width="100%" height={height}>
      <ChartComponent data={data}>
        {showGrid && (
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
        )}
        <XAxis 
          dataKey="date" 
          stroke="rgba(255,255,255,0.3)"
          style={{ fontSize: '12px' }}
          tickLine={false}
        />
        <YAxis 
          stroke="rgba(255,255,255,0.3)"
          style={{ fontSize: '12px' }}
          tickLine={false}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: 'rgba(17, 24, 39, 0.95)',
            border: '1px solid rgba(255,255,255,0.1)',
            borderRadius: '8px',
            padding: '12px'
          }}
          labelStyle={{ color: 'rgba(255,255,255,0.7)', marginBottom: '4px' }}
          itemStyle={{ color: color }}
        />
        <DataComponent
          type="monotone"
          dataKey={dataKey}
          stroke={color}
          strokeWidth={2}
          fill={type === 'area' ? `${color}30` : undefined}
          dot={false}
          activeDot={{ r: 6, fill: color }}
        />
      </ChartComponent>
    </ResponsiveContainer>
  );
}

interface MultiLineChartProps {
  data: Array<{ date: string; [key: string]: any }>;
  lines: Array<{ dataKey: string; color: string; name: string }>;
  height?: number;
}

export function MultiLineChart({ data, lines, height = 300 }: MultiLineChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
        <XAxis 
          dataKey="date" 
          stroke="rgba(255,255,255,0.3)"
          style={{ fontSize: '12px' }}
          tickLine={false}
        />
        <YAxis 
          stroke="rgba(255,255,255,0.3)"
          style={{ fontSize: '12px' }}
          tickLine={false}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: 'rgba(17, 24, 39, 0.95)',
            border: '1px solid rgba(255,255,255,0.1)',
            borderRadius: '8px',
            padding: '12px'
          }}
          labelStyle={{ color: 'rgba(255,255,255,0.7)', marginBottom: '8px' }}
        />
        <Legend 
          wrapperStyle={{ paddingTop: '20px' }}
          iconType="line"
        />
        {lines.map((line) => (
          <Line
            key={line.dataKey}
            type="monotone"
            dataKey={line.dataKey}
            stroke={line.color}
            strokeWidth={2}
            name={line.name}
            dot={false}
            activeDot={{ r: 6, fill: line.color }}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
}
