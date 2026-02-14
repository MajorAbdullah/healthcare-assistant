import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Edit2, Save, X, Calendar, Mail, User, Calendar as CalendarIcon } from "lucide-react";
import { toast } from "sonner";
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
import api from "@/lib/api";

const PatientProfile = () => {
  const navigate = useNavigate();
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [userId, setUserId] = useState<number>(0);
  
  // Profile data
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [dob, setDob] = useState("");
  const [gender, setGender] = useState("male");
  
  // Preferences
  const [emailNotifications, setEmailNotifications] = useState(true);
  const [smsReminders, setSmsReminders] = useState(true);
  const [autoSyncCalendar, setAutoSyncCalendar] = useState(false);
  
  // Stats
  const [totalAppointments, setTotalAppointments] = useState(0);
  const [upcomingCount, setUpcomingCount] = useState(0);
  const [completedCount, setCompletedCount] = useState(0);

  useEffect(() => {
    const storedUserId = localStorage.getItem("user_id");
    if (!storedUserId) {
      toast.error("Please login first");
      navigate("/patient/auth");
      return;
    }
    const id = parseInt(storedUserId);
    setUserId(id);
    loadProfile(id);
    loadPreferences(id);
    loadAppointmentStats(id);
  }, [navigate]);

  const loadProfile = async (id: number) => {
    try {
      const result = await api.patient.getProfile(id);
      if (result.success && result.data) {
        setName(result.data.name);
        setEmail(result.data.email || "");
        setDob(result.data.date_of_birth || "");
        setGender(result.data.gender || "male");
      }
    } catch (error: any) {
      toast.error(error.message || "Failed to load profile");
    }
  };

  const loadPreferences = async (id: number) => {
    try {
      const result = await api.patient.getPreferences(id);
      if (result.success && result.data) {
        const prefs = result.data.preferences;
        setEmailNotifications(prefs.email_notifications ?? true);
        setSmsReminders(prefs.sms_reminders ?? true);
        setAutoSyncCalendar(prefs.auto_sync_calendar ?? false);
      }
    } catch (error: any) {
      // Preferences might not exist yet, that's okay
      console.log("No preferences found, using defaults");
    }
  };

  const loadAppointmentStats = async (id: number) => {
    try {
      const result = await api.appointment.getByPatient(id, false);
      if (result.success && result.data) {
        const appointments = result.data.appointments;
        setTotalAppointments(appointments.length);
        setUpcomingCount(appointments.filter(a => a.status === "scheduled").length);
        setCompletedCount(appointments.filter(a => a.status === "completed").length);
      }
    } catch (error: any) {
      console.log("Failed to load appointment stats");
    }
  };

  const handleSave = async () => {
    if (!userId) return;
    
    try {
      setIsLoading(true);
      
      // Update profile
      const profileResult = await api.patient.updateProfile(userId, {
        name,
        email,
        date_of_birth: dob,
        gender: gender as "male" | "female" | "other"
      });

      // Update preferences
      const prefsResult = await api.patient.updatePreferences(userId, {
        email_notifications: emailNotifications,
        sms_reminders: smsReminders,
        auto_sync_calendar: autoSyncCalendar
      });

      if (profileResult.success && prefsResult.success) {
        toast.success("Profile updated successfully");
        setIsEditing(false);
        
        // Update localStorage if email changed
        if (email) {
          localStorage.setItem("user_email", email);
        }
        if (name) {
          localStorage.setItem("user_name", name);
        }
      } else {
        toast.error("Failed to update profile");
      }
    } catch (error: any) {
      toast.error(error.message || "Failed to update profile");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    // Reload profile to reset changes
    loadProfile(userId);
    loadPreferences(userId);
    toast.info("Changes discarded");
    setIsEditing(false);
  };

  const stats = [
    { label: "Total Appointments", value: String(totalAppointments), icon: CalendarIcon },
    { label: "Upcoming", value: String(upcomingCount), icon: Calendar },
    { label: "Completed", value: String(completedCount), icon: Calendar },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="glass-header sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Button variant="ghost" onClick={() => navigate("/patient/dashboard")}>
            <ArrowLeft className="h-5 w-5 mr-2" />
            Back
          </Button>
          <h1 className="text-xl font-semibold">My Profile</h1>
          {!isEditing ? (
            <Button onClick={() => setIsEditing(true)} className="gap-2">
              <Edit2 className="h-4 w-4" />
              Edit
            </Button>
          ) : (
            <div className="flex gap-2">
              <Button variant="outline" onClick={handleCancel} className="gap-2">
                <X className="h-4 w-4" />
                Cancel
              </Button>
              <Button onClick={handleSave} className="gap-2">
                <Save className="h-4 w-4" />
                Save
              </Button>
            </div>
          )}
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 max-w-4xl space-y-6">
        {/* Profile Header */}
        <Card className="glass-card">
          <CardContent className="pt-6">
            <div className="flex items-center gap-6">
              <Avatar className="w-24 h-24 border-4 border-white shadow-lg">
                <AvatarFallback className="bg-primary text-primary-foreground text-3xl">
                  {name.split(" ").map(n => n[0]).join("").toUpperCase()}
                </AvatarFallback>
              </Avatar>
              <div className="flex-1">
                <h2 className="text-3xl font-bold">{name}</h2>
                <p className="text-muted-foreground">{email}</p>
                <Badge className="mt-2">Patient since Jan 2024</Badge>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Statistics */}
        <div className="grid md:grid-cols-3 gap-6">
          {stats.map((stat, index) => (
            <Card key={index} className="glass-card">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">
                  {stat.label}
                </CardTitle>
                <stat.icon className="h-5 w-5 text-primary" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">{stat.value}</div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Personal Information */}
        <Card className="glass-card">
          <CardHeader>
            <CardTitle>Personal Information</CardTitle>
            <CardDescription>
              {isEditing ? "Update your personal details" : "Your personal information"}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="name">Full Name</Label>
                {isEditing ? (
                  <Input
                    id="name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                  />
                ) : (
                  <div className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg">
                    <User className="w-4 h-4 text-muted-foreground" />
                    <span>{name}</span>
                  </div>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                {isEditing ? (
                  <Input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                ) : (
                  <div className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg">
                    <Mail className="w-4 h-4 text-muted-foreground" />
                    <span>{email}</span>
                  </div>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="dob">Date of Birth</Label>
                {isEditing ? (
                  <Input
                    id="dob"
                    type="date"
                    value={dob}
                    onChange={(e) => setDob(e.target.value)}
                  />
                ) : (
                  <div className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg">
                    <Calendar className="w-4 h-4 text-muted-foreground" />
                    <span>{new Date(dob).toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" })}</span>
                  </div>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="gender">Gender</Label>
                {isEditing ? (
                  <Select value={gender} onValueChange={setGender}>
                    <SelectTrigger id="gender">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="male">Male</SelectItem>
                      <SelectItem value="female">Female</SelectItem>
                      <SelectItem value="other">Other</SelectItem>
                    </SelectContent>
                  </Select>
                ) : (
                  <div className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg">
                    <span className="capitalize">{gender}</span>
                  </div>
                )}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Preferences */}
        <Card className="glass-card">
          <CardHeader>
            <CardTitle>Preferences</CardTitle>
            <CardDescription>Manage your notification and sync preferences</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>Email Notifications</Label>
                <p className="text-sm text-muted-foreground">
                  Receive appointment reminders via email
                </p>
              </div>
              <Switch
                checked={emailNotifications}
                onCheckedChange={setEmailNotifications}
              />
            </div>

            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>SMS Reminders</Label>
                <p className="text-sm text-muted-foreground">
                  Get text message reminders for appointments
                </p>
              </div>
              <Switch
                checked={smsReminders}
                onCheckedChange={setSmsReminders}
              />
            </div>

            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>Auto-Sync Calendar</Label>
                <p className="text-sm text-muted-foreground">
                  Automatically add appointments to your calendar
                </p>
              </div>
              <Switch
                checked={autoSyncCalendar}
                onCheckedChange={setAutoSyncCalendar}
              />
            </div>
          </CardContent>
        </Card>

        {/* Danger Zone */}
        <Card className="glass-card border-destructive/50">
          <CardHeader>
            <CardTitle className="text-destructive">Danger Zone</CardTitle>
            <CardDescription>Irreversible actions for your account</CardDescription>
          </CardHeader>
          <CardContent>
            <AlertDialog>
              <AlertDialogTrigger asChild>
                <Button variant="destructive">Delete Account</Button>
              </AlertDialogTrigger>
              <AlertDialogContent>
                <AlertDialogHeader>
                  <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
                  <AlertDialogDescription>
                    This action cannot be undone. This will permanently delete your account
                    and remove all your data from our servers including appointment history.
                  </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                  <AlertDialogCancel>Cancel</AlertDialogCancel>
                  <AlertDialogAction className="bg-destructive text-destructive-foreground hover:bg-destructive/90">
                    Delete Account
                  </AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

export default PatientProfile;
