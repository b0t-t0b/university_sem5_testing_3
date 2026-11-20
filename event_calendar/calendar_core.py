"""
Основная доменная логика приложения «Календарь событий».
Реализует операции добавления, редактирования, удаления событий,
проверку корректности дат и временных интервалов, а также обнаружение конфликтов.
"""
from datetime import date, time, datetime
from typing import List, Optional, Dict, Any, Union

from .models import Event, EventCategory


class EventCalendar:
    def __init__(self):
        self._events: Dict[int, Event] = {}
        self._next_id: int = 1

    @staticmethod
    def parse_date(d: Union[str, date]) -> date:
        """Валидирует и парсит дату."""
        if isinstance(d, date):
            return d
        if isinstance(d, str):
            try:
                return datetime.strptime(d.strip(), "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(f"Неверный формат даты: '{d}'. Ожидается YYYY-MM-DD")
        raise TypeError("Дата должна быть строкой формата YYYY-MM-DD или объектом date")

    @staticmethod
    def parse_time(t: Union[str, time]) -> time:
        """Валидирует и парсит время."""
        if isinstance(t, time):
            return t
        if isinstance(t, str):
            try:
                return datetime.strptime(t.strip(), "%H:%M").time()
            except ValueError:
                raise ValueError(f"Неверный формат времени: '{t}'. Ожидается HH:MM")
        raise TypeError("Время должно быть строкой формата HH:MM или объектом time")

    def find_conflicts(
        self,
        event_date: date,
        start_time: time,
        end_time: time,
        exclude_id: Optional[int] = None
    ) -> List[Event]:
        """Определяет события, пересекающиеся по времени с заданным интервалом на ту же дату."""
        conflicts = []
        for e in self._events.values():
            if exclude_id and e.id == exclude_id:
                continue
            if e.event_date == event_date:
                # Пересечение: start < e.end and end > e.start
                if start_time < e.end_time and end_time > e.start_time:
                    conflicts.append(e)
        return conflicts

    def add_event(
        self,
        title: str,
        event_date: Union[str, date],
        start_time: Union[str, time],
        end_time: Union[str, time],
        description: str = "",
        category: str = "meeting",
        location: str = ""
    ) -> Event:
        """Добавляет новое событие в календарь с валидацией данных."""
        if not title or not isinstance(title, str) or not title.strip():
            raise ValueError("Название события не может быть пустым")

        clean_title = title.strip()
        if len(clean_title) > 100:
            raise ValueError("Название события не должно превышать 100 символов")

        parsed_date = self.parse_date(event_date)
        parsed_start = self.parse_time(start_time)
        parsed_end = self.parse_time(end_time)

        if parsed_start >= parsed_end:
            raise ValueError("Время начала события должно быть строго раньше времени окончания")

        cat = category.lower().strip()
        if cat not in EventCategory.list():
            raise ValueError(f"Недопустимая категория: '{category}'. Допустимые: {EventCategory.list()}")

        event = Event(
            id=self._next_id,
            title=clean_title,
            event_date=parsed_date,
            start_time=parsed_start,
            end_time=parsed_end,
            description=description.strip() if description else "",
            category=cat,
            location=location.strip() if location else ""
        )
        self._events[event.id] = event
        self._next_id += 1
        return event

    def edit_event(self, event_id: int, **kwargs) -> Event:
        """Редактирует существующее событие с повторной валидацией."""
        if event_id not in self._events:
            raise KeyError(f"Событие с ID {event_id} не найдено в календаре")

        event = self._events[event_id]

        new_title = kwargs.get("title", event.title)
        if not new_title or not isinstance(new_title, str) or not new_title.strip():
            raise ValueError("Название события не может быть пустым")
        new_title = new_title.strip()
        if len(new_title) > 100:
            raise ValueError("Название события не должно превышать 100 символов")

        new_date = self.parse_date(kwargs["event_date"]) if "event_date" in kwargs else event.event_date
        new_start = self.parse_time(kwargs["start_time"]) if "start_time" in kwargs else event.start_time
        new_end = self.parse_time(kwargs["end_time"]) if "end_time" in kwargs else event.end_time

        if new_start >= new_end:
            raise ValueError("Время начала события должно быть строго раньше времени окончания")

        new_cat = kwargs.get("category", event.category).lower().strip()
        if new_cat not in EventCategory.list():
            raise ValueError(f"Недопустимая категория: '{new_cat}'. Допустимые: {EventCategory.list()}")

        event.title = new_title
        event.event_date = new_date
        event.start_time = new_start
        event.end_time = new_end
        event.category = new_cat
        if "description" in kwargs:
            event.description = kwargs["description"].strip()
        if "location" in kwargs:
            event.location = kwargs["location"].strip()

        return event

    def delete_event(self, event_id: int) -> bool:
        """Удаляет событие по ID."""
        if event_id in self._events:
            del self._events[event_id]
            return True
        return False

    def get_event(self, event_id: int) -> Optional[Event]:
        """Возвращает событие по идентификатору."""
        return self._events.get(event_id)

    def get_events(
        self,
        event_date: Optional[Union[str, date]] = None,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        category: Optional[str] = None
    ) -> List[Event]:
        """Возвращает отсортированный список событий с поддержкой фильтрации."""
        results = list(self._events.values())

        if event_date is not None:
            target_date = self.parse_date(event_date)
            results = [e for e in results if e.event_date == target_date]

        if start_date is not None:
            s_date = self.parse_date(start_date)
            results = [e for e in results if e.event_date >= s_date]

        if end_date is not None:
            e_date = self.parse_date(end_date)
            results = [e for e in results if e.event_date <= e_date]

        if category is not None:
            cat = category.lower().strip()
            results = [e for e in results if e.category == cat]

        # Сортировка по дате и времени начала
        results.sort(key=lambda e: (e.event_date, e.start_time))
        return results

    def get_calendar_summary(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None
    ) -> Dict[str, Any]:
        """Возвращает сводную статистику календаря за период."""
        events = self.get_events(start_date=start_date, end_date=end_date)
        by_category: Dict[str, int] = {}
        for e in events:
            by_category[e.category] = by_category.get(e.category, 0) + 1

        dates_with_events = len(set(e.event_date for e in events))

        return {
            "total_events": len(events),
            "unique_days_with_events": dates_with_events,
            "by_category": by_category
        }
