import { motion, useInView } from "framer-motion";
import { useRef, useEffect, useState } from "react";
import { Clock, Zap, Server, Lock } from "lucide-react";

function useCountUp(target: number, inView: boolean, duration = 2000) {
  const [count, setCount] = useState(0);
  useEffect(() => {
    if (!inView) return;
    let start = 0;
    const startTime = performance.now();
    const step = (now: number) => {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setCount(Math.floor(eased * target));
      if (progress < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }, [inView, target, duration]);
  return count;
}

const stats = [
  { icon: Clock, value: 24, suffix: "/7", label: "AI Availability", prefix: "" },
  { icon: Zap, value: 2, suffix: " min", label: "Average Booking Time", prefix: "< " },
  { icon: Server, value: 99.9, suffix: "%", label: "Platform Uptime", prefix: "" },
  { icon: Lock, value: 256, suffix: "-bit", label: "Data Encryption", prefix: "" },
];

const StatsCounter = () => {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: "-100px" });

  return (
    <section className="py-20 bg-slate-950/50">
      <div className="max-w-6xl mx-auto px-6" ref={ref}>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
          {stats.map((stat, i) => {
            const count = useCountUp(
              stat.value === 99.9 ? 999 : stat.value,
              inView
            );
            const display = stat.value === 99.9
              ? (count / 10).toFixed(1)
              : count;

            return (
              <motion.div
                key={stat.label}
                className="text-center"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.1 }}
              >
                <div className="w-12 h-12 mx-auto rounded-xl bg-white/[0.05] border border-white/[0.08] flex items-center justify-center mb-3">
                  <stat.icon className="w-5 h-5 text-blue-400" />
                </div>
                <div className="text-3xl sm:text-4xl font-bold text-white mb-1">
                  {stat.prefix}{display}{stat.suffix}
                </div>
                <p className="text-sm text-white/40">{stat.label}</p>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default StatsCounter;
