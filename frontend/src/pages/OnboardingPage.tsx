import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { FileUp, PenLine, ArrowRight } from 'lucide-react'

export default function OnboardingPage() {
  const navigate = useNavigate()
  const [choice, setChoice] = useState<'upload' | 'manual' | null>(null)

  return (
    <div className="max-w-3xl mx-auto py-12">
      <h1 className="text-3xl font-bold text-center mb-4">Build Your Master Career Profile</h1>
      <p className="text-gray-600 text-center mb-12">Choose how you want to create your verified profile</p>

      <div className="grid md:grid-cols-2 gap-6">
        <button
          onClick={() => setChoice('upload')}
          className={`bg-white rounded-lg shadow-sm border p-8 text-left hover:shadow-md transition-all ${choice === 'upload' ? 'ring-2 ring-blue-500' : 'border-gray-200'}`}
        >
          <FileUp className="h-10 w-10 text-blue-600 mb-4" />
          <h3 className="text-xl font-semibold mb-2">Upload Existing Resume</h3>
          <p className="text-gray-600 text-sm">Upload your PDF or DOCX resume. We'll extract and structure your information for review.</p>
        </button>

        <button
          onClick={() => setChoice('manual')}
          className={`bg-white rounded-lg shadow-sm border p-8 text-left hover:shadow-md transition-all ${choice === 'manual' ? 'ring-2 ring-blue-500' : 'border-gray-200'}`}
        >
          <PenLine className="h-10 w-10 text-blue-600 mb-4" />
          <h3 className="text-xl font-semibold mb-2">Create Profile Manually</h3>
          <p className="text-gray-600 text-sm">Enter your career information step by step for maximum accuracy and control.</p>
        </button>
      </div>

      {choice && (
        <div className="mt-8 text-center">
          <button
            onClick={() => navigate('/profile', { state: { mode: choice } })}
            className="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700"
          >
            Continue <ArrowRight className="h-4 w-4 ml-2" />
          </button>
        </div>
      )}
    </div>
  )
}
