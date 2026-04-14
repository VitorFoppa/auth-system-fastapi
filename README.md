# FastAPI Auth System

Um sistema completo de autenticação desenvolvido com **FastAPI**, incluindo registro de usuários, verificação de e-mail via **Mailtrap**, login com **JWT (JSON Web Tokens)** e um frontend responsivo.

## Tecnologias Utilizadas

- **Backend:** FastAPI, SQLAlchemy, Pydantic, Python-jose (JWT).
- **Banco de Dados:** SQLite.
- **E-mail:** SMTP com Mailtrap (Background Tasks).
- **Frontend:** HTML5, Tailwind CSS e JavaScript (Fetch API).

## Funcionalidades

- [x] Registro de novos usuários com senha criptografada (Bcrypt).
- [x] Envio de e-mail de verificação em segundo plano.
- [x] Ativação de conta via link de token único.
- [x] Login seguro com geração de Token de Acesso.
- [x] Área logada (Dashboard) protegida.
- [x] Configuração de CORS para integração Frontend/Backend.

