from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from models import Jugador, Partido, Estadistica, engine
from datetime import date

app = FastAPI()

@app.post("/partidos/")
async def registrar_partido(partido: Partido):
    with Session(engine) as session:
        partido.determinar_resultado()  # Calculamos el resultado
        session.add(partido)
        session.commit()
        session.refresh(partido)
        return partido

@app.get("/partidos/")
async def obtener_historial_partidos():
    with Session(engine) as session:
        partidos = session.exec(select(Partido)).all()
        if not partidos:
            raise HTTPException(status_code=404, detail="No se han encontrado partidos")
        return partidos

@app.get("/partidos/{partido_id}")
async def obtener_partido(partido_id: int):
    with Session(engine) as session:
        partido = session.exec(select(Partido).where(Partido.id == partido_id)).first()
        if not partido:
            raise HTTPException(status_code=404, detail="Partido no encontrado")
        return partido

@app.post("/desempeno/")
async def registrar_desempeno(desempeno: Estadistica):
    with Session(engine) as session:
        partido = session.exec(select(Partido).where(Partido.id == desempeno.partido_id)).first()
        jugador = session.exec(select(Jugador).where(Jugador.id == desempeno.jugador_id)).first()

        if not partido:
            raise HTTPException(status_code=404, detail="Partido no encontrado")
        if not jugador:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")

        session.add(desempeno)
        session.commit()
        session.refresh(desempeno)
        return desempeno
