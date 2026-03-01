import React, { useState } from "react";

const severityStyles = {
  high: { border: "border-l-accent-red", badge: "bg-accent-red/10 text-accent-red" },
  medium: { border: "border-l-accent-amber", badge: "bg-accent-amber/10 text-accent-amber" },
  low: { border: "border-l-accent-blue", badge: "bg-accent-blue/10 text-accent-blue" },
  unknown: { border: "border-l-ghost-muted", badge: "bg-ghost-700 text-ghost-muted" },
};

const AlertsPanel = React.memo(({ alerts }) => {
  const [expanded, setExpanded] = useState({});
  const toggle = (alertId, e) => {
    e.stopPropagation();
    setExpanded((prev) => ({ ...prev, [alertId]: !prev[alertId] }));
  };

  return (
    <div className="bg-ghost-800 border border-ghost-700 rounded-lg h-full flex flex-col overflow-hidden shadow-sm">
      <div className="px-4 py-3 border-b border-ghost-700 bg-ghost-900/50 flex justify-between items-center">
        <h2 className="text-sm font-semibold tracking-wide text-ghost-subtle uppercase">Live Alerts</h2>
        <span className="text-xs font-mono text-ghost-muted">{alerts.length} Total</span>
      </div>
      <div className="overflow-y-auto flex-1 p-2 space-y-1">
        {alerts.map((alert, idx) => {
          const alertKey =
            alert.id != null
              ? alert.id
              : `${alert.timestamp}-${alert.pid}-${alert.rule}-${idx}`;
          const sev = severityStyles[alert.severity] || severityStyles.unknown;
          const isExpanded = expanded[alertKey];

          return (
            <div
              key={alertKey}
              onClick={(e) => toggle(alertKey, e)}
              className={`group flex flex-col bg-ghost-900/30 border border-ghost-700 border-l-2 ${sev.border} rounded cursor-pointer hover:bg-ghost-700/30 transition-colors duration-150`}
            >
              <div className="flex items-center p-2 text-sm">
                <div className="flex-shrink-0 w-16">
                  <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${sev.badge}`}>
                    {alert.severity}
                  </span>
                </div>
                <div className="flex-1 flex items-center space-x-2 truncate px-2">
                  <span className="font-medium text-ghost-text truncate">{alert.rule}</span>
                  <span className="text-ghost-muted">—</span>
                  <span className="font-mono text-xs text-ghost-subtle truncate">{alert.process_name}</span>
                </div>
                <div className="flex-shrink-0 text-xs font-mono text-ghost-muted flex items-center space-x-3">
                  <span>{new Date(alert.timestamp * 1000).toLocaleTimeString([], { hour12: false })}</span>
                  <span className="text-ghost-subtle w-4 text-center">{isExpanded ? '▼' : '▶'}</span>
                </div>
              </div>
              
              {isExpanded && (
                <div className="px-4 py-3 border-t border-ghost-700 bg-ghost-900/50 text-xs text-ghost-muted space-y-2">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <span className="block text-[10px] uppercase tracking-wider text-ghost-subtle mb-1">Process ID</span>
                      <span className="font-mono">{alert.pid}</span>
                    </div>
                    <div>
                      <span className="block text-[10px] uppercase tracking-wider text-ghost-subtle mb-1">Timestamp</span>
                      <span className="font-mono">{new Date(alert.timestamp * 1000).toLocaleString()}</span>
                    </div>
                  </div>
                  <div>
                    <span className="block text-[10px] uppercase tracking-wider text-ghost-subtle mb-1">Reason</span>
                    <span className="text-ghost-text font-mono break-words">{alert.reason}</span>
                  </div>
                </div>
              )}
            </div>
          );
        })}
        {alerts.length === 0 && (
          <div className="h-full flex items-center justify-center text-ghost-muted text-sm pb-8">
            No active alerts
          </div>
        )}
      </div>
    </div>
  );
});

export default AlertsPanel;
