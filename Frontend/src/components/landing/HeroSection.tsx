import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { Heart, Stethoscope, Activity, Pill, Brain, ShieldCheck } from "lucide-react";

const floatingIcons = [
  { Icon: Heart, x: "10%", y: "20%", delay: 0 },
  { Icon: Stethoscope, x: "85%", y: "15%", delay: 0.5 },
  { Icon: Activity, x: "75%", y: "70%", delay: 1 },
  { Icon: Pill, x: "15%", y: "75%", delay: 1.5 },
  { Icon: Brain, x: "90%", y: "45%", delay: 0.8 },
  { Icon: ShieldCheck, x: "5%", y: "50%", delay: 1.2 },
];

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.12, delayChildren: 0.3 },
  },
};

const item = {
  hidden: { opacity: 0, y: 30 },
  show: { opacity: 1, y: 0, transition: { duration: 0.6, ease: "easeOut" } },
};

const HeroSection = () => {
  const navigate = useNavigate();

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-slate-950 pt-16">
      {/* Animated gradient mesh */}
      <div className="absolute inset-0 overflow-hidden">
        <motion.div
          className="absolute w-[600px] h-[600px] rounded-full opacity-20 blur-[120px]"
          style={{ background: "radial-gradient(circle, #3b82f6, transparent)", top: "-10%", left: "-5%" }}
          animate={{ x: [0, 60, 0], y: [0, 40, 0] }}
          transition={{ duration: 15, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.div
          className="absolute w-[500px] h-[500px] rounded-full opacity-15 blur-[120px]"
          style={{ background: "radial-gradient(circle, #8b5cf6, transparent)", bottom: "-10%", right: "-5%" }}
          animate={{ x: [0, -50, 0], y: [0, -60, 0] }}
          transition={{ duration: 18, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.div
          className="absolute w-[400px] h-[400px] rounded-full opacity-10 blur-[100px]"
          style={{ background: "radial-gradient(circle, #06b6d4, transparent)", top: "40%", left: "50%" }}
          animate={{ x: [0, 40, -30, 0], y: [0, -30, 20, 0] }}
          transition={{ duration: 20, repeat: Infinity, ease: "easeInOut" }}
        />
      </div>

      {/* Floating medical icons */}
      {floatingIcons.map(({ Icon, x, y, delay }, i) => (
        <motion.div
          key={i}
          className="absolute text-white/[0.06] hidden lg:block"
          style={{ left: x, top: y }}
          animate={{ y: [0, -15, 0] }}
          transition={{ duration: 4 + i * 0.5, repeat: Infinity, ease: "easeInOut", delay }}
        >
          <Icon className="w-8 h-8" />
        </motion.div>
      ))}

      {/* Content */}
      <div className="relative z-10 max-w-7xl mx-auto px-6 grid lg:grid-cols-2 gap-12 items-center">
        <motion.div variants={container} initial="hidden" animate="show">
          <motion.div variants={item} className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-white/10 bg-white/5 text-xs text-white/60 mb-6">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            AI-Powered Healthcare Platform
          </motion.div>

          <motion.h1 variants={item} className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white leading-tight mb-6">
            Your Health,{" "}
            <span className="bg-gradient-to-r from-blue-400 via-cyan-400 to-blue-500 bg-clip-text text-transparent animate-shimmer bg-[length:200%_auto]">
              Reimagined
            </span>
            <br />
            with AI
          </motion.h1>

          <motion.p variants={item} className="text-lg text-white/60 max-w-lg mb-8 leading-relaxed">
            Book appointments, chat with an AI medical assistant, and manage your entire health journey — all in one modern platform built for patients and doctors.
          </motion.p>

          <motion.div variants={item} className="flex flex-wrap gap-4">
            <button
              onClick={() => navigate("/patient/auth")}
              className="relative px-6 py-3 bg-gradient-to-r from-blue-500 to-cyan-500 text-white font-medium rounded-xl hover:shadow-lg hover:shadow-blue-500/25 transition-all duration-300 hover:-translate-y-0.5"
            >
              Get Started as Patient
            </button>
            <button
              onClick={() => navigate("/doctor/auth")}
              className="px-6 py-3 border border-white/15 text-white/90 font-medium rounded-xl hover:bg-white/5 transition-all duration-300 hover:-translate-y-0.5"
            >
              Join as Doctor
            </button>
          </motion.div>
        </motion.div>

        {/* Chat mockup */}
        <motion.div
          className="hidden lg:block"
          initial={{ opacity: 0, x: 40, rotateY: -5 }}
          animate={{ opacity: 1, x: 0, rotateY: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
        >
          <div className="relative">
            <div className="absolute -inset-4 bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-3xl blur-2xl" />
            <div className="relative bg-white/[0.05] border border-white/10 rounded-2xl p-6 backdrop-blur-sm">
              <div className="flex items-center gap-2 mb-4 pb-4 border-b border-white/10">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-cyan-400 flex items-center justify-center">
                  <Brain className="w-4 h-4 text-white" />
                </div>
                <div>
                  <p className="text-sm text-white font-medium">AI Health Assistant</p>
                  <p className="text-xs text-emerald-400">Online</p>
                </div>
              </div>
              <div className="space-y-3">
                <motion.div
                  className="bg-white/[0.05] rounded-xl rounded-tl-sm px-4 py-2.5 text-sm text-white/70 max-w-[80%]"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 1.0 }}
                >
                  Hello! I'm your AI health assistant. How can I help you today?
                </motion.div>
                <motion.div
                  className="bg-blue-500/20 rounded-xl rounded-tr-sm px-4 py-2.5 text-sm text-white/80 max-w-[80%] ml-auto"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 1.5 }}
                >
                  I've been having headaches lately
                </motion.div>
                <motion.div
                  className="bg-white/[0.05] rounded-xl rounded-tl-sm px-4 py-2.5 text-sm text-white/70 max-w-[85%]"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 2.0 }}
                >
                  I understand. Let me ask a few questions to help. How often do you experience these headaches, and where is the pain located?
                </motion.div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default HeroSection;
