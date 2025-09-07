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
    <div className="min-h-screen flex flex-col items-center justify-center gap-4">
      <h1>Bem-vindo ao sistema</h1>
      {me && <p>Usuário: <b>{me.username}</b> | Papel: <b>{me.role}</b></p>}
      <button onClick={logout} className="px-4 py-2 rounded bg-gray-800 text-white">Sair</button>
    </div>
  );
}
