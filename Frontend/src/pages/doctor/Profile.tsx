import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Switch } from "@/components/ui/switch";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import {
  User,
  Mail,
  Phone,
  Briefcase,
  Award,
  Calendar,
  Clock,
  LogOut,
  ArrowLeft,
  Save,
  Edit2,
  X,
  Users,
  CheckCircle,
  TrendingUp,
  Shield
} from "lucide-react";
import { toast } from "sonner";
import api, { type DoctorProfile as DoctorProfileData } from "@/lib/api";

const DoctorProfile = () => {
  const navigate = useNavigate();
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [doctorId, setDoctorId] = useState<number>(0);

  const [doctorData, setDoctorData] = useState({
    name: "",
    email: "",
    specialty: "",
    consultation_duration: 30,
    created_at: "",
  });

  const [stats, setStats] = useState({
    totalPatients: 0,
    totalAppointments: 0,
    completedAppointments: 0,
    upcomingAppointments: 0,
    completionRate: 0,
  });

  const [preferences, setPreferences] = useState({
    emailNotifications: true,
    smsReminders: false,
    autoConfirmAppointments: false,
    weekendAvailability: false,
  });

  const [availability, setAvailability] = useState({
    startTime: "09:00",
    endTime: "17:00",
    slotDuration: "30",
    maxPatientsPerDay: "20"
  });

  const [formData, setFormData] = useState(doctorData);

  useEffect(() => {
    const id = localStorage.getItem("doctor_id");
    if (!id) {
      toast.error("Please login first");
      navigate("/doctor/auth");
      return;
    }
    setDoctorId(parseInt(id));
    loadProfileData(parseInt(id));
  }, [navigate]);

  const loadProfileData = async (id: number) => {
    try {
      setIsLoading(true);

      // Load doctor profile with stats
      const profileResult = await api.doctor.getProfile(id);
      if (profileResult.success && profileResult.data) {
        const p = profileResult.data;
        const data = {
          name: p.name,
          email: p.email,
          specialty: p.specialty,
          consultation_duration: p.consultation_duration,
          created_at: p.created_at,
        };
        setDoctorData(data);
        setFormData(data);
        setStats({
          totalPatients: p.stats.total_patients,
          totalAppointments: p.stats.total_appointments,
          completedAppointments: p.stats.completed_appointments,
          upcomingAppointments: p.stats.upcoming_appointments,
          completionRate: p.stats.completion_rate,
        });
      }

      // Load availability settings
      const availResult = await api.doctor.getAvailabilitySettings(id);
      if (availResult.success && availResult.data) {
        setAvailability({
          startTime: availResult.data.start_time,
          endTime: availResult.data.end_time,
          slotDuration: String(availResult.data.consultation_duration),
          maxPatientsPerDay: "20",
        });
      }
    } catch (error: any) {
      toast.error(error.message || "Failed to load profile");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      const result = await api.doctor.updateProfile(doctorId, {
        name: formData.name,
        email: formData.email,
        specialty: formData.specialty,
      });
      if (result.success) {
        setDoctorData(formData);
        // Update localStorage so header stays in sync
        localStorage.setItem("doctor_name", formData.name);
        localStorage.setItem("doctor_specialty", formData.specialty);
        setIsEditing(false);
        toast.success("Profile updated successfully!");
      } else {
        toast.error(result.message || "Failed to update profile");
      }
    } catch (error: any) {
      toast.error(error.message || "Failed to update profile");
    }
  };

  const handleCancel = () => {
    setFormData(doctorData);
    setIsEditing(false);
  };

  const handleLogout = () => {
    localStorage.removeItem("doctor_id");
    localStorage.removeItem("doctor_name");
    localStorage.removeItem("doctor_specialty");
    toast.success("Logged out successfully");
    navigate("/doctor/auth");
  };

  const handlePreferenceChange = (key: string, value: boolean) => {
    setPreferences(prev => ({ ...prev, [key]: value }));
    toast.success("Preference updated");
  };

  const handleAvailabilityChange = (key: string, value: string) => {
    setAvailability(prev => ({ ...prev, [key]: value }));
  };

  const saveAvailability = async () => {
    try {
      const result = await api.doctor.updateAvailabilitySettings(doctorId, {
        start_time: availability.startTime,
        end_time: availability.endTime,
        consultation_duration: parseInt(availability.slotDuration),
      });
      if (result.success) {
        toast.success("Availability settings saved!");
      } else {
        toast.error(result.message || "Failed to save availability");
      }
    } catch (error: any) {
      toast.error(error.message || "Failed to save availability");
    }
  };

  const getInitials = (name: string) => {
    return name
      .split(" ")
      .map(n => n[0])
      .join("")
      .toUpperCase();
  };

  const memberSince = doctorData.created_at
    ? new Date(doctorData.created_at).toLocaleDateString("en-US", {
        month: "long",
        year: "numeric"
      })
    : "N/A";

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-purple-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="glass-header border-b border-white/20 sticky top-0 z-10 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                size="icon"
                onClick={() => navigate("/doctor/dashboard")}
                className="hover-lift"
              >
                <ArrowLeft className="h-5 w-5" />
              </Button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Doctor Profile</h1>
                <p className="text-sm text-gray-600">Manage your professional information</p>
              </div>
            </div>
            <Button
              variant="outline"
              onClick={handleLogout}
              className="gap-2 hover-lift glass"
            >
              <LogOut className="h-4 w-4" />
              Logout
            </Button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Profile Card & Stats */}
          <div className="lg:col-span-1 space-y-6">
            {/* Profile Header Card */}
            <Card className="glass-card border-0 hover-lift animate-slide-in-up">
              <CardContent className="pt-6">
                <div className="flex flex-col items-center text-center space-y-4">
                  <Avatar className="h-32 w-32 border-4 border-white shadow-lg">
                    <AvatarFallback className="text-3xl bg-gradient-to-br from-blue-500 to-purple-500 text-white">
                      {doctorData.name ? getInitials(doctorData.name) : "DR"}
                    </AvatarFallback>
                  </Avatar>

                  <div className="space-y-2">
                    <h2 className="text-2xl font-bold text-gray-900">{doctorData.name}</h2>
                    <Badge className="bg-blue-100 text-blue-700 hover:bg-blue-200">
                      {doctorData.specialty}
                    </Badge>
                    <div className="flex items-center justify-center gap-2 text-sm text-gray-600">
                      <Mail className="h-4 w-4" />
                      <span>{doctorData.email}</span>
                    </div>
                    <div className="flex items-center justify-center gap-2 text-sm text-gray-600">
                      <Clock className="h-4 w-4" />
                      <span>{doctorData.consultation_duration} min consultations</span>
                    </div>
                  </div>

                  {!isEditing && (
                    <Button
                      onClick={() => setIsEditing(true)}
                      className="w-full gap-2 hover-lift bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600"
                    >
                      <Edit2 className="h-4 w-4" />
                      Edit Profile
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Statistics Cards */}
            <Card className="glass-card border-0 hover-lift animate-slide-in-up" style={{ animationDelay: "0.1s" }}>
              <CardHeader>
                <CardTitle className="text-lg">Professional Statistics</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between p-3 glass rounded-lg hover-lift">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-blue-100 rounded-lg">
                      <Users className="h-5 w-5 text-blue-600" />
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Total Patients</p>
                      <p className="text-xl font-bold text-gray-900">{stats.totalPatients}</p>
                    </div>
                  </div>
                </div>

                <div className="flex items-center justify-between p-3 glass rounded-lg hover-lift">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-green-100 rounded-lg">
                      <CheckCircle className="h-5 w-5 text-green-600" />
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Completed</p>
                      <p className="text-xl font-bold text-gray-900">{stats.completedAppointments}</p>
                    </div>
                  </div>
                </div>

                <div className="flex items-center justify-between p-3 glass rounded-lg hover-lift">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-purple-100 rounded-lg">
                      <Calendar className="h-5 w-5 text-purple-600" />
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Upcoming</p>
                      <p className="text-xl font-bold text-gray-900">{stats.upcomingAppointments}</p>
                    </div>
                  </div>
                </div>

                <div className="flex items-center justify-between p-3 glass rounded-lg hover-lift">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-amber-100 rounded-lg">
                      <TrendingUp className="h-5 w-5 text-amber-600" />
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Success Rate</p>
                      <p className="text-xl font-bold text-gray-900">{stats.completionRate}%</p>
                    </div>
                  </div>
                </div>

                <div className="pt-4 border-t border-gray-200">
                  <p className="text-sm text-gray-600">Member Since</p>
                  <p className="text-base font-semibold text-gray-900">{memberSince}</p>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Right Column - Information & Settings */}
          <div className="lg:col-span-2">
            <Tabs defaultValue="information" className="space-y-6">
              <TabsList className="glass w-full justify-start">
                <TabsTrigger value="information" className="flex-1">Personal Information</TabsTrigger>
                <TabsTrigger value="availability" className="flex-1">Availability</TabsTrigger>
                <TabsTrigger value="preferences" className="flex-1">Preferences</TabsTrigger>
              </TabsList>

              {/* Personal Information Tab */}
              <TabsContent value="information" className="space-y-6">
                <Card className="glass-card border-0 hover-lift animate-slide-in-up">
                  <CardHeader>
                    <CardTitle>Personal Information</CardTitle>
                    <CardDescription>Update your professional details</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="name">Full Name</Label>
                        <div className="relative">
                          <User className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                          <Input
                            id="name"
                            value={formData.name}
                            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                            disabled={!isEditing}
                            className="pl-10 glass"
                          />
                        </div>
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="specialty">Specialty</Label>
                        <div className="relative">
                          <Briefcase className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                          <Input
                            id="specialty"
                            value={formData.specialty}
                            onChange={(e) => setFormData({ ...formData, specialty: e.target.value })}
                            disabled={!isEditing}
                            className="pl-10 glass"
                          />
                        </div>
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="email">Email</Label>
                        <div className="relative">
                          <Mail className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                          <Input
                            id="email"
                            type="email"
                            value={formData.email}
                            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                            disabled={!isEditing}
                            className="pl-10 glass"
                          />
                        </div>
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="duration">Consultation Duration (min)</Label>
                        <div className="relative">
                          <Clock className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                          <Input
                            id="duration"
                            type="number"
                            value={formData.consultation_duration}
                            onChange={(e) => setFormData({ ...formData, consultation_duration: parseInt(e.target.value) || 30 })}
                            disabled={!isEditing}
                            className="pl-10 glass"
                          />
                        </div>
                      </div>
                    </div>

                    {isEditing && (
                      <div className="flex gap-3 pt-4">
                        <Button onClick={handleSave} className="flex-1 gap-2 hover-lift bg-gradient-to-r from-blue-500 to-purple-500">
                          <Save className="h-4 w-4" />
                          Save Changes
                        </Button>
                        <Button onClick={handleCancel} variant="outline" className="flex-1 gap-2 hover-lift glass">
                          <X className="h-4 w-4" />
                          Cancel
                        </Button>
                      </div>
                    )}
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Availability Tab */}
              <TabsContent value="availability" className="space-y-6">
                <Card className="glass-card border-0 hover-lift animate-slide-in-up">
                  <CardHeader>
                    <CardTitle>Availability Settings</CardTitle>
                    <CardDescription>Configure your working hours and appointment slots</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="startTime">Start Time</Label>
                        <div className="relative">
                          <Clock className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                          <Input
                            id="startTime"
                            type="time"
                            value={availability.startTime}
                            onChange={(e) => handleAvailabilityChange("startTime", e.target.value)}
                            className="pl-10 glass"
                          />
                        </div>
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="endTime">End Time</Label>
                        <div className="relative">
                          <Clock className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                          <Input
                            id="endTime"
                            type="time"
                            value={availability.endTime}
                            onChange={(e) => handleAvailabilityChange("endTime", e.target.value)}
                            className="pl-10 glass"
                          />
                        </div>
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="slotDuration">Slot Duration (minutes)</Label>
                        <Select
                          value={availability.slotDuration}
                          onValueChange={(value) => handleAvailabilityChange("slotDuration", value)}
                        >
                          <SelectTrigger className="glass">
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="15">15 minutes</SelectItem>
                            <SelectItem value="30">30 minutes</SelectItem>
                            <SelectItem value="45">45 minutes</SelectItem>
                            <SelectItem value="60">60 minutes</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="maxPatients">Max Patients Per Day</Label>
                        <Input
                          id="maxPatients"
                          type="number"
                          value={availability.maxPatientsPerDay}
                          onChange={(e) => handleAvailabilityChange("maxPatientsPerDay", e.target.value)}
                          className="glass"
                        />
                      </div>
                    </div>

                    <Button onClick={saveAvailability} className="w-full gap-2 hover-lift bg-gradient-to-r from-blue-500 to-purple-500">
                      <Save className="h-4 w-4" />
                      Save Availability Settings
                    </Button>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Preferences Tab */}
              <TabsContent value="preferences" className="space-y-6">
                <Card className="glass-card border-0 hover-lift animate-slide-in-up">
                  <CardHeader>
                    <CardTitle>Notification Preferences</CardTitle>
                    <CardDescription>Manage how you receive updates and alerts</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <div className="flex items-center justify-between p-4 glass rounded-lg hover-lift">
                      <div className="space-y-0.5">
                        <Label htmlFor="email-notifications" className="text-base">Email Notifications</Label>
                        <p className="text-sm text-gray-600">Receive appointment updates via email</p>
                      </div>
                      <Switch
                        id="email-notifications"
                        checked={preferences.emailNotifications}
                        onCheckedChange={(checked) => handlePreferenceChange("emailNotifications", checked)}
                      />
                    </div>

                    <div className="flex items-center justify-between p-4 glass rounded-lg hover-lift">
                      <div className="space-y-0.5">
                        <Label htmlFor="sms-reminders" className="text-base">SMS Reminders</Label>
                        <p className="text-sm text-gray-600">Get text message reminders before appointments</p>
                      </div>
                      <Switch
                        id="sms-reminders"
                        checked={preferences.smsReminders}
                        onCheckedChange={(checked) => handlePreferenceChange("smsReminders", checked)}
                      />
                    </div>

                    <div className="flex items-center justify-between p-4 glass rounded-lg hover-lift">
                      <div className="space-y-0.5">
                        <Label htmlFor="auto-confirm" className="text-base">Auto-confirm Appointments</Label>
                        <p className="text-sm text-gray-600">Automatically confirm new appointment requests</p>
                      </div>
                      <Switch
                        id="auto-confirm"
                        checked={preferences.autoConfirmAppointments}
                        onCheckedChange={(checked) => handlePreferenceChange("autoConfirmAppointments", checked)}
                      />
                    </div>

                    <div className="flex items-center justify-between p-4 glass rounded-lg hover-lift">
                      <div className="space-y-0.5">
                        <Label htmlFor="weekend-availability" className="text-base">Weekend Availability</Label>
                        <p className="text-sm text-gray-600">Accept appointments on weekends</p>
                      </div>
                      <Switch
                        id="weekend-availability"
                        checked={preferences.weekendAvailability}
                        onCheckedChange={(checked) => handlePreferenceChange("weekendAvailability", checked)}
                      />
                    </div>
                  </CardContent>
                </Card>

                {/* Danger Zone */}
                <Card className="glass-card border-0 border-red-200 hover-lift animate-slide-in-up">
                  <CardHeader>
                    <CardTitle className="text-red-600">Danger Zone</CardTitle>
                    <CardDescription>Irreversible actions</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <AlertDialog>
                      <AlertDialogTrigger asChild>
                        <Button variant="destructive" className="w-full hover-lift">
                          Delete Account
                        </Button>
                      </AlertDialogTrigger>
                      <AlertDialogContent className="glass-card">
                        <AlertDialogHeader>
                          <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
                          <AlertDialogDescription>
                            This action cannot be undone. This will permanently delete your account
                            and remove all your data from our servers including patient records and appointment history.
                          </AlertDialogDescription>
                        </AlertDialogHeader>
                        <AlertDialogFooter>
                          <AlertDialogCancel className="glass">Cancel</AlertDialogCancel>
                          <AlertDialogAction className="bg-red-600 hover:bg-red-700">
                            Yes, delete my account
                          </AlertDialogAction>
                        </AlertDialogFooter>
                      </AlertDialogContent>
                    </AlertDialog>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DoctorProfile;
