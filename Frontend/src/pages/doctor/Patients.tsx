import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Search, Filter, LogOut, User, Mail, Phone, Calendar, Eye } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { toast } from "sonner";
import api, { type Patient } from "@/lib/api";

const PatientsDirectory = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState("");
  const [sortBy, setSortBy] = useState("name");
  const [filterStatus, setFilterStatus] = useState("all");
  const [isLoading, setIsLoading] = useState(false);
  const [allPatients, setAllPatients] = useState<Patient[]>([]);
  const [doctorId, setDoctorId] = useState<number>(0);

  const doctorName = localStorage.getItem("doctor_name") || "Doctor";

  useEffect(() => {
    const id = localStorage.getItem("doctor_id");
    if (!id) {
      toast.error("Please login first");
      navigate("/doctor/auth");
      return;
    }
    setDoctorId(parseInt(id));
    loadPatients(parseInt(id));
  }, [navigate]);

  const loadPatients = async (id: number) => {
    try {
      setIsLoading(true);
      const result = await api.doctor.getPatients(id);
      if (result.success && result.data) {
        setAllPatients(result.data.patients);
      }
    } catch (error: any) {
      toast.error(error.message || "Failed to load patients");
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

  // Filter and sort patients
  const filteredPatients = allPatients
    .filter(patient => {
      const matchesSearch = patient.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                           (patient.email?.toLowerCase() || "").includes(searchQuery.toLowerCase()) ||
                           (patient.phone || "").includes(searchQuery);
      return matchesSearch;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case "name":
          return a.name.localeCompare(b.name);
        default:
          return 0;
      }
    });

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      {/* Header */}
      <header className="glass-header sticky top-0 z-50 border-b border-white/20">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-foreground">Patient Directory</h1>
            <p className="text-sm text-muted-foreground">Dr. {doctorName}</p>
          </div>
          <div className="flex items-center gap-3">
            <Button variant="outline" onClick={() => navigate("/doctor/dashboard")} className="glass hover:scale-105 transition-transform">
              Dashboard
            </Button>
            <Button variant="outline" onClick={() => navigate("/doctor/calendar")} className="glass hover:scale-105 transition-transform">
              Calendar
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
        {/* Search and Filters */}
        <Card className="glass-card shadow-card border-white/20 mb-6">
          <CardContent className="pt-6">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  type="text"
                  placeholder="Search by name, email, or phone..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 glass border-white/20"
                />
              </div>
              <Select value={sortBy} onValueChange={setSortBy}>
                <SelectTrigger className="w-full md:w-[200px] glass border-white/20">
                  <SelectValue placeholder="Sort by" />
                </SelectTrigger>
                <SelectContent className="glass-card border-white/20">
                  <SelectItem value="name">Name (A-Z)</SelectItem>
                  <SelectItem value="visits">Total Visits</SelectItem>
                  <SelectItem value="lastVisit">Last Visit</SelectItem>
                </SelectContent>
              </Select>
              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger className="w-full md:w-[200px] glass border-white/20">
                  <SelectValue placeholder="Filter by status" />
                </SelectTrigger>
                <SelectContent className="glass-card border-white/20">
                  <SelectItem value="all">All Patients</SelectItem>
                  <SelectItem value="active">Active</SelectItem>
                  <SelectItem value="inactive">Inactive</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Patients Grid */}
        {isLoading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        ) : filteredPatients.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredPatients.map((patient) => (
              <Card
                key={patient.user_id}
                className="glass-card shadow-card hover:shadow-card-hover transition-all duration-300 border-white/20 hover:scale-[1.02] cursor-pointer"
                onClick={() => navigate(`/doctor/patients/${patient.user_id}`)}
              >
                <CardHeader>
                  <div className="flex items-center gap-3">
                    <Avatar className="h-12 w-12">
                      <AvatarFallback className="bg-primary/10 text-primary">
                        {getInitials(patient.name)}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1">
                      <CardTitle className="text-lg">{patient.name}</CardTitle>
                      <p className="text-sm text-success">Active</p>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <Mail className="h-4 w-4" />
                      <span className="truncate">{patient.email || "N/A"}</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <Phone className="h-4 w-4" />
                      <span>{patient.phone || "N/A"}</span>
                    </div>
                    <div className="flex items-center justify-between pt-3 border-t border-white/20">
                      <div className="text-center">
                        <p className="text-sm font-medium">{patient.date_of_birth ? new Date(patient.date_of_birth).toLocaleDateString() : "N/A"}</p>
                        <p className="text-xs text-muted-foreground">Date of Birth</p>
                      </div>
                      <div className="text-center">
                        <p className="text-sm font-medium capitalize">{patient.gender || "N/A"}</p>
                        <p className="text-xs text-muted-foreground">Gender</p>
                      </div>
                    </div>
                    <Button className="w-full mt-4 hover:scale-105 transition-transform" size="sm">
                      <Eye className="h-4 w-4 mr-2" />
                      View Details
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <Card className="glass-card shadow-card border-white/20">
            <CardContent className="py-12 text-center">
              <User className="h-12 w-12 mx-auto text-muted-foreground/50 mb-4" />
              <p className="text-muted-foreground">No patients found matching your criteria</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default PatientsDirectory;
