import { useParams, Link } from 'react-router-dom'
import { useQuery, useMutation } from '@tanstack/react-query'
import { api } from '../services/api'
import { ArrowRight, Loader } from 'lucide-react'

export default function JobAnalysisPage() {
  const { id } = useParams<{ id: string }>()

  const { data: job, isLoading } = useQuery({
    queryKey: ['job', id],
    queryFn: () => api.get('/jobs/history').then(r => r.data.find((j: any) => j.id === Number(id))),
  })

  const generateResume = useMutation({
    mutationFn: () => api.post('/resumes/generate', {
      job_description_id: Number(id),
      title: job?.job_title ? `Resume for ${job.job_title}` : 'Tailored Resume'
    }),
    onSuccess: (res) => {
      window.location.href = `/resumes/${res.data.id}/edit`
    },
  })

  if (isLoading) return <div className="text-center py-12">Loading analysis...</div>
  if (!job) return <div className="text-center py-12">Job not found</div>

  const analysis = job.analysis || {}

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-2">JD Match Analysis</h1>
      <p className="text-gray-600 mb-6">
        {job.company_name && `${job.company_name} • `}{job.job_title || 'Job Analysis'}
      </p>

      <div className="grid md:grid-cols-2 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Detected Role</h3>
          <p className="text-gray-900 font-medium">{analysis.detected_role || 'Not detected'}</p>
          <p className="text-sm text-gray-600 mt-1">Seniority: {analysis.seniority || 'Unknown'}</p>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Skills Analysis</h3>
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Mandatory Skills</span>
              <span className="font-medium">{analysis.mandatory_skills?.length || 0}</span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Preferred Skills</span>
              <span className="font-medium">{analysis.preferred_skills?.length || 0}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Extracted Skills & Keywords</h3>
        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <p className="text-sm font-medium text-gray-700 mb-2">Mandatory Skills</p>
            <div className="flex flex-wrap gap-2">
              {(analysis.mandatory_skills || []).map((s: string) => (
                <span key={s} className="px-2 py-1 bg-red-50 text-red-700 text-xs rounded-full border border-red-200">{s}</span>
              ))}
            </div>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-700 mb-2">Preferred Skills</p>
            <div className="flex flex-wrap gap-2">
              {(analysis.preferred_skills || []).map((s: string) => (
                <span key={s} className="px-2 py-1 bg-blue-50 text-blue-700 text-xs rounded-full border border-blue-200">{s}</span>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Responsibilities</h3>
        <ul className="space-y-2">
          {(analysis.responsibilities || []).map((r: string, i: number) => (
            <li key={i} className="text-sm text-gray-600 flex items-start gap-2">
              <span className="text-blue-600 mt-0.5">•</span> {r}
            </li>
          ))}
        </ul>
      </div>

      <div className="flex justify-end">
        <button onClick={() => generateResume.mutate()} disabled={generateResume.isPending} className="inline-flex items-center gap-2 px-4 py-2 text-sm text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50">
          {generateResume.isPending ? <Loader className="h-4 w-4 animate-spin" /> : <ArrowRight className="h-4 w-4" />}
          {generateResume.isPending ? 'Generating...' : 'Generate Tailored Resume'}
        </button>
      </div>
    </div>
  )
}
