1. O que você precisa instalar no computador

Antes de começar, precisamos instalar alguns programas:


Python 3.11 ou superior

Linguagem usada no backend (parte do servidor).

Baixe e instale.

Na instalação, marque a opção “Add Python to PATH”.

PostgreSQL (versão 15 ou superior)

É o banco de dados.

Baixe e instale.

Anote em algum lugar (IMPORTANTE):

Usuário (normalmente é postgres)

Senha que você escolher

Nome do banco (vamos usar automacao_db) <-- IMPORTAMTE -->

Node.js (versão 18 ou superior)

Necessário para rodar o frontend (parte visual).

Baixe e instale.

2. Extensões para o VSCode

Abra o VSCode, vá até a aba de Extensões (ícone de quadradinhos na esquerda) e instale:

Python (ms-python.python)

Pylance (ms-python.vscode-pylance)

SQLTools (para visualizar o banco, opcional)

Prettier (para formatar o código do frontend, opcional)

// AGORA IREMOS PARA OS TESTES 

PASSO 1 — Ativar ambiente virtual

// No VSCode, abra o terminal (atalho: Ctrl + aspas) e digite:

   python -m venv venv
.\venv\Scripts\activate



// Agora no começo da linha do terminal deve aparecer (venv) → isso significa que o ambiente está ativo.

PASSO 2 — Instalar bibliotecas do backend

// Com o ambiente ativo, digite:

    pip install fastapi uvicorn sqlalchemy psycopg2-binary passlib[bcrypt] python-jose

PASSO 3 — Criar o banco no PostgreSQL

// Abra o pgAdmin (vem junto com o PostgreSQL) ou use o terminal e rode:

    CREATE DATABASE automacao_db;

PASSO 4 — Rodar o backend

// Ainda no terminal:

    uvicorn backend.main:app --reload

// Se deu certo, deve aparecer no final:

// Application startup complete.


    Agora abra o navegador e vá até http://127.0.0.1:8000/docs.

// Você verá a documentação automática da API.

4. Preparando o Frontend (React + Vite)

PASSO 1 — Entrar na pasta

// No terminal do VSCode:

    cd frontend

PASSO 2 — Instalar dependências

// Digite:
    npm install
    npm install react@18 react-dom@18 react-router-dom@6
    npm install -D vite @vitejs/plugin-react
    npm install axios

PASSO 3 — Criar o arquivo .env (ELE JÁ DEVE EXISTIR, CASO NÃO, CRIE)

// Dentro da pasta frontend, crie um arquivo chamado .env com este conteúdo:

    VITE_API_BASE=http://127.0.0.1:8000


// Isso serve para o frontend saber onde está o backend.

PASSO 4 — Rodar o frontend

// No terminal:

    npm run dev


// Se deu certo, vai aparecer algo assim:

Local:   http://localhost:5173/


// Abra esse endereço no navegador → vai carregar a tela de Login.

5. Testando o Sistema

PARTE 1 — Testando pelo Swagger (backend)

Abra http://127.0.0.1:8000/docs
.

> Crie um usuário diretor (POST /users/).

> Faça login (POST /auth/token) com esse usuário.

Deve retornar um access_token.

> Clique em Authorize no topo direito e cole Bearer <token>.

Agora:

> GET /me → retorna dados do usuário.

> GET /admin-only → só funciona para diretor.

PARTE 2 — Testando pelo Frontend

> Abra http://localhost:5173.

> Digite o mesmo usuário e senha criados no backend.

> Se login correto → redireciona para Home.

> Se senha errada → mostra mensagem de erro.

> O token JWT fica salvo no navegador (pode ver em DevTools → Application → Local Storage).

6. Checklist Final

Antes de rodar, confira se você tem:

✅ Python instalado e funcionando

✅ PostgreSQL instalado e banco criado (automacao_db)

✅ Node.js instalado (testar node -v no terminal)

✅ Pacotes instalados no backend

✅ Pacotes instalados no frontend

✅ .env criado no frontend

Se tudo estiver OK, o sistema roda sem erro 🚀