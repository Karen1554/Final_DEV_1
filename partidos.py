from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Partido

router = APIRouter()

@router.post("/", response_model=Partido)
def crear_partido(partido: Partido, session: Session = Depends(get_session)):
    partido.determinar_resultado()
    session.add(partido)
    session.commit()
    session.refresh(partido)
    return partido

@router.get("/", response_model=list[Partido])
def listar_partidos(session: Session = Depends(get_session)):
    return session.exec(select(Partido)).all()

@router.get("/{partido_id}", response_model=Partido)
def obtener_partido(partido_id: int, session: Session = Depends(get_session)):
    partido = session.get(Partido, partido_id)
    if not partido:
        raise HTTPException(404, "Partido no encontrado")
    return partido

@router.put("/{partido_id}", response_model=Partido)
def actualizar_partido(partido_id: int, data: Partido, session: Session = Depends(get_session)):
    partido = session.get(Partido, partido_id)
    if not partido:
        raise HTTPException(404, "Partido no encontrado")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(partido, key, value)

    partido.determinar_resultado()
    session.commit()
    session.refresh(partido)
    return partido

@router.delete("/{partido_id}")
def eliminar_partido(partido_id: int, session: Session = Depends(get_session)):
    partido = session.get(Partido, partido_id)
    if not partido:
        raise HTTPException(404, "Partido no encontrado")

    session.delete(partido)
    session.commit()
    return {"message": "Partido eliminado"}
