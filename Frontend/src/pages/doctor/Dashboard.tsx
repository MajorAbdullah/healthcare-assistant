import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Calendar, Users, Clock, TrendingUp, LogOut, CalendarDays, UserCircle, BarChart3, User, CheckCircle, XCircle } from "lucide-react";
import { toast } from "sonner";
import api, { type Appointment, type DoctorStats } from "@/lib/api";

const DoctorDashboard = () => {
  const navigate = useNavigate();
  const [doctorName, setDoctorName] = useState("");
  const [specialty, setSpecialty] = useState("");
  const [doctorId, setDoctorId] = useState<number>(0);
  const [isLoading, setIsLoading] = useState(false);
  
  // Stats
  const [stats, setStats] = useState<DoctorStats>({
    today_count: 0,
    total_patients: 0,
    week_count: 0,
    completion_rate: 0
  });
  
  // Today's appointments
  const [todaySchedule, setTodaySchedule] = useState<Appointment[]>([]);

  useEffect(() => {
    const name = localStorage.getItem("doctor_name") || "Doctor";
    const spec = localStorage.getItem("doctor_specialty") || "";
    const id = localStorage.getItem("doctor_id");
    
    if (!id) {
      toast.error("Please login first");
      navigate("/doctor/auth");
      return;
    }
    
    setDoctorName(name);
    setSpecialty(spec);
    setDoctorId(parseInt(id));
    
    loadDashboardData(parseInt(id));
  }, [navigate]);

  const loadDashboardData = async (id: number) => {
    try {
      setIsLoading(true);
      
      // Load stats
      const statsResult = await api.doctor.getStats(id);
      if (statsResult.success && statsResult.data) {
        setStats(statsResult.data);
      }
      
      // Load today's appointments
      const appointmentsResult = await api.doctor.getAppointments(id);
      if (appointmentsResult.success && appointmentsResult.data) {
        // Handle both array and object with appointments property
        const appointments = Array.isArray(appointmentsResult.data) 
          ? appointmentsResult.data 
          : appointmentsResult.data.appointments || [];
        setTodaySchedule(appointments);
      }
    } catch (error: any) {
      console.error("Dashboard load error:", error);
      toast.error(error.message || "Failed to load dashboard data");
      // Set empty array on error to prevent crashes
      setTodaySchedule([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleApprove = async (appointmentId: number) => {
    try {
      const result = await api.appointment.approve(appointmentId);
      if (result.success) {
        toast.success("Appointment approved and patient notified!");
        loadDashboardData(doctorId);
      } else {
        toast.error(result.message || "Failed to approve appointment");
      }
    } catch (error: any) {
      toast.error(error.message || "Failed to approve appointment");
    }
  };

  const handleReject = async (appointmentId: number) => {
    try {
      const result = await api.appointment.reject(appointmentId);
      if (result.success) {
        toast.success("Appointment request rejected");
        loadDashboardData(doctorId);
      } else {
        toast.error(result.message || "Failed to reject appointment");
      }
    } catch (error: any) {
      toast.error(error.message || "Failed to reject appointment");
    }
  };

  const handleLogout = () => {
    localStorage.clear();
    navigate("/");
  };

  const statCards = [
    { label: "Today's Appointments", value: String(stats.today_count), icon: Calendar, color: "text-primary" },
    { label: "Total Patients", value: String(stats.total_patients), icon: Users, color: "text-secondary" },
    { label: "This Week", value: String(stats.week_count), icon: Clock, color: "text-accent" },
    { label: "Completion Rate", value: `${stats.completion_rate}%`, icon: TrendingUp, color: "text-success" },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b shadow-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Avatar className="h-12 w-12 border-2 border-primary">
              <AvatarFallback className="bg-primary text-primary-foreground">
                {doctorName.split(" ").map(n => n[1] || n[0]).join("").toUpperCase()}
              </AvatarFallback>
            </Avatar>
            <div>
              <h1 className="text-xl font-semibold">Welcome back, {doctorName}</h1>
              <p className="text-sm text-muted-foreground">{specialty}</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Button 
              variant="outline" 
              className="gap-2"
              onClick={() => navigate("/doctor/calendar")}
            >
              <CalendarDays className="h-4 w-4" />
              Calendar
            </Button>
            <Button 
              variant="outline" 
              className="gap-2"
              onClick={() => navigate("/doctor/patients")}
            >
              <UserCircle className="h-4 w-4" />
              Patients
            </Button>
            <Button 
              variant="outline" 
              className="gap-2"
              onClick={() => navigate("/doctor/analytics")}
            >
              <BarChart3 className="h-4 w-4" />
              Analytics
            </Button>
            <Button 
              variant="outline" 
              size="icon"
              onClick={() => navigate("/doctor/profile")}
            >
              <User className="h-5 w-5" />
            </Button>
            <Button 
              variant="ghost" 
              size="icon"
              onClick={handleLogout}
            >
              <LogOut className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Statistics Cards */}
        {isLoading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        ) : (
          <>
            <div className="grid md:grid-cols-4 gap-6 mb-8">
              {statCards.map((stat, index) => (
                <Card key={index} className="shadow-card">
                  <CardHeader className="flex flex-row items-center justify-between pb-2">
                    <CardTitle className="text-sm font-medium text-muted-foreground">
                      {stat.label}
                    </CardTitle>
                    <stat.icon className={`h-5 w-5 ${stat.color}`} />
                  </CardHeader>
                  <CardContent>
                    <div className="text-3xl font-bold">{stat.value}</div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Today's Schedule */}
            <Card className="shadow-card">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-2xl">Today's Schedule</CardTitle>
                  <Badge variant="secondary" className="text-sm">
                    {new Date().toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" })}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                {todaySchedule && todaySchedule.length > 0 ? (
                  todaySchedule.map((appointment) => (
                    <div 
                      key={appointment.appointment_id}
                      className={`flex items-center gap-4 p-4 rounded-lg border ${
                        appointment.status === 'pending_approval' ? 'bg-amber-50 border-amber-300' : 'bg-card'
                      } hover:shadow-md transition-shadow`}
                    >
                      <div className="w-20 flex-shrink-0">
                        <div className="text-sm font-semibold">{appointment.start_time}</div>
                      </div>
                      <div className="flex-1">
                        <div className="font-medium">{appointment.patient_name || "Patient"}</div>
                        <div className="text-sm text-muted-foreground">{appointment.reason || "Consultation"}</div>
                      </div>
                      <Badge 
                        variant={
                          appointment.status === "completed" ? "default" : 
                          appointment.status === "pending_approval" ? "outline" : 
                          "secondary"
                        }
                        className={
                          appointment.status === "completed" ? "bg-success" : 
                          appointment.status === "pending_approval" ? "bg-amber-100 text-amber-800 border-amber-300" : 
                          ""
                        }
                      >
                        {appointment.status === 'pending_approval' ? 'Pending Approval' : 
                         appointment.status.charAt(0).toUpperCase() + appointment.status.slice(1)}
                      </Badge>
                      <div className="flex gap-2">
                        {appointment.status === "pending_approval" ? (
                          <>
                            <Button 
                              variant="default" 
                              size="sm"
                              className="bg-green-600 hover:bg-green-700"
                              onClick={() => handleApprove(appointment.appointment_id)}
                            >
                              <CheckCircle className="h-4 w-4 mr-1" />
                              Approve
                            </Button>
                            <Button 
                              variant="outline" 
                              size="sm"
                              className="text-red-600 hover:bg-red-50"
                              onClick={() => handleReject(appointment.appointment_id)}
                            >
                              <XCircle className="h-4 w-4 mr-1" />
                              Reject
                            </Button>
                          </>
                        ) : (
                          <>
                            <Button 
                              variant="outline" 
                              size="sm"
                              onClick={() => navigate(`/doctor/patients/${appointment.user_id}`)}
                            >
                              View Details
                            </Button>
                            {appointment.status === "scheduled" && (
                              <Button 
                                variant="default" 
                                size="sm"
                                onClick={() => navigate(`/doctor/patients/${appointment.user_id}`)}
                              >
                                Add Notes
                              </Button>
                            )}
                          </>
                        )}
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-8 text-muted-foreground">
                    No appointments scheduled for today
                  </div>
                )}
              </CardContent>
            </Card>
          </>
        )}
      </main>
    </div>
  );
};

export default DoctorDashboard;
