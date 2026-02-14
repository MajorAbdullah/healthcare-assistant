import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";
import PatientAuth from "./pages/patient/Auth";
import PatientDashboard from "./pages/patient/Dashboard";
import DoctorAuth from "./pages/doctor/Auth";
import DoctorDashboard from "./pages/doctor/Dashboard";
import PatientBook from "./pages/patient/Book";
import PatientChat from "./pages/patient/Chat";
import PatientAppointments from "./pages/patient/Appointments";
import PatientProfile from "./pages/patient/Profile";
import DoctorCalendar from "./pages/doctor/Calendar";
import DoctorPatients from "./pages/doctor/Patients";
import DoctorPatientDetail from "./pages/doctor/PatientDetail";
import DoctorAnalytics from "./pages/doctor/Analytics";
import DoctorProfile from "./pages/doctor/Profile";
import AdminAuth from "./pages/admin/Auth";
import AdminDashboard from "./pages/admin/Dashboard";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />} />
          
          {/* Patient Routes */}
          <Route path="/patient/auth" element={<PatientAuth />} />
          <Route path="/patient/dashboard" element={<PatientDashboard />} />
          <Route path="/patient/book" element={<PatientBook />} />
          <Route path="/patient/chat" element={<PatientChat />} />
          <Route path="/patient/appointments" element={<PatientAppointments />} />
          <Route path="/patient/profile" element={<PatientProfile />} />
          
          {/* Doctor Routes */}
          <Route path="/doctor/auth" element={<DoctorAuth />} />
          <Route path="/doctor/dashboard" element={<DoctorDashboard />} />
          <Route path="/doctor/calendar" element={<DoctorCalendar />} />
          <Route path="/doctor/patients" element={<DoctorPatients />} />
          <Route path="/doctor/patients/:id" element={<DoctorPatientDetail />} />
          <Route path="/doctor/analytics" element={<DoctorAnalytics />} />
          <Route path="/doctor/profile" element={<DoctorProfile />} />
          
          {/* Admin Routes */}
          <Route path="/admin/auth" element={<AdminAuth />} />
          <Route path="/admin/dashboard" element={<AdminDashboard />} />
          
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
