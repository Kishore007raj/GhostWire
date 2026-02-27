import React, { useState, useMemo } from "react";

const ConnectionsTable = React.memo(({ connections }) => {
  const [search, setSearch] = useState("");
  const [sortDir, setSortDir] = useState("desc");
  const [page, setPage] = useState(0);
  const pageSize = 15; // Increased page size for a denser view

  const filtered = useMemo(() => {
    return connections.filter(
      (c) =>
        c.process_name &&
        c.process_name.toLowerCase().includes(search.toLowerCase()),
    );
  }, [connections, search]);

  const sorted = useMemo(() => {
    return filtered.slice().sort((a, b) => {
      if (sortDir === "asc") return a.bytes_sent - b.bytes_sent;
      return b.bytes_sent - a.bytes_sent;
    });
  }, [filtered, sortDir]);

  const paginated = useMemo(
    () => sorted.slice(page * pageSize, (page + 1) * pageSize),
    [sorted, page],
  );

  const pageCount = Math.ceil(sorted.length / pageSize);

  React.useEffect(() => {
    if (page >= pageCount && pageCount > 0) {
      setPage(Math.max(0, pageCount - 1));
    }
  }, [pageCount, page]);

  React.useEffect(() => {
    setPage(0);
  }, [filtered]);

  if (!connections || connections.length === 0) {
    return (
      <div className="bg-ghost-800 border border-ghost-700 rounded-lg p-4 flex flex-col items-center justify-center shadow-sm h-64">
        <p className="text-ghost-muted text-sm animate-pulse">Waiting for connection data...</p>
      </div>
    );
  }

  return (
    <div className="bg-ghost-800 border border-ghost-700 rounded-lg shadow-sm flex flex-col overflow-hidden">
      <div className="px-4 py-3 border-b border-ghost-700 bg-ghost-900/50 flex justify-between items-center z-20">
        <h2 className="text-sm font-semibold tracking-wide text-ghost-subtle uppercase">Active Connections</h2>
        <div className="flex space-x-3 text-xs">
          <input
            placeholder="Search process..."
            className="px-3 py-1.5 rounded bg-ghost-900/50 border border-ghost-700 text-ghost-text placeholder-ghost-muted focus:outline-none focus:border-accent-blue transition-colors w-64"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <button
            className="px-3 py-1.5 rounded bg-ghost-700 hover:bg-ghost-600 border border-ghost-600 text-ghost-text font-medium transition-colors flex items-center space-x-2"
            onClick={() => setSortDir((d) => (d === "asc" ? "desc" : "asc"))}
          >
            <span>Sort Bytes</span>
            <span className="text-accent-blue font-bold">{sortDir === "asc" ? "↑" : "↓"}</span>
          </button>
        </div>
      </div>
      
      <div className="overflow-x-auto">
        <div className="max-h-[500px] overflow-y-auto custom-scrollbar">
          <table className="w-full text-xs text-left whitespace-nowrap">
            <thead className="sticky top-0 bg-ghost-900/95 backdrop-blur-sm z-10 border-b border-ghost-700 shadow-sm">
              <tr className="text-ghost-subtle uppercase tracking-wider">
                <th className="px-4 py-3 font-semibold w-1/5">Process</th>
                <th className="px-4 py-3 font-semibold w-1/12">Proto</th>
                <th className="px-4 py-3 font-semibold w-1/4">Local IP:Port</th>
                <th className="px-4 py-3 font-semibold w-1/4">Remote IP:Port</th>
                <th className="px-4 py-3 font-semibold text-right w-1/12">Sent</th>
                <th className="px-4 py-3 font-semibold text-right w-1/12">Recv</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-ghost-700/50 text-ghost-text">
              {paginated.map((c, i) => (
                <tr
                  key={c.id != null ? c.id : `${c.timestamp}-${i}`}
                  className="even:bg-ghost-900/30 hover:bg-ghost-700/40 transition-colors duration-150"
                >
                  <td className="px-4 py-2.5 font-medium">{c.process_name}</td>
                  <td className="px-4 py-2.5">
                    <span className="px-1.5 py-0.5 rounded bg-ghost-700 text-[10px] uppercase font-bold text-ghost-subtle">
                        {c.protocol}
                    </span>
                  </td>
                  <td className="px-4 py-2.5 font-mono text-ghost-subtle">
                    {c.local_ip}<span className="text-ghost-muted/50">:</span>{c.local_port}
                  </td>
                  <td className="px-4 py-2.5 font-mono text-ghost-subtle">
                    {c.remote_ip}<span className="text-ghost-muted/50">:</span>{c.remote_port}
                  </td>
                  <td className="px-4 py-2.5 text-right font-mono text-accent-blue/90">
                    {(c.bytes_sent / 1024).toFixed(1)} <span className="text-[10px] text-ghost-muted">KB</span>
                  </td>
                  <td className="px-4 py-2.5 text-right font-mono text-accent-green/90">
                    {(c.bytes_recv / 1024).toFixed(1)} <span className="text-[10px] text-ghost-muted">KB</span>
                  </td>
                </tr>
              ))}
              {paginated.length === 0 && (
                 <tr>
                     <td colSpan={6} className="px-4 py-8 text-center text-ghost-muted">
                        No matches found.
                     </td>
                 </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
      
      <div className="px-4 py-3 border-t border-ghost-700 bg-ghost-900/30 flex justify-between items-center text-xs">
        <span className="text-ghost-muted">
          Showing <span className="font-semibold text-ghost-text">{sorted.length === 0 ? 0 : page * pageSize + 1}</span> to <span className="font-semibold text-ghost-text">{Math.min((page + 1) * pageSize, sorted.length)}</span> of <span className="font-semibold text-ghost-text">{sorted.length}</span> connections
        </span>
        <div className="flex space-x-2">
          <button
            disabled={page === 0}
            onClick={() => setPage((p) => Math.max(0, p - 1))}
            className="px-3 py-1.5 bg-ghost-700 hover:bg-ghost-600 rounded disabled:opacity-30 disabled:cursor-not-allowed transition-colors font-medium border border-ghost-600"
          >
            Prev
          </button>
          <button
            disabled={page >= pageCount - 1 || pageCount === 0}
            onClick={() => setPage((p) => Math.min(pageCount - 1, p + 1))}
            className="px-3 py-1.5 bg-ghost-700 hover:bg-ghost-600 rounded disabled:opacity-30 disabled:cursor-not-allowed transition-colors font-medium border border-ghost-600"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
});

export default ConnectionsTable;
