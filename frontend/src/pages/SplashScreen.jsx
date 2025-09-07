import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function SplashScreen() {
  const navigate = useNavigate();

  useEffect(() => {
    const t = setTimeout(() => navigate("/login"), 2000);
    return () => clearTimeout(t);
  }, [navigate]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-[#0d4a74] text-white">
      {/* Substitua pelo seu logo em /public/logo-seedf.png */}
      <img src="/logo-seedf.png" alt="SEEDF" className="w-24 h-24 mb-8" onError={(e)=>{e.currentTarget.style.display='none'}}/>
      <h1 className="text-2xl md:text-3xl font-semibold text-center leading-tight">
        SISTEMA DE AUTOMAÇÃO<br/>DE ESP – SEEDF
      </h1>
      <div className="mt-10 w-10 h-10 border-4 border-white/40 border-t-white rounded-full animate-spin"/>
    </div>
  );
}
