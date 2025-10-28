import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Search, Filter, LogOut, User, Mail, Phone, Calendar, Eye } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

interface Patient {
  id: number;
  name: string;
  email: string;
  phone: string;
  totalVisits: number;
  lastVisit: string;
  status: "active" | "inactive";
}

const PatientsDirectory = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState("");
  const [sortBy, setSortBy] = useState("name");
  const [filterStatus, setFilterStatus] = useState("all");

  const doctorName = localStorage.getItem("doctorName") || "Doctor";

  // Mock patients data
  const allPatients: Patient[] = [
    { id: 1, name: "Sarah Johnson", email: "sarah.j@email.com", phone: "+1 234-567-8901", totalVisits: 12, lastVisit: "2025-10-20", status: "active" },
    { id: 2, name: "Michael Chen", email: "m.chen@email.com", phone: "+1 234-567-8902", totalVisits: 8, lastVisit: "2025-10-18", status: "active" },
    { id: 3, name: "Emily Davis", email: "emily.d@email.com", phone: "+1 234-567-8903", totalVisits: 15, lastVisit: "2025-10-25", status: "active" },
    { id: 4, name: "James Wilson", email: "j.wilson@email.com", phone: "+1 234-567-8904", totalVisits: 5, lastVisit: "2025-09-15", status: "inactive" },
    { id: 5, name: "Lisa Anderson", email: "lisa.a@email.com", phone: "+1 234-567-8905", totalVisits: 20, lastVisit: "2025-10-22", status: "active" },
    { id: 6, name: "Robert Taylor", email: "r.taylor@email.com", phone: "+1 234-567-8906", totalVisits: 3, lastVisit: "2025-08-10", status: "inactive" },
  ];

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
                           patient.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
                           patient.phone.includes(searchQuery);
      const matchesStatus = filterStatus === "all" || patient.status === filterStatus;
      return matchesSearch && matchesStatus;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case "name":
          return a.name.localeCompare(b.name);
        case "visits":
          return b.totalVisits - a.totalVisits;
        case "lastVisit":
          return new Date(b.lastVisit).getTime() - new Date(a.lastVisit).getTime();
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
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredPatients.map((patient) => (
            <Card
              key={patient.id}
              className="glass-card shadow-card hover:shadow-card-hover transition-all duration-300 border-white/20 hover:scale-[1.02] cursor-pointer"
              onClick={() => navigate(`/doctor/patients/${patient.id}`)}
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
                    <p className={`text-sm ${patient.status === "active" ? "text-success" : "text-muted-foreground"}`}>
                      {patient.status === "active" ? "Active" : "Inactive"}
                    </p>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <Mail className="h-4 w-4" />
                    <span className="truncate">{patient.email}</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <Phone className="h-4 w-4" />
                    <span>{patient.phone}</span>
                  </div>
                  <div className="flex items-center justify-between pt-3 border-t border-white/20">
                    <div className="text-center">
                      <p className="text-2xl font-bold text-primary">{patient.totalVisits}</p>
                      <p className="text-xs text-muted-foreground">Total Visits</p>
                    </div>
                    <div className="text-center">
                      <p className="text-sm font-medium">{new Date(patient.lastVisit).toLocaleDateString()}</p>
                      <p className="text-xs text-muted-foreground">Last Visit</p>
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

        {filteredPatients.length === 0 && (
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
