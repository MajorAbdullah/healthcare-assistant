import { useState } from "react";
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

interface Appointment {
  id: number;
  time: string;
  patientName: string;
  patientId: number;
  reason: string;
  status: "scheduled" | "completed" | "cancelled";
  notes?: string;
}

const CalendarView = () => {
  const navigate = useNavigate();
  const [date, setDate] = useState<Date | undefined>(new Date());
  const [selectedAppointment, setSelectedAppointment] = useState<Appointment | null>(null);
  const [notes, setNotes] = useState("");
  const [view, setView] = useState<"month" | "week" | "day">("month");

  const doctorName = localStorage.getItem("doctorName") || "Doctor";

  // Mock appointments data
  const appointments: Appointment[] = [
    { id: 1, time: "09:00 AM", patientName: "Sarah Johnson", patientId: 1, reason: "Regular checkup", status: "scheduled" },
    { id: 2, time: "10:30 AM", patientName: "Michael Chen", patientId: 2, reason: "Blood pressure monitoring", status: "completed", notes: "BP normal, continue medication" },
    { id: 3, time: "11:00 AM", patientName: "Emily Davis", patientId: 3, reason: "Diabetes consultation", status: "scheduled" },
    { id: 4, time: "02:00 PM", patientName: "James Wilson", patientId: 4, reason: "Follow-up appointment", status: "cancelled" },
    { id: 5, time: "03:30 PM", patientName: "Lisa Anderson", patientId: 5, reason: "Vaccination", status: "scheduled" },
  ];

  const handleLogout = () => {
    localStorage.clear();
    navigate("/");
  };

  const handleAppointmentClick = (appointment: Appointment) => {
    setSelectedAppointment(appointment);
    setNotes(appointment.notes || "");
  };

  const handleSaveNotes = () => {
    if (selectedAppointment) {
      toast.success("Notes saved successfully");
      setSelectedAppointment(null);
    }
  };

  const handleMarkComplete = () => {
    if (selectedAppointment) {
      toast.success("Appointment marked as completed");
      setSelectedAppointment(null);
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
                  {appointments.map((appointment) => (
                    <div
                      key={appointment.id}
                      onClick={() => handleAppointmentClick(appointment)}
                      className="glass p-4 rounded-lg border border-white/20 hover:scale-[1.02] transition-all duration-300 cursor-pointer hover:shadow-card"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex items-start gap-3 flex-1">
                          <Avatar className="h-10 w-10">
                            <AvatarFallback className="bg-primary/10 text-primary">
                              {getInitials(appointment.patientName)}
                            </AvatarFallback>
                          </Avatar>
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                              <h4 className="font-semibold">{appointment.patientName}</h4>
                              <Badge variant="outline" className={getStatusColor(appointment.status)}>
                                {appointment.status}
                              </Badge>
                            </div>
                            <div className="flex items-center gap-4 text-sm text-muted-foreground">
                              <span className="flex items-center gap-1">
                                <Clock className="h-3 w-3" />
                                {appointment.time}
                              </span>
                              <span className="flex items-center gap-1">
                                <FileText className="h-3 w-3" />
                                {appointment.reason}
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
                  ))}

                  {appointments.length === 0 && (
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
                    {getInitials(selectedAppointment.patientName)}
                  </AvatarFallback>
                </Avatar>
                <div>
                  <h3 className="font-semibold text-lg">{selectedAppointment.patientName}</h3>
                  <p className="text-sm text-muted-foreground">{selectedAppointment.time}</p>
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Reason:</span>
                  <span className="text-sm font-medium">{selectedAppointment.reason}</span>
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
