import { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { api } from '../services/api'
import { FileText, User, Briefcase, Plus, TrendingUp } from 'lucide-react'

export default function DashboardPage() {
  const { data: profile } = useQuery({
    queryKey: ['profile'],
    queryFn: () => api.get('/profile').then(r => r.data),
  })

  const { data: resumes } = useQuery({
    queryKey: ['resumes'],
    queryFn: () => api.get('/resumes').then(r => r.data),
  })

  const completion = profile?.completion_percentage || 0

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600">Welcome back! Here's your career overview.</p>
        </div>
        <Link to="/jobs/new" className="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700">
          <Plus className="h-4 w-4 mr-2" /> Create New Resume
        </Link>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Profile Completion</h3>
            <User className="h-5 w-5 text-gray-400" />
          </div>
          <div className="flex items-center gap-3">
            <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
              <div className="h-full bg-blue-600 rounded-full transition-all" style={{ width: `${completion}%` }} />
            </div>
            <span className="text-sm font-medium">{completion}%</span>
          </div>
          <p className="text-sm text-gray-600 mt-3">
            {completion < 100 ? 'Complete your profile for better resume generation.' : 'Your profile is complete and verified!'}
          </p>
          <Link to="/profile" className="text-sm text-blue-600 font-medium mt-2 inline-block">Edit Profile</Link>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Generated Resumes</h3>
            <FileText className="h-5 w-5 text-gray-400" />
          </div>
          <p className="text-3xl font-bold text-gray-900">{resumes?.length || 0}</p>
          <p className="text-sm text-gray-600 mt-1">Tailored resumes created</p>
          <Link to="/resumes" className="text-sm text-blue-600 font-medium mt-3 inline-block">View History</Link>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Quick Actions</h3>
            <Briefcase className="h-5 w-5 text-gray-400" />
          </div>
          <div className="space-y-2">
            <Link to="/jobs/new" className="block text-sm text-blue-600 hover:underline">Analyze a new job description</Link>
            <Link to="/profile" className="block text-sm text-blue-600 hover:underline">Update your skills</Link>
          </div>
        </div>
      </div>

      {resumes && resumes.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">Recent Resumes</h3>
          </div>
          <div className="divide-y divide-gray-200">
            {resumes.slice(0, 5).map((resume: any) => (
              <div key={resume.id} className="p-4 flex items-center justify-between hover:bg-gray-50">
                <div>
                  <p className="font-medium text-gray-900">{resume.title}</p>
                  <p className="text-sm text-gray-600">
                    {resume.company_name && `${resume.company_name} • `}
                    {resume.job_title || 'Custom Resume'}
                  </p>
                </div>
                <div className="flex items-center gap-3">
                  {resume.overall_match !== null && (
                    <span className={`inline-flex items-center gap-1 text-xs font-medium px-2.5 py-0.5 rounded-full ${
                      resume.overall_match >= 70 ? 'bg-green-100 text-green-800' :
                      resume.overall_match >= 40 ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      <TrendingUp className="h-3 w-3" />
                      {resume.overall_match}% Match
                    </span>
                  )}
                  <span className={`text-xs font-medium px-2.5 py-0.5 rounded-full ${
                    resume.status === 'approved' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                  }`}>
                    {resume.status}
                  </span>
                  <Link to={`/resumes/${resume.id}/edit`} className="text-sm text-blue-600 hover:underline">Edit</Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
