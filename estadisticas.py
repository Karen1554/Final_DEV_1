from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Estadistica, Jugador, Partido

router = APIRouter()

@router.post("/", response_model=Estadistica)
def crear_estadistica(est: Estadistica, session: Session = Depends(get_session)):

    jugador = session.get(Jugador, est.jugador_id)
    if not jugador:
        raise HTTPException(404, "Jugador no existe")
    partido = session.get(Partido, est.partido_id)
    if not partido:
        raise HTTPException(404, "Partido no existe")

    session.add(est)
    session.commit()
    session.refresh(est)
    return est

@router.get("/", response_model=list[Estadistica])
def listar_estadisticas(session: Session = Depends(get_session)):
    return session.exec(select(Estadistica)).all()

# Obtener
@router.get("/{estadistica_id}", response_model=Estadistica)
def obtener_estadistica(estadistica_id: int, session: Session = Depends(get_session)):
    est = session.get(Estadistica, estadistica_id)
    if not est:
        raise HTTPException(404, "Estadística no encontrada")
    return est

@router.put("/{estadistica_id}", response_model=Estadistica)
def actualizar_estadistica(estadistica_id: int, data: Estadistica, session: Session = Depends(get_session)):
    est = session.get(Estadistica, estadistica_id)
    if not est:
        raise HTTPException(404, "Estadística no encontrada")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(est, key, value)

    session.commit()
    session.refresh(est)
    return est

@router.delete("/{estadistica_id}")
def eliminar_estadistica(estadistica_id: int, session: Session = Depends(get_session)):
    est = session.get(Estadistica, estadistica_id)
    if not est:
        raise HTTPException(404, "Estadística no encontrada")

    session.delete(est)
    session.commit()
    return {"message": "Estadística eliminada"}
