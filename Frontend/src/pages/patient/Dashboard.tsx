import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Calendar, MessageCircle, ClipboardList, Clock, LogOut, User } from "lucide-react";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";

const PatientDashboard = () => {
  const navigate = useNavigate();
  const [userName, setUserName] = useState("");
  const [greeting, setGreeting] = useState("");

  useEffect(() => {
    const name = localStorage.getItem("user_name") || "Guest";
    setUserName(name);

    const hour = new Date().getHours();
    if (hour < 12) setGreeting("Good morning");
    else if (hour < 18) setGreeting("Good afternoon");
    else setGreeting("Good evening");
  }, []);

  const handleLogout = () => {
    localStorage.clear();
    navigate("/");
  };

  const quickActions = [
    {
      title: "Book Appointment",
      description: "Schedule a visit with our doctors",
      icon: Calendar,
      gradient: "gradient-card",
      action: () => navigate("/patient/book"),
    },
    {
      title: "Ask Medical Questions",
      description: "Chat with AI medical assistant",
      icon: MessageCircle,
      gradient: "gradient-success",
      action: () => navigate("/patient/chat"),
    },
    {
      title: "View Appointments",
      description: "See your appointment history",
      icon: ClipboardList,
      gradient: "bg-gradient-to-br from-amber-500 to-orange-500",
      action: () => navigate("/patient/appointments"),
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="glass-header sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Avatar className="h-12 w-12 border-2 border-primary">
              <AvatarFallback className="bg-primary text-primary-foreground">
                {userName.split(" ").map(n => n[0]).join("").toUpperCase()}
              </AvatarFallback>
            </Avatar>
            <div>
              <h1 className="text-xl font-semibold">
                {greeting}, {userName}!
              </h1>
              <p className="text-sm text-muted-foreground">Welcome to your health dashboard</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Button 
              variant="outline" 
              size="icon"
              onClick={() => navigate("/patient/profile")}
            >
              <User className="h-5 w-5" />
            </Button>
            <Button 
              variant="outline"
              size="icon"
              onClick={handleLogout}
            >
              <LogOut className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Upcoming Appointment Alert */}
        <Card className="mb-8 glass-card border-secondary/30 bg-secondary/5 shadow-card">
          <CardContent className="flex items-center gap-4 p-6">
            <div className="w-12 h-12 rounded-full bg-secondary/20 flex items-center justify-center flex-shrink-0">
              <Clock className="h-6 w-6 text-secondary" />
            </div>
            <div className="flex-1">
              <h3 className="font-semibold text-lg">Upcoming Appointment</h3>
              <p className="text-muted-foreground">Tomorrow at 11:30 AM with Dr. Aisha Khan</p>
            </div>
            <Button variant="secondary">View Details</Button>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-6">Quick Actions</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {quickActions.map((action, index) => (
              <Card
                key={index}
                className="group cursor-pointer transition-all duration-300 hover:shadow-card-hover hover:-translate-y-1 overflow-hidden glass-card"
                onClick={action.action}
              >
                <div className={`h-2 ${action.gradient}`} />
                <CardHeader>
                  <div className={`w-12 h-12 rounded-lg ${action.gradient} flex items-center justify-center mb-3`}>
                    <action.icon className="h-6 w-6 text-white" />
                  </div>
                  <CardTitle className="text-xl">{action.title}</CardTitle>
                  <CardDescription className="text-base">{action.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <Button className="w-full">Get Started</Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Recent Activity */}
        <div>
          <h2 className="text-2xl font-bold mb-6">Recent Activity</h2>
          <div className="grid md:grid-cols-2 gap-4">
            <Card className="glass-card shadow-card">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg">Dr. Aisha Khan</CardTitle>
                  <Badge className="bg-success text-success-foreground">Completed</Badge>
                </div>
                <CardDescription>Cardiologist</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Calendar className="h-4 w-4" />
                  <span>Oct 15, 2025 at 10:00 AM</span>
                </div>
              </CardContent>
            </Card>

            <Card className="glass-card shadow-card">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg">Dr. James Wilson</CardTitle>
                  <Badge className="bg-success text-success-foreground">Completed</Badge>
                </div>
                <CardDescription>General Physician</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Calendar className="h-4 w-4" />
                  <span>Sep 28, 2025 at 2:30 PM</span>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
};

export default PatientDashboard;
