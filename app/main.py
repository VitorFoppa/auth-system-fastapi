from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, security, database
from fastapi import BackgroundTasks
from .security import create_verification_token, SECRET_KEY, ALGORITHM
from .email import send_verification_email
from jose import JWTError, jwt
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user: schemas.UserCreate, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    hashed_pass = security.get_password_hash(user.password)

    new_user = models.User(
        email=user.email, 
        hashed_password=hashed_pass,
        is_verified=False 
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = security.create_verification_token(user.email)
    background_tasks.add_task(send_verification_email, user.email, token)
    
    return new_user

@app.get("/verify")
def verify_email(token: str, db: Session = Depends(database.get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        
        if email is None:
            raise HTTPException(status_code=400, detail="Token inválido")
            
    except JWTError:
        raise HTTPException(status_code=400, detail="Token inválido ou expirado")

    user = db.query(models.User).filter(models.User.email == email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if user.is_verified:
        return {"message": "Este e-mail já foi verificado anteriormente!"}

    user.is_verified = True
    db.commit()

    return {"message": f"Sucesso! O e-mail {email} foi verificado. Você já pode fazer login."}

@app.post("/login")
def login(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_data.email).first()
    
    if not user or not security.verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="E-mail ou senha incorretos"
        )
    
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Por favor, verifique seu e-mail no Mailtrap antes de fazer login."
        )

    access_token = security.create_verification_token(user.email)
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "message": "Login realizado com sucesso!"
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/users/me")
def read_users_me(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Sessão expirada")

    user = db.query(models.User).filter(models.User.email == email).first()
    return {"email": user.email, "id": user.id, "status": "Ativo"}