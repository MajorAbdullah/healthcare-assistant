import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";
import { Stethoscope, LogIn, UserPlus } from "lucide-react";
import api from "@/lib/api";

const DoctorAuth = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);

  // Login form state
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPhone, setLoginPhone] = useState("");

  // Register form state
  const [registerName, setRegisterName] = useState("");
  const [registerEmail, setRegisterEmail] = useState("");
  const [registerPhone, setRegisterPhone] = useState("");
  const [registerSpecialty, setRegisterSpecialty] = useState("");
  const [registerDuration, setRegisterDuration] = useState("30");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    if (!loginEmail || !loginPhone) {
      toast.error("Please fill in all fields");
      setIsLoading(false);
      return;
    }

    try {
      const result = await api.doctor.login({
        email: loginEmail,
        phone: loginPhone,
      });

      if (result.success && result.data) {
        localStorage.setItem("user_type", "doctor");
        localStorage.setItem("doctor_id", result.data.doctor_id.toString());
        localStorage.setItem("doctor_name", result.data.name);
        localStorage.setItem("doctor_specialty", result.data.specialty);
        toast.success(`Welcome back, ${result.data.name}!`);
        navigate("/doctor/dashboard");
      } else {
        toast.error(result.message || "Login failed");
      }
    } catch (error: any) {
      toast.error(error.message || "Login failed. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    if (!registerName || !registerEmail || !registerPhone || !registerSpecialty) {
      toast.error("Please fill in all required fields");
      setIsLoading(false);
      return;
    }

    try {
      const result = await api.doctor.register({
        name: registerName,
        email: registerEmail,
        phone: registerPhone,
        specialty: registerSpecialty,
        consultation_duration: parseInt(registerDuration) || 30,
      });

      if (result.success && result.data) {
        localStorage.setItem("user_type", "doctor");
        localStorage.setItem("doctor_id", result.data.doctor_id.toString());
        localStorage.setItem("doctor_name", result.data.name);
        localStorage.setItem("doctor_specialty", result.data.specialty);
        toast.success(`Welcome, Dr. ${result.data.name}! Registration successful!`);
        navigate("/doctor/dashboard");
      } else {
        toast.error(result.message || "Registration failed");
      }
    } catch (error: any) {
      toast.error(error.message || "Registration failed. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen gradient-bg flex items-center justify-center p-4">
      <Card className="w-full max-w-md shadow-elevated">
        <CardHeader className="text-center space-y-2">
          <div className="flex justify-center mb-2">
            <div className="w-16 h-16 rounded-full bg-secondary/10 flex items-center justify-center">
              <Stethoscope className="w-8 h-8 text-secondary" />
            </div>
          </div>
          <CardTitle className="text-3xl">Doctor Portal</CardTitle>
          <CardDescription>Access your professional dashboard</CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="login" className="w-full">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="login" className="gap-2">
                <LogIn className="w-4 h-4" />
                Login
              </TabsTrigger>
              <TabsTrigger value="register" className="gap-2">
                <UserPlus className="w-4 h-4" />
                Register
              </TabsTrigger>
            </TabsList>

            <TabsContent value="login">
              <form onSubmit={handleLogin} className="space-y-4 mt-4">
                <div className="space-y-2">
                  <Label htmlFor="login-email">Email</Label>
                  <Input
                    id="login-email"
                    type="email"
                    placeholder="doctor@example.com"
                    value={loginEmail}
                    onChange={(e) => setLoginEmail(e.target.value)}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="login-phone">Phone Number</Label>
                  <Input
                    id="login-phone"
                    type="tel"
                    placeholder="03001234567"
                    value={loginPhone}
                    onChange={(e) => setLoginPhone(e.target.value)}
                    required
                  />
                </div>
                <Button type="submit" className="w-full" size="lg" disabled={isLoading}>
                  {isLoading ? "Logging in..." : "Access Dashboard"}
                </Button>
              </form>
            </TabsContent>

            <TabsContent value="register">
              <form onSubmit={handleRegister} className="space-y-4 mt-4">
                <div className="space-y-2">
                  <Label htmlFor="register-name">Full Name</Label>
                  <Input
                    id="register-name"
                    type="text"
                    placeholder="Dr. Jane Smith"
                    value={registerName}
                    onChange={(e) => setRegisterName(e.target.value)}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="register-email">Email</Label>
                  <Input
                    id="register-email"
                    type="email"
                    placeholder="doctor@example.com"
                    value={registerEmail}
                    onChange={(e) => setRegisterEmail(e.target.value)}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="register-phone">Phone Number</Label>
                  <Input
                    id="register-phone"
                    type="tel"
                    placeholder="03001234567"
                    value={registerPhone}
                    onChange={(e) => setRegisterPhone(e.target.value)}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="register-specialty">Specialty</Label>
                  <Input
                    id="register-specialty"
                    type="text"
                    placeholder="e.g. Cardiology, General Medicine"
                    value={registerSpecialty}
                    onChange={(e) => setRegisterSpecialty(e.target.value)}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="register-duration">Consultation Duration (minutes)</Label>
                  <Input
                    id="register-duration"
                    type="number"
                    min="10"
                    max="120"
                    placeholder="30"
                    value={registerDuration}
                    onChange={(e) => setRegisterDuration(e.target.value)}
                  />
                </div>
                <Button type="submit" className="w-full" size="lg" disabled={isLoading}>
                  {isLoading ? "Creating account..." : "Register"}
                </Button>
              </form>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
};

export default DoctorAuth;
