import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { ArrowLeft, Calendar, Clock, X, RotateCcw } from "lucide-react";
import { toast } from "sonner";
import api, { type Appointment } from "@/lib/api";

const PatientAppointments = () => {
  const navigate = useNavigate();
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [cancelDialogOpen, setCancelDialogOpen] = useState(false);
  const [selectedAppointment, setSelectedAppointment] = useState<Appointment | null>(null);
  const [userId, setUserId] = useState<number>(0);

  useEffect(() => {
    const storedUserId = localStorage.getItem("user_id");
    if (!storedUserId) {
      toast.error("Please login first");
      navigate("/patient/auth");
      return;
    }
    setUserId(parseInt(storedUserId));
    loadAppointments(parseInt(storedUserId));
  }, [navigate]);

  const loadAppointments = async (id: number) => {
    try {
      setIsLoading(true);
      const result = await api.appointment.getByPatient(id, false);
      if (result.success && result.data) {
        setAppointments(Array.isArray(result.data) ? result.data : []);
      } else {
        toast.error("Failed to load appointments");
      }
    } catch (error: any) {
      toast.error(error.message || "Failed to load appointments");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancelClick = (appointment: Appointment) => {
    setSelectedAppointment(appointment);
    setCancelDialogOpen(true);
  };

  const handleCancelConfirm = async () => {
    if (!selectedAppointment) return;

    try {
      const result = await api.appointment.cancel(selectedAppointment.appointment_id);
      if (result.success) {
        toast.success("Appointment cancelled successfully");
        loadAppointments(userId); // Reload appointments
      } else {
        toast.error(result.message || "Failed to cancel appointment");
      }
    } catch (error: any) {
      toast.error(error.message || "Failed to cancel appointment");
    } finally {
      setCancelDialogOpen(false);
      setSelectedAppointment(null);
    }
  };

  const handleBookAgain = (appointment: Appointment) => {
    toast.success("Redirecting to booking...");
    navigate("/patient/book");
  };

  const filterAppointments = (status?: Appointment["status"]) => {
    if (!status) return appointments;
    return appointments.filter((apt) => apt.status === status);
  };

  const AppointmentCard = ({ appointment }: { appointment: Appointment }) => {
    const doctorName = appointment.doctor_name || "Unknown Doctor";
    const doctorInitials = doctorName.split(" ").map(n => n[0]).join("");
    
    return (
      <Card className="glass-card hover:shadow-lg transition-all duration-300">
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-4">
              <Avatar className="w-14 h-14 border-2 border-white">
                <AvatarFallback className="bg-primary text-primary-foreground">
                  {doctorInitials}
                </AvatarFallback>
              </Avatar>
              <div>
                <CardTitle className="text-lg">{doctorName}</CardTitle>
                <CardDescription>{appointment.doctor_specialty || "General"}</CardDescription>
              </div>
            </div>
            <Badge
              variant={
                appointment.status === "scheduled"
                  ? "default"
                  : appointment.status === "completed"
                  ? "secondary"
                  : "destructive"
              }
              className={
                appointment.status === "completed"
                  ? "bg-success text-success-foreground"
                  : ""
              }
            >
              {appointment.status.charAt(0).toUpperCase() + appointment.status.slice(1)}
            </Badge>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Calendar className="w-4 h-4" />
              <span>
                {new Date(appointment.appointment_date).toLocaleDateString("en-US", {
                  month: "short",
                  day: "numeric",
                  year: "numeric",
                })}
              </span>
            </div>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Clock className="w-4 h-4" />
              <span>{appointment.start_time}</span>
            </div>
          </div>
          {appointment.reason && (
            <div className="p-3 bg-gray-50 rounded-lg">
              <p className="text-sm text-muted-foreground">
                <span className="font-medium text-foreground">Reason: </span>
                {appointment.reason}
              </p>
            </div>
          )}
          <div className="flex gap-2">
            {appointment.status === "scheduled" && (
              <>
                <Button variant="outline" className="flex-1">
                  View Details
                </Button>
                <Button
                  variant="destructive"
                  size="icon"
                  onClick={() => handleCancelClick(appointment)}
                >
                  <X className="h-4 w-4" />
                </Button>
              </>
            )}
            {(appointment.status === "completed" || appointment.status === "cancelled") && (
              <Button
                variant="outline"
                className="flex-1 gap-2"
                onClick={() => handleBookAgain(appointment)}
              >
                <RotateCcw className="h-4 w-4" />
                Book Again
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="glass-header sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Button variant="ghost" onClick={() => navigate("/patient/dashboard")}>
            <ArrowLeft className="h-5 w-5 mr-2" />
            Back
          </Button>
          <h1 className="text-xl font-semibold">My Appointments</h1>
          <Button onClick={() => navigate("/patient/book")}>Book New</Button>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 max-w-6xl">
        <Tabs defaultValue="all" className="space-y-6">
          <TabsList className="grid w-full max-w-md grid-cols-4">
            <TabsTrigger value="all">All</TabsTrigger>
            <TabsTrigger value="upcoming">Upcoming</TabsTrigger>
            <TabsTrigger value="past">Past</TabsTrigger>
            <TabsTrigger value="cancelled">Cancelled</TabsTrigger>
          </TabsList>

          <TabsContent value="all" className="space-y-4">
            {isLoading ? (
              <div className="flex justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
              </div>
            ) : filterAppointments().length > 0 ? (
              <div className="grid md:grid-cols-2 gap-6">
                {filterAppointments().map((appointment) => (
                  <AppointmentCard key={appointment.appointment_id} appointment={appointment} />
                ))}
              </div>
            ) : (
              <EmptyState />
            )}
          </TabsContent>

          <TabsContent value="upcoming" className="space-y-4">
            {isLoading ? (
              <div className="flex justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
              </div>
            ) : filterAppointments("scheduled").length > 0 ? (
              <div className="grid md:grid-cols-2 gap-6">
                {filterAppointments("scheduled").map((appointment) => (
                  <AppointmentCard key={appointment.appointment_id} appointment={appointment} />
                ))}
              </div>
            ) : (
              <EmptyState message="No upcoming appointments" />
            )}
          </TabsContent>

          <TabsContent value="past" className="space-y-4">
            {isLoading ? (
              <div className="flex justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
              </div>
            ) : filterAppointments("completed").length > 0 ? (
              <div className="grid md:grid-cols-2 gap-6">
                {filterAppointments("completed").map((appointment) => (
                  <AppointmentCard key={appointment.appointment_id} appointment={appointment} />
                ))}
              </div>
            ) : (
              <EmptyState message="No completed appointments" />
            )}
          </TabsContent>

          <TabsContent value="cancelled" className="space-y-4">
            {isLoading ? (
              <div className="flex justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
              </div>
            ) : filterAppointments("cancelled").length > 0 ? (
              <div className="grid md:grid-cols-2 gap-6">
                {filterAppointments("cancelled").map((appointment) => (
                  <AppointmentCard key={appointment.appointment_id} appointment={appointment} />
                ))}
              </div>
            ) : (
              <EmptyState message="No cancelled appointments" />
            )}
          </TabsContent>
        </Tabs>
      </main>

      {/* Cancel Confirmation Dialog */}
      <AlertDialog open={cancelDialogOpen} onOpenChange={setCancelDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Cancel Appointment?</AlertDialogTitle>
            <AlertDialogDescription>
              Are you sure you want to cancel your appointment with{" "}
              {selectedAppointment?.doctor_name || "the doctor"} on{" "}
              {selectedAppointment &&
                new Date(selectedAppointment.appointment_date).toLocaleDateString("en-US", {
                  month: "long",
                  day: "numeric",
                  year: "numeric",
                })}{" "}
              at {selectedAppointment?.start_time}? This action cannot be undone.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Keep Appointment</AlertDialogCancel>
            <AlertDialogAction onClick={handleCancelConfirm} className="bg-destructive text-destructive-foreground hover:bg-destructive/90">
              Cancel Appointment
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
};

const EmptyState = ({ message = "No appointments found" }: { message?: string }) => (
  <Card className="glass-card">
    <CardContent className="flex flex-col items-center justify-center py-16">
      <Calendar className="w-16 h-16 text-muted-foreground mb-4" />
      <h3 className="text-lg font-semibold mb-2">{message}</h3>
      <p className="text-muted-foreground text-center mb-6">
        Start your health journey by booking your first appointment
      </p>
      <Button onClick={() => window.location.href = "/patient/book"}>
        Book Appointment
      </Button>
    </CardContent>
  </Card>
);

export default PatientAppointments;
