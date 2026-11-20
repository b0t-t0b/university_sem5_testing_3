"""
Сервисный слой (API/Service Layer) приложения «Календарь событий».
Используется для реализации приёмочного тестирования (ATDD).
"""
from dataclasses import dataclass
from typing import Optional, Any, Dict, List
from .calendar_core import EventCalendar


@dataclass
class ApiResponse:
    status_code: int
    data: Optional[Any] = None
    error: Optional[str] = None

    @property
    def is_success(self) -> bool:
        return 200 <= self.status_code < 300

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status_code": self.status_code,
            "data": self.data,
            "error": self.error
        }


class CalendarService:
    def __init__(self, calendar: Optional[EventCalendar] = None):
        self.calendar = calendar if calendar is not None else EventCalendar()

    def schedule_event(self, payload: Dict[str, Any]) -> ApiResponse:
        """Планирует новое событие через API."""
        required = ["title", "event_date", "start_time", "end_time"]
        missing = [f for f in required if f not in payload]
        if missing:
            return ApiResponse(
                status_code=400,
                error=f"Отсутствуют обязательные поля: {', '.join(missing)}"
            )

        try:
            # Проверка конфликтов перед созданием
            target_date = self.calendar.parse_date(payload["event_date"])
            start_t = self.calendar.parse_time(payload["start_time"])
            end_t = self.calendar.parse_time(payload["end_time"])

            event = self.calendar.add_event(
                title=payload["title"],
                event_date=target_date,
                start_time=start_t,
                end_time=end_t,
                description=payload.get("description", ""),
                category=payload.get("category", "meeting"),
                location=payload.get("location", "")
            )

            # Проверяем, есть ли другие события в это же время
            conflicts = self.calendar.find_conflicts(target_date, start_t, end_t, exclude_id=event.id)
            res_data = event.to_dict()
            res_data["has_conflicts"] = len(conflicts) > 0
            if conflicts:
                res_data["conflicting_event_ids"] = [c.id for c in conflicts]

            return ApiResponse(status_code=201, data=res_data)
        except (ValueError, TypeError) as e:
            return ApiResponse(status_code=400, error=str(e))

    def update_event(self, event_id: int, payload: Dict[str, Any]) -> ApiResponse:
        """Обновляет параметры события."""
        try:
            event = self.calendar.edit_event(event_id, **payload)
            return ApiResponse(status_code=200, data=event.to_dict())
        except KeyError as e:
            return ApiResponse(status_code=404, error=str(e))
        except (ValueError, TypeError) as e:
            return ApiResponse(status_code=400, error=str(e))

    def cancel_event(self, event_id: int) -> ApiResponse:
        """Отменяет/удаляет событие."""
        success = self.calendar.delete_event(event_id)
        if success:
            return ApiResponse(status_code=200, data={"deleted": True, "id": event_id})
        return ApiResponse(status_code=404, error=f"Событие с ID {event_id} не найдено")

    def view_calendar(
        self,
        event_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        category: Optional[str] = None
    ) -> ApiResponse:
        """Возвращает события календаря с фильтрацией."""
        try:
            events = self.calendar.get_events(
                event_date=event_date,
                start_date=start_date,
                end_date=end_date,
                category=category
            )
            return ApiResponse(status_code=200, data=[e.to_dict() for e in events])
        except (ValueError, TypeError) as e:
            return ApiResponse(status_code=400, error=str(e))
