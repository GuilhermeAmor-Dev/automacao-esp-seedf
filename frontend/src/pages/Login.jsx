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
    <div style={{minHeight:'100vh',display:'grid',placeItems:'center',background:'#f6f6f6',padding:16}}>
      <div style={{width:380,maxWidth:'100%',background:'#fff',padding:24,borderRadius:16,boxShadow:'0 10px 30px rgba(0,0,0,.1)'}}>
        <h2 style={{textAlign:'center',marginBottom:16,fontSize:28}}>Login</h2>

        <form onSubmit={handleSubmit} style={{display:'grid',gap:12}}>
          <label>
            <div style={{fontSize:12,marginBottom:4}}>Usuário</div>
            <div style={{display:'flex',gap:8,border:'1px solid #ddd',borderRadius:10,padding:'8px 12px'}}>
              <span aria-hidden="true" style={{fontSize:16}}>👤</span>
              <input
                style={{border:'none',outline:'none',flex:1}}
                value={username}
                onChange={(e)=>setUsername(e.target.value)}
                placeholder="Usuário"
                required
                autoFocus
              />
            </div>
          </label>

          <label>
            <div style={{fontSize:12,marginBottom:4}}>Senha</div>
            <div style={{display:'flex',gap:8,border:'1px solid #ddd',borderRadius:10,padding:'8px 12px'}}>
              <span aria-hidden="true" style={{fontSize:16}}>🔒</span>
              <input
                type="password"
                style={{border:'none',outline:'none',flex:1}}
                value={password}
                onChange={(e)=>setPassword(e.target.value)}
                placeholder="Senha"
                required
              />
            </div>
          </label>

          {error && <div style={{color:'#c62828',fontSize:13}}>{error}</div>}

          <button
            type="submit"
            disabled={loading}
            style={{
              width:'100%',background:'#0d4a74',color:'#fff',border:'none',
              borderRadius:10,padding:'10px 12px',fontWeight:600, cursor:'pointer',
              opacity: loading ? .6 : 1
            }}
          >
            {loading ? "Entrando..." : "Entrar"}
          </button>
        </form>

        <div style={{textAlign:'center',marginTop:12}}>
          <button style={{fontSize:13,color:'#555',background:'none',border:'none',cursor:'pointer'}}>Esqueci minha senha</button>
          <div>
            <button style={{fontSize:13,color:'#555',background:'none',border:'none',cursor:'pointer'}}>Cadastrar</button>
          </div>
        </div>

        <div style={{marginTop:16,display:'flex',gap:12,alignItems:'center',justifyContent:'center'}}>
          <div style={{width:40,height:40,background:'#0d4a74',borderRadius:6}}/>
          <div style={{fontSize:12,color:'#444'}}>
            <div style={{fontWeight:700}}>SECRETARIA DE EDUCAÇÃO</div>
            <div>GOVERNO DO DISTRITO FEDERAL</div>
          </div>
        </div>
      </div>
    </div>
  );
}
