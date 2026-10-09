import { useState } from 'react';

export default function AddData() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [progress, setProgress] = useState<any>(null);

  const upload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    const r = await fetch('/api/upload', { method: 'POST', body: formData });
    setResult(await r.json());
  };

  const checkProgress = async () => {
    const r = await fetch('/api/ingest/progress');
    setProgress(await r.json());
  };

  const startIngest = async () => {
    const r = await fetch('/api/ingest/start', { method: 'POST' });
    setResult(await r.json());
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Add Data</h1>
      <input type="file" accept=".csv,.xlsx" onChange={(e) => setFile(e.target.files?.[0] || null)} />
      <button onClick={upload} className="ml-2 bg-blue-500 text-white px-4 py-2 rounded">Upload</button>
      <button onClick={startIngest} className="ml-2 bg-green-500 text-white px-4 py-2 rounded">Start Ingest</button>
      <button onClick={checkProgress} className="ml-2 bg-gray-500 text-white px-4 py-2 rounded">Check Progress</button>
      {result && <pre className="mt-4 p-4 bg-gray-100 rounded">{JSON.stringify(result, null, 2)}</pre>}
      {progress && <pre className="mt-4 p-4 bg-gray-100 rounded">{JSON.stringify(progress, null, 2)}</pre>}
    </div>
  );
}
