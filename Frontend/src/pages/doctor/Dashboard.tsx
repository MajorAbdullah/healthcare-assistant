import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Calendar, Users, Clock, TrendingUp, LogOut, CalendarDays, UserCircle, BarChart3, User } from "lucide-react";

const DoctorDashboard = () => {
  const navigate = useNavigate();
  const [doctorName, setDoctorName] = useState("");
  const [specialty, setSpecialty] = useState("");

  useEffect(() => {
    const name = localStorage.getItem("doctor_name") || "Doctor";
    const spec = localStorage.getItem("doctor_specialty") || "";
    setDoctorName(name);
    setSpecialty(spec);
  }, []);

  const handleLogout = () => {
    localStorage.clear();
    navigate("/");
  };

  const stats = [
    { label: "Today's Appointments", value: "8", icon: Calendar, color: "text-primary" },
    { label: "Total Patients", value: "127", icon: Users, color: "text-secondary" },
    { label: "This Week", value: "32", icon: Clock, color: "text-accent" },
    { label: "Completion Rate", value: "95%", icon: TrendingUp, color: "text-success" },
  ];

  const todaySchedule = [
    { time: "09:00 AM", patient: "John Anderson", reason: "Regular checkup", status: "scheduled" },
    { time: "09:30 AM", patient: "Sarah Johnson", reason: "Follow-up visit", status: "completed" },
    { time: "10:00 AM", patient: "Michael Chen", reason: "Blood pressure monitoring", status: "scheduled" },
    { time: "11:00 AM", patient: "Emma Davis", reason: "Consultation", status: "scheduled" },
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
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
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
            {todaySchedule.map((appointment, index) => (
              <div 
                key={index}
                className="flex items-center gap-4 p-4 rounded-lg border bg-card hover:shadow-md transition-shadow"
              >
                <div className="w-20 flex-shrink-0">
                  <div className="text-sm font-semibold">{appointment.time}</div>
                </div>
                <div className="flex-1">
                  <div className="font-medium">{appointment.patient}</div>
                  <div className="text-sm text-muted-foreground">{appointment.reason}</div>
                </div>
                <Badge 
                  variant={appointment.status === "completed" ? "default" : "secondary"}
                  className={appointment.status === "completed" ? "bg-success" : ""}
                >
                  {appointment.status === "completed" ? "Completed" : "Scheduled"}
                </Badge>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm">View Details</Button>
                  {appointment.status === "scheduled" && (
                    <Button variant="default" size="sm">Add Notes</Button>
                  )}
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

export default DoctorDashboard;
