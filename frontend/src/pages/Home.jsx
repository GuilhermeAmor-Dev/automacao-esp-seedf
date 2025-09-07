import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

export default function Home() {
  const navigate = useNavigate();
  const [me, setMe] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      navigate("/login");
      return;
    }
    api.get("/me")
      .then(res => setMe(res.data))
      .catch(() => {
        localStorage.removeItem("access_token");
        navigate("/login");
      });
  }, [navigate]);

  function logout() {
    localStorage.removeItem("access_token");
    navigate("/login");
  }

  return (
    <div style={{minHeight:'100vh',display:'grid',placeItems:'center',gap:12}}>
      <div>
        <h1 style={{textAlign:'center'}}>Bem-vindo ao sistema</h1>
        {me && (
          <p style={{textAlign:'center'}}>
            Usuário: <b>{me.username}</b> | Papel: <b>{me.role}</b>
          </p>
        )}
        <div style={{textAlign:'center',marginTop:12}}>
          <button onClick={logout} style={{padding:'8px 14px',borderRadius:8,border:'none',background:'#444',color:'#fff',cursor:'pointer'}}>
            Sair
          </button>
        </div>
      </div>
    </div>
  );
}
