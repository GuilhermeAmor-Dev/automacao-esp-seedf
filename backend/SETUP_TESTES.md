# 🛠️ Guia de Instalação e Testes do Projeto

Este guia assume que você só tem o **Visual Studio Code** instalado.\
Passos para configurar **backend** (FastAPI + PostgreSQL) e **frontend**
(React + Vite).

------------------------------------------------------------------------

## 1. Pré-requisitos Globais

### 🖥️ Programas

-   [Python 3.11+](https://www.python.org/downloads/)\
-   [PostgreSQL 15+](https://www.postgresql.org/download/)
    -   Lembre-se de anotar:
        -   usuário (ex.: `postgres`)\
        -   senha\
        -   nome do banco (ex.: `automacao_db`)\
-   [Node.js 18+](https://nodejs.org/) (vem com `npm`)\
-   [Git](https://git-scm.com/) --- já configurado no VSCode.

### 🔧 Extensões no VSCode

-   **Python** (ms-python.python)\
-   **Pylance** (ms-python.vscode-pylance)\
-   **SQLTools** (para explorar o banco se quiser)\
-   **Prettier** (opcional, para formatar JS/React)

------------------------------------------------------------------------

## 2. Backend (FastAPI + PostgreSQL)

### Instalar dependências

No terminal do VSCode, dentro da pasta do projeto:

``` bash
# criar ambiente virtual (Windows PowerShell)
python -m venv venv
.env\Scriptsctivate

# instalar pacotes necessários
pip install fastapi uvicorn sqlalchemy psycopg2-binary passlib[bcrypt] python-jose
```

### Banco de Dados

Crie o banco manualmente no PostgreSQL:

``` sql
CREATE DATABASE automacao_db;
```

### Rodar backend

``` bash
uvicorn backend.main:app --reload
```

Abra: <http://127.0.0.1:8000/docs> → interface Swagger.

------------------------------------------------------------------------

## 3. Frontend (React + Vite)

### Instalar dependências

No terminal, na pasta `frontend`:

``` bash
# instalar pacotes básicos
npm install

# garantir pacotes necessários
npm install react@18 react-dom@18 react-router-dom@6
npm install -D vite @vitejs/plugin-react
npm install axios
```

### Arquivo `.env`

Na raiz de `frontend/`, crie `.env`:

    VITE_API_BASE=http://127.0.0.1:8000

### Rodar frontend

``` bash
npm run dev
```

Acesse: <http://localhost:5173>.

------------------------------------------------------------------------

## 4. Testes

### Back-end (Swagger)

1.  `POST /users/` → criar usuário `diretor`.
2.  `POST /auth/token` → login → copiar token.
3.  **Authorize** → colar `Bearer <token>`.
4.  `GET /me` → deve retornar usuário.
5.  `GET /admin-only` → deve funcionar apenas para `diretor`.

### Front-end (React)

1.  Abrir <http://localhost:5173>.
2.  Logar com usuário criado no backend.
3.  Se sucesso → redireciona para `/home`.
4.  Testar cenários:
    -   Senha errada → deve mostrar erro.
    -   Usuário correto → deve ir para Home.

------------------------------------------------------------------------

## 5. Checklist de Instalação

✅ Python 3.11+\
✅ PostgreSQL (com banco criado)\
✅ Node.js 18+ (com npm)\
✅ VSCode + extensões (Python, Pylance, SQLTools, Prettier)\
✅ Pacotes do backend (`fastapi`, `uvicorn`, etc.)\
✅ Pacotes do frontend (`react`, `vite`, `axios`, etc.)

------------------------------------------------------------------------
