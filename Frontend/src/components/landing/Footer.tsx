import { motion } from "framer-motion";
import { Heart, Shield } from "lucide-react";
import { useNavigate } from "react-router-dom";

const Footer = () => {
  const navigate = useNavigate();

  return (
    <motion.footer
      className="bg-slate-950 border-t border-white/[0.06] py-12"
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5 }}
    >
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8 mb-10">
          {/* Brand */}
          <div className="sm:col-span-2 lg:col-span-1">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-blue-500 to-cyan-400 flex items-center justify-center">
                <Heart className="w-3.5 h-3.5 text-white" />
              </div>
              <span className="text-white font-semibold">HealthBuddy</span>
            </div>
            <p className="text-sm text-white/40 max-w-xs">
              Modern healthcare management powered by AI. Connecting patients and doctors seamlessly.
            </p>
          </div>

          {/* Product */}
          <div>
            <h4 className="text-sm font-medium text-white/70 mb-3">Product</h4>
            <ul className="space-y-2">
              <li><a href="#features" className="text-sm text-white/40 hover:text-white/70 transition-colors">Features</a></li>
              <li><a href="#how-it-works" className="text-sm text-white/40 hover:text-white/70 transition-colors">How It Works</a></li>
              <li><a href="#ai" className="text-sm text-white/40 hover:text-white/70 transition-colors">AI Assistant</a></li>
            </ul>
          </div>

          {/* Company */}
          <div>
            <h4 className="text-sm font-medium text-white/70 mb-3">Company</h4>
            <ul className="space-y-2">
              <li><span className="text-sm text-white/40">About</span></li>
              <li><span className="text-sm text-white/40">Contact</span></li>
              <li><span className="text-sm text-white/40">Careers</span></li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h4 className="text-sm font-medium text-white/70 mb-3">Legal</h4>
            <ul className="space-y-2">
              <li><span className="text-sm text-white/40">Privacy Policy</span></li>
              <li><span className="text-sm text-white/40">Terms of Service</span></li>
              <li>
                <button
                  onClick={() => navigate("/admin/auth")}
                  className="text-sm text-white/40 hover:text-white/70 transition-colors flex items-center gap-1"
                >
                  <Shield className="w-3 h-3" /> Admin Access
                </button>
              </li>
            </ul>
          </div>
        </div>

        <div className="pt-6 border-t border-white/[0.06] text-center">
          <p className="text-xs text-white/30">
            &copy; {new Date().getFullYear()} HealthBuddy. All rights reserved.
          </p>
        </div>
      </div>
    </motion.footer>
  );
};

export default Footer;
