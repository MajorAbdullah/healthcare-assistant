import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { Stethoscope } from "lucide-react";
import api, { type Doctor } from "@/lib/api";

const DoctorAuth = () => {
  const navigate = useNavigate();
  const [selectedDoctor, setSelectedDoctor] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [doctors, setDoctors] = useState<Doctor[]>([]);

  useEffect(() => {
    loadDoctors();
  }, []);

  const loadDoctors = async () => {
    try {
      const result = await api.doctor.getAll();
      if (result.success && result.data) {
        setDoctors(Array.isArray(result.data) ? result.data : []);
      }
    } catch (error: any) {
      toast.error(error.message || "Failed to load doctors");
    }
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedDoctor) {
      toast.error("Please select a doctor");
      return;
    }

    setIsLoading(true);
    const doctorId = parseInt(selectedDoctor);

    try {
      const result = await api.doctor.login(doctorId);
      
      if (result.success && result.data) {
        const doctor = doctors.find(d => d.doctor_id === doctorId);
        
        localStorage.setItem("user_type", "doctor");
        localStorage.setItem("doctor_id", selectedDoctor);
        localStorage.setItem("doctor_name", doctor?.name || "");
        localStorage.setItem("doctor_specialty", doctor?.specialty || "");
        
        toast.success(`Welcome back, ${doctor?.name}!`);
        navigate("/doctor/dashboard");
      } else {
        toast.error(result.message || "Login failed");
      }
    } catch (error: any) {
      toast.error(error.message || "Login failed");
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
          <form onSubmit={handleLogin} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="doctor-select">Select Your Profile</Label>
              <Select value={selectedDoctor} onValueChange={setSelectedDoctor}>
                <SelectTrigger id="doctor-select" className="h-auto py-3">
                  <SelectValue placeholder="Choose your doctor profile" />
                </SelectTrigger>
                <SelectContent>
                  {doctors.map((doctor) => (
                    <SelectItem key={doctor.doctor_id} value={doctor.doctor_id.toString()} className="py-3">
                      <div className="flex flex-col items-start">
                        <span className="font-medium">{doctor.name}</span>
                        <span className="text-sm text-muted-foreground">{doctor.specialty} • ID: {doctor.doctor_id}</span>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <Button type="submit" className="w-full" size="lg" disabled={isLoading}>
              {isLoading ? "Logging in..." : "Access Dashboard"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default DoctorAuth;
