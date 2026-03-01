import React from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend,
} from "recharts";

const BandwidthChart = React.memo(({ data }) => {
  if (!data || data.length === 0) {
    return (
      <div className="bg-ghost-800 border border-ghost-700 rounded-lg h-full flex items-center justify-center shadow-sm">
        <p className="text-ghost-muted animate-pulse text-sm">Awaiting telemetry...</p>
      </div>
    );
  }

  const formatted = data.map((d) => ({
    ...d,
    time: new Date(d.timestamp * 1000).toLocaleTimeString([], { hour12: false }),
  }));

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-ghost-800 border border-ghost-700 p-3 rounded shadow-lg text-xs font-mono">
          <p className="text-ghost-subtle mb-2 border-b border-ghost-700 pb-1">{label}</p>
          {payload.map((entry, index) => (
            <p key={index} style={{ color: entry.color }} className="flex justify-between space-x-4">
              <span>{entry.name}:</span>
              <span className="font-bold">{(entry.value / 1024).toFixed(2)} KB/s</span>
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-ghost-800 border border-ghost-700 rounded-lg h-full flex flex-col shadow-sm">
      <div className="px-4 py-3 border-b border-ghost-700 bg-ghost-900/50 flex items-center justify-between">
         <h2 className="text-sm font-semibold tracking-wide text-ghost-subtle uppercase">Network Telemetry</h2>
         <span className="flex h-2 w-2 relative">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-accent-blue opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-accent-blue"></span>
         </span>
      </div>
      <div className="flex-1 p-4 pb-2">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={formatted} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="colorSent" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="colorRecv" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#22c55e" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#22c55e" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
            <XAxis 
                dataKey="time" 
                stroke="#94a3b8" 
                fontSize={10} 
                tickLine={false}
                axisLine={false}
                minTickGap={30}
            />
            <YAxis 
                stroke="#94a3b8" 
                fontSize={10} 
                tickLine={false}
                axisLine={false}
                tickFormatter={(val) => `${(val / 1024).toFixed(0)}k`}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend iconType="circle" wrapperStyle={{ fontSize: '11px', color: '#cbd5e1', paddingTop: '10px' }} />
            <Area
              type="monotone"
              dataKey="bytes_sent"
              name="Bytes Sent"
              stroke="#3b82f6"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#colorSent)"
              isAnimationActive={false}
            />
            <Area
              type="monotone"
              dataKey="bytes_recv"
              name="Bytes Received"
              stroke="#22c55e"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#colorRecv)"
              isAnimationActive={false}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
});

export default BandwidthChart;
