import { Link } from 'react-router-dom'
import { Sparkles, FileText, Target, Shield } from 'lucide-react'

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="h-6 w-6 text-blue-600" />
            <span className="font-bold text-xl">CareerForge AI</span>
          </div>
          <div className="flex items-center gap-4">
            <Link to="/login" className="text-sm font-medium text-gray-600 hover:text-gray-900">Sign in</Link>
            <Link to="/register" className="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700">Get Started</Link>
          </div>
        </div>
      </header>

      <section className="pt-20 pb-16 text-center">
        <div className="max-w-4xl mx-auto px-4">
          <h1 className="text-5xl font-extrabold text-gray-900 tracking-tight mb-6">
            One Profile. Every Job.<br />
            <span className="text-blue-600">A Better Resume.</span>
          </h1>
          <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
            Build your verified Master Career Profile once. Generate tailored, ATS-optimized resumes for every job application.
          </p>
          <div className="flex justify-center gap-4">
            <Link to="/register" className="inline-flex items-center justify-center px-8 py-3 border border-transparent text-lg font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700">Create Free Account</Link>
            <Link to="/login" className="inline-flex items-center justify-center px-8 py-3 border border-gray-300 text-lg font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50">Try Demo Mode</Link>
          </div>
        </div>
      </section>

      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 grid md:grid-cols-3 gap-8">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <FileText className="h-8 w-8 text-blue-600 mb-4" />
            <h3 className="text-lg font-semibold mb-2">Verified Profile</h3>
            <p className="text-gray-600">Upload your resume or build manually. One source of truth for your entire career.</p>
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <Target className="h-8 w-8 text-blue-600 mb-4" />
            <h3 className="text-lg font-semibold mb-2">JD Analysis</h3>
            <p className="text-gray-600">Paste any job description. We extract skills, tools, and ATS keywords automatically.</p>
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <Shield className="h-8 w-8 text-blue-600 mb-4" />
            <h3 className="text-lg font-semibold mb-2">Anti-Hallucination</h3>
            <p className="text-gray-600">We never invent skills or experience. Every claim is validated against your verified profile.</p>
          </div>
        </div>
      </section>

      <footer className="border-t border-gray-200 py-8 text-center text-sm text-gray-500">
        CareerForge AI — Built for modern job seekers.
      </footer>
    </div>
  )
}
