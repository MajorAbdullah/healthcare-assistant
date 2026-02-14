import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { LogOut, TrendingUp, Users, Calendar as CalendarIcon, CheckCircle, BarChart3, Download } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { toast } from "sonner";
import api, { type Analytics as AnalyticsData } from "@/lib/api";

const Analytics = () => {
  const navigate = useNavigate();
  const [dateRange, setDateRange] = useState("30");
  const [isLoading, setIsLoading] = useState(false);
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
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
    loadAnalytics(parseInt(id));
  }, [navigate, dateRange]);

  const loadAnalytics = async (id: number) => {
    try {
      setIsLoading(true);
      const result = await api.doctor.getAnalytics(id);
      if (result.success && result.data) {
        setAnalytics(result.data);
      }
    } catch (error: any) {
      toast.error(error.message || "Failed to load analytics");
    } finally {
      setIsLoading(false);
    }
  };

  // Transform API data for charts
  const statusColors: Record<string, string> = {
    completed: "hsl(var(--success))",
    scheduled: "hsl(var(--primary))",
    cancelled: "hsl(var(--destructive))",
    pending_approval: "hsl(var(--warning))",
    confirmed: "hsl(142 76% 36%)",
  };

  const completionRate = analytics?.status_breakdown
    ? Object.entries(analytics.status_breakdown).map(([name, value]) => ({
        name: name.charAt(0).toUpperCase() + name.slice(1).replace('_', ' '),
        value,
        color: statusColors[name] || "hsl(var(--muted))",
      }))
    : [];

  const dayOrder = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
  const dayShort: Record<string, string> = { Monday: "Mon", Tuesday: "Tue", Wednesday: "Wed", Thursday: "Thu", Friday: "Fri", Saturday: "Sat", Sunday: "Sun" };

  const weeklyBreakdown = analytics?.weekly_breakdown
    ? dayOrder
        .filter(day => day in analytics.weekly_breakdown)
        .map(day => ({ day: dayShort[day], count: analytics.weekly_breakdown[day] }))
    : [];

  const appointmentTrends = analytics?.daily_breakdown || [];

  const patientGrowth = analytics?.patient_growth || [];

  const stats = [
    {
      label: "Total Appointments",
      value: String(analytics?.total_appointments || 0),
      icon: CalendarIcon,
      color: "text-primary",
      bgColor: "bg-primary/10"
    },
    {
      label: "Total Patients",
      value: String(analytics?.total_patients || 0),
      icon: Users,
      color: "text-secondary",
      bgColor: "bg-secondary/10"
    },
    {
      label: "Avg Daily Appointments",
      value: String(analytics?.avg_daily_appointments || 0),
      icon: TrendingUp,
      color: "text-accent",
      bgColor: "bg-accent/10"
    },
    {
      label: "Completion Rate",
      value: `${analytics?.completion_rate || 0}%`,
      icon: CheckCircle,
      color: "text-success",
      bgColor: "bg-success/10"
    },
  ];

  const handleLogout = () => {
    localStorage.clear();
    navigate("/");
  };

  const handleExport = () => {
    if (!analytics) {
      toast.error("No analytics data to export");
      return;
    }

    const rows = [
      ["Metric", "Value"],
      ["Total Appointments", String(analytics.total_appointments)],
      ["Total Patients", String(analytics.total_patients)],
      ["Avg Daily Appointments", String(analytics.avg_daily_appointments)],
      ["Completion Rate", `${analytics.completion_rate}%`],
      [],
      ["Status", "Count"],
      ...Object.entries(analytics.status_breakdown).map(([status, count]) => [status, String(count)]),
      [],
      ["Date", "Appointments"],
      ...analytics.daily_breakdown.map(d => [d.date, String(d.count)]),
    ];

    const csv = rows.map(row => row.join(",")).join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `analytics_${analytics.period.start_date}_${analytics.period.end_date}.csv`;
    a.click();
    URL.revokeObjectURL(url);
    toast.success("Analytics exported successfully");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      {/* Header */}
      <header className="glass-header sticky top-0 z-50 border-b border-white/20">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-foreground">Analytics Dashboard</h1>
            <p className="text-sm text-muted-foreground">Dr. {doctorName}</p>
          </div>
          <div className="flex items-center gap-3">
            <Button variant="outline" onClick={() => navigate("/doctor/dashboard")} className="glass hover:scale-105 transition-transform">
              Dashboard
            </Button>
            <Button variant="outline" onClick={() => navigate("/doctor/calendar")} className="glass hover:scale-105 transition-transform">
              Calendar
            </Button>
            <Button variant="outline" onClick={() => navigate("/doctor/patients")} className="glass hover:scale-105 transition-transform">
              Patients
            </Button>
            <Button variant="outline" onClick={handleLogout} className="glass hover:scale-105 transition-transform">
              <LogOut className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Date Range Selector */}
        <div className="flex justify-between items-center mb-6">
          <div className="flex items-center gap-3">
            <BarChart3 className="h-6 w-6 text-primary" />
            <h2 className="text-xl font-semibold">Performance Overview</h2>
          </div>
          <div className="flex gap-3">
            <Select value={dateRange} onValueChange={setDateRange}>
              <SelectTrigger className="w-[180px] glass border-white/20">
                <SelectValue placeholder="Select period" />
              </SelectTrigger>
              <SelectContent className="glass-card border-white/20">
                <SelectItem value="7">Last 7 days</SelectItem>
                <SelectItem value="30">Last 30 days</SelectItem>
                <SelectItem value="90">Last 3 months</SelectItem>
                <SelectItem value="365">Last year</SelectItem>
              </SelectContent>
            </Select>
            <Button onClick={handleExport} className="hover:scale-105 transition-transform">
              <Download className="h-4 w-4 mr-2" />
              Export CSV
            </Button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
          {stats.map((stat, index) => (
            <Card
              key={index}
              className="glass-card shadow-card hover:shadow-card-hover transition-all duration-300 border-white/20 hover:scale-105"
            >
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground mb-1">{stat.label}</p>
                    <p className="text-3xl font-bold">{stat.value}</p>
                  </div>
                  <div className={`${stat.bgColor} p-3 rounded-full`}>
                    <stat.icon className={`h-6 w-6 ${stat.color}`} />
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Appointment Trends */}
          <Card className="glass-card shadow-card hover:shadow-card-hover transition-all duration-300 border-white/20">
            <CardHeader>
              <CardTitle>Appointment Trends</CardTitle>
              <CardDescription>Scheduled vs Completed appointments over time</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={appointmentTrends}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" opacity={0.3} />
                  <XAxis dataKey="date" stroke="hsl(var(--muted-foreground))" />
                  <YAxis stroke="hsl(var(--muted-foreground))" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "hsl(var(--background))",
                      border: "1px solid hsl(var(--border))",
                      borderRadius: "8px",
                    }}
                  />
                  <Legend />
                  <Line type="monotone" dataKey="scheduled" stroke="hsl(var(--primary))" strokeWidth={2} dot={{ r: 4 }} />
                  <Line type="monotone" dataKey="completed" stroke="hsl(var(--success))" strokeWidth={2} dot={{ r: 4 }} />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Completion Rate */}
          <Card className="glass-card shadow-card hover:shadow-card-hover transition-all duration-300 border-white/20">
            <CardHeader>
              <CardTitle>Completion Rate</CardTitle>
              <CardDescription>Breakdown of appointment outcomes</CardDescription>
            </CardHeader>
            <CardContent className="flex items-center justify-center">
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={completionRate}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, value }) => `${name}: ${value}%`}
                    outerRadius={100}
                    fill="hsl(var(--primary))"
                    dataKey="value"
                  >
                    {completionRate.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Busiest Days */}
          <Card className="glass-card shadow-card hover:shadow-card-hover transition-all duration-300 border-white/20">
            <CardHeader>
              <CardTitle>Busiest Days</CardTitle>
              <CardDescription>Weekly appointment distribution</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={weeklyBreakdown}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" opacity={0.3} />
                  <XAxis dataKey="day" stroke="hsl(var(--muted-foreground))" />
                  <YAxis stroke="hsl(var(--muted-foreground))" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "hsl(var(--background))",
                      border: "1px solid hsl(var(--border))",
                      borderRadius: "8px",
                    }}
                  />
                  <Bar dataKey="count" fill="hsl(var(--accent))" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Patient Growth */}
          <Card className="glass-card shadow-card hover:shadow-card-hover transition-all duration-300 border-white/20">
            <CardHeader>
              <CardTitle>Patient Growth</CardTitle>
              <CardDescription>Total patient base over time</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={patientGrowth}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" opacity={0.3} />
                  <XAxis dataKey="month" stroke="hsl(var(--muted-foreground))" />
                  <YAxis stroke="hsl(var(--muted-foreground))" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "hsl(var(--background))",
                      border: "1px solid hsl(var(--border))",
                      borderRadius: "8px",
                    }}
                  />
                  <Area
                    type="monotone"
                    dataKey="patients"
                    stroke="hsl(var(--secondary))"
                    fill="hsl(var(--secondary))"
                    fillOpacity={0.3}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
