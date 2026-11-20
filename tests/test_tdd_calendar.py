"""
Полный набор юнит-тестов TDD для EventCalendar (Вариант № 29).
Охватывает операции с событиями, проверки дат, времени, редактирование, удаление и фильтрацию.
"""
import unittest
from datetime import date, time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from event_calendar.calendar_core import EventCalendar
from event_calendar.models import EventCategory


class TestEventCalendarTDD(unittest.TestCase):
    def setUp(self):
        self.calendar = EventCalendar()

    # --- 1. Тесты добавления событий и валидации дат/времени ---

    def test_add_event_valid(self):
        """TDD-01: Успешное добавление корректного события."""
        event = self.calendar.add_event(
            title="Лекция по тестированию ПО",
            event_date="2026-11-20",
            start_time="09:00",
            end_time="10:30",
            description="Аудитория А-12",
            category="study",
            location="МИРЭА"
        )
        self.assertEqual(event.id, 1)
        self.assertEqual(event.title, "Лекция по тестированию ПО")
        self.assertEqual(event.event_date, date(2026, 11, 20))
        self.assertEqual(event.start_time, time(9, 0))
        self.assertEqual(event.end_time, time(10, 30))
        self.assertEqual(event.category, "study")
        self.assertEqual(event.location, "МИРЭА")

    def test_add_event_empty_or_whitespace_title(self):
        """TDD-02: Ошибка при пустом названии события."""
        with self.assertRaises(ValueError) as ctx:
            self.calendar.add_event("", "2026-11-20", "10:00", "11:00")
        self.assertIn("не может быть пустым", str(ctx.exception))

        with self.assertRaises(ValueError):
            self.calendar.add_event("   ", "2026-11-20", "10:00", "11:00")

    def test_add_event_title_too_long(self):
        """TDD-03: Ошибка при названии длиннее 100 символов."""
        long_title = "A" * 101
        with self.assertRaises(ValueError) as ctx:
            self.calendar.add_event(long_title, "2026-11-20", "10:00", "11:00")
        self.assertIn("100 символов", str(ctx.exception))

    def test_add_event_invalid_date_format(self):
        """TDD-04: Ошибка при неверном формате даты (проверка дат)."""
        with self.assertRaises(ValueError) as ctx:
            self.calendar.add_event("Встреча", "20-11-2026", "10:00", "11:00")
        self.assertIn("Неверный формат даты", str(ctx.exception))

    def test_add_event_invalid_time_format(self):
        """TDD-05: Ошибка при неверном формате времени."""
        with self.assertRaises(ValueError) as ctx:
            self.calendar.add_event("Встреча", "2026-11-20", "25:00", "11:00")
        self.assertIn("Неверный формат времени", str(ctx.exception))

    def test_add_event_start_time_after_or_equal_end_time(self):
        """TDD-06: Ошибка, если время начала >= времени окончания."""
        with self.assertRaises(ValueError) as ctx:
            self.calendar.add_event("Встреча", "2026-11-20", "14:00", "13:00")
        self.assertIn("раньше времени окончания", str(ctx.exception))

        with self.assertRaises(ValueError):
            self.calendar.add_event("Встреча", "2026-11-20", "14:00", "14:00")

    def test_add_event_invalid_category(self):
        """TDD-07: Ошибка при неизвестной категории."""
        with self.assertRaises(ValueError) as ctx:
            self.calendar.add_event("Встреча", "2026-11-20", "10:00", "11:00", category="party")
        self.assertIn("Недопустимая категория", str(ctx.exception))

    # --- 2. Тесты редактирования и удаления событий ---

    def test_edit_event_success(self):
        """TDD-08: Успешное редактирование параметров события."""
        event = self.calendar.add_event("Стендап", "2026-11-20", "10:00", "10:30", category="work")
        updated = self.calendar.edit_event(
            event.id,
            title="Утренний командный стендап",
            start_time="10:15",
            end_time="10:45",
            location="Конференц-зал 1"
        )
        self.assertEqual(updated.title, "Утренний командный стендап")
        self.assertEqual(updated.start_time, time(10, 15))
        self.assertEqual(updated.end_time, time(10, 45))
        self.assertEqual(updated.location, "Конференц-зал 1")

    def test_edit_non_existent_event_raises_key_error(self):
        """TDD-09: Ошибка при редактировании несуществующего события."""
        with self.assertRaises(KeyError):
            self.calendar.edit_event(999, title="Новый заголовок")

    def test_delete_event(self):
        """TDD-10: Успешное удаление события по ID."""
        event = self.calendar.add_event("Событие для удаления", "2026-11-20", "11:00", "12:00")
        self.assertTrue(self.calendar.delete_event(event.id))
        self.assertIsNone(self.calendar.get_event(event.id))
        self.assertFalse(self.calendar.delete_event(event.id))

    # --- 3. Тесты просмотра календаря и фильтрации ---

    def test_view_calendar_chronological_sorting(self):
        """TDD-11: Просмотр календаря с хронологической сортировкой."""
        self.calendar.add_event("Вечерняя тренировка", "2026-11-20", "18:00", "19:30")
        self.calendar.add_event("Утренний кофе", "2026-11-20", "08:30", "09:00")
        self.calendar.add_event("Обед с коллегами", "2026-11-20", "13:00", "14:00")

        events = self.calendar.get_events(event_date="2026-11-20")
        self.assertEqual(len(events), 3)
        self.assertEqual(events[0].title, "Утренний кофе")
        self.assertEqual(events[1].title, "Обед с коллегами")
        self.assertEqual(events[2].title, "Вечерняя тренировка")

    def test_view_calendar_range_and_category_filter(self):
        """TDD-12: Фильтрация событий по диапазону дат и категории."""
        self.calendar.add_event("Зачет", "2026-11-15", "10:00", "12:00", category="study")
        self.calendar.add_event("Митинг", "2026-11-18", "14:00", "15:00", category="work")
        self.calendar.add_event("Экзамен", "2026-11-25", "09:00", "13:00", category="study")

        study_events = self.calendar.get_events(
            start_date="2026-11-10",
            end_date="2026-11-30",
            category="study"
        )
        self.assertEqual(len(study_events), 2)
        self.assertEqual(study_events[0].title, "Зачет")
        self.assertEqual(study_events[1].title, "Экзамен")

    def test_conflict_detection(self):
        """TDD-13: Обнаружение пересечений (конфликтов) событий."""
        self.calendar.add_event("Встреча А", "2026-11-20", "10:00", "11:30")
        # Встреча Б: 11:00 - 12:00 (пересекается с 10:00-11:30)
        conflicts = self.calendar.find_conflicts(
            date(2026, 11, 20),
            time(11, 0),
            time(12, 0)
        )
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0].title, "Встреча А")


if __name__ == "__main__":
    unittest.main()
