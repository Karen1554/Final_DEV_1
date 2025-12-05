from fastapi import FastAPI
from sqlmodel import SQLModel

from models import engine
import jugadores
import partidos
import estadisticas

app = FastAPI(title="Futbol API")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(jugadores.router, prefix="/jugadores", tags=["Jugadores"])
app.include_router(partidos.router, prefix="/partidos", tags=["Partidos"])
app.include_router(estadisticas.router, prefix="/estadisticas", tags=["Estadísticas"])
