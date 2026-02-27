import React, { useState, useEffect, useRef } from "react";
import Header from "./components/Header";
import AlertsPanel from "./components/AlertsPanel";
import BandwidthChart from "./components/BandwidthChart";
import ConnectionsTable from "./components/ConnectionsTable";
import { getConnections, getAlerts, getBandwidth } from "./services/api";

function App() {
  const [alerts, setAlerts] = useState([]);
  const [connections, setConnections] = useState([]);
  const [bandwidth, setBandwidth] = useState([]);
  const [loading, setLoading] = useState(true);
  const ws = useRef(null);
  const alertKeys = useRef(new Set());
  const [live, setLive] = useState(false);
  const reconnectTimer = useRef(null);

  // Fetch initial data from backend
  useEffect(() => {
    Promise.all([
      getAlerts().catch((err) => {
        console.error("Failed to fetch alerts:", err);
        return [];
      }),
      getConnections().catch((err) => {
        console.error("Failed to fetch connections:", err);
        return [];
      }),
      getBandwidth().catch((err) => {
        console.error("Failed to fetch bandwidth:", err);
        return [];
      }),
    ]).then(([alertsData, connsData, bwData]) => {
      // Deduplicate alerts from server by id/timestamp/pid/rule
      const unique = [];
      (alertsData || []).forEach((a) => {
        const key = a.id != null ? a.id : `${a.timestamp}-${a.pid}-${a.rule}`;
        if (!alertKeys.current.has(key)) {
          alertKeys.current.add(key);
          unique.push(a);
        }
      });
      setAlerts(unique);
      setConnections(connsData || []);
      setBandwidth(bwData || []);
      setLoading(false);
    });
  }, []);

  // Setup WebSocket connection with reconnect
  useEffect(() => {
    const connect = () => {
      // avoid opening multiple sockets if one already exists
      if (ws.current && ws.current.readyState === WebSocket.OPEN) {
        return;
      }
      const protocol = window.location.protocol === "https:" ? "wss" : "ws";
      // Backend WebSocket on port 8000
      const ws_url = `${protocol}://localhost:8000/live`;
      const socket = new WebSocket(ws_url);
      ws.current = socket;

      socket.onopen = () => {
        setLive(true);
        // Clear any pending reconnect attempt
        if (reconnectTimer.current) {
          clearTimeout(reconnectTimer.current);
          reconnectTimer.current = null;
        }
      };

      socket.onclose = () => {
        setLive(false);
        ws.current = null;
        // Schedule reconnect after 5 seconds (backoff could be improved)
        reconnectTimer.current = setTimeout(connect, 5000);
      };

      socket.onmessage = (e) => {
        try {
          const a = JSON.parse(e.data);
          const key = a.id != null ? a.id : `${a.timestamp}-${a.pid}-${a.rule}`;
          if (!alertKeys.current.has(key)) {
            alertKeys.current.add(key);
            setAlerts((prev) => [a, ...prev]);
          }
        } catch (err) {
          console.error("Failed to parse WebSocket message:", err);
        }
      };

      socket.onerror = (err) => {
        console.error("WebSocket error:", err);
        setLive(false);
        ws.current = null;
      };
    };

    connect();

    return () => {
      if (ws.current) {
        ws.current.close();
        ws.current = null;
      }
      if (reconnectTimer.current) {
        clearTimeout(reconnectTimer.current);
        reconnectTimer.current = null;
      }
    };
  }, []);

  return (
    <div className="min-h-screen bg-ghost-900 text-ghost-text flex flex-col">
      <Header live={live} alerts={alerts} />
      {loading ? (
        <div className="flex flex-1 items-center justify-center p-8">
          <p className="text-ghost-muted animate-pulse">Initializing Command Center...</p>
        </div>
      ) : (
        <div className="flex-1 p-6 grid grid-cols-1 md:grid-cols-4 gap-6 max-w-[1600px] mx-auto w-full">
          {/* Top row: Alerts and Chart */}
          <div className="md:col-span-1 h-[450px]">
            <AlertsPanel alerts={alerts} />
          </div>
          <div className="md:col-span-3 h-[450px]">
            <BandwidthChart data={bandwidth} />
          </div>
          {/* Bottom row: Connections Table */}
          <div className="md:col-span-4">
            <ConnectionsTable connections={connections} />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
