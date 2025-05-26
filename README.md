# API Backend Lu Estilo

Esta é uma API RESTful desenvolvida com FastAPI para a Lu Estilo, facilitando a comunicação entre o time comercial, os clientes e a empresa.

## Funcionalidades

* **Autenticação & Autorização**:
    * Cadastro e login de usuários.
    * Autenticação baseada em JWT.
    * Atualização de token (Refresh Token).
    * Controle de acesso baseado em roles (`admin` e `regular`).
* **Gerenciamento de Clientes**:
    * Operações CRUD (Criar, Ler, Atualizar, Deletar) para clientes.
    * Paginação e filtros por nome e email para listagem de clientes.
    * Validação de email e CPF únicos.
* **Gerenciamento de Produtos**:
    * Operações CRUD para produtos.
    * Paginação e filtros por categoria, preço e disponibilidade.
    * Atributos do produto: descrição, valor de venda, código de barras, seção, estoque inicial, data de validade e imagens.
* **Gerenciamento de Pedidos**:
    * Operações CRUD para pedidos.
    * Criação de pedidos com múltiplos produtos, validando estoque disponível.
    * Filtros de pedidos por período, seção de produto, ID do pedido, status do pedido e cliente.
    * Atualização do status do pedido.
* **Integração com WhatsApp (Desafio Extra)**:
    * Funcionalidade para enviar mensagens automáticas via WhatsApp para clientes baseadas em eventos comerciais (novos pedidos, orçamentos, promoções). *(Nota: Esta funcionalidade requer configuração com um provedor de API do WhatsApp)*.
* **Banco de Dados**: PostgreSQL com SQLAlchemy ORM e Alembic para migrações de esquema.
* **Documentação da API**: Documentação interativa automática (Swagger UI e ReDoc) fornecida pelo FastAPI.
* **Testes**: Testes unitários e de integração usando Pytest.
* **Containerização**: Aplicação containerizada com Docker para fácil configuração e deploy.

## Tecnologias Utilizadas

* **Python 3.9+**
* **FastAPI**: Framework web para construção de APIs.
* **Uvicorn**: Servidor ASGI para FastAPI.
* **SQLAlchemy**: ORM para interação com o banco de dados.
* **PostgreSQL**: Banco de dados relacional.
* **Alembic**: Ferramenta para migrações de banco de dados com SQLAlchemy.
* **Pydantic**: Para validação de dados e schemas.
* **Psycopg2-binary**: Adaptador Python para PostgreSQL.
* **python-jose[cryptography]**: Para manipulação de JWT.
* **Passlib[bcrypt]**: Para hashing de senhas.
* **python-multipart**: Para processamento de dados de formulário (upload de arquivos, etc.).
* **python-dotenv**: Para gerenciamento de variáveis de ambiente.
* **Httpx**: Cliente HTTP assíncrono (usado nos testes e pode ser usado para serviços externos).
* **Pytest**: Framework para testes automatizados.
* **Docker & Docker Compose**: Para containerização e orquestração.

## Pré-requisitos

* Docker instalado: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
* Docker Compose instalado (geralmente vem com o Docker Desktop).

## Configuração e Execução do Ambiente de Desenvolvimento

1.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/lu-estilo-api.git](https://github.com/seu-usuario/lu-estilo-api.git) # Substitua pela URL do seu repositório
    cd lu-estilo-api
    ```

2.  **Configure as Variáveis de Ambiente:**
    * Copie o arquivo `.env.example` para um novo arquivo chamado `.env` na raiz do projeto.
        ```bash
        cp .env.example .env
        ```
    * Abra o arquivo `.env` e edite as variáveis conforme necessário. As mais importantes para rodar localmente são:
        * `DATABASE_URL="postgresql://user:password@db:5432/lu_estilo_db"` (geralmente o padrão já funciona com o Docker Compose)
        * `SECRET_KEY="coloque_uma_chave_secreta_bem_forte_aqui"` (essencial para segurança do JWT)
        * `ALGORITHM="HS256"`
        * `ACCESS_TOKEN_EXPIRE_MINUTES=30`
        * (Opcional) `WHATSAPP_API_URL` e `WHATSAPP_API_TOKEN` se for configurar a integração.

3.  **Construa e Inicie os Contêineres com Docker Compose:**
    * No terminal, na raiz do projeto, execute:
        ```bash
        docker compose up --build -d
        ```
    * Este comando irá:
        * Construir a imagem Docker para a API (se ainda não existir ou se o `Dockerfile` mudou).
        * Iniciar um contêiner para o banco de dados PostgreSQL.
        * Iniciar um contêiner para o banco de dados de TESTE PostgreSQL.
        * Iniciar o contêiner da API.
        * O serviço da API está configurado para esperar o banco de dados principal estar pronto e então executar as migrações do Alembic (`alembic upgrade head`) antes de iniciar o servidor Uvicorn.
        * Se tabelas não for criadas executar `alembic upgrade head` && `alembic revision --autogenerate`
        * 
4.  **Acesse a Aplicação e a Documentação:**
    * A API estará rodando em: `http://localhost:8000`
    * Documentação Interativa (Swagger UI): `http://localhost:8000/api/v1/docs`
    * Documentação Alternativa (ReDoc): `http://localhost:8000/api/v1/redoc`

## Como Testar a Aplicação

Existem algumas formas de testar sua API:

### 1. Teste Manual com Swagger UI (Recomendado para Início)

1.  **Acesse a Documentação:** Vá para `http://localhost:8000/api/v1/docs`.
2.  **Autenticação (Exemplo com usuário admin):**
    * Primeiro, cadastre um usuário com a role "admin" se ainda não o fez:
        * Vá para a seção `Authentication`, expanda `POST /auth/register`.
        * Clique em "Try it out".
        * No corpo da requisição (Request body), coloque:
            ```json
            {
              "username": "admin_principal",
              "email": "admin@example.com",
              "password": "sua_senha_admin",
              "role": "admin"
            }
            ```
        * Clique em "Execute".
    * Agora, faça login com esse usuário admin:
        * Vá para `POST /auth/login` (ainda em `Authentication`).
        * Clique em "Try it out".
        * Nos campos `username` e `password` (form data), coloque as credenciais do seu usuário admin.
        * Clique em "Execute".
        * Na resposta, copie o valor do `access_token` (a string longa, sem as aspas).
    * Autorize o Swagger UI:
        * No topo da página do Swagger UI, clique no botão **"Authorize"** (verde, com um cadeado).
        * Na janela que abrir, na seção "BearerAuth (JWT)", no campo "Value", digite `Bearer ` (com espaço) e cole o `access_token` que você copiou.
        * Clique em "Authorize" e depois "Close". O cadeado no botão principal deve fechar.
3.  **Testando um Endpoint Protegido (Ex: Criar Cliente):**
    * Com o Swagger UI autorizado, vá para a seção `Clients`.
    * Expanda `POST /clients`.
    * Clique em "Try it out".
    * No "Request body", cole um JSON para o cliente (lembre-se de usar um CPF e email únicos se já cadastrou outros):
        ```json
        {
          "name": "Cliente Teste Docs",
          "email": "clientedocs@example.com",
          "cpf": "11122233344",
          "phone": "11988887777",
          "address": "Rua da Documentação, 123"
        }
        ```
    * Clique em "Execute". Você deve receber uma resposta `201 Created`.

### 2. Teste Manual com Insomnia (ou similar como Postman)

1.  **Registrar Usuário (se necessário) e Fazer Login:**
    * Crie uma requisição `POST` para `http://localhost:8000/api/v1/auth/register` (Body: JSON) para criar seu usuário (ex: admin).
    * Crie uma requisição `POST` para `http://localhost:8000/api/v1/auth/login` (Body: Form URL Encoded, com campos `username` e `password`).
    * Copie o `access_token` da resposta do login.
2.  **Testar Endpoints Protegidos:**
    * Crie uma nova requisição (ex: `POST http://localhost:8000/api/v1/clients`).
    * Na aba "Auth", selecione "Bearer Token".
    * No campo "TOKEN", cole o `access_token` copiado.
    * No campo "PREFIX", deixe `Bearer ` (com espaço).
    * Na aba "Body", selecione "JSON" e coloque o payload do cliente.
    * Envie a requisição.

### 3. Testes Automatizados com Pytest

1.  Certifique-se de que seus contêineres Docker estão rodando:
    ```bash
    docker compose ps
    ```
    (Todos devem estar `Up` ou `running (healthy)`).
2.  No terminal, na raiz do projeto, execute:
    ```bash
    docker compose exec api pytest
    ```
3.  Isso executará todos os testes definidos na pasta `tests/` dentro do contêiner da API. Observe a saída para ver quais testes passaram ou falharam.

### 4. (Opcional) Verificando o Banco de Dados Diretamente

1.  Acesse o `psql` dentro do contêiner do banco de dados principal:
    ```bash
    docker compose exec db psql -U user -d lu_estilo_db
    ```
    (A senha será `password`, conforme definido no `docker-compose.yml`, mas o `psql` pode não pedir se a conexão for local dentro do Docker).
2.  Dentro do `psql`, você pode executar comandos SQL:
    * `\dt` - Lista todas as tabelas (verifique se `users`, `clients`, `products`, `orders`, etc., foram criadas pelo Alembic).
    * `SELECT * FROM users;`
    * `SELECT * FROM products WHERE barcode = 'seu_codigo_de_barras_unico';`
    * `\q` - Para sair do `psql`.

## Endpoints da API

A lista completa de endpoints, com detalhes sobre os parâmetros, corpos de requisição e respostas esperadas, está disponível na documentação interativa:

* **Swagger UI**: `http://localhost:8000/api/v1/docs`
* **ReDoc**: `http://localhost:8000/api/v1/redoc`

