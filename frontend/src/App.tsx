import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './features/auth/Login';
import Register from './features/auth/Register';
import Profile from './features/auth/Profile';
import ResumesPage from './features/resumes/ResumesPage';
import { useAuth } from './features/auth/AuthContext';

function Dashboard() {
  return (
    <div className="bg-white shadow rounded-lg p-6 text-center">
      <h2 className="text-2xl font-bold mb-4">Welcome to MatchMind AI Dashboard</h2>
      <p className="text-gray-600">You are successfully logged in!</p>
    </div>
  );
}

function App() {
  const { isAuthenticated } = useAuth();

  return (
    <Router>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={isAuthenticated ? <Navigate to="/dashboard" /> : <Navigate to="/login" />} />
          <Route path="/login" element={!isAuthenticated ? <Login /> : <Navigate to="/dashboard" />} />
          <Route path="/register" element={!isAuthenticated ? <Register /> : <Navigate to="/dashboard" />} />
          
          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/resumes" element={<ResumesPage />} />
          </Route>
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
