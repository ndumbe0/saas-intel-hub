import { useState, useEffect } from 'react';

export default function Dashboard() {
  const [summary, setSummary] = useState<any>(null);

  useEffect(() => {
    fetch('/api/facets/summary')
      .then(r => r.json())
      .then(setSummary)
      .catch(() => {});
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">SaaS Intel Hub - Dashboard</h1>
      {summary && (
        <div className="bg-blue-100 p-4 rounded">
          <h2 className="text-xl">Total Ideas</h2>
          <p className="text-3xl">{summary.total}</p>
        </div>
      )}
    </div>
  );
}
