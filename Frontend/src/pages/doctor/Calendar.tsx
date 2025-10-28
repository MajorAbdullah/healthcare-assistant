import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Calendar as CalendarIcon, ChevronLeft, ChevronRight, Clock, User, FileText, CheckCircle, XCircle, LogOut } from "lucide-react";
import { Calendar } from "@/components/ui/calendar";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "sonner";
import api, { type Appointment } from "@/lib/api";

const CalendarView = () => {
  const navigate = useNavigate();
  const [date, setDate] = useState<Date | undefined>(new Date());
  const [selectedAppointment, setSelectedAppointment] = useState<Appointment | null>(null);
  const [notes, setNotes] = useState("");
  const [view, setView] = useState<"month" | "week" | "day">("month");
  const [isLoading, setIsLoading] = useState(false);
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [doctorId, setDoctorId] = useState<number>(0);

  const doctorName = localStorage.getItem("doctor_name") || "Doctor";

  useEffect(() => {
    const id = localStorage.getItem("doctor_id");
    if (!id) {
      toast.error("Please login first");
      navigate("/doctor/auth");
      return;
    }
    setDoctorId(parseInt(id));
    loadAppointments(parseInt(id));
  }, [navigate]);

  const loadAppointments = async (id: number) => {
    try {
      setIsLoading(true);
      const result = await api.doctor.getAppointments(id);
      if (result.success && result.data) {
        setAppointments(Array.isArray(result.data.appointments) ? result.data.appointments : []);
      }
    } catch (error: any) {
      toast.error(error.message || "Failed to load appointments");
      setAppointments([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.clear();
    navigate("/");
  };

  const handleAppointmentClick = (appointment: Appointment) => {
    setSelectedAppointment(appointment);
    setNotes(appointment.notes || "");
  };

  const handleSaveNotes = async () => {
    if (!selectedAppointment) return;
    
    try {
      const result = await api.appointment.updateNotes(
        selectedAppointment.appointment_id,
        notes
      );
      
      if (result.success) {
        toast.success("Notes saved successfully");
        loadAppointments(doctorId); // Reload appointments
        setSelectedAppointment(null);
      } else {
        toast.error(result.message || "Failed to save notes");
      }
    } catch (error: any) {
      toast.error(error.message || "Failed to save notes");
    }
  };

  const handleMarkComplete = async () => {
    if (!selectedAppointment) return;
    
    try {
      const result = await api.appointment.updateStatus(
        selectedAppointment.appointment_id,
        "completed"
      );
      
      if (result.success) {
        toast.success("Appointment marked as completed");
        loadAppointments(doctorId); // Reload appointments
        setSelectedAppointment(null);
      } else {
        toast.error(result.message || "Failed to update status");
      }
    } catch (error: any) {
      toast.error(error.message || "Failed to update status");
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "scheduled": return "bg-primary/20 text-primary border-primary/30";
      case "completed": return "bg-success/20 text-success border-success/30";
      case "cancelled": return "bg-destructive/20 text-destructive border-destructive/30";
      default: return "bg-muted";
    }
  };

  const getInitials = (name: string) => {
    return name.split(" ").map(n => n[0]).join("").toUpperCase();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      {/* Header */}
      <header className="glass-header sticky top-0 z-50 border-b border-white/20">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-foreground">Calendar</h1>
            <p className="text-sm text-muted-foreground">Dr. {doctorName}</p>
          </div>
          <div className="flex items-center gap-3">
            <Button variant="outline" onClick={() => navigate("/doctor/dashboard")} className="glass hover:scale-105 transition-transform">
              Dashboard
            </Button>
            <Button variant="outline" onClick={() => navigate("/doctor/patients")} className="glass hover:scale-105 transition-transform">
              Patients
            </Button>
            <Button variant="outline" onClick={() => navigate("/doctor/analytics")} className="glass hover:scale-105 transition-transform">
              Analytics
            </Button>
            <Button variant="outline" onClick={handleLogout} className="glass hover:scale-105 transition-transform">
              <LogOut className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Calendar Section */}
          <div className="lg:col-span-1">
            <Card className="glass-card shadow-card hover:shadow-card-hover transition-all duration-300 border-white/20">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <CalendarIcon className="h-5 w-5 text-primary" />
                  Select Date
                </CardTitle>
                <CardDescription>Choose a date to view appointments</CardDescription>
              </CardHeader>
              <CardContent>
                <Calendar
                  mode="single"
                  selected={date}
                  onSelect={setDate}
                  className="rounded-md"
                />
                <div className="mt-4 space-y-2">
                  <div className="flex items-center gap-2 text-sm">
                    <div className="w-3 h-3 rounded-full bg-primary"></div>
                    <span>Scheduled</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <div className="w-3 h-3 rounded-full bg-success"></div>
                    <span>Completed</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <div className="w-3 h-3 rounded-full bg-destructive"></div>
                    <span>Cancelled</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Appointments List */}
          <div className="lg:col-span-2">
            <Card className="glass-card shadow-card hover:shadow-card-hover transition-all duration-300 border-white/20">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Appointments</CardTitle>
                    <CardDescription>
                      {date?.toLocaleDateString("en-US", { weekday: "long", year: "numeric", month: "long", day: "numeric" })}
                    </CardDescription>
                  </div>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm" className={view === "day" ? "bg-primary text-primary-foreground" : ""} onClick={() => setView("day")}>
                      Day
                    </Button>
                    <Button variant="outline" size="sm" className={view === "week" ? "bg-primary text-primary-foreground" : ""} onClick={() => setView("week")}>
                      Week
                    </Button>
                    <Button variant="outline" size="sm" className={view === "month" ? "bg-primary text-primary-foreground" : ""} onClick={() => setView("month")}>
                      Month
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {isLoading ? (
                    <div className="flex justify-center py-8">
                      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
                    </div>
                  ) : appointments.length > 0 ? (
                    appointments.map((appointment) => (
                      <div
                        key={appointment.appointment_id}
                        onClick={() => handleAppointmentClick(appointment)}
                        className="glass p-4 rounded-lg border border-white/20 hover:scale-[1.02] transition-all duration-300 cursor-pointer hover:shadow-card"
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex items-start gap-3 flex-1">
                            <Avatar className="h-10 w-10">
                              <AvatarFallback className="bg-primary/10 text-primary">
                                {getInitials(appointment.patient_name || "Patient")}
                              </AvatarFallback>
                            </Avatar>
                            <div className="flex-1">
                              <div className="flex items-center gap-2 mb-1">
                                <h4 className="font-semibold">{appointment.patient_name || "Patient"}</h4>
                                <Badge variant="outline" className={getStatusColor(appointment.status)}>
                                  {appointment.status}
                                </Badge>
                              </div>
                              <div className="flex items-center gap-4 text-sm text-muted-foreground">
                                <span className="flex items-center gap-1">
                                  <Clock className="h-3 w-3" />
                                  {appointment.start_time}
                                </span>
                                <span className="flex items-center gap-1">
                                  <FileText className="h-3 w-3" />
                                  {appointment.reason || "Consultation"}
                                </span>
                              </div>
                              {appointment.notes && (
                                <p className="text-sm text-muted-foreground mt-2 italic">
                                  Notes: {appointment.notes}
                                </p>
                              )}
                            </div>
                          </div>
                          <Button variant="ghost" size="sm" className="hover:scale-110 transition-transform">
                            View
                          </Button>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-12">
                      <CalendarIcon className="h-12 w-12 mx-auto text-muted-foreground/50 mb-4" />
                      <p className="text-muted-foreground">No appointments scheduled for this date</p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      {/* Appointment Detail Dialog */}
      <Dialog open={!!selectedAppointment} onOpenChange={() => setSelectedAppointment(null)}>
        <DialogContent className="glass-card border-white/20">
          <DialogHeader>
            <DialogTitle>Appointment Details</DialogTitle>
            <DialogDescription>
              View and manage appointment information
            </DialogDescription>
          </DialogHeader>

          {selectedAppointment && (
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <Avatar className="h-16 w-16">
                  <AvatarFallback className="bg-primary/10 text-primary text-lg">
                    {getInitials(selectedAppointment.patient_name || "Patient")}
                  </AvatarFallback>
                </Avatar>
                <div>
                  <h3 className="font-semibold text-lg">{selectedAppointment.patient_name || "Patient"}</h3>
                  <p className="text-sm text-muted-foreground">{selectedAppointment.start_time}</p>
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Reason:</span>
                  <span className="text-sm font-medium">{selectedAppointment.reason || "Consultation"}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Status:</span>
                  <Badge variant="outline" className={getStatusColor(selectedAppointment.status)}>
                    {selectedAppointment.status}
                  </Badge>
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Medical Notes</label>
                <Textarea
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="Add medical notes here..."
                  className="glass border-white/20 min-h-[120px]"
                />
              </div>
            </div>
          )}

          <DialogFooter className="flex gap-2">
            {selectedAppointment?.status === "scheduled" && (
              <Button onClick={handleMarkComplete} className="bg-success hover:bg-success/90">
                <CheckCircle className="h-4 w-4 mr-2" />
                Mark Complete
              </Button>
            )}
            <Button onClick={handleSaveNotes} className="hover:scale-105 transition-transform">
              Save Notes
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default CalendarView;
