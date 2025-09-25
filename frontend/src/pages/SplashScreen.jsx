import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function SplashScreen() {
  const navigate = useNavigate();

  useEffect(() => {
    const t = setTimeout(() => navigate("/login"), 2000);
    return () => clearTimeout(t);
  }, [navigate]);

  return (
    <div style={{
      minHeight:'100vh', display:'grid', placeItems:'center',
      background:'#0d4a74', color:'#fff', textAlign:'center'
    }}>
      <div>
        <div style={{
          width:96,height:96, background:'#f5c518', margin:'0 auto 24px',
          display:'grid',placeItems:'center',color:'#0d4a74',fontWeight:700
        }}>LOGO</div>
        <h1 style={{lineHeight:1.3}}>
          SISTEMA DE AUTOMAÇÃO<br/>DE ESP Nº SEEDF
        </h1>
        <div style={{
          margin:'24px auto', width:40, height:40,
          border:'4px solid rgba(255,255,255,.4)',
          borderTop:'4px solid #fff', borderRadius:'50%',
          animation:'spin 1s linear infinite'
        }}/>
        <style>{`@keyframes spin{to{transform:rotate(360deg)}}`}</style>
      </div>
    </div>
  );
}
