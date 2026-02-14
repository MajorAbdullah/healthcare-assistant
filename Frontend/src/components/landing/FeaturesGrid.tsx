import { motion } from "framer-motion";
import { Brain, Calendar, LayoutDashboard, Users, CalendarSync, MessageCircle } from "lucide-react";

const features = [
  {
    icon: Brain,
    title: "AI Assistant",
    description: "Get instant answers to medical questions from our intelligent AI chatbot, available 24/7.",
    color: "from-blue-500 to-cyan-500",
    glow: "group-hover:shadow-blue-500/20",
  },
  {
    icon: Calendar,
    title: "Smart Scheduling",
    description: "Book, reschedule, or cancel appointments with real-time availability in just a few clicks.",
    color: "from-purple-500 to-indigo-500",
    glow: "group-hover:shadow-purple-500/20",
  },
  {
    icon: LayoutDashboard,
    title: "Doctor Dashboard",
    description: "Powerful tools for doctors to manage patients, appointments, and practice analytics.",
    color: "from-emerald-500 to-teal-500",
    glow: "group-hover:shadow-emerald-500/20",
  },
  {
    icon: Users,
    title: "Patient Profiles",
    description: "Comprehensive health profiles with medical history, prescriptions, and visit records.",
    color: "from-orange-500 to-amber-500",
    glow: "group-hover:shadow-orange-500/20",
  },
  {
    icon: CalendarSync,
    title: "Calendar Sync",
    description: "Seamless calendar integration keeps your schedule organized across all your devices.",
    color: "from-pink-500 to-rose-500",
    glow: "group-hover:shadow-pink-500/20",
  },
  {
    icon: MessageCircle,
    title: "Real-time Chat",
    description: "Communicate with your healthcare team instantly through our secure messaging system.",
    color: "from-violet-500 to-purple-500",
    glow: "group-hover:shadow-violet-500/20",
  },
];

const FeaturesGrid = () => {
  return (
    <section id="features" className="relative py-24 bg-slate-950">
      <div className="max-w-7xl mx-auto px-6">
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
        >
          <p className="text-sm text-blue-400 font-medium mb-2 uppercase tracking-wider">Features</p>
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Everything you need for modern healthcare
          </h2>
          <p className="text-white/50 max-w-2xl mx-auto">
            A comprehensive platform designed for both patients and doctors with powerful tools and intelligent features.
          </p>
        </motion.div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, i) => (
            <motion.div
              key={feature.title}
              className={`group relative bg-white/[0.03] border border-white/[0.06] rounded-2xl p-6 hover:bg-white/[0.06] transition-all duration-300 hover:-translate-y-1 hover:shadow-xl ${feature.glow}`}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
            >
              <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${feature.color} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300`}>
                <feature.icon className="w-5 h-5 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
              <p className="text-sm text-white/50 leading-relaxed">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesGrid;
