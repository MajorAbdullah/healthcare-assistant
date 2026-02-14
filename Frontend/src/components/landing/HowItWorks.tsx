import { motion, useScroll, useTransform } from "framer-motion";
import { useRef } from "react";
import { UserPlus, CalendarCheck, MessageSquare, TrendingUp } from "lucide-react";

const steps = [
  {
    icon: UserPlus,
    title: "Create Account",
    description: "Sign up in seconds as a patient or doctor. Quick, secure, and hassle-free.",
  },
  {
    icon: CalendarCheck,
    title: "Book & Manage",
    description: "Browse available doctors, pick a time slot, and book your appointment instantly.",
  },
  {
    icon: MessageSquare,
    title: "Chat with AI",
    description: "Ask our AI assistant any health question and get informed, instant responses.",
  },
  {
    icon: TrendingUp,
    title: "Track & Improve",
    description: "Monitor your health journey with insights, analytics, and appointment history.",
  },
];

const HowItWorks = () => {
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start 0.8", "end 0.6"],
  });
  const pathLength = useTransform(scrollYProgress, [0, 1], [0, 1]);

  return (
    <section id="how-it-works" className="relative py-24 bg-slate-950/80">
      <div className="max-w-5xl mx-auto px-6" ref={ref}>
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
        >
          <p className="text-sm text-purple-400 font-medium mb-2 uppercase tracking-wider">How It Works</p>
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Get started in four simple steps
          </h2>
        </motion.div>

        <div className="relative">
          {/* Connecting line (desktop) */}
          <svg
            className="absolute top-10 left-0 right-0 w-full h-2 hidden md:block"
            viewBox="0 0 1000 2"
            preserveAspectRatio="none"
          >
            <motion.line
              x1="125" y1="1" x2="875" y2="1"
              stroke="url(#lineGrad)"
              strokeWidth="2"
              strokeLinecap="round"
              style={{ pathLength }}
            />
            <defs>
              <linearGradient id="lineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#3b82f6" />
                <stop offset="100%" stopColor="#8b5cf6" />
              </linearGradient>
            </defs>
          </svg>

          <div className="grid md:grid-cols-4 gap-8">
            {steps.map((step, i) => (
              <motion.div
                key={step.title}
                className="text-center"
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.15 }}
              >
                <motion.div
                  className="w-20 h-20 mx-auto rounded-2xl bg-gradient-to-br from-blue-500/10 to-purple-500/10 border border-white/10 flex items-center justify-center mb-4"
                  whileHover={{ scale: 1.1 }}
                  transition={{ type: "spring", stiffness: 300 }}
                >
                  <step.icon className="w-8 h-8 text-blue-400" />
                </motion.div>
                <div className="text-xs text-white/30 font-medium mb-1">Step {i + 1}</div>
                <h3 className="text-lg font-semibold text-white mb-2">{step.title}</h3>
                <p className="text-sm text-white/50 leading-relaxed">{step.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
