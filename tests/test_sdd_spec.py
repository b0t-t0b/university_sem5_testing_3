"""
Тесты Specification by Example (SDD) для календаря событий.
Автоматически считывают живую спецификацию из JSON и валидируют поведение системы по примерам дат и событий.
"""
import json
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from event_calendar.calendar_core import EventCalendar


def load_specification():
    spec_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../specifications/calendar_spec.json")
    )
    with open(spec_path, "r", encoding="utf-8") as f:
        return json.load(f)


SPEC = load_specification()


@pytest.mark.parametrize("example", SPEC["examples_calendar_schedule"], ids=lambda e: e["case_id"])
def test_sdd_schedule_examples(example):
    """Проверка выборки и сортировки событий календаря по примерам из спецификации."""
    calendar = EventCalendar()
    for ev in example["initial_events"]:
        calendar.add_event(
            title=ev["title"],
            event_date=ev["event_date"],
            start_time=ev["start_time"],
            end_time=ev["end_time"],
            category=ev["category"]
        )

    q = example["query_filter"]
    results = calendar.get_events(
        event_date=q.get("event_date"),
        start_date=q.get("start_date"),
        end_date=q.get("end_date"),
        category=q.get("category")
    )

    expected = example["expected_result"]
    assert len(results) == expected["count"]
    assert [e.title for e in results] == expected["ordered_titles"]


@pytest.mark.parametrize("example", SPEC["examples_date_time_validation"], ids=lambda e: e["reason"])
def test_sdd_date_time_validation(example):
    """Проверка граничной валидации дат и времени по спецификации примеров."""
    calendar = EventCalendar()
    if example["expected_valid"]:
        event = calendar.add_event(
            "Тестовое событие",
            example["date_str"],
            example["start"],
            example["end"]
        )
        assert event is not None
    else:
        with pytest.raises((ValueError, TypeError)):
            calendar.add_event(
                "Тестовое событие",
                example["date_str"],
                example["start"],
                example["end"]
            )


@pytest.mark.parametrize("example", SPEC["examples_conflict_detection"], ids=lambda e: e["reason"])
def test_sdd_conflict_detection(example):
    """Проверка алгоритма обнаружения конфликтов интервалов времени."""
    calendar = EventCalendar()
    test_date = "2026-11-20"
    calendar.add_event(
        "Базовое событие",
        test_date,
        example["existing_start"],
        example["existing_end"]
    )

    parsed_d = calendar.parse_date(test_date)
    parsed_s = calendar.parse_time(example["new_start"])
    parsed_e = calendar.parse_time(example["new_end"])

    conflicts = calendar.find_conflicts(parsed_d, parsed_s, parsed_e)
    has_conflict = len(conflicts) > 0
    assert has_conflict == example["expected_conflict"]
