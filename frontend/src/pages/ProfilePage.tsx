import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '../services/api'
import { Plus, Trash2, Save, Upload, Check } from 'lucide-react'

export default function ProfilePage() {
  const queryClient = useQueryClient()
  const [activeTab, setActiveTab] = useState('personal')
  const [file, setFile] = useState<File | null>(null)
  const [uploadMessage, setUploadMessage] = useState('')

  const { data: profile, isLoading } = useQuery({
    queryKey: ['profile'],
    queryFn: () => api.get('/profile').then(r => r.data),
  })

  const updateProfile = useMutation({
    mutationFn: (data: any) => api.put('/profile', data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['profile'] }),
  })

  const uploadResume = useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData()
      formData.append('file', file)
      return api.post('/profile/resume-upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
    },
    onSuccess: (res) => {
      setUploadMessage(res.data.message)
      queryClient.invalidateQueries({ queryKey: ['profile'] })
    },
  })

  const handleFileUpload = async () => {
    if (!file) return
    await uploadResume.mutateAsync(file)
    setFile(null)
  }

  if (isLoading) return <div className="text-center py-12">Loading profile...</div>

  const personalInfo = profile?.personal_info || {}

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Master Career Profile</h1>
        <div className="flex items-center gap-2">
          {profile?.is_verified && (
            <span className="inline-flex items-center gap-1 text-xs font-medium px-2.5 py-1 rounded-full bg-green-100 text-green-800">
              <Check className="h-3 w-3" /> Verified
            </span>
          )}
          <span className="text-sm text-gray-600">Completion: {profile?.completion_percentage || 0}%</span>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-6">
        <div className="border-b border-gray-200">
          <nav className="flex -mb-px">
            {['personal', 'experience', 'skills', 'projects', 'education', 'certifications'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-4 py-3 text-sm font-medium border-b-2 ${
                  activeTab === tab
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'personal' && (
            <div className="space-y-6">
              <div className="bg-blue-50 border border-blue-200 rounded-md p-4 mb-4">
                <h4 className="text-sm font-medium text-blue-900 mb-1">Upload Resume</h4>
                <p className="text-sm text-blue-700 mb-3">Quickly populate your profile by uploading an existing resume.</p>
                <div className="flex items-center gap-3">
                  <input type="file" accept=".pdf,.docx,.doc" onChange={e => setFile(e.target.files?.[0] || null)} className="text-sm" />
                  <button onClick={handleFileUpload} disabled={!file || uploadResume.isPending} className="inline-flex items-center gap-1 px-3 py-1.5 text-sm text-white bg-blue-600 rounded-md hover:bg-blue-700">
                    <Upload className="h-3 w-3" /> {uploadResume.isPending ? 'Parsing...' : 'Parse'}
                  </button>
                </div>
                {uploadMessage && <p className="text-sm text-green-600 mt-2">{uploadMessage}</p>}
              </div>

              <PersonalInfoForm data={personalInfo} onSave={(data) => updateProfile.mutate({ personal_info: data })} />
            </div>
          )}

          {activeTab === 'experience' && <ExperienceManager experiences={profile?.experiences || []} />}
          {activeTab === 'skills' && <SkillsManager skills={profile?.skills || []} />}
          {activeTab === 'projects' && <ProjectsManager projects={profile?.projects || []} />}
          {activeTab === 'education' && <EducationManager education={profile?.education || []} />}
          {activeTab === 'certifications' && <CertificationsManager certifications={profile?.certifications || []} />}
        </div>
      </div>
    </div>
  )
}

function PersonalInfoForm({ data, onSave }: { data: any; onSave: (d: any) => void }) {
  const [form, setForm] = useState(data)

  return (
    <div className="grid md:grid-cols-2 gap-4">
      {[
        ['full_name', 'Full Name'],
        ['professional_headline', 'Professional Headline'],
        ['email', 'Email'],
        ['phone', 'Phone'],
        ['city', 'City'],
        ['state', 'State'],
        ['country', 'Country'],
        ['linkedin_url', 'LinkedIn URL'],
        ['github_url', 'GitHub URL'],
        ['portfolio_url', 'Portfolio URL'],
      ].map(([key, label]) => (
        <div key={key} className={key === 'professional_headline' ? 'md:col-span-2' : ''}>
          <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
          <input type={key.includes('url') ? 'url' : 'text'} value={form[key] || ''} onChange={e => setForm({ ...form, [key]: e.target.value })} className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" />
        </div>
      ))}
      <div className="md:col-span-2">
        <label className="block text-sm font-medium text-gray-700 mb-1">Professional Summary Facts</label>
        <textarea rows={4} value={form.professional_summary_facts || ''} onChange={e => setForm({ ...form, professional_summary_facts: e.target.value })} className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" placeholder="Verified facts about your career..." />
      </div>
      <div className="md:col-span-2">
        <button onClick={() => onSave(form)} className="inline-flex items-center gap-2 px-4 py-2 text-sm text-white bg-blue-600 rounded-md hover:bg-blue-700">
          <Save className="h-4 w-4" /> Save Personal Info
        </button>
      </div>
    </div>
  )
}

function ExperienceManager({ experiences }: { experiences: any[] }) {
  const queryClient = useQueryClient()
  const [adding, setAdding] = useState(false)

  const addExp = useMutation({
    mutationFn: (data: any) => api.post('/profile/experiences', data),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['profile'] }); setAdding(false) },
  })

  const deleteExp = useMutation({
    mutationFn: (id: number) => api.delete(`/profile/experiences/${id}`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['profile'] }),
  })

  return (
    <div>
      <button onClick={() => setAdding(true)} className="mb-4 inline-flex items-center gap-2 px-4 py-2 border border-gray-300 text-sm font-medium rounded-md bg-white hover:bg-gray-50">
        <Plus className="h-4 w-4" /> Add Experience
      </button>

      {adding && (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-4 space-y-3">
          <input placeholder="Company" className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" id="exp-company" />
          <input placeholder="Role" className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" id="exp-role" />
          <input placeholder="Employment Type" className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" id="exp-type" />
          <textarea placeholder="Description" className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" rows={2} id="exp-desc" />
          <textarea placeholder="Technologies Used (comma separated)" className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" rows={1} id="exp-tech" />
          <div className="flex gap-2">
            <button onClick={() => {
              const data = {
                company: (document.getElementById('exp-company') as HTMLInputElement).value,
                role: (document.getElementById('exp-role') as HTMLInputElement).value,
                employment_type: (document.getElementById('exp-type') as HTMLInputElement).value,
                description: (document.getElementById('exp-desc') as HTMLTextAreaElement).value,
                technologies_used: (document.getElementById('exp-tech') as HTMLInputElement).value,
              }
              addExp.mutate(data)
            }} className="px-3 py-1.5 text-sm text-white bg-blue-600 rounded-md hover:bg-blue-700">Save</button>
            <button onClick={() => setAdding(false)} className="px-3 py-1.5 text-sm border border-gray-300 rounded-md bg-white hover:bg-gray-50">Cancel</button>
          </div>
        </div>
      )}

      <div className="space-y-4">
        {experiences.map((exp: any) => (
          <div key={exp.id} className="border border-gray-200 rounded-lg p-4">
            <div className="flex items-start justify-between">
              <div>
                <p className="font-medium text-gray-900">{exp.role}</p>
                <p className="text-sm text-gray-600">{exp.company} {exp.employment_type && `• ${exp.employment_type}`}</p>
                <p className="text-sm text-gray-500 mt-1">{exp.description}</p>
                {exp.technologies_used && <p className="text-xs text-gray-500 mt-1">Tech: {exp.technologies_used}</p>}
              </div>
              <button onClick={() => deleteExp.mutate(exp.id)} className="text-red-600 hover:text-red-800">
                <Trash2 className="h-4 w-4" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

function SkillsManager({ skills }: { skills: any[] }) {
  const queryClient = useQueryClient()
  const [name, setName] = useState('')
  const [category, setCategory] = useState('programming_languages')

  const addSkill = useMutation({
    mutationFn: (data: any) => api.post('/profile/skills', data),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['profile'] }); setName('') },
  })

  const deleteSkill = useMutation({
    mutationFn: (id: number) => api.delete(`/profile/skills/${id}`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['profile'] }),
  })

  const categories = ['programming_languages', 'backend', 'frontend', 'databases', 'cloud', 'devops', 'ai_ml', 'tools', 'other']

  return (
    <div>
      <div className="flex gap-2 mb-4">
        <input placeholder="Skill name" className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" value={name} onChange={e => setName(e.target.value)} />
        <select className="block w-40 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" value={category} onChange={e => setCategory(e.target.value)}>
          {categories.map(c => <option key={c} value={c}>{c.replace('_', ' ')}</option>)}
        </select>
        <button onClick={() => addSkill.mutate({ name, category })} className="px-3 py-1.5 text-sm text-white bg-blue-600 rounded-md hover:bg-blue-700">Add</button>
      </div>

      <div className="flex flex-wrap gap-2">
        {skills.map((skill: any) => (
          <span key={skill.id} className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-blue-50 text-blue-700 text-sm border border-blue-200">
            {skill.name}
            <button onClick={() => deleteSkill.mutate(skill.id)} className="hover:text-blue-900">
              <Trash2 className="h-3 w-3" />
            </button>
          </span>
        ))}
      </div>
    </div>
  )
}

function ProjectsManager({ projects }: { projects: any[] }) {
  const queryClient = useQueryClient()
  const [adding, setAdding] = useState(false)

  const addProject = useMutation({
    mutationFn: (data: any) => api.post('/profile/projects', data),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['profile'] }); setAdding(false) },
  })

  const deleteProject = useMutation({
    mutationFn: (id: number) => api.delete(`/profile/projects/${id}`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['profile'] }),
  })

  return (
    <div>
      <button onClick={() => setAdding(true)} className="mb-4 inline-flex items-center gap-2 px-4 py-2 border border-gray-300 text-sm font-medium rounded-md bg-white hover:bg-gray-50">
        <Plus className="h-4 w-4" /> Add Project
      </button>

      {adding && (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-4 space-y-3">
          <input placeholder="Project Name" className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" id="proj-name" />
          <textarea placeholder="Description" className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" rows={2} id="proj-desc" />
          <input placeholder="Technologies" className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" id="proj-tech" />
          <div className="flex gap-2">
            <button onClick={() => addProject.mutate({
              name: (document.getElementById('proj-name') as HTMLInputElement).value,
              description: (document.getElementById('proj-desc') as HTMLTextAreaElement).value,
              technologies: (document.getElementById('proj-tech') as HTMLInputElement).value,
            })} className="px-3 py-1.5 text-sm text-white bg-blue-600 rounded-md hover:bg-blue-700">Save</button>
            <button onClick={() => setAdding(false)} className="px-3 py-1.5 text-sm border border-gray-300 rounded-md bg-white hover:bg-gray-50">Cancel</button>
          </div>
        </div>
      )}

      <div className="space-y-4">
        {projects.map((proj: any) => (
          <div key={proj.id} className="border border-gray-200 rounded-lg p-4">
            <div className="flex items-start justify-between">
              <div>
                <p className="font-medium text-gray-900">{proj.name}</p>
                <p className="text-sm text-gray-600">{proj.description}</p>
                {proj.technologies && <p className="text-xs text-gray-500 mt-1">Tech: {proj.technologies}</p>}
              </div>
              <button onClick={() => deleteProject.mutate(proj.id)} className="text-red-600 hover:text-red-800">
                <Trash2 className="h-4 w-4" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

function EducationManager({ education }: { education: any[] }) {
  const queryClient = useQueryClient()
  const [adding, setAdding] = useState(false)

  const addEdu = useMutation({
    mutationFn: (data: any) => api.post('/profile/education', data),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['profile'] }); setAdding(false) },
  })

  const deleteEdu = useMutation({
    mutationFn: (id: number) => api.delete(`/profile/education/${id}`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['profile'] }),
  })

  return (
    <div>
      <button onClick={() => setAdding(true)} className="mb-4 inline-flex items-center gap-2 px-4 py-2 border border-gray-300 text-sm font-medium rounded-md bg-white hover:bg-gray-50">
        <Plus className="h-4 w-4" /> Add Education
      </button>

      {adding && (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-4 space-y-3">
          <input placeholder="Institution" className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" id="edu-inst" />
          <input placeholder="Degree" className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" id="edu-degree" />
          <input placeholder="Field" className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" id="edu-field" />
          <div className="flex gap-2">
            <button onClick={() => addEdu.mutate({
              institution: (document.getElementById('edu-inst') as HTMLInputElement).value,
              degree: (document.getElementById('edu-degree') as HTMLInputElement).value,
              field: (document.getElementById('edu-field') as HTMLInputElement).value,
            })} className="px-3 py-1.5 text-sm text-white bg-blue-600 rounded-md hover:bg-blue-700">Save</button>
            <button onClick={() => setAdding(false)} className="px-3 py-1.5 text-sm border border-gray-300 rounded-md bg-white hover:bg-gray-50">Cancel</button>
          </div>
        </div>
      )}

      <div className="space-y-4">
        {education.map((edu: any) => (
          <div key={edu.id} className="border border-gray-200 rounded-lg p-4 flex items-start justify-between">
            <div>
              <p className="font-medium text-gray-900">{edu.degree} {edu.field && `in ${edu.field}`}</p>
              <p className="text-sm text-gray-600">{edu.institution}</p>
            </div>
            <button onClick={() => deleteEdu.mutate(edu.id)} className="text-red-600 hover:text-red-800">
              <Trash2 className="h-4 w-4" />
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}

function CertificationsManager({ certifications }: { certifications: any[] }) {
  const queryClient = useQueryClient()
  const [adding, setAdding] = useState(false)

  const addCert = useMutation({
    mutationFn: (data: any) => api.post('/profile/certifications', data),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['profile'] }); setAdding(false) },
  })

  const deleteCert = useMutation({
    mutationFn: (id: number) => api.delete(`/profile/certifications/${id}`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['profile'] }),
  })

  return (
    <div>
      <button onClick={() => setAdding(true)} className="mb-4 inline-flex items-center gap-2 px-4 py-2 border border-gray-300 text-sm font-medium rounded-md bg-white hover:bg-gray-50">
        <Plus className="h-4 w-4" /> Add Certification
      </button>

      {adding && (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-4 space-y-3">
          <input placeholder="Certification Name" className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" id="cert-name" />
          <input placeholder="Issuing Organization" className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" id="cert-org" />
          <input placeholder="Credential URL" className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" id="cert-url" />
          <div className="flex gap-2">
            <button onClick={() => addCert.mutate({
              name: (document.getElementById('cert-name') as HTMLInputElement).value,
              issuing_organization: (document.getElementById('cert-org') as HTMLInputElement).value,
              credential_url: (document.getElementById('cert-url') as HTMLInputElement).value,
            })} className="px-3 py-1.5 text-sm text-white bg-blue-600 rounded-md hover:bg-blue-700">Save</button>
            <button onClick={() => setAdding(false)} className="px-3 py-1.5 text-sm border border-gray-300 rounded-md bg-white hover:bg-gray-50">Cancel</button>
          </div>
        </div>
      )}

      <div className="space-y-4">
        {certifications.map((cert: any) => (
          <div key={cert.id} className="border border-gray-200 rounded-lg p-4 flex items-start justify-between">
            <div>
              <p className="font-medium text-gray-900">{cert.name}</p>
              <p className="text-sm text-gray-600">{cert.issuing_organization}</p>
            </div>
            <button onClick={() => deleteCert.mutate(cert.id)} className="text-red-600 hover:text-red-800">
              <Trash2 className="h-4 w-4" />
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
