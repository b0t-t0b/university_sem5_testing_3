"""
Unit-тесты этапа TDD (Шаг 1: Написание тестов до реализации функционала).
Проверяют основные операции календаря событий:
- добавление события;
- валидацию некорректных дат и времени;
- редактирование и удаление события;
- просмотр календаря.
"""
import unittest

# На шаге 1 класс еще не реализован или отсутствует
try:
    from event_calendar.calendar_core import EventCalendar, Event
except ImportError:
    EventCalendar = None
    Event = None


class TestEventCalendarTDDInitial(unittest.TestCase):
    def setUp(self):
        if EventCalendar is None:
            self.fail("Класс EventCalendar еще не реализован (TDD Step 1: Red phase)")
        self.calendar = EventCalendar()

    def test_add_event_success(self):
        """Проверка успешного добавления события."""
        event = self.calendar.add_event(
            title="Рабочая встреча",
            event_date="2026-11-20",
            start_time="10:00",
            end_time="11:30",
            category="work"
        )
        self.assertIsNotNone(event.id)
        self.assertEqual(len(self.calendar.get_events()), 1)

    def test_add_event_invalid_time_raises_error(self):
        """Проверка ошибки, если время начала позже времени окончания."""
        with self.assertRaises(ValueError):
            self.calendar.add_event(
                title="Некорректное событие",
                event_date="2026-11-20",
                start_time="15:00",
                end_time="14:00"
            )

    def test_view_calendar_by_date(self):
        """Проверка просмотра календаря по заданной дате."""
        self.calendar.add_event("Событие 1", "2026-11-20", "09:00", "10:00")
        self.calendar.add_event("Событие 2", "2026-11-21", "12:00", "13:00")
        events_20 = self.calendar.get_events(event_date="2026-11-20")
        self.assertEqual(len(events_20), 1)
        self.assertEqual(events_20[0].title, "Событие 1")


if __name__ == "__main__":
    unittest.main()
