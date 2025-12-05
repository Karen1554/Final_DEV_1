from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import date

from utils.states import States
from utils.positions import Position
from db import engine


class Partido(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: date
    rival: str
    goles_sigmotoa: int
    goles_rival: int
    tipo_partido: str
    resultado: str = Field(default="Pendiente")

    estadisticas: List["Estadistica"] = Relationship(back_populates="partido")

    def determinar_resultado(self):
        if self.goles_sigmotoa > self.goles_rival:
            self.resultado = "Victoria"
        elif self.goles_sigmotoa < self.goles_rival:
            self.resultado = "Derrota"
        else:
            self.resultado = "Empate"


class Estadistica(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    jugador_id: int = Field(foreign_key="jugador.id")
    partido_id: int = Field(foreign_key="partido.id")
    minutos_jugados: int
    goles: int
    tarjetas: int

    jugador: "Jugador" = Relationship(back_populates="estadisticas")
    partido: "Partido" = Relationship(back_populates="estadisticas")


class Jugador(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    numero_unico: int = Field(ge=1, le=99, unique=True)
    fecha_nacimiento: date
    nacionalidad: str
    altura: float
    peso: float
    pie_dominante: str
    posicion: Position
    estado: States = Field(default=States.ACTIVO)

    estadisticas: List[Estadistica] = Relationship(back_populates="jugador")
