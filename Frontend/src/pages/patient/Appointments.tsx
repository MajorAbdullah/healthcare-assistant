import { useState } from "react";
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

interface Appointment {
  id: string;
  doctorId: number;
  doctorName: string;
  specialty: string;
  date: string;
  time: string;
  status: "scheduled" | "completed" | "cancelled";
  reason?: string;
}

const mockAppointments: Appointment[] = [
  {
    id: "1",
    doctorId: 1,
    doctorName: "Dr. Aisha Khan",
    specialty: "Cardiologist",
    date: "2025-10-28",
    time: "11:30 AM",
    status: "scheduled",
    reason: "Regular checkup",
  },
  {
    id: "2",
    doctorId: 2,
    doctorName: "Dr. James Wilson",
    specialty: "General Physician",
    date: "2025-10-15",
    time: "10:00 AM",
    status: "completed",
    reason: "Annual physical examination",
  },
  {
    id: "3",
    doctorId: 3,
    doctorName: "Dr. Sarah Chen",
    specialty: "Pediatrician",
    date: "2025-09-28",
    time: "02:30 PM",
    status: "completed",
  },
  {
    id: "4",
    doctorId: 4,
    doctorName: "Dr. Michael Brown",
    specialty: "Orthopedic",
    date: "2025-09-10",
    time: "09:00 AM",
    status: "cancelled",
    reason: "Knee pain consultation",
  },
];

const PatientAppointments = () => {
  const navigate = useNavigate();
  const [appointments, setAppointments] = useState(mockAppointments);
  const [cancelDialogOpen, setCancelDialogOpen] = useState(false);
  const [selectedAppointment, setSelectedAppointment] = useState<Appointment | null>(null);

  const handleCancelClick = (appointment: Appointment) => {
    setSelectedAppointment(appointment);
    setCancelDialogOpen(true);
  };

  const handleCancelConfirm = () => {
    if (selectedAppointment) {
      setAppointments(
        appointments.map((apt) =>
          apt.id === selectedAppointment.id ? { ...apt, status: "cancelled" as const } : apt
        )
      );
      toast.success("Appointment cancelled successfully");
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

  const AppointmentCard = ({ appointment }: { appointment: Appointment }) => (
    <Card className="glass-card hover:shadow-lg transition-all duration-300">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-4">
            <Avatar className="w-14 h-14 border-2 border-white">
              <AvatarFallback className="bg-primary text-primary-foreground">
                {appointment.doctorName.split(" ")[1][0]}
                {appointment.doctorName.split(" ")[2]?.[0] || ""}
              </AvatarFallback>
            </Avatar>
            <div>
              <CardTitle className="text-lg">{appointment.doctorName}</CardTitle>
              <CardDescription>{appointment.specialty}</CardDescription>
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
              {new Date(appointment.date).toLocaleDateString("en-US", {
                month: "short",
                day: "numeric",
                year: "numeric",
              })}
            </span>
          </div>
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Clock className="w-4 h-4" />
            <span>{appointment.time}</span>
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
            {filterAppointments().length > 0 ? (
              <div className="grid md:grid-cols-2 gap-6">
                {filterAppointments().map((appointment) => (
                  <AppointmentCard key={appointment.id} appointment={appointment} />
                ))}
              </div>
            ) : (
              <EmptyState />
            )}
          </TabsContent>

          <TabsContent value="upcoming" className="space-y-4">
            {filterAppointments("scheduled").length > 0 ? (
              <div className="grid md:grid-cols-2 gap-6">
                {filterAppointments("scheduled").map((appointment) => (
                  <AppointmentCard key={appointment.id} appointment={appointment} />
                ))}
              </div>
            ) : (
              <EmptyState message="No upcoming appointments" />
            )}
          </TabsContent>

          <TabsContent value="past" className="space-y-4">
            {filterAppointments("completed").length > 0 ? (
              <div className="grid md:grid-cols-2 gap-6">
                {filterAppointments("completed").map((appointment) => (
                  <AppointmentCard key={appointment.id} appointment={appointment} />
                ))}
              </div>
            ) : (
              <EmptyState message="No completed appointments" />
            )}
          </TabsContent>

          <TabsContent value="cancelled" className="space-y-4">
            {filterAppointments("cancelled").length > 0 ? (
              <div className="grid md:grid-cols-2 gap-6">
                {filterAppointments("cancelled").map((appointment) => (
                  <AppointmentCard key={appointment.id} appointment={appointment} />
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
              {selectedAppointment?.doctorName} on{" "}
              {selectedAppointment &&
                new Date(selectedAppointment.date).toLocaleDateString("en-US", {
                  month: "long",
                  day: "numeric",
                  year: "numeric",
                })}{" "}
              at {selectedAppointment?.time}? This action cannot be undone.
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
