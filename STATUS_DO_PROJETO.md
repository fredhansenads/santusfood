# Santusfood — Status do projeto

Este arquivo é a fonte de acompanhamento do projeto. Ele registra o estado atual, as decisões já tomadas, o próximo passo autorizado e o trabalho que ainda falta. Deve ser atualizado ao final de cada etapa relevante.

Última atualização: 14/08/2026

## Forma de trabalho

- O projeto tem finalidade de aprendizado.
- O aluno cria os arquivos, escreve o código e executa os comandos.
- Cada passo deve ser apresentado separadamente e explicado antes da execução.
- O assistente só altera arquivos quando houver pedido explícito.
- Senhas, chaves e conteúdo real do `.env` nunca devem ser exibidos ou versionados.
- Antes de cada commit, revisar `git status` e o conteúdo preparado.

## Estado atual

### Ambiente

- [x] Python 3.14.5 instalado.
- [x] Git 2.53.0 instalado.
- [x] PostgreSQL 18.3 instalado.
- [x] Serviço `postgresql-x64-18` em execução.
- [x] `psql` disponível no `PATH`.
- [x] VS Code escolhido como editor.
- [x] Ambiente virtual `.venv` criado e validado.
- [x] Interpretador da `.venv` selecionado no VS Code.

### Banco de dados

- [x] Usuário `santusfood_user` criado.
- [x] Banco `santusfood_db` criado.
- [x] `santusfood_user` definido como proprietário do banco.
- [x] Codificação `UTF8` confirmada.
- [x] Conexão do usuário da aplicação testada.
- [ ] Migrações iniciais executadas.

### Dependências

- [x] Django 5.2.17 instalado.
- [x] Psycopg 3.3.4 instalado.
- [x] python-dotenv 1.2.2 instalado.
- [x] Versões registradas em `requirements.txt`.

### Projeto Django

- [x] Projeto `config` criado.
- [x] Função do `manage.py` estudada.
- [x] Função dos arquivos de `config/` apresentada.
- [x] `.env` carregado por `python-dotenv`.
- [x] `SECRET_KEY` removida do código-fonte.
- [x] `DEBUG` configurado por variável de ambiente.
- [x] PostgreSQL configurado em `DATABASES`.
- [x] `python manage.py check` executado sem problemas.
- [ ] Demais blocos de `settings.py` estudados.
- [ ] Aplicação `accounts` criada.
- [ ] Modelo personalizado de usuário criado.
- [ ] `AUTH_USER_MODEL` configurado.

### Segurança e configuração local

- [x] `.gitignore` criado.
- [x] `.venv/` ignorada.
- [x] `.env` ignorado.
- [x] `.env.example` criado com valores fictícios.
- [x] Ausência de chave e senha reais na área de preparação verificada.
- [ ] Configuração de `ALLOWED_HOSTS` por ambiente.
- [ ] Configurações de segurança para produção.

### Git e documentação

- [x] Repositório Git inicializado.
- [x] Primeiro commit criado: `cb0d67b chore: inicio projeto Django`.
- [x] Árvore de trabalho confirmada como limpa após o commit.
- [x] `GUIA_DE_ESTUDO.md` criado e incluído no primeiro commit.
- [x] `STATUS_DO_PROJETO.md` criado e aprovado.
- [ ] Estratégia de branches definida, se necessária.
- [ ] Repositório remoto configurado, se desejado.

## Próximo passo

Criar a aplicação `accounts` antes da primeira migração:

```powershell
python manage.py startapp accounts
```

Motivo: o projeto utilizará um modelo personalizado de usuário. Defini-lo antes das migrações iniciais evita alterações complexas nas relações de autenticação e no banco de dados.

Depois da criação, a sequência imediata será:

1. Examinar cada arquivo gerado em `accounts/`.
2. Implementar o modelo personalizado com base em `AbstractUser`.
3. Registrar `accounts` em `INSTALLED_APPS`.
4. Configurar `AUTH_USER_MODEL`.
5. Executar `python manage.py check`.
6. Criar e revisar as migrações.
7. Aplicar as migrações ao PostgreSQL.
8. Criar um commit da etapa.

## Roadmap do MVP

### Fase 1 — Fundação

- [x] Definir stack e arquitetura.
- [x] Preparar Python, PostgreSQL, VS Code e Git.
- [x] Criar projeto Django.
- [x] Configurar variáveis de ambiente.
- [x] Conectar configurações ao PostgreSQL.
- [ ] Criar modelo personalizado de usuário.
- [ ] Executar migrações iniciais.
- [ ] Criar superusuário administrativo.
- [ ] Testar acesso ao Django Admin.

### Fase 2 — Contas e clientes

- [ ] Definir campos e regras do usuário.
- [ ] Implementar autenticação.
- [ ] Criar perfil de cliente.
- [ ] Criar endereços de entrega.
- [ ] Validar telefone, CEP e campos obrigatórios.
- [ ] Criar testes de contas e endereços.

### Fase 3 — Catálogo

- [ ] Criar aplicação `catalog`.
- [ ] Criar modelo `Category`.
- [ ] Criar modelo `Product`.
- [ ] Configurar imagens de produtos.
- [ ] Configurar disponibilidade e ordenação.
- [ ] Registrar catálogo no Django Admin.
- [ ] Criar cardápio público.
- [ ] Criar página de detalhes do produto.
- [ ] Criar testes do catálogo.

### Fase 4 — Carrinho

- [ ] Definir estratégia de carrinho por sessão.
- [ ] Adicionar produto.
- [ ] Alterar quantidade.
- [ ] Remover produto.
- [ ] Calcular subtotal.
- [ ] Impedir produtos indisponíveis.
- [ ] Criar testes do carrinho.

### Fase 5 — Entrega e checkout

- [ ] Criar áreas e taxas de entrega.
- [ ] Validar endereço atendido.
- [ ] Criar fluxo de checkout.
- [ ] Revisar dados do cliente.
- [ ] Escolher forma de pagamento.
- [ ] Calcular o total exclusivamente no backend.
- [ ] Criar testes de checkout.

### Fase 6 — Pedidos

- [ ] Criar aplicação `orders`.
- [ ] Criar modelos `Order` e `OrderItem`.
- [ ] Salvar nome e preço históricos nos itens.
- [ ] Definir estados válidos do pedido.
- [ ] Criar pedido de forma transacional.
- [ ] Criar acompanhamento para o cliente.
- [ ] Criar gerenciamento pelo restaurante.
- [ ] Criar testes de pedidos e transições de estado.

### Fase 7 — Pagamentos

- [ ] Implementar dinheiro na entrega.
- [ ] Implementar cartão na entrega.
- [ ] Criar PIX simulado.
- [ ] Modelar registros de pagamento.
- [ ] Criar testes de pagamento.
- [ ] Deixar integração real para etapa posterior.

### Fase 8 — Interface

- [ ] Criar template base.
- [ ] Configurar CSS e arquivos estáticos.
- [ ] Criar cabeçalho e navegação.
- [ ] Tornar cardápio responsivo.
- [ ] Criar telas de carrinho e checkout.
- [ ] Criar acompanhamento do pedido.
- [ ] Melhorar acessibilidade e mensagens de erro.

### Fase 9 — Qualidade e segurança

- [ ] Adicionar validações de entrada.
- [ ] Revisar permissões administrativas.
- [ ] Impedir alteração indevida de pedidos.
- [ ] Adicionar tratamento de erros.
- [ ] Aumentar cobertura de testes.
- [ ] Configurar logs.
- [ ] Revisar CSRF, cookies e sessões.
- [ ] Executar checklist de implantação do Django.

### Fase 10 — Publicação

- [ ] Escolher hospedagem.
- [ ] Criar banco de produção.
- [ ] Configurar variáveis de produção.
- [ ] Configurar `ALLOWED_HOSTS`.
- [ ] Configurar arquivos estáticos e mídia.
- [ ] Configurar HTTPS.
- [ ] Executar migrações de produção.
- [ ] Configurar backup e monitoramento.
- [ ] Realizar teste final do fluxo completo.

## Decisões técnicas já tomadas

- Backend e renderização inicial com Django.
- Templates Django antes de considerar React ou outro frontend separado.
- PostgreSQL como banco desde o início.
- Psycopg 3 como driver.
- Configurações sensíveis em `.env`.
- Valores monetários com `Decimal`.
- Um restaurante no MVP.
- Pagamentos reais fora da primeira versão.
- Modelo personalizado de usuário antes das primeiras migrações.
- Aplicações Django separadas por domínio funcional.

## Cuidados permanentes

- Nunca compartilhar ou versionar `.env`.
- Nunca usar o superusuário `postgres` na aplicação.
- Nunca calcular o valor final apenas no navegador.
- Nunca utilizar `float` para dinheiro.
- Nunca alterar migrações já aplicadas sem entender o impacto.
- Nunca executar `git add .` sem revisar `git status`.
- Atualizar este arquivo quando uma etapa for concluída ou o plano mudar.
