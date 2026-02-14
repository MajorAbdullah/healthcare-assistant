import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { Heart, Stethoscope, Calendar, MessageCircle, BarChart3, Users, ClipboardList, Activity } from "lucide-react";

const portals = [
  {
    title: "Patient Portal",
    description: "Everything you need to manage your health in one place.",
    icon: Heart,
    gradient: "from-blue-500 to-cyan-500",
    hoverGlow: "hover:shadow-blue-500/10",
    features: [
      { icon: Calendar, text: "Book appointments instantly" },
      { icon: MessageCircle, text: "Chat with AI assistant" },
      { icon: Activity, text: "Track your health journey" },
    ],
    cta: "Get Started as Patient",
    route: "/patient/auth",
    slideFrom: -50,
  },
  {
    title: "Doctor Portal",
    description: "Powerful tools to streamline your medical practice.",
    icon: Stethoscope,
    gradient: "from-purple-500 to-indigo-500",
    hoverGlow: "hover:shadow-purple-500/10",
    features: [
      { icon: Users, text: "Manage patient records" },
      { icon: ClipboardList, text: "Organize appointments" },
      { icon: BarChart3, text: "View practice analytics" },
    ],
    cta: "Join as Doctor",
    route: "/doctor/auth",
    slideFrom: 50,
  },
];

const PortalCards = () => {
  const navigate = useNavigate();

  return (
    <section className="py-24 bg-slate-950">
      <div className="max-w-5xl mx-auto px-6">
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
        >
          <p className="text-sm text-blue-400 font-medium mb-2 uppercase tracking-wider">Get Started</p>
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Choose your portal
          </h2>
          <p className="text-white/50 max-w-xl mx-auto">
            Whether you're a patient seeking care or a doctor managing your practice, we have the right tools for you.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-8">
          {portals.map((portal) => (
            <motion.div
              key={portal.title}
              className={`relative bg-white/[0.03] border border-white/[0.08] rounded-2xl p-8 hover:bg-white/[0.05] transition-all duration-300 hover:-translate-y-1 hover:shadow-xl ${portal.hoverGlow}`}
              initial={{ opacity: 0, x: portal.slideFrom }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, type: "spring", stiffness: 100 }}
            >
              <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${portal.gradient} flex items-center justify-center mb-5`}>
                <portal.icon className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-2">{portal.title}</h3>
              <p className="text-white/50 mb-6">{portal.description}</p>

              <div className="space-y-3 mb-8">
                {portal.features.map((f, i) => (
                  <div key={i} className="flex items-center gap-3">
                    <f.icon className="w-4 h-4 text-white/30" />
                    <span className="text-sm text-white/60">{f.text}</span>
                  </div>
                ))}
              </div>

              <button
                onClick={() => navigate(portal.route)}
                className={`w-full py-3 rounded-xl bg-gradient-to-r ${portal.gradient} text-white font-medium hover:shadow-lg transition-all duration-300 hover:opacity-90`}
              >
                {portal.cta}
              </button>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default PortalCards;
