import { Outlet } from 'react-router-dom';
import Navigation from './Navigation';
import { useAuth } from '../features/auth/AuthContext';

export default function Layout() {
  const { isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Navigation />
      <main className="flex-grow w-full max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <Outlet />
      </main>
      <footer className="bg-white border-t py-4 text-center text-sm text-gray-500">
        <p>&copy; {new Date().getFullYear()} MatchMind AI. All rights reserved.</p>
      </footer>
    </div>
  );
}
