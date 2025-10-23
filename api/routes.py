# %%
from datetime import datetime, timedelta, timezone

from db import SessionLocal
from dependency import pegar_sessao, verificar_token
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from main import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, bcrypt_context
from models import Book, Usuario
from schemas_ import LoginSchema, UsuarioSchema, livrosSchema
from sqlalchemy.orm import Session

# %%
router_books = APIRouter(prefix="/api/v1", tags=["Tech Challenge FIAP"])

session = SessionLocal()


# session.close()


@router_books.get("/lista", response_model=list[livrosSchema])
async def livros():
    """Essa é a rota responsável por listar todos os livros disponíveis."""
    books = session.query(Book).filter(Book.id.isnot(None)).order_by(Book.id).all()
    return books


@router_books.post("/criar_usuario")
async def criar_conta(
    usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)
):
    """Essa é a rota responsável por criar um usuário para acessar a API."""
    usuario = (
        session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    )
    if usuario:
        raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado!")
    senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
    novo_usuario = Usuario(
        usuario_schema.nome,
        usuario_schema.email,
        senha_criptografada,
        usuario_schema.admin,
    )
    session.add(novo_usuario)
    session.commit()
    return {"mensagem": "User cadastrado com sucesso"}


def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario or not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario


def criar_token(
    id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_codificado


@router_books.post("/auth/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    """Essa é a rota responsável por realizar o login do usuário."""
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(
            status_code=400, detail="Usuário não encontrado ou credenciais inválidas"
        )
    acess_token = criar_token(usuario.id)
    refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
    return {
        "access_token": acess_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
    }


@router_books.post("/login_form")
async def login_form(
    dados_formulario: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(pegar_sessao),
):
    usuario = autenticar_usuario(
        dados_formulario.username, dados_formulario.password, session
    )
    if not usuario:
        raise HTTPException(
            status_code=400, detail="Usuário não encontrado ou credenciais inválidas"
        )
    acess_token = criar_token(usuario.id)

    return {"access_token": acess_token, "token_type": "bearer"}


@router_books.get("/auth/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    """Essa é a rota responsável por renovar o token."""
    access_token = criar_token(usuario.id)
    print(access_token)
    return {"access_token": access_token, "token_type": "Bearer"}


@router_books.get("/scraping/trigger")
async def ativar_raspagem(usuario: Usuario = Depends(verificar_token)):
    """Essa é a rota responsável por ativar o WebScapring que alimenta a API. Acesso exclusivo para administradores."""
    if not usuario.admin:
        raise HTTPException(
            status_code=403, detail="Apenas administradores podem ativar o scraping"
        )
    return {"mensagem": "Scraping iniciado com sucesso"}


@router_books.get("/books/{id}", response_model=livrosSchema)
async def busca_livro_id(id):
    """Essa é a rota responsável por pesquisar um livro por ID."""
    book = session.query(Book).filter(Book.id == id).first()
    if not book:
        raise HTTPException(status_code=404, detail="O ID especificado não existe!")
    return book
