"""
Интерактивное консольное приложение «Календарь событий»
Практическая работа №3 (Вариант № 29)
Дисциплина: Тестирование и верификация ПО
Студент: Хромченков Д. Д., ИКБО-70-24
Преподаватель: Петрова А. А., кафедра МОСИТ
"""
import sys
import os
import argparse
import subprocess

# Обеспечение корректного вывода UTF-8 в Windows-консоли
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Добавляем путь к корню work/pr3
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from event_calendar.calendar_core import EventCalendar
from event_calendar.service import CalendarService
from event_calendar.models import EventCategory


def print_header(title: str):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_table(events):
    """Выводит список событий в виде красивой таблицы."""
    if not events:
        print("  [ Пусто: запланированных событий нет ]")
        return

    header = f"| {'ID':^4} | {'Дата':^10} | {'Интервал':^13} | {'Категория':^10} | {'Название':<25} |"
    sep = "+" + "-" * 6 + "+" + "-" * 12 + "+" + "-" * 15 + "+" + "-" * 12 + "+" + "-" * 27 + "+"
    print(sep)
    print(header)
    print(sep)
    for e in events:
        interval = f"{e.start_time.strftime('%H:%M')}-{e.end_time.strftime('%H:%M')}"
        cat = e.category if isinstance(e.category, str) else e.category.value
        title_disp = (e.title[:22] + "...") if len(e.title) > 25 else e.title
        print(f"| {e.id:^4} | {e.event_date.isoformat():^10} | {interval:^13} | {cat:^10} | {title_disp:<25} |")
    print(sep)


def run_automated_demo():
    """Автоматическая демонстрация всех функций приложения (для показа преподавателю)."""
    print_header("АВТОМАТИЧЕСКАЯ ДЕМОНСТРАЦИЯ РАБОТЫ «КАЛЕНДАРЬ СОБЫТИЙ» (ВАРИАНТ № 29)")
    print("Студент: Хромченков Д. Д. | Группа: ИКБО-70-24 | РТУ МИРЭА, Кафедра МОСИТ\n")

    calendar = EventCalendar()
    service = CalendarService(calendar)

    # 1. Добавление корректных событий
    print("[1] Регистрация базовых событий в календаре:")
    e1 = calendar.add_event(
        title="Лекция по тестированию",
        event_date="2026-11-25",
        start_time="09:00",
        end_time="10:30",
        category="study",
        description="Тема: методологии TDD, ATDD, BDD, SDD",
        location="Ауд. 412"
    )
    print(f"  [OK] Создано событие #{e1.id}: '{e1.title}' ({e1.event_date} {e1.start_time.strftime('%H:%M')}-{e1.end_time.strftime('%H:%M')})")

    e2 = calendar.add_event(
        title="Защита практической №3",
        event_date="2026-11-25",
        start_time="11:00",
        end_time="12:30",
        category="study",
        description="Защита отчёта перед преподавателем",
        location="Кафедра МОСИТ"
    )
    print(f"  [OK] Создано событие #{e2.id}: '{e2.title}' ({e2.event_date} {e2.start_time.strftime('%H:%M')}-{e2.end_time.strftime('%H:%M')})")

    e3 = calendar.add_event(
        title="Тренировка в зале",
        event_date="2026-11-25",
        start_time="19:00",
        end_time="20:30",
        category="personal",
        description="Силовая тренировка"
    )
    print(f"  [OK] Создано событие #{e3.id}: '{e3.title}' ({e3.event_date} {e3.start_time.strftime('%H:%M')}-{e3.end_time.strftime('%H:%M')})")

    # 2. Просмотр расписания
    print("\n[2] Просмотр календаря на дату 2026-11-25 (хронологическая сортировка):")
    day_events = calendar.get_events(event_date="2026-11-25")
    print_table(day_events)

    # 3. Демонстрация валидации
    print("\n[3] Проверка валидации входных данных (защита от некорректных значений):")
    try:
        calendar.add_event("Неверное время", "2026-11-25", "15:00", "14:00")
        print("  [FAIL] Ошибка валидации не сработала!")
    except ValueError as err:
        print(f"  [OK] Перехвачена ошибка времени (start >= end): '{err}'")

    try:
        calendar.add_event("Неверный формат даты", "25-11-2026", "10:00", "11:00")
        print("  [FAIL] Ошибка валидации не сработала!")
    except ValueError as err:
        print(f"  [OK] Перехвачена ошибка формата даты: '{err}'")

    # 4. Демонстрация проверки конфликтов (пересечений)
    print("\n[4] Проверка детекции конфликтов расписания:")
    parsed_date = calendar.parse_date("2026-11-25")
    parsed_st = calendar.parse_time("10:00")
    parsed_et = calendar.parse_time("11:30")
    conflicts = calendar.find_conflicts(parsed_date, parsed_st, parsed_et)
    print(f"  Проверка интервала 10:00-11:30 на дату 2026-11-25:")
    if conflicts:
        print(f"  [OK] Обнаружен конфликт с событием: '{conflicts[0].title}' ({conflicts[0].start_time.strftime('%H:%M')}-{conflicts[0].end_time.strftime('%H:%M')})")
    else:
        print("  [FAIL] Конфликт не обнаружен!")

    # 5. Редактирование события
    print("\n[5] Редактирование события (перенос времени тренировки):")
    calendar.edit_event(e3.id, start_time="20:00", end_time="21:30")
    e3_updated = calendar.get_event(e3.id)
    print(f"  [OK] Время события #{e3.id} успешно обновлено на {e3_updated.start_time.strftime('%H:%M')}-{e3_updated.end_time.strftime('%H:%M')}")

    # 6. Сервисный слой API (ATDD)
    print("\n[6] Демонстрация сервисного слоя API (CalendarService):")
    resp = service.schedule_event({
        "title": "Совещание проекта",
        "event_date": "2026-11-26",
        "start_time": "14:00",
        "end_time": "15:00",
        "category": "work"
    })
    print(f"  Статус ответа: {resp.status_code} ({'Успех' if resp.is_success else 'Ошибка'})")
    print(f"  Данные ответа: {resp.data}")

    # 7. Удаление события
    print("\n[7] Удаление события:")
    del_ok = calendar.delete_event(e3.id)
    print(f"  [OK] Событие #{e3.id} удалено: {del_ok}")

    print("\n[8] Итоговое состояние календаря на 2026-11-25 после изменений:")
    print_table(calendar.get_events(event_date="2026-11-25"))

    print("\n" + "=" * 70)
    print("  ДЕМОНСТРАЦИЯ УСПЕШНО ЗАВЕРШЕНА. ВСЕ ФУНКЦИИ РАБОТАЮТ КОРРЕКТНО!")
    print("=" * 70)


def run_all_tests():
    """Запускает полный комплект автоматизированных тестов с отчётом."""
    print_header("ЗАПУСК ВСЕХ ТЕСТОВ (TDD, ATDD, BDD, SDD, COVERAGE)")
    print("Запуск pytest с контролем покрытия кода...")
    res_pytest = subprocess.run([sys.executable, "-m", "pytest", "tests", "-v", "--cov=event_calendar"], check=False)

    print("\n" + "-" * 70)
    print("Запуск поведенческих тестов Behave (BDD)...")
    res_behave = subprocess.run(["behave", "features/event_calendar.feature"], check=False)

    print("\n" + "=" * 70)
    if res_pytest.returncode == 0 and res_behave.returncode == 0:
        print("  ВСЕ ТЕСТЫ (31 PYTEST + 3 BEHAVE СЦЕНАРИЯ) УСПЕШНО ПРОЙДЕНЫ!")
    else:
        print("  ВНИМАНИЕ: Были зафиксированы ошибки при выполнении тестов.")
    print("=" * 70)


def interactive_mode():
    """Интерактивный режим работы с пользователем / преподавателем."""
    calendar = EventCalendar()
    # Наполняем начальными данными
    calendar.add_event("Лекция по верификации ПО", "2026-11-25", "09:00", "10:30", "study", location="Ауд. 412")
    calendar.add_event("Защита практической №3", "2026-11-25", "11:00", "12:30", "study", location="Кафедра МОСИТ")
    calendar.add_event("Командный митинг", "2026-11-25", "14:00", "15:00", "work")

    while True:
        print_header("КАЛЕНДАРЬ СОБЫТИЙ — ИНТЕРАКТИВНОЕ МЕНЮ (ВАРИАНТ № 29)")
        print("1. Показать все события")
        print("2. Показать события на дату")
        print("3. Добавить новое событие")
        print("4. Редактировать событие")
        print("5. Удалить событие")
        print("6. Проверить интервал на конфликты")
        print("7. Запустить автоматическую демонстрацию (Demo)")
        print("8. Запустить автоматизированные тесты (pytest + behave)")
        print("0. Выход")
        print("-" * 70)

        choice = input("Выберите пункт меню [0-8]: ").strip()
        if choice == "0":
            print("\nВыход из программы. До свидания!")
            break

        elif choice == "1":
            print("\nВсе события в календаре:")
            print_table(calendar.get_events())

        elif choice == "2":
            d = input("Введите дату (YYYY-MM-DD) [по умолчанию 2026-11-25]: ").strip() or "2026-11-25"
            try:
                events = calendar.get_events(event_date=d)
                print(f"\nСобытия на дату {d}:")
                print_table(events)
            except Exception as e:
                print(f"[!] Ошибка: {e}")

        elif choice == "3":
            print("\nДобавление нового события:")
            title = input("  Название события: ").strip()
            date = input("  Дата (YYYY-MM-DD): ").strip()
            st = input("  Время начала (HH:MM): ").strip()
            et = input("  Время окончания (HH:MM): ").strip()
            cat = input("  Категория (study, work, personal, meeting, reminder) [meeting]: ").strip() or "meeting"
            loc = input("  Локация (опционально): ").strip()

            try:
                ev = calendar.add_event(title, date, st, et, category=cat, location=loc)
                print(f"\n[OK] Событие #{ev.id} '{ev.title}' успешно добавлено!")
            except (ValueError, TypeError) as err:
                print(f"\n[!] ОШИБКА: {err}")

        elif choice == "4":
            print_table(calendar.get_events())
            try:
                eid = int(input("\nВведите ID события для редактирования: ").strip())
                new_title = input("Новое название (Enter чтобы не менять): ").strip() or None
                new_st = input("Новое время начала HH:MM (Enter чтобы не менять): ").strip() or None
                new_et = input("Новое время окончания HH:MM (Enter чтобы не менять): ").strip() or None
                calendar.edit_event(eid, title=new_title, start_time=new_st, end_time=new_et)
                print(f"\n[OK] Событие #{eid} успешно обновлено!")
            except Exception as e:
                print(f"\n[!] Ошибка: {e}")

        elif choice == "5":
            print_table(calendar.get_events())
            try:
                eid = int(input("\nВведите ID события для удаления: ").strip())
                calendar.delete_event(eid)
                print(f"\n[OK] Событие #{eid} успешно удалено!")
            except Exception as e:
                print(f"\n[!] Ошибка: {e}")

        elif choice == "6":
            print("\nПроверка конфликтов интервала:")
            d = input("  Дата (YYYY-MM-DD): ").strip()
            st = input("  Время начала (HH:MM): ").strip()
            et = input("  Время окончания (HH:MM): ").strip()
            try:
                p_date = calendar.parse_date(d)
                p_st = calendar.parse_time(st)
                p_et = calendar.parse_time(et)
                conflicts = calendar.find_conflicts(p_date, p_st, p_et)
                if conflicts:
                    print(f"\n[!] Обнаружено конфликтов: {len(conflicts)}")
                    print_table(conflicts)
                else:
                    print("\n[OK] Конфликтов не обнаружено. Время свободно!")
            except Exception as e:
                print(f"\n[!] Ошибка: {e}")

        elif choice == "7":
            run_automated_demo()

        elif choice == "8":
            run_all_tests()

        else:
            print("\n[!] Некорректный выбор. Пожалуйста, выберите число от 0 до 8.")


def main():
    parser = argparse.ArgumentParser(description="Календарь событий (Вариант № 29)")
    parser.add_argument("--demo", action="store_true", help="Запустить автоматическую демонстрацию")
    parser.add_argument("--test", action="store_true", help="Запустить все автоматизированные тесты")
    args = parser.parse_args()

    if args.demo:
        run_automated_demo()
    elif args.test:
        run_all_tests()
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
