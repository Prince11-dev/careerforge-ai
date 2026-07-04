import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { api } from '../services/api'
import { FileText, TrendingUp, Calendar } from 'lucide-react'

export default function ResumeHistoryPage() {
  const { data: resumes, isLoading } = useQuery({
    queryKey: ['resumes'],
    queryFn: () => api.get('/resumes').then(r => r.data),
  })

  if (isLoading) return <div className="text-center py-12">Loading...</div>

  return (
    <div className="max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Resume History</h1>

      {resumes && resumes.length > 0 ? (
        <div className="space-y-4">
          {resumes.map((resume: any) => (
            <div key={resume.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 flex items-center justify-between hover:shadow-md transition-shadow">
              <div className="flex items-start gap-4">
                <div className="p-2 bg-blue-50 rounded-lg">
                  <FileText className="h-6 w-6 text-blue-600" />
                </div>
                <div>
                  <h3 className="font-medium text-gray-900">{resume.title}</h3>
                  <p className="text-sm text-gray-600">
                    {resume.company_name && `${resume.company_name} • `}
                    {resume.job_title || 'Custom'}
                  </p>
                  <div className="flex items-center gap-3 mt-2">
                    <span className="text-xs text-gray-500 flex items-center gap-1">
                      <Calendar className="h-3 w-3" />
                      {new Date(resume.created_at).toLocaleDateString()}
                    </span>
                    {resume.overall_match !== null && (
                      <span className={`text-xs font-medium px-2 py-0.5 rounded-full flex items-center gap-1 ${
                        resume.overall_match >= 70 ? 'bg-green-100 text-green-800' :
                        resume.overall_match >= 40 ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        <TrendingUp className="h-3 w-3" />
                        {resume.overall_match}% match
                      </span>
                    )}
                    <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                      resume.status === 'approved' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {resume.status}
                    </span>
                  </div>
                </div>
              </div>
              <Link to={`/resumes/${resume.id}/edit`} className="px-4 py-2 text-sm border border-gray-300 rounded-md bg-white hover:bg-gray-50">
                View / Edit
              </Link>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-16 bg-white rounded-lg shadow-sm border border-gray-200">
          <FileText className="h-12 w-12 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No resumes yet</h3>
          <p className="text-gray-600 mb-4">Create your first tailored resume by analyzing a job description.</p>
          <Link to="/jobs/new" className="inline-flex items-center justify-center px-4 py-2 text-sm text-white bg-blue-600 rounded-md hover:bg-blue-700">Analyze a Job</Link>
        </div>
      )}
    </div>
  )
}
