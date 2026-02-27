import React from "react";

const Header = React.memo(({ live, alerts }) => {
  let risk = "LOW RISK";
  let badgeColor = "bg-accent-blue/10 text-accent-blue border-accent-blue/20";
  
  if (alerts && alerts.length) {
    const sevOrder = { low: 1, medium: 2, high: 3 };
    let max = 0;
    alerts.forEach((a) => {
      const v = sevOrder[a.severity] || 0;
      if (v > max) max = v;
    });
    if (max >= 3) {
      risk = "HIGH RISK";
      badgeColor = "bg-accent-red/10 text-accent-red border-accent-red/20";
    } else if (max === 2) {
      risk = "MEDIUM RISK";
      badgeColor = "bg-accent-amber/10 text-accent-amber border-accent-amber/20";
    }
  }

  return (
    <header className="flex items-center justify-between px-6 py-4 bg-ghost-900 border-b border-ghost-700 shadow-sm relative z-10 w-full h-[72px]">
      <div className="flex items-center space-x-3">
        {/* Abstract logo mark (optional visual weight) */}
        <div className="w-8 h-8 rounded shrink-0 bg-gradient-to-br from-ghost-700 to-ghost-800 border border-ghost-700 flex items-center justify-center">
            <div className="w-3 h-3 bg-ghost-subtle rounded-sm" />
        </div>
        <h1 className="text-xl font-semibold tracking-widest text-ghost-text">GHOSTWIRE</h1>
      </div>
      
      <div className="flex items-center space-x-6">
        <div className="flex items-center space-x-2">
          <div className="relative flex items-center justify-center w-3 h-3">
            {live ? (
              <>
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-accent-green opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-accent-green"></span>
              </>
            ) : (
              <span className="relative inline-flex rounded-full h-2 w-2 bg-accent-red"></span>
            )}
          </div>
          <span className="text-sm font-medium tracking-wide text-ghost-subtle uppercase">
            {live ? "SYSTEM LIVE" : "DISCONNECTED"}
          </span>
        </div>
        
        <div className="h-6 w-px bg-ghost-700" />
        
        <div
          className={`px-3 py-1 rounded text-xs font-bold tracking-wider border ${badgeColor}`}
        >
          {risk}
        </div>
      </div>
    </header>
  );
});

export default Header;
