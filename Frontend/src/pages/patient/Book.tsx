import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Calendar } from "@/components/ui/calendar";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import { ArrowLeft, ArrowRight, Star, CheckCircle2, Calendar as CalendarIcon } from "lucide-react";

const doctors = [
  { id: 1, name: "Dr. Aisha Khan", specialty: "Cardiologist", rating: 4.9 },
  { id: 2, name: "Dr. James Wilson", specialty: "General Physician", rating: 4.8 },
  { id: 3, name: "Dr. Sarah Chen", specialty: "Pediatrician", rating: 4.7 },
  { id: 4, name: "Dr. Michael Brown", specialty: "Orthopedic", rating: 4.9 },
  { id: 5, name: "Dr. Emily Davis", specialty: "Dermatologist", rating: 4.6 },
  { id: 6, name: "Dr. Robert Taylor", specialty: "Neurologist", rating: 4.8 },
];

const BookAppointment = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [selectedDoctor, setSelectedDoctor] = useState<typeof doctors[0] | null>(null);
  const [selectedDate, setSelectedDate] = useState<Date | undefined>();
  const [selectedTime, setSelectedTime] = useState("");
  const [reason, setReason] = useState("");

  const timeSlots = [
    "09:00 AM", "09:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM",
    "02:00 PM", "02:30 PM", "03:00 PM", "03:30 PM", "04:00 PM", "04:30 PM",
  ];

  const handleDoctorSelect = (doctor: typeof doctors[0]) => {
    setSelectedDoctor(doctor);
    setStep(2);
  };

  const handleDateSelect = (date: Date | undefined) => {
    setSelectedDate(date);
  };

  const handleTimeSelect = (time: string) => {
    setSelectedTime(time);
  };

  const handleConfirm = () => {
    toast.success("Appointment booked successfully!");
    setStep(5);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="glass-header sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Button variant="ghost" onClick={() => step === 1 ? navigate("/patient/dashboard") : setStep(step - 1)}>
            <ArrowLeft className="h-5 w-5 mr-2" />
            Back
          </Button>
          <h1 className="text-xl font-semibold">Book Appointment</h1>
          <div className="w-20" />
        </div>
      </header>

      {/* Progress Indicator */}
      {step < 5 && (
        <div className="container mx-auto px-4 py-6 max-w-4xl">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium">Step {step} of 4</span>
            <span className="text-sm text-muted-foreground">
              {step === 1 && "Select Doctor"}
              {step === 2 && "Choose Date"}
              {step === 3 && "Pick Time"}
              {step === 4 && "Confirm Details"}
            </span>
          </div>
          <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-primary to-secondary transition-all duration-300"
              style={{ width: `${(step / 4) * 100}%` }}
            />
          </div>
        </div>
      )}

      <main className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Step 1: Select Doctor */}
        {step === 1 && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold">Select a Doctor</h2>
            <div className="grid md:grid-cols-3 gap-6">
              {doctors.map((doctor) => (
                <Card 
                  key={doctor.id}
                  className="glass-card cursor-pointer hover:shadow-lg transition-all duration-300 hover:-translate-y-1"
                  onClick={() => handleDoctorSelect(doctor)}
                >
                  <CardHeader className="text-center">
                    <Avatar className="w-24 h-24 mx-auto mb-4 border-4 border-white">
                      <AvatarFallback className="bg-primary text-primary-foreground text-2xl">
                        {doctor.name.split(" ")[1][0]}{doctor.name.split(" ")[2]?.[0] || ""}
                      </AvatarFallback>
                    </Avatar>
                    <CardTitle className="text-lg">{doctor.name}</CardTitle>
                    <CardDescription>{doctor.specialty}</CardDescription>
                    <div className="flex items-center justify-center gap-1 mt-2">
                      <Star className="w-4 h-4 fill-amber-400 text-amber-400" />
                      <span className="font-semibold">{doctor.rating}</span>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <Button className="w-full">Select Doctor</Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        )}

        {/* Step 2: Select Date */}
        {step === 2 && selectedDoctor && (
          <div className="max-w-2xl mx-auto space-y-6">
            <div className="glass-card p-4 flex items-center gap-4">
              <Avatar className="w-16 h-16">
                <AvatarFallback className="bg-primary text-primary-foreground">
                  {selectedDoctor.name.split(" ")[1][0]}{selectedDoctor.name.split(" ")[2]?.[0] || ""}
                </AvatarFallback>
              </Avatar>
              <div>
                <h3 className="font-semibold text-lg">{selectedDoctor.name}</h3>
                <p className="text-muted-foreground">{selectedDoctor.specialty}</p>
              </div>
            </div>

            <Card className="glass-card">
              <CardHeader>
                <CardTitle>Choose a Date</CardTitle>
                <CardDescription>Select an available date for your appointment</CardDescription>
              </CardHeader>
              <CardContent className="flex justify-center">
                <Calendar
                  mode="single"
                  selected={selectedDate}
                  onSelect={handleDateSelect}
                  disabled={(date) => date < new Date()}
                  className="rounded-md border pointer-events-auto"
                />
              </CardContent>
            </Card>

            {selectedDate && (
              <Button onClick={() => setStep(3)} className="w-full" size="lg">
                Continue to Time Selection
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            )}
          </div>
        )}

        {/* Step 3: Select Time */}
        {step === 3 && selectedDate && (
          <div className="max-w-2xl mx-auto space-y-6">
            <Card className="glass-card">
              <CardHeader>
                <CardTitle>Select Time Slot</CardTitle>
                <CardDescription>
                  Available slots for {selectedDate.toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" })}
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <h4 className="font-semibold mb-3">Morning</h4>
                  <div className="grid grid-cols-3 gap-3">
                    {timeSlots.slice(0, 6).map((time) => (
                      <Button
                        key={time}
                        variant={selectedTime === time ? "default" : "outline"}
                        onClick={() => handleTimeSelect(time)}
                        className="w-full"
                      >
                        {time}
                      </Button>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="font-semibold mb-3">Afternoon</h4>
                  <div className="grid grid-cols-3 gap-3">
                    {timeSlots.slice(6).map((time) => (
                      <Button
                        key={time}
                        variant={selectedTime === time ? "default" : "outline"}
                        onClick={() => handleTimeSelect(time)}
                        className="w-full"
                      >
                        {time}
                      </Button>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>

            {selectedTime && (
              <Button onClick={() => setStep(4)} className="w-full" size="lg">
                Continue to Confirmation
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            )}
          </div>
        )}

        {/* Step 4: Confirmation */}
        {step === 4 && selectedDoctor && selectedDate && selectedTime && (
          <div className="max-w-2xl mx-auto space-y-6">
            <Card className="glass-card">
              <CardHeader>
                <CardTitle>Confirm Your Appointment</CardTitle>
                <CardDescription>Please review your appointment details</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="space-y-4">
                  <div className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
                    <Avatar className="w-16 h-16">
                      <AvatarFallback className="bg-primary text-primary-foreground">
                        {selectedDoctor.name.split(" ")[1][0]}{selectedDoctor.name.split(" ")[2]?.[0] || ""}
                      </AvatarFallback>
                    </Avatar>
                    <div>
                      <h3 className="font-semibold text-lg">{selectedDoctor.name}</h3>
                      <p className="text-muted-foreground">{selectedDoctor.specialty}</p>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-4 bg-gray-50 rounded-lg">
                      <div className="flex items-center gap-2 mb-2">
                        <CalendarIcon className="w-5 h-5 text-primary" />
                        <span className="font-semibold">Date</span>
                      </div>
                      <p className="text-muted-foreground">
                        {selectedDate.toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric", year: "numeric" })}
                      </p>
                    </div>

                    <div className="p-4 bg-gray-50 rounded-lg">
                      <div className="flex items-center gap-2 mb-2">
                        <CalendarIcon className="w-5 h-5 text-primary" />
                        <span className="font-semibold">Time</span>
                      </div>
                      <p className="text-muted-foreground">{selectedTime}</p>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="reason">Reason for Visit (Optional)</Label>
                    <Textarea
                      id="reason"
                      placeholder="Brief description of your symptoms or reason for appointment..."
                      value={reason}
                      onChange={(e) => setReason(e.target.value)}
                      className="min-h-[100px]"
                    />
                  </div>
                </div>

                <div className="flex gap-3">
                  <Button variant="outline" onClick={() => setStep(3)} className="flex-1">
                    Go Back
                  </Button>
                  <Button onClick={handleConfirm} className="flex-1">
                    Confirm Booking
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Step 5: Success */}
        {step === 5 && selectedDoctor && selectedDate && selectedTime && (
          <div className="max-w-2xl mx-auto">
            <Card className="glass-card text-center">
              <CardContent className="pt-12 pb-12 space-y-6">
                <div className="flex justify-center">
                  <div className="w-20 h-20 rounded-full bg-success/10 flex items-center justify-center">
                    <CheckCircle2 className="w-12 h-12 text-success" />
                  </div>
                </div>
                <div>
                  <h2 className="text-3xl font-bold mb-2">Appointment Confirmed!</h2>
                  <p className="text-muted-foreground">Your appointment has been successfully booked</p>
                </div>

                <div className="p-6 bg-gray-50 rounded-lg space-y-3 text-left max-w-md mx-auto">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Doctor:</span>
                    <span className="font-semibold">{selectedDoctor.name}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Date:</span>
                    <span className="font-semibold">
                      {selectedDate.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Time:</span>
                    <span className="font-semibold">{selectedTime}</span>
                  </div>
                </div>

                <div className="flex gap-3 max-w-md mx-auto">
                  <Button onClick={() => navigate("/patient/dashboard")} className="flex-1">
                    Back to Dashboard
                  </Button>
                  <Button onClick={() => navigate("/patient/appointments")} variant="outline" className="flex-1">
                    View Appointments
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </main>
    </div>
  );
};

export default BookAppointment;
