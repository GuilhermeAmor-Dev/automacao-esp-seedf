import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

export default function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading]   = useState(false);
  const [error, setError]       = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      // /auth/token espera x-www-form-urlencoded
      const form = new URLSearchParams();
      form.append("username", username);
      form.append("password", password);

      const { data } = await api.post("/auth/token", form, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });

      localStorage.setItem("access_token", data.access_token);
      navigate("/home");
    } catch (err) {
      setError("Usuário ou senha inválidos.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-lg p-8">
        <h2 className="text-3xl font-semibold text-center mb-6">Login</h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm mb-1">Usuário</label>
            <div className="flex items-center gap-2 border rounded-lg px-3 py-2">
              <span>👤</span>
              <input
                className="w-full outline-none"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Usuário"
                autoFocus
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-sm mb-1">Senha</label>
            <div className="flex items-center gap-2 border rounded-lg px-3 py-2">
              <span>🔒</span>
              <input
                className="w-full outline-none"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Senha"
                required
              />
            </div>
          </div>

          {error && <p className="text-red-600 text-sm">{error}</p>}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[#0d4a74] text-white rounded-lg py-2 font-medium hover:opacity-90 disabled:opacity-60"
          >
            {loading ? "Entrando..." : "Entrar"}
          </button>
        </form>

        <div className="text-center mt-4 space-y-1">
          <button className="text-sm text-gray-600 hover:underline" type="button">
            Esqueci minha senha
          </button>
          <div>
            <button className="text-sm text-gray-600 hover:underline" type="button">
              Cadastrar
            </button>
          </div>
        </div>

        <div className="mt-6 flex items-center justify-center gap-3">
          <img src="/logo-seedf-mini.png" alt="SEEDF" className="w-10 h-10" onError={(e)=>{e.currentTarget.style.display='none'}}/>
          <div className="text-xs text-gray-700">
            <div className="font-semibold">SECRETARIA DE EDUCAÇÃO</div>
            <div>GOVERNO DO DISTRITO FEDERAL</div>
          </div>
        </div>
      </div>
    </div>
  );
}
