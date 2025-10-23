from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from main import ALGORITHM, SECRET_KEY, oauth2_schema
from models import Usuario, db_user
from sqlalchemy.orm import Session, sessionmaker


def pegar_sessao():
    try:
        Session = sessionmaker(bind=db_user)
        session = Session()
        yield session
    finally:
        session.close()


def verificar_token(
    token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)
):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = dic_info.get("sub")
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Acesso Negado, verifique a validade do token"
        )

    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso inválido")
    return usuario
