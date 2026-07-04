import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '../services/api'
import { Save, Download, Check, RefreshCw, ArrowLeft, Loader } from 'lucide-react'

export default function ResumeEditorPage() {
  const { id } = useParams<{ id: string }>()
  const queryClient = useQueryClient()
  const [editingSection, setEditingSection] = useState<number | null>(null)
  const [editContent, setEditContent] = useState('')

  const { data: resume, isLoading } = useQuery({
    queryKey: ['resume', id],
    queryFn: () => api.get(`/resumes/${id}`).then(r => r.data),
  })

  const updateResume = useMutation({
    mutationFn: (sections: any[]) => api.put(`/resumes/${id}`, { sections }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['resume', id] }),
  })

  const regenerateSection = useMutation({
    mutationFn: (sectionType: string) => api.post(`/resumes/${id}/regenerate-section`, null, { params: { section_type: sectionType } }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['resume', id] }),
  })

  const approveResume = useMutation({
    mutationFn: () => api.post(`/resumes/${id}/approve`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['resume', id] }),
  })

  const handleExport = (format: 'pdf' | 'docx') => {
    window.open(`http://localhost:8000/api/resumes/${id}/export/${format}`, '_blank')
  }

  if (isLoading) return <div className="text-center py-12">Loading resume...</div>
  if (!resume) return <div className="text-center py-12">Resume not found</div>

  const sections = resume.sections || []

  const startEdit = (section: any) => {
    setEditingSection(section.id)
    setEditContent(section.content)
  }

  const saveEdit = () => {
    const updated = sections.map((s: any) => s.id === editingSection ? { ...s, content: editContent } : s)
    updateResume.mutate(updated)
    setEditingSection(null)
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <Link to="/dashboard" className="text-gray-600 hover:text-gray-900">
            <ArrowLeft className="h-5 w-5" />
          </Link>
          <div>
            <h1 className="text-2xl font-bold">{resume.title}</h1>
            <p className="text-sm text-gray-600">
              Status: <span className={`font-medium ${resume.status === 'approved' ? 'text-green-600' : 'text-amber-600'}`}>{resume.status}</span>
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={() => handleExport('pdf')} className="inline-flex items-center gap-2 px-3 py-1.5 text-sm border border-gray-300 rounded-md bg-white hover:bg-gray-50">
            <Download className="h-4 w-4" /> PDF
          </button>
          <button onClick={() => handleExport('docx')} className="inline-flex items-center gap-2 px-3 py-1.5 text-sm border border-gray-300 rounded-md bg-white hover:bg-gray-50">
            <Download className="h-4 w-4" /> DOCX
          </button>
          {resume.status !== 'approved' && (
            <button onClick={() => approveResume.mutate()} disabled={approveResume.isPending} className="inline-flex items-center gap-2 px-3 py-1.5 text-sm text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50">
              <Check className="h-4 w-4" /> Approve
            </button>
          )}
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-gray-900">Edit Sections</h2>
          {sections.map((section: any) => (
            <div key={section.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide">{section.section_type}</h3>
                <div className="flex items-center gap-1">
                  {section.is_ai_generated && !section.is_edited && (
                    <span className="text-xs bg-purple-50 text-purple-700 px-2 py-0.5 rounded-full">AI</span>
                  )}
                  {section.is_edited && (
                    <span className="text-xs bg-amber-50 text-amber-700 px-2 py-0.5 rounded-full">Edited</span>
                  )}
                </div>
              </div>

              {editingSection === section.id ? (
                <div className="space-y-2">
                  <textarea rows={8} value={editContent} onChange={e => setEditContent(e.target.value)} className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm font-mono" />
                  <div className="flex gap-2">
                    <button onClick={saveEdit} className="inline-flex items-center gap-1 px-3 py-1.5 text-sm text-white bg-blue-600 rounded-md hover:bg-blue-700">
                      <Save className="h-3 w-3" /> Save
                    </button>
                    <button onClick={() => setEditingSection(null)} className="px-3 py-1.5 text-sm border border-gray-300 rounded-md bg-white hover:bg-gray-50">Cancel</button>
                  </div>
                </div>
              ) : (
                <div>
                  <pre className="text-sm text-gray-600 whitespace-pre-wrap font-sans bg-gray-50 p-3 rounded-md max-h-48 overflow-y-auto">
                    {section.content}
                  </pre>
                  <div className="flex gap-2 mt-2">
                    <button onClick={() => startEdit(section)} className="text-sm text-blue-600 hover:underline">Edit</button>
                    <button onClick={() => regenerateSection.mutate(section.section_type)} disabled={regenerateSection.isPending} className="text-sm text-gray-600 hover:text-gray-900 inline-flex items-center gap-1">
                      <RefreshCw className="h-3 w-3" /> Regenerate
                    </button>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        <div>
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Live Preview</h2>
          <div className="bg-white shadow-lg border border-gray-300 rounded-sm p-8 min-h-[800px]">
            {sections.map((section: any) => (
              <div key={section.id} className="mb-6">
                {section.section_type === 'header' ? (
                  <div className="text-center border-b-2 border-gray-800 pb-4 mb-6">
                    {section.content.split('\n').map((line: string, i: number) => (
                      <p key={i} className={i === 0 ? 'text-2xl font-bold text-gray-900' : 'text-sm text-gray-600'}>
                        {line}
                      </p>
                    ))}
                  </div>
                ) : section.section_type !== 'header' && (
                  <div>
                    <h3 className="text-sm font-bold text-gray-900 uppercase tracking-wider border-b border-gray-400 pb-1 mb-3">
                      {section.section_type === 'summary' && 'Professional Summary'}
                      {section.section_type === 'skills' && 'Technical Skills'}
                      {section.section_type === 'experience' && 'Professional Experience'}
                      {section.section_type === 'projects' && 'Projects'}
                      {section.section_type === 'education' && 'Education'}
                      {section.section_type === 'certifications' && 'Certifications'}
                    </h3>
                    <div className="text-sm text-gray-700 whitespace-pre-wrap leading-relaxed">
                      {section.content}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
