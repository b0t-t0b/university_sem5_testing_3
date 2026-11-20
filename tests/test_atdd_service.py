"""
Приёмочные тесты (ATDD) для приложения «Календарь событий».
Реализуют проверку согласованных сценариев планирования событий на уровне сервисного API.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from event_calendar.service import CalendarService
from event_calendar.calendar_core import EventCalendar


class TestCalendarServiceATDD(unittest.TestCase):
    def setUp(self):
        self.calendar = EventCalendar()
        self.service = CalendarService(self.calendar)

    def test_acceptance_successful_event_scheduling(self):
        """
        Сценарий 1 (ATDD): Планирование и регистрация события.
        Критерий приемки: При передаче валидных параметров возвращается код 201 Created,
        назначается уникальный ID, событие отображается в календаре на указанную дату.
        """
        payload = {
            "title": "Защита практической работы",
            "event_date": "2026-11-25",
            "start_time": "14:00",
            "end_time": "15:30",
            "description": "Защита ПР №3 по тестированию ПО",
            "category": "study",
            "location": "Аудитория В-102"
        }
        response = self.service.schedule_event(payload)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.is_success)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["title"], "Защита практической работы")

        # Проверка отображения в календаре
        view_res = self.service.view_calendar(event_date="2026-11-25")
        self.assertEqual(view_res.status_code, 200)
        self.assertEqual(len(view_res.data), 1)
        self.assertEqual(view_res.data[0]["title"], "Защита практической работы")

    def test_acceptance_invalid_time_interval_rejection(self):
        """
        Сценарий 2 (ATDD): Валидация некорректного временного интервала.
        Критерий приемки: Если время начала позже времени окончания, возвращается
        код 400 Bad Request с описанием ошибки, событие не создается.
        """
        invalid_payload = {
            "title": "Некорректная встреча",
            "event_date": "2026-11-25",
            "start_time": "16:00",
            "end_time": "15:00"
        }
        response = self.service.schedule_event(invalid_payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("раньше времени окончания", response.error)

        # Проверка, что в календаре пусто
        events = self.service.view_calendar(event_date="2026-11-25").data
        self.assertEqual(len(events), 0)

    def test_acceptance_event_updating(self):
        """
        Сценарий 3 (ATDD): Редактирование параметров существующего события.
        Критерий приемки: Пользователь может изменить время и название события,
        календарь мгновенно отражает изменения со статусом 200 OK.
        """
        created = self.service.schedule_event({
            "title": "Совещание",
            "event_date": "2026-11-22",
            "start_time": "10:00",
            "end_time": "11:00"
        }).data

        update_res = self.service.update_event(created["id"], {
            "title": "Срочное совещание отдела",
            "start_time": "10:30",
            "end_time": "11:30"
        })
        self.assertEqual(update_res.status_code, 200)
        self.assertEqual(update_res.data["title"], "Срочное совещание отдела")
        self.assertEqual(update_res.data["start_time"], "10:30")

    def test_acceptance_event_cancellation(self):
        """
        Сценарий 4 (ATDD): Отмена (удаление) запланированного события.
        Критерий приемки: После отмены событие удаляется из календаря и больше не возвращается.
        """
        created = self.service.schedule_event({
            "title": "Встреча для отмены",
            "event_date": "2026-11-23",
            "start_time": "12:00",
            "end_time": "13:00"
        }).data

        del_res = self.service.cancel_event(created["id"])
        self.assertEqual(del_res.status_code, 200)

        # Проверка отсутствия события
        events = self.service.view_calendar(event_date="2026-11-23").data
        self.assertEqual(len(events), 0)


if __name__ == "__main__":
    unittest.main()
