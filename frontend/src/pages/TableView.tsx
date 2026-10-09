import { useState, useEffect } from 'react';

export default function TableView() {
  const [items, setItems] = useState<any[]>([]);
  
  useEffect(() => {
    fetch('/api/saas?page=1&limit=20')
      .then(r => r.json())
      .then(setItems)
      .catch(() => {});
  }, []);
  
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Ideas</h1>
      <div className="overflow-x-auto">
        <table className="min-w-full border">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-2 text-left">Idea</th>
              <th className="px-4 py-2 text-left">Monthly Revenue</th>
              <th className="px-4 py-2 text-left">Monthly Traffic</th>
              <th className="px-4 py-2 text-left">Score</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item, i) => (
              <tr key={i} className="border-t">
                <td className="px-4 py-2">{item.idea}</td>
                <td className="px-4 py-2">{item.monthly_revenue}</td>
                <td className="px-4 py-2">{item.monthly_traffic}</td>
                <td className="px-4 py-2">{item.solopreneur_score}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
