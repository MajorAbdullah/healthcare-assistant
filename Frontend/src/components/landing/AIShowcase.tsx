import { motion } from "framer-motion";
import { Brain, CheckCircle2, Sparkles, Clock, ShieldCheck } from "lucide-react";

const features = [
  { icon: Sparkles, text: "Intelligent symptom analysis and health guidance" },
  { icon: Clock, text: "Available 24/7 — no waiting rooms or hold times" },
  { icon: ShieldCheck, text: "Private and secure health conversations" },
  { icon: CheckCircle2, text: "Helps you prepare for doctor appointments" },
];

const chatMessages = [
  { role: "ai", text: "Hi! I'm here to help with any health questions. What's on your mind?" },
  { role: "user", text: "I've been feeling tired and having trouble sleeping" },
  { role: "ai", text: "I'm sorry to hear that. Fatigue and sleep issues can be connected. Let me ask — how many hours of sleep are you getting, and do you consume caffeine late in the day?" },
  { role: "user", text: "About 5-6 hours, and yes I drink coffee around 4pm" },
  { role: "ai", text: "That helps! Late caffeine and insufficient sleep often go hand-in-hand. I'd recommend cutting caffeine after 2pm and aiming for 7-8 hours. Would you like me to help book an appointment if symptoms persist?" },
];

const AIShowcase = () => {
  return (
    <section id="ai" className="relative py-24 bg-slate-950">
      <div className="max-w-7xl mx-auto px-6 grid lg:grid-cols-2 gap-16 items-center">
        {/* Left: Feature list */}
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <p className="text-sm text-cyan-400 font-medium mb-2 uppercase tracking-wider">AI Assistant</p>
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Meet your personal health AI
          </h2>
          <p className="text-white/50 mb-8 leading-relaxed">
            Our AI assistant uses advanced language models to understand your symptoms, answer health questions, and guide you toward better healthcare decisions.
          </p>
          <div className="space-y-4">
            {features.map((f, i) => (
              <motion.div
                key={i}
                className="flex items-start gap-3"
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: i * 0.1 }}
              >
                <div className="w-8 h-8 rounded-lg bg-cyan-500/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <f.icon className="w-4 h-4 text-cyan-400" />
                </div>
                <p className="text-white/70 text-sm">{f.text}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Right: Chat mockup */}
        <motion.div
          initial={{ opacity: 0, x: 30 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <div className="relative">
            <div className="absolute -inset-6 bg-gradient-to-r from-cyan-500/10 to-blue-500/10 rounded-3xl blur-2xl" />
            <div className="relative bg-white/[0.03] border border-white/[0.08] rounded-2xl overflow-hidden">
              {/* Header */}
              <div className="flex items-center gap-3 px-5 py-3 border-b border-white/[0.06] bg-white/[0.02]">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-cyan-500 to-blue-500 flex items-center justify-center">
                  <Brain className="w-4 h-4 text-white" />
                </div>
                <div>
                  <p className="text-sm text-white font-medium">AI Health Assistant</p>
                  <p className="text-[11px] text-emerald-400 flex items-center gap-1">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" /> Online
                  </p>
                </div>
              </div>

              {/* Messages */}
              <div className="p-4 space-y-3 max-h-[400px] overflow-y-auto">
                {chatMessages.map((msg, i) => (
                  <motion.div
                    key={i}
                    className={`${
                      msg.role === "ai"
                        ? "bg-white/[0.05] rounded-xl rounded-tl-sm max-w-[85%]"
                        : "bg-blue-500/15 rounded-xl rounded-tr-sm max-w-[75%] ml-auto"
                    } px-4 py-2.5`}
                    initial={{ opacity: 0, y: 10 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.4, delay: 0.4 + i * 0.2 }}
                  >
                    <p className="text-sm text-white/70">{msg.text}</p>
                  </motion.div>
                ))}
                {/* Typing indicator */}
                <motion.div
                  className="bg-white/[0.05] rounded-xl rounded-tl-sm px-4 py-3 w-16"
                  initial={{ opacity: 0 }}
                  whileInView={{ opacity: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: 1.6 }}
                >
                  <div className="flex gap-1">
                    {[0, 1, 2].map((d) => (
                      <motion.span
                        key={d}
                        className="w-1.5 h-1.5 rounded-full bg-white/40"
                        animate={{ opacity: [0.3, 1, 0.3] }}
                        transition={{ duration: 1.2, repeat: Infinity, delay: d * 0.2 }}
                      />
                    ))}
                  </div>
                </motion.div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default AIShowcase;
