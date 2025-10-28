import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { ArrowLeft, LogOut, Mail, Phone, Calendar, User, FileText, Edit, Save, X } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Textarea } from "@/components/ui/textarea";
import { Separator } from "@/components/ui/separator";
import { toast } from "sonner";
import api, { type Patient, type Appointment } from "@/lib/api";

const PatientDetail = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [editingNote, setEditingNote] = useState<number | null>(null);
  const [noteText, setNoteText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [patient, setPatient] = useState<Patient | null>(null);
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [doctorId, setDoctorId] = useState<number>(0);

  const doctorName = localStorage.getItem("doctor_name") || "Doctor";

  useEffect(() => {
    const docId = localStorage.getItem("doctor_id");
    if (!docId) {
      toast.error("Please login first");
      navigate("/doctor/auth");
      return;
    }
    if (!id) {
      toast.error("Invalid patient ID");
      navigate("/doctor/patients");
      return;
    }
    
    setDoctorId(parseInt(docId));
    loadPatientData(parseInt(id), parseInt(docId));
  }, [id, navigate]);

  const loadPatientData = async (patientId: number, docId: number) => {
    try {
      setIsLoading(true);
      
      // Load patient profile
      const profileResult = await api.patient.getProfile(patientId);
      if (profileResult.success && profileResult.data) {
        setPatient(profileResult.data);
      }
      
      // Load appointment history
      const historyResult = await api.appointment.getPatientHistory(patientId);
      if (historyResult.success && historyResult.data) {
        setAppointments(Array.isArray(historyResult.data.appointments) ? historyResult.data.appointments : []);
      }
    } catch (error: any) {
      toast.error(error.message || "Failed to load patient data");
      setAppointments([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.clear();
    navigate("/");
  };

  const getInitials = (name: string) => {
    return name.split(" ").map(n => n[0]).join("").toUpperCase();
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "scheduled": return "bg-primary/20 text-primary border-primary/30";
      case "completed": return "bg-success/20 text-success border-success/30";
      case "cancelled": return "bg-destructive/20 text-destructive border-destructive/30";
      default: return "bg-muted";
    }
  };

  const handleEditNote = (appointmentId: number, currentNote: string) => {
    setEditingNote(appointmentId);
    setNoteText(currentNote);
  };

  const handleSaveNote = async (appointmentId: number) => {
    try {
      const result = await api.appointment.updateNotes(appointmentId, noteText);
      if (result.success) {
        // Reload patient data to refresh appointments
        if (patient) {
          loadPatientData(patient.user_id, doctorId);
        }
        setEditingNote(null);
        setNoteText("");
        toast.success("Notes saved successfully");
      } else {
        toast.error(result.message || "Failed to save notes");
      }
    } catch (error: any) {
      toast.error(error.message || "Failed to save notes");
    }
  };

  const handleCancelEdit = () => {
    setEditingNote(null);
    setNoteText("");
  };

  const stats = [
    { label: "Total Visits", value: Array.isArray(appointments) ? appointments.length : 0, color: "text-primary" },
    { label: "Completed", value: Array.isArray(appointments) ? appointments.filter(a => a.status === "completed").length : 0, color: "text-success" },
    { label: "Upcoming", value: Array.isArray(appointments) ? appointments.filter(a => a.status === "scheduled").length : 0, color: "text-warning" },
    { label: "Cancelled", value: Array.isArray(appointments) ? appointments.filter(a => a.status === "cancelled").length : 0, color: "text-destructive" },
  ];

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!patient) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-muted-foreground">Patient not found</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      {/* Header */}
      <header className="glass-header sticky top-0 z-50 border-b border-white/20">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button variant="ghost" onClick={() => navigate("/doctor/patients")} className="hover:scale-110 transition-transform">
              <ArrowLeft className="h-5 w-5" />
            </Button>
            <div>
              <h1 className="text-2xl font-bold text-foreground">Patient Details</h1>
              <p className="text-sm text-muted-foreground">Dr. {doctorName}</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <Button variant="outline" onClick={() => navigate("/doctor/dashboard")} className="glass hover:scale-105 transition-transform">
              Dashboard
            </Button>
            <Button variant="outline" onClick={handleLogout} className="glass hover:scale-105 transition-transform">
              <LogOut className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Patient Profile Card */}
          <div className="lg:col-span-1">
            <Card className="glass-card shadow-card hover:shadow-card-hover transition-all duration-300 border-white/20">
              <CardHeader className="text-center">
                <Avatar className="h-24 w-24 mx-auto mb-4">
                  <AvatarFallback className="bg-primary/10 text-primary text-2xl">
                    {getInitials(patient.name)}
                  </AvatarFallback>
                </Avatar>
                <CardTitle className="text-xl">{patient.name}</CardTitle>
                <CardDescription>
                  {patient.gender ? patient.gender.charAt(0).toUpperCase() + patient.gender.slice(1) : "N/A"}
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <Separator className="bg-white/20" />
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-sm">
                    <Mail className="h-4 w-4 text-muted-foreground" />
                    <span className="text-muted-foreground">{patient.email || "N/A"}</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <Phone className="h-4 w-4 text-muted-foreground" />
                    <span className="text-muted-foreground">{patient.phone || "N/A"}</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <Calendar className="h-4 w-4 text-muted-foreground" />
                    <span className="text-muted-foreground">
                      Date of Birth: {patient.date_of_birth ? new Date(patient.date_of_birth).toLocaleDateString() : "N/A"}
                    </span>
                  </div>
                </div>

                <Separator className="bg-white/20" />

                {/* Statistics */}
                <div className="grid grid-cols-2 gap-4">
                  {stats.map((stat, index) => (
                    <div key={index} className="glass p-3 rounded-lg text-center hover:scale-105 transition-transform">
                      <p className={`text-2xl font-bold ${stat.color}`}>{stat.value}</p>
                      <p className="text-xs text-muted-foreground">{stat.label}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Appointment History */}
          <div className="lg:col-span-2">
            <Card className="glass-card shadow-card hover:shadow-card-hover transition-all duration-300 border-white/20">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5 text-primary" />
                  Appointment History
                </CardTitle>
                <CardDescription>Complete medical visit timeline</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {Array.isArray(appointments) && appointments.map((appointment, index) => (
                    <div key={appointment.appointment_id} className="relative">
                      {/* Timeline line */}
                      {index !== appointments.length - 1 && (
                        <div className="absolute left-6 top-12 w-0.5 h-full bg-gradient-to-b from-primary/30 to-transparent"></div>
                      )}

                      <div className="glass p-4 rounded-lg border border-white/20 hover:scale-[1.01] transition-all duration-300">
                        <div className="flex items-start gap-4">
                          <div className="flex-shrink-0">
                            <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                              appointment.status === "completed" ? "bg-success/20" :
                              appointment.status === "scheduled" ? "bg-primary/20" :
                              "bg-destructive/20"
                            }`}>
                              <Calendar className={`h-5 w-5 ${
                                appointment.status === "completed" ? "text-success" :
                                appointment.status === "scheduled" ? "text-primary" :
                                "text-destructive"
                              }`} />
                            </div>
                          </div>

                          <div className="flex-1">
                            <div className="flex items-center justify-between mb-2">
                              <div>
                                <h4 className="font-semibold">{appointment.reason || "Consultation"}</h4>
                                <p className="text-sm text-muted-foreground">
                                  {new Date(appointment.appointment_date).toLocaleDateString()} at {appointment.start_time}
                                </p>
                              </div>
                              <Badge variant="outline" className={getStatusColor(appointment.status)}>
                                {appointment.status}
                              </Badge>
                            </div>

                            {editingNote === appointment.appointment_id ? (
                              <div className="space-y-2 mt-3">
                                <Textarea
                                  value={noteText}
                                  onChange={(e) => setNoteText(e.target.value)}
                                  placeholder="Add medical notes..."
                                  className="glass border-white/20 min-h-[100px]"
                                />
                                <div className="flex gap-2">
                                  <Button size="sm" onClick={() => handleSaveNote(appointment.appointment_id)} className="hover:scale-105 transition-transform">
                                    <Save className="h-3 w-3 mr-1" />
                                    Save
                                  </Button>
                                  <Button size="sm" variant="outline" onClick={handleCancelEdit} className="hover:scale-105 transition-transform">
                                    <X className="h-3 w-3 mr-1" />
                                    Cancel
                                  </Button>
                                </div>
                              </div>
                            ) : (
                              <>
                                {appointment.notes ? (
                                  <div className="mt-3 p-3 bg-muted/30 rounded-md">
                                    <p className="text-sm text-muted-foreground italic">{appointment.notes}</p>
                                  </div>
                                ) : (
                                  <p className="text-sm text-muted-foreground italic mt-2">No notes added yet</p>
                                )}
                                <Button
                                  size="sm"
                                  variant="ghost"
                                  onClick={() => handleEditNote(appointment.appointment_id, appointment.notes || "")}
                                  className="mt-2 hover:scale-105 transition-transform"
                                >
                                  <Edit className="h-3 w-3 mr-1" />
                                  {appointment.notes ? "Edit Notes" : "Add Notes"}
                                </Button>
                              </>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}

                  {(!Array.isArray(appointments) || appointments.length === 0) && (
                    <div className="text-center py-12">
                      <FileText className="h-12 w-12 mx-auto text-muted-foreground/50 mb-4" />
                      <p className="text-muted-foreground">No appointment history available</p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PatientDetail;
