from sqlmodel import Session
from models import Estadistica

def crear_estadistica(session: Session, jugador_id: int, partido_id: int, minutos_jugados: int, goles: int, tarjetas: int):
    estadistica = Estadistica(jugador_id=jugador_id, partido_id=partido_id, minutos_jugados=minutos_jugados, goles=goles, tarjetas=tarjetas)
    session.add(estadistica)
    session.commit()
    session.refresh(estadistica)
    return estadistica


def leer_estadistica(session: Session, estadistica_id: int):
    estadistica = session.query(Estadistica).filter(Estadistica.id == estadistica_id).first()
    return estadistica


def actualizar_estadistica(session: Session, estadistica_id: int, goles: int, tarjetas: int):
    estadistica = session.query(Estadistica).filter(Estadistica.id == estadistica_id).first()
    if estadistica:
        estadistica.goles = goles
        estadistica.tarjetas = tarjetas
        session.commit()
        session.refresh(estadistica)
    return estadistica


def eliminar_estadistica(session: Session, estadistica_id: int):
    estadistica = session.query(Estadistica).filter(Estadistica.id == estadistica_id).first()
    if estadistica:
        session.delete(estadistica)
        session.commit()
    return estadistica
