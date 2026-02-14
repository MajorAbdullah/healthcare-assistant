import Navbar from "@/components/landing/Navbar";
import HeroSection from "@/components/landing/HeroSection";
import FeaturesGrid from "@/components/landing/FeaturesGrid";
import DemoVideos from "@/components/landing/DemoVideos";
import HowItWorks from "@/components/landing/HowItWorks";
import AIShowcase from "@/components/landing/AIShowcase";
import StatsCounter from "@/components/landing/StatsCounter";
import PortalCards from "@/components/landing/PortalCards";
import CTASection from "@/components/landing/CTASection";
import Footer from "@/components/landing/Footer";

const Index = () => {
  return (
    <div className="bg-slate-950 min-h-screen">
      <Navbar />
      <HeroSection />
      <FeaturesGrid />
      <DemoVideos />
      <HowItWorks />
      <AIShowcase />
      <StatsCounter />
      <PortalCards />
      <CTASection />
      <Footer />
    </div>
  );
};

export default Index;
