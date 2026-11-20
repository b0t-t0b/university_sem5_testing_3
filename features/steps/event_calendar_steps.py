"""
Шаги автоматизации (Step Definitions) для Behave / Gherkin (Вариант № 29: «Календарь событий»).
"""
from behave import given, when, then
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from event_calendar.calendar_core import EventCalendar


@given('календарь событий инициализирован')
def step_init_calendar(context):
    context.calendar = EventCalendar()
    context.last_created_event = None
    context.last_error = None
    context.viewed_events = []


@given('событие с названием "{title}" запланировано на дату "{event_date}" с "{start_time}" до "{end_time}"')
def step_schedule_event(context, title, event_date, start_time, end_time):
    context.last_created_event = context.calendar.add_event(
        title=title,
        event_date=event_date,
        start_time=start_time,
        end_time=end_time
    )


@when('я просматриваю календарь на дату "{event_date}"')
def step_view_calendar(context, event_date):
    context.viewed_events = context.calendar.get_events(event_date=event_date)


@then('я вижу событие с названием "{title}" в нужную дату')
def step_verify_event_in_date(context, title):
    found = any(e.title == title for e in context.viewed_events)
    assert found, f"Событие '{title}' не найдено среди событий: {[e.title for e in context.viewed_events]}"


@then('время события указано с "{start_time}" до "{end_time}"')
def step_verify_event_time(context, start_time, end_time):
    event = context.viewed_events[0]
    actual_start = event.start_time.strftime("%H:%M")
    actual_end = event.end_time.strftime("%H:%M")
    assert actual_start == start_time, f"Ожидалось время начала {start_time}, получено {actual_start}"
    assert actual_end == end_time, f"Ожидалось время окончания {end_time}, получено {actual_end}"


@when('я изменяю время события на интервал с "{new_start}" до "{new_end}"')
def step_edit_event_time(context, new_start, new_end):
    context.last_created_event = context.calendar.edit_event(
        context.last_created_event.id,
        start_time=new_start,
        end_time=new_end
    )


@then('обновленное событие отображается с временем начала "{expected_start}" и окончания "{expected_end}"')
def step_verify_updated_time(context, expected_start, expected_end):
    event = context.calendar.get_event(context.last_created_event.id)
    assert event.start_time.strftime("%H:%M") == expected_start
    assert event.end_time.strftime("%H:%M") == expected_end


@when('я пытаюсь запланировать событие "{title}" на дату "{event_date}" с "{start_time}" до "{end_time}"')
def step_try_invalid_event(context, title, event_date, start_time, end_time):
    try:
        context.calendar.add_event(title, event_date, start_time, end_time)
    except Exception as e:
        context.last_error = e


@then('система отклоняет планирование с ошибкой валидации времени')
def step_verify_validation_error(context):
    assert context.last_error is not None, "Ожидалась ошибка валидации, но операция завершилась успешно"
    assert isinstance(context.last_error, ValueError)
