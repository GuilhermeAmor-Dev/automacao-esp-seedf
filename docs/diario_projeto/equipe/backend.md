# Documentação - Backend

## Visão Geral
O backend é responsável pela lógica de negócio, autenticação de usuários, integração com banco de dados e exportação de documentos.

## Tecnologias Utilizadas
- Linguagem: Python / Node.js
- Framework: Django ou Express.js
- Banco de Dados: PostgreSQL (Web) / SQLite (Desktop)
- Segurança: AES, SHA-256
- Versionamento: Git + GitHub

## Arquitetura
- Módulo de autenticação
- Módulo de criação de ESP
- Módulo de exportação (PDF/DOCX)
- Módulo de histórico e logs

## Endpoints / APIs
- `POST /login`
- `POST /esp/criar`
- `GET /esp/{id}`
- `PUT /esp/{id}`
- `DELETE /esp/{id}`

## Entregas e Status
-  Configuração inicial do ambiente
-  Integração com banco de dados
-  Implementação de autenticação
-  Exportação de documentos

## Observações
- Verificar performance em múltiplos acessos simultâneos.
---------------------------------------------------------------------------------------------------------------------------------------


Exemplo base:
# Diário do Backend

## DIA: 04/09/2025
### Responsável:
Marcos Adriano

### Atividade Realizada:
- Concluída a modelagem inicial do banco de dados.
- Criadas 4 tabelas principais:
  1. **usuarios** – controle de login, senha, perfil.
  2. **esp_items** – cadastro dos itens do caderno de especificações.
  3. **historico** – registro de versões exportadas.
  4. **log_auditoria** – controle de todas as alterações (insert, update, delete).

### Situação:
- [x] Concluído  
- Liberado para testes de integração.

### Observações:
- Estrutura atende aos requisitos levantados.
- Sugestão: validar relacionamento entre `esp_items` e `historico` com a equipe de testes antes de popular com dados.
---------------------------------------------------------------------------------------------------------------------------------------

