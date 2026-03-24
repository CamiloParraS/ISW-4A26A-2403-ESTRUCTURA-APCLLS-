"""
models/doctor.py — Healcia · Peciatech
"""

from dataclasses import dataclass


@dataclass
class Doctor:
    doctor_id: str
    name: str
    specialty: str
