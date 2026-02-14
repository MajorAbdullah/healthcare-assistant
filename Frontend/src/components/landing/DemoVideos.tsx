import { useState, useRef } from "react";
import { motion } from "framer-motion";

const tabs = [
  { id: "patient", label: "Patient Portal", file: "/videos/patient-demo.mp4" },
  { id: "doctor", label: "Doctor Portal", file: "/videos/doctor-demo.mp4" },
];

const DemoVideos = () => {
  const [activeTab, setActiveTab] = useState("patient");
  const [isPlaying, setIsPlaying] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);

  const activeVideo = tabs.find((t) => t.id === activeTab)!;

  const handlePlayPause = () => {
    if (!videoRef.current) return;
    if (videoRef.current.paused) {
      videoRef.current.play();
      setIsPlaying(true);
    } else {
      videoRef.current.pause();
      setIsPlaying(false);
    }
  };

  const handleTabChange = (id: string) => {
    setActiveTab(id);
    setIsPlaying(false);
  };

  return (
    <section id="demo" className="relative py-24 bg-slate-950">
      <div className="max-w-5xl mx-auto px-6">
        <motion.div
          className="text-center mb-12"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
        >
          <p className="text-sm text-blue-400 font-medium mb-2 uppercase tracking-wider">
            Demo
          </p>
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            See It In Action
          </h2>
          <p className="text-white/50 max-w-2xl mx-auto">
            Watch how patients and doctors use Health Buddy to streamline healthcare
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          {/* Tabs */}
          <div className="flex justify-center gap-2 mb-6">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => handleTabChange(tab.id)}
                className={`px-6 py-2.5 rounded-xl text-sm font-medium transition-all duration-300 ${
                  activeTab === tab.id
                    ? "bg-blue-500/20 text-blue-400 border border-blue-500/30"
                    : "text-white/50 hover:text-white/70 border border-transparent"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Video container */}
          <div className="relative rounded-2xl overflow-hidden border border-white/[0.06] bg-white/[0.03] shadow-2xl">
            <div
              className="relative cursor-pointer group"
              onClick={handlePlayPause}
            >
              <video
                ref={videoRef}
                key={activeVideo.file}
                className="w-full aspect-video bg-slate-900"
                muted
                playsInline
                onPlay={() => setIsPlaying(true)}
                onPause={() => setIsPlaying(false)}
                onEnded={() => setIsPlaying(false)}
              >
                <source src={activeVideo.file} type="video/mp4" />
              </video>

              {/* Play overlay */}
              {!isPlaying && (
                <div className="absolute inset-0 flex items-center justify-center bg-black/30 group-hover:bg-black/20 transition-colors">
                  <div className="w-16 h-16 sm:w-20 sm:h-20 rounded-full bg-blue-500/90 flex items-center justify-center group-hover:scale-110 transition-transform shadow-lg shadow-blue-500/30">
                    <svg
                      className="w-7 h-7 sm:w-8 sm:h-8 text-white ml-1"
                      fill="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path d="M8 5v14l11-7z" />
                    </svg>
                  </div>
                </div>
              )}
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default DemoVideos;
