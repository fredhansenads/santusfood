# Santusfood — Guia de estudo

Este documento resume a preparação inicial do sistema de delivery Santusfood. Ele registra as decisões tomadas, os comandos executados, os problemas encontrados e o motivo de cada configuração.

## 1. Objetivo do projeto

Construir, como exercício de aprendizado, um sistema web de delivery para um restaurante.

O projeto será desenvolvido principalmente com Python. O navegador ainda utilizará HTML, CSS e, quando necessário, JavaScript.

### Funcionalidades planejadas para o MVP

#### Cliente

- Visualizar categorias e produtos.
- Adicionar produtos ao carrinho.
- Alterar quantidades.
- Informar dados pessoais e endereço.
- Escolher uma forma de pagamento.
- Criar e acompanhar um pedido.

#### Administrador

- Autenticar-se no painel.
- Cadastrar categorias e produtos.
- Definir preços e disponibilidade.
- Visualizar pedidos.
- Atualizar o status dos pedidos.

### Funcionalidades deixadas para etapas posteriores

- Aplicativo mobile nativo.
- Múltiplos restaurantes.
- Cupons e fidelidade.
- Rastreamento do entregador.
- Pagamentos reais.
- Integração com WhatsApp.
- Avaliações.

## 2. Tecnologias escolhidas

- Python 3.14.5
- Django 5.2.17 LTS
- PostgreSQL 18.3
- Psycopg 3.3.4
- python-dotenv 1.2.2
- Git 2.53.0
- Visual Studio Code
- Extensões Python e Pylance, da Microsoft

O Django foi escolhido porque já oferece ORM, migrações, autenticação, segurança, formulários, templates e painel administrativo.

## 3. Arquitetura inicial

```text
Navegador
   ↓
HTML + CSS + JavaScript
   ↓
Django
   ↓
Django ORM
   ↓
PostgreSQL
```

O navegador envia requisições ao Django. O Django executa as regras de negócio e utiliza o ORM para conversar com o PostgreSQL.

## 4. Regras de negócio definidas

1. O backend calculará subtotal, taxa de entrega e total.
2. O sistema nunca confiará no preço enviado pelo navegador.
3. Produtos indisponíveis não poderão entrar em novos pedidos.
4. Um item de pedido guardará o nome e o preço praticados no momento da compra.
5. Alterar um produto não modificará pedidos antigos.
6. Mudanças de status deverão seguir uma sequência válida.
7. Valores monetários utilizarão `Decimal`, nunca `float`.
8. Os dados serão validados no formulário e no backend.

Guardar o preço no item do pedido é importante. Consultar apenas `order_item.product.price` faria pedidos antigos mudarem quando o preço atual do produto fosse alterado.

## 5. Verificação das ferramentas

Foram executados:

```powershell
python --version
python -m pip --version
git --version
psql --version
```

Usar `python -m pip` garante que o `pip` pertence ao mesmo interpretador chamado por `python`.

O PostgreSQL estava instalado e funcionando, mas `psql` não estava inicialmente no `PATH`.

### Diagnóstico do PostgreSQL

```powershell
Get-ChildItem "C:\Program Files\PostgreSQL" -ErrorAction SilentlyContinue
Get-Service | Where-Object { $_.Name -like "postgresql*" }
```

Os comandos confirmaram:

- Instalação em `C:\Program Files\PostgreSQL\18`.
- Serviço `postgresql-x64-18` em execução.

### Inclusão temporária do psql no PATH

```powershell
$env:Path += ";C:\Program Files\PostgreSQL\18\bin"
```

Essa mudança vale somente para a sessão atual do PowerShell. A pasta também foi adicionada permanentemente ao `Path` pelas configurações de variáveis de ambiente do Windows.

## 6. Teste do PostgreSQL

A conexão administrativa foi testada com:

```powershell
psql -U postgres -h localhost -d postgres
```

- `-U postgres`: usuário administrativo.
- `-h localhost`: servidor local.
- `-d postgres`: banco administrativo padrão.

Dentro do `psql`, foram utilizados:

```sql
SELECT version();
```

```text
\conninfo
\q
```

Comandos iniciados por `\` pertencem ao `psql` e não são SQL.

### Advertência de codificação no Windows

O console utilizava a página de código 850, enquanto o Windows utilizava 1252. Isso poderia prejudicar a exibição de caracteres acentuados, mas não indicava falha no banco.

O ajuste utilizado foi:

```powershell
cmd.exe /c chcp 1252
```

## 7. Usuário e banco da aplicação

O Django não utilizará o superusuário `postgres`. Foi criado um usuário com permissões limitadas à aplicação.

Dentro do `psql`:

```sql
CREATE USER santusfood_user;
```

A senha foi definida sem escrevê-la no comando:

```text
\password santusfood_user
```

O banco foi criado com o usuário da aplicação como proprietário:

```sql
CREATE DATABASE santusfood_db
    WITH
    OWNER = santusfood_user
    ENCODING = 'UTF8'
    TEMPLATE = template0;
```

A conexão foi testada com:

```powershell
psql -U santusfood_user -h localhost -d santusfood_db
```

E confirmada por:

```sql
SELECT current_user, current_database();
SHOW server_encoding;
```

Resultados esperados e obtidos:

- Usuário: `santusfood_user`
- Banco: `santusfood_db`
- Codificação: `UTF8`

## 8. Preparação do VS Code

A pasta aberta no VS Code é:

```text
C:\Users\PC-01\Documents\ChatGPT\Santusfood
```

O terminal integrado deve iniciar nessa mesma pasta. O VS Code é o editor; o ambiente virtual continua sendo responsável por isolar o Python e suas dependências.

O interpretador selecionado no VS Code é:

```text
.venv\Scripts\python.exe
```

## 9. Ambiente virtual

O ambiente foi criado com:

```powershell
python -m venv .venv
```

### Problema encontrado

A primeira criação foi interrompida durante o `ensurepip`, gerando `KeyboardInterrupt`. A pasta ficou incompleta: possuía `python.exe`, mas não `pip.exe` nem os scripts de ativação.

O caminho foi conferido antes da remoção:

```powershell
Resolve-Path .\.venv
```

Depois, somente o ambiente incompleto foi removido:

```powershell
Remove-Item -LiteralPath .\.venv -Recurse -Force
```

O ambiente foi criado novamente e concluído sem interrupção:

```powershell
python -m venv .venv
```

### Ativação

```powershell
.\.venv\Scripts\Activate.ps1
```

O prefixo `(.venv)` no terminal indica que o ambiente está ativo.

O interpretador foi verificado com:

```powershell
where.exe python
python --version
python -m pip --version
```

O primeiro resultado de `where.exe python` deve apontar para `.venv\Scripts\python.exe`.

## 10. Dependências Python

As dependências iniciais foram instaladas com:

```powershell
python -m pip install "Django>=5.2.8,<5.3" "psycopg[binary]>=3.2.13,<4"
```

- Django 5.2 foi mantido por ser uma versão LTS.
- O limite inferior garante compatibilidade com Python 3.14.
- O limite superior evita uma atualização principal inesperada.
- `psycopg[binary]` instala o driver PostgreSQL e seus componentes binários.

As versões foram verificadas com:

```powershell
python -m django --version
python -c "import psycopg; print(psycopg.__version__)"
```

Para carregar variáveis do arquivo `.env`, foi instalado:

```powershell
python -m pip install "python-dotenv>=1.1,<2"
```

O arquivo `requirements.txt` registra as versões exatas:

```text
Django==5.2.17
psycopg[binary]==3.3.4
python-dotenv==1.2.2
```

## 11. Criação do projeto Django

O projeto foi criado na pasta atual:

```powershell
python -m django startproject config .
```

- `python -m django`: usa o Django da `.venv`.
- `startproject`: cria um projeto.
- `config`: nome do pacote de configurações.
- `.`: usa a pasta atual como raiz.

Estrutura gerada:

```text
Santusfood/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```

### Função dos arquivos

- `manage.py`: executa comandos administrativos do Django.
- `config/__init__.py`: marca `config` como pacote Python.
- `config/settings.py`: configurações gerais.
- `config/urls.py`: roteador principal de URLs.
- `config/wsgi.py`: entrada para servidores WSGI.
- `config/asgi.py`: entrada para servidores ASGI.

No `manage.py`, esta linha informa onde estão as configurações:

```python
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
```

E esta linha entrega ao Django os argumentos do terminal:

```python
execute_from_command_line(sys.argv)
```

## 12. Arquivos ignorados pelo Git

Foi criado `.gitignore` na raiz com regras para não versionar:

- `.venv/`
- `.env`
- `__pycache__/`
- Arquivos Python compilados.
- Banco SQLite local.
- Imagens enviadas em `media/`.
- Resultado de `collectstatic` em `staticfiles/`.
- Configurações locais do VS Code.
- Cobertura e cache de testes.
- Arquivos específicos do sistema operacional.

### Problema encontrado no .gitignore

O Python 3.14 havia criado automaticamente um `.gitignore` dentro da `.venv` contendo `*`. O arquivo foi movido acidentalmente para a raiz, fazendo o Git ignorar todo o projeto.

A regra `*` foi removida. Depois disso, `git status` voltou a mostrar corretamente os arquivos do projeto.

## 13. Variáveis de ambiente

Foi criado um `.env` local com a seguinte estrutura, sem versionar valores reais:

```dotenv
DJANGO_SECRET_KEY="valor-secreto"
DJANGO_DEBUG=True

DB_NAME="santusfood_db"
DB_USER="santusfood_user"
DB_PASSWORD="senha-secreta"
DB_HOST="localhost"
DB_PORT="5432"
```

A chave foi gerada com:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Também foi criado `.env.example`, que documenta as variáveis usando apenas valores fictícios.

## 14. Carregamento do .env no Django

No início de `config/settings.py`, foram adicionados:

```python
import os
from pathlib import Path

from dotenv import load_dotenv
```

Depois de definir `BASE_DIR`, o `.env` é carregado:

```python
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")
```

A chave secreta passou a vir obrigatoriamente do ambiente:

```python
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
```

Usar colchetes faz o sistema falhar imediatamente se a variável obrigatória estiver ausente.

O modo de depuração foi convertido de texto para booleano:

```python
DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() == "true"
```

Se a variável estiver ausente, o padrão seguro será `False`.

## 15. Configuração do PostgreSQL no Django

O bloco SQLite foi substituído por:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ["DB_HOST"],
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}
```

- `default` é a conexão principal.
- `ENGINE` seleciona PostgreSQL.
- Os dados sensíveis vêm do ambiente.
- A porta possui `5432` como padrão por não ser um segredo.

## 16. Verificação do Django

As configurações foram verificadas com:

```powershell
python manage.py check
```

Resultado:

```text
System check identified no issues (0 silenced).
```

Esse comando valida configurações, aplicativos e URLs, mas não executa migrações.

## 17. Preparação do primeiro commit

Os arquivos foram adicionados à área de preparação com `git add`. A área de preparação é a versão candidata ao próximo commit; ela não é o commit em si.

Depois de remover a chave do código, `settings.py` e `requirements.txt` foram adicionados novamente para atualizar suas versões preparadas.

A ausência de segredos na versão preparada foi verificada com:

```powershell
git show :config/settings.py | Select-String -Pattern "SECRET_KEY|DB_PASSWORD"
```

O resultado utiliza somente variáveis de ambiente:

```python
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
"PASSWORD": os.environ["DB_PASSWORD"],
```

O `.env` não aparece no `git status`, enquanto `.env.example` está preparado para versionamento.

## 18. Estado atual e próximo passo

Até este ponto:

- Python, Git e PostgreSQL estão funcionando.
- O banco e o usuário da aplicação foram criados.
- A `.venv` está ativa.
- Django, Psycopg e python-dotenv estão instalados.
- O projeto Django foi criado.
- O Django está configurado para PostgreSQL.
- Os segredos estão fora do código.
- `python manage.py check` foi concluído sem problemas.
- Os arquivos estão preparados para o primeiro commit.

O primeiro commit ainda não foi criado. Após revisar e adicionar este guia, a mensagem planejada é:

```powershell
git commit -m "chore: inicia projeto Django"
```

Depois do primeiro commit, o próximo assunto será a análise dos demais blocos de `settings.py`, seguida pelas migrações iniciais do Django.

## 19. Aplicação accounts e usuário personalizado

A aplicação de autenticação foi criada com:

```powershell
python manage.py startapp accounts
```

O modelo personalizado utiliza a implementação completa do Django:

```python
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass
```

Mesmo sem campos adicionais, essa classe permite evoluir o usuário sem trocar o modelo central depois que o banco estiver em uso.

A aplicação foi registrada em `INSTALLED_APPS`:

```python
"accounts.apps.AccountsConfig",
```

E o modelo principal de autenticação foi definido por:

```python
AUTH_USER_MODEL = "accounts.User"
```

A migração inicial foi gerada com:

```powershell
python manage.py makemigrations accounts
```

Antes de alterar o banco, foram executados:

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test accounts
python manage.py migrate --plan
```

O usuário personalizado também foi registrado no Django Admin usando `UserAdmin`, preservando os formulários, grupos e permissões do sistema de autenticação.

As migrações foram aplicadas ao PostgreSQL com:

```powershell
python manage.py migrate
```

Foram criadas as estruturas de `accounts`, `admin`, `auth`, `contenttypes` e `sessions`. Todas as operações terminaram com `OK`.

### Superusuário e validação do Admin

O superusuário foi criado de forma interativa para que a senha não aparecesse na conversa nem em arquivos:

```powershell
python manage.py createsuperuser
```

Depois da criação, o login foi testado em:

```text
http://127.0.0.1:8000/admin/
```

O painel exibiu o modelo personalizado `accounts.User`, confirmando que o registro com `UserAdmin` e a autenticação estavam funcionando.
