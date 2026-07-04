import { Outlet, Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../features/auth/AuthContext'
import { FileText, LayoutDashboard, User, Briefcase, LogOut, Sparkles } from 'lucide-react'

export default function MainLayout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  if (!user) return <Outlet />

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center gap-8">
              <Link to="/dashboard" className="flex items-center gap-2">
                <Sparkles className="h-6 w-6 text-blue-600" />
                <span className="font-bold text-xl text-gray-900">CareerForge AI</span>
              </Link>
              <div className="hidden md:flex items-center gap-4">
                <Link to="/dashboard" className="flex items-center gap-1.5 text-sm font-medium text-gray-600 hover:text-gray-900">
                  <LayoutDashboard className="h-4 w-4" /> Dashboard
                </Link>
                <Link to="/profile" className="flex items-center gap-1.5 text-sm font-medium text-gray-600 hover:text-gray-900">
                  <User className="h-4 w-4" /> Profile
                </Link>
                <Link to="/jobs/new" className="flex items-center gap-1.5 text-sm font-medium text-gray-600 hover:text-gray-900">
                  <Briefcase className="h-4 w-4" /> New Job
                </Link>
                <Link to="/resumes" className="flex items-center gap-1.5 text-sm font-medium text-gray-600 hover:text-gray-900">
                  <FileText className="h-4 w-4" /> History
                </Link>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600">{user.email}</span>
              <button
                onClick={() => { logout(); navigate('/login') }}
                className="flex items-center gap-1.5 text-sm text-gray-600 hover:text-red-600"
              >
                <LogOut className="h-4 w-4" /> Logout
              </button>
            </div>
          </div>
        </div>
      </nav>
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>
    </div>
  )
}
