# Documentação - Testes

## Visão Geral
Os testes garantem que as funcionalidades atendam aos requisitos definidos no levantamento e validem a qualidade do sistema.

## Tipos de Testes
- Testes unitários
- Testes de integração
- Testes de desempenho
- Testes de usabilidade

## Ferramentas
- Postman (testes de API)
- Selenium / Cypress (testes de interface)
- JMeter (testes de carga)
- Planilhas de checklist manual

## Casos de Teste Iniciais
- Login válido/inválido
- Criação de novo ESP
- Exportação de documento PDF
- Controle de permissões por perfil (Arquiteto, Gerente, Diretor)

## Relatórios de Status
-  Testes unitários backend – pendente/em andamento/realizado
-  Testes de usabilidade – pendente/em andamento/realizado
-  Testes de desempenho – pendente/em andamento/realizado

## Observações
- Documentar bugs encontrados e linkar issues no GitHub.
---------------------------------------------------------------------------------------------------------------------------------------

Exemplo base:
# Diário de Testes

## DIA: 04/09/2025
### Responsável:
Henrique Barbosa

### Atividade Realizada:
- Criados **5 casos de teste iniciais** para autenticação:
  1. Login válido
  2. Login inválido (senha errada)
  3. Usuário inexistente
  4. Campo vazio
  5. Permissão de acesso conforme perfil (Arquiteto/Gerente/Diretor)

### Situação:
- [ ] Em andamento  
- Aguardando backend liberar endpoint de login para execução prática.

### Observações:
- Testes documentados em planilha.
- Próxima etapa: expandir casos para exportação de ESP.
---------------------------------------------------------------------------------------------------------------------------------------

