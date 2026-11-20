"""
Модели данных для приложения «Календарь событий».
"""
from dataclasses import dataclass
from datetime import date, time
from enum import Enum
from typing import Optional, Dict, Any


class EventCategory(str, Enum):
    MEETING = "meeting"
    PERSONAL = "personal"
    WORK = "work"
    STUDY = "study"
    REMINDER = "reminder"

    @classmethod
    def list(cls):
        return [c.value for c in cls]


@dataclass
class Event:
    id: int
    title: str
    event_date: date
    start_time: time
    end_time: time
    description: str = ""
    category: str = "meeting"
    location: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "event_date": self.event_date.isoformat(),
            "start_time": self.start_time.strftime("%H:%M"),
            "end_time": self.end_time.strftime("%H:%M"),
            "description": self.description,
            "category": self.category,
            "location": self.location
        }


@dataclass
class EventConflict:
    event_id_1: int
    event_id_2: int
    event_date: str
    message: str
