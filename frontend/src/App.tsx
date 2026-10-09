import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import TableView from './pages/TableView';
import AddData from './pages/AddData';

export default function App() {
  return (
    <BrowserRouter>
      <nav className="bg-gray-800 text-white p-4">
        <div className="flex gap-4">
          <Link to="/">Dashboard</Link>
          <Link to="/table">Table</Link>
          <Link to="/add">Add Data</Link>
        </div>
      </nav>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/table" element={<TableView />} />
        <Route path="/add" element={<AddData />} />
      </Routes>
    </BrowserRouter>
  );
}
