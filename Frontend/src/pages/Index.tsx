import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useNavigate } from "react-router-dom";
import { Heart, Stethoscope, Calendar, MessageCircle, Users, BarChart3 } from "lucide-react";

const Index = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: Calendar,
      title: "Easy Appointment Booking",
      description: "Schedule appointments with top doctors in just a few clicks"
    },
    {
      icon: MessageCircle,
      title: "AI Medical Assistant",
      description: "Get instant answers to your medical questions 24/7"
    },
    {
      icon: Users,
      title: "Patient Management",
      description: "Doctors can efficiently manage their patient records"
    },
    {
      icon: BarChart3,
      title: "Analytics & Insights",
      description: "Track health trends and appointment statistics"
    }
  ];

  return (
    <div className="min-h-screen gradient-bg">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16 max-w-6xl">
        <div className="text-center mb-16">
          <div className="flex justify-center mb-6">
            <div className="w-20 h-20 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center">
              <Heart className="w-10 h-10 text-white" />
            </div>
          </div>
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
            HealthCare Assistant
          </h1>
          <p className="text-xl text-white/80 mb-12 max-w-2xl mx-auto">
            Modern healthcare management system for patients and doctors. 
            Book appointments, chat with AI, and manage your health journey.
          </p>

          {/* Portal Selection */}
          <div className="grid md:grid-cols-2 gap-8 max-w-3xl mx-auto">
            <Card className="shadow-elevated hover:shadow-card-hover transition-all duration-300 hover:-translate-y-1">
              <CardHeader>
                <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-primary/10 flex items-center justify-center">
                  <Heart className="w-8 h-8 text-primary" />
                </div>
                <CardTitle className="text-2xl">Patient Portal</CardTitle>
                <CardDescription className="text-base">
                  Book appointments, chat with AI medical assistant, and manage your health
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button 
                  onClick={() => navigate("/patient/auth")} 
                  className="w-full"
                  size="lg"
                >
                  Access Patient Portal
                </Button>
              </CardContent>
            </Card>

            <Card className="shadow-elevated hover:shadow-card-hover transition-all duration-300 hover:-translate-y-1">
              <CardHeader>
                <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-secondary/10 flex items-center justify-center">
                  <Stethoscope className="w-8 h-8 text-secondary" />
                </div>
                <CardTitle className="text-2xl">Doctor Portal</CardTitle>
                <CardDescription className="text-base">
                  Manage appointments, view patient records, and track analytics
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button 
                  onClick={() => navigate("/doctor/auth")} 
                  variant="secondary"
                  className="w-full"
                  size="lg"
                >
                  Access Doctor Portal
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Features Section */}
        <div className="mt-24">
          <h2 className="text-3xl font-bold text-white text-center mb-12">
            Key Features
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <Card key={index} className="shadow-card bg-white/95 backdrop-blur-sm">
                <CardHeader>
                  <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-3">
                    <feature.icon className="w-6 h-6 text-primary" />
                  </div>
                  <CardTitle className="text-lg">{feature.title}</CardTitle>
                  <CardDescription>{feature.description}</CardDescription>
                </CardHeader>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
