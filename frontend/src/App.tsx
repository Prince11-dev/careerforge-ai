import { Routes, Route } from 'react-router-dom'
import MainLayout from './layouts/MainLayout'
import LandingPage from './pages/LandingPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import OnboardingPage from './pages/OnboardingPage'
import DashboardPage from './pages/DashboardPage'
import ProfilePage from './pages/ProfilePage'
import NewJobPage from './pages/NewJobPage'
import JobAnalysisPage from './pages/JobAnalysisPage'
import ResumeEditorPage from './pages/ResumeEditorPage'
import ResumeHistoryPage from './pages/ResumeHistoryPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route element={<MainLayout />}>
        <Route path="/onboarding" element={<OnboardingPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/jobs/new" element={<NewJobPage />} />
        <Route path="/jobs/:id/analysis" element={<JobAnalysisPage />} />
        <Route path="/resumes/:id/edit" element={<ResumeEditorPage />} />
        <Route path="/resumes" element={<ResumeHistoryPage />} />
      </Route>
    </Routes>
  )
}

export default App
