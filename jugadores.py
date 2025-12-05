from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Jugador

router = APIRouter()

@router.post("/", response_model=Jugador)
def crear_jugador(jugador: Jugador, session: Session = Depends(get_session)):
    session.add(jugador)
    session.commit()
    session.refresh(jugador)
    return jugador


@router.get("/", response_model=list[Jugador])
def listar_jugadores(session: Session = Depends(get_session)):
    jugadores = session.exec(select(Jugador)).all()
    return jugadores

@router.get("/{jugador_id}", response_model=Jugador)
def obtener_jugador(jugador_id: int, session: Session = Depends(get_session)):
    jugador = session.get(Jugador, jugador_id)
    if not jugador:
        raise HTTPException(404, "Jugador no encontrado")
    return jugador

@router.put("/{jugador_id}", response_model=Jugador)
def actualizar_jugador(jugador_id: int, data: Jugador, session: Session = Depends(get_session)):
    jugador = session.get(Jugador, jugador_id)
    if not jugador:
        raise HTTPException(404, "Jugador no encontrado")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(jugador, key, value)

    session.add(jugador)
    session.commit()
    session.refresh(jugador)
    return jugador

# Eliminar
@router.delete("/{jugador_id}")
def eliminar_jugador(jugador_id: int, session: Session = Depends(get_session)):
    jugador = session.get(Jugador, jugador_id)
    if not jugador:
        raise HTTPException(404, "Jugador no encontrado")

    session.delete(jugador)
    session.commit()
    return {"message": "Jugador eliminado"}
