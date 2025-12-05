from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select

from models import Jugador
from db import get_session

router = APIRouter()

@router.post("/")
def crear_jugador(jugador: Jugador, session: Session = Depends(get_session)):
    session.add(jugador)
    session.commit()
    session.refresh(jugador)
    return jugador

@router.get("/")
def obtener_jugadores(session: Session = Depends(get_session)):
    jugadores = session.exec(select(Jugador)).all()
    return jugadores

@router.get("/{jugador_id}")
def obtener_jugador(jugador_id: int, session: Session = Depends(get_session)):
    jugador = session.get(Jugador, jugador_id)
    if not jugador:
        raise HTTPException(404, "Jugador no encontrado")
    return jugador
