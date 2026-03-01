import React, { useMemo } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const TopTalkersChart = React.memo(({ data }) => {
  const aggregated = useMemo(() => {
    if (!data || data.length === 0) return [];
    const map = {};
    data.forEach((d) => {
      const name = d.process_name || "unknown";
      map[name] = (map[name] || 0) + d.bytes_sent;
    });
    const arr = Object.entries(map).map(([process_name, bytes_sent]) => ({
      process_name,
      bytes_sent,
    }));
    return arr.sort((a, b) => b.bytes_sent - a.bytes_sent).slice(0, 5);
  }, [data]);

  if (!aggregated || aggregated.length === 0) {
    return (
      <div className="bg-gray-800 p-4 rounded h-64 flex items-center justify-center">
        <p className="text-gray-400">No process data available</p>
      </div>
    );
  }

  return (
    <div className="bg-gray-800 p-4 rounded h-64">
      <h2 className="text-xl mb-2">Top Talkers</h2>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={aggregated}>
          <XAxis dataKey="process_name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="bytes_sent" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
});

export default TopTalkersChart;
