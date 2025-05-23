# Sistema de Registro Criminal - Backend API

## Como rodar o backend

1. **Instale as dependências:**
   ```sh
   pip install -r requirements.txt
   pip install djangorestframework djangorestframework-simplejwt
   ```

2. **Aplique as migrações:**
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Crie um superusuário (opcional, para acessar o admin):**
   ```sh
   python manage.py createsuperuser
   ```

4. **Rode o servidor:**
   ```sh
   python manage.py runserver
   ```

## Endpoints principais

- Autenticação JWT:
  - `POST /api/token/` (usuário e senha)
  - `POST /api/token/refresh/`
- Dashboard: `GET /api/dashboard/`
- Atividade recente: `GET /api/atividade-recente/`
- Usuário logado: `GET /api/user/me/`
- Cidadãos: `GET /api/cidadaos/`, `POST /api/cidadaos/`, `GET /api/cidadaos/<id>/`, etc
- Registros: `GET /api/registros/`, `POST /api/registros/`, `GET /api/registros/<id>/`, etc
- Informações: `GET /api/info/`

## Como testar a API

1. **Obtenha um token JWT:**
   ```sh
   curl -X POST http://localhost:8000/api/token/ -H "Content-Type: application/json" -d '{"username": "seu_usuario", "password": "sua_senha"}'
   ```
   Guarde o campo `access` do JSON retornado.

2. **Faça requisições autenticadas:**
   ```sh
   curl -H "Authorization: Bearer SEU_TOKEN_AQUI" http://localhost:8000/api/dashboard/
   ```

3. **Acesse o admin:**
   - http://localhost:8000/admin/

4. **Explore outros endpoints:**
   - `/api/cidadaos/`, `/api/registros/`, `/api/atividade-recente/`, etc.

---

Se precisar de mais detalhes, consulte os arquivos em `core/` ou peça ajuda! 