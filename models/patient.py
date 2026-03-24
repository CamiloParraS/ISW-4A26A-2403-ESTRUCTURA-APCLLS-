"""
models/patient.py — Healcia · Peciatech
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    priority_level: int  # 1=Resucitacion · 2=Emergencia · 3=Urgente · 4=Menos urgente · 5=No urgente
    arrival_time: str = field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))

    def priority_label(self) -> str:
        labels = {
            1: "Nivel 1 - Resucitacion",
            2: "Nivel 2 - Emergencia",
            3: "Nivel 3 - Urgente",
            4: "Nivel 4 - Menos urgente",
            5: "Nivel 5 - No urgente",
        }
        return labels.get(self.priority_level, "Desconocido")

    def priority_color(self) -> str:
        colors = {
            1: "#E53935",
            2: "#FB8C00",
            3: "#FDD835",
            4: "#43A047",
            5: "#1E88E5",
        }
        return colors.get(self.priority_level, "#9E9E9E")
