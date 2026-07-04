import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import { api } from '../services/api'
import { AlertCircle, Loader } from 'lucide-react'

export default function NewJobPage() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ company_name: '', job_title: '', job_url: '', raw_text: '' })
  const [error, setError] = useState('')

  const analyze = useMutation({
    mutationFn: (data: any) => api.post('/jobs/analyze', data),
    onSuccess: (res) => {
      navigate(`/jobs/${res.data.id}/analysis`)
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || 'Analysis failed')
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    if (form.raw_text.length < 50) {
      setError('Job description must be at least 50 characters')
      return
    }
    analyze.mutate(form)
  }

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-2">New Job Application</h1>
      <p className="text-gray-600 mb-6">Paste the job description to analyze and generate a tailored resume.</p>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        {error && (
          <div className="mb-4 p-3 bg-red-50 text-red-700 rounded-md text-sm flex items-center gap-2">
            <AlertCircle className="h-4 w-4" /> {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Company Name</label>
              <input type="text" value={form.company_name} onChange={e => setForm({ ...form, company_name: e.target.value })} className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" placeholder="e.g. Acme Corp" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Job Title</label>
              <input type="text" value={form.job_title} onChange={e => setForm({ ...form, job_title: e.target.value })} className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" placeholder="e.g. Senior Engineer" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Job URL</label>
              <input type="url" value={form.job_url} onChange={e => setForm({ ...form, job_url: e.target.value })} className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" placeholder="https://..." />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Job Description *</label>
            <textarea rows={12} required value={form.raw_text} onChange={e => setForm({ ...form, raw_text: e.target.value })} className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" placeholder="Paste the full job description here..." />
            <p className="text-xs text-gray-500 mt-1">{form.raw_text.length} characters</p>
          </div>

          <button type="submit" disabled={analyze.isPending} className="inline-flex items-center gap-2 px-4 py-2 text-sm text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50">
            {analyze.isPending ? <Loader className="h-4 w-4 animate-spin" /> : null}
            {analyze.isPending ? 'Analyzing...' : 'Analyze Job Description'}
          </button>
        </form>
      </div>
    </div>
  )
}
