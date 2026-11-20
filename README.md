# Календарь событий (Event Calendar)

> **Дисциплина:** Тестирование и верификация программного обеспечения  
> **Практическая работа №3:** Подходы для разработки программного обеспечения (TDD, ATDD, BDD, SDD)  
> **Вариант № 29:** «Календарь событий»  
> **Студент:** Хромченков Д. Д., гр. ИКБО-70-24  
> **Кафедра:** МОСИТ, ИИТ, РТУ МИРЭА (2026)

---

## 📌 Описание проекта

Программный модуль персонального календаря событий, разработанный с применением четырёх методологий разработки через тестирование:
* **TDD (Test-Driven Development):** модульные тесты доменного ядра расписания (`unittest`).
* **ATDD (Acceptance Test-Driven Development):** приёмочные сценарии контрактов сервисного API (`CalendarService`, `ApiResponse`).
* **BDD (Behavior-Driven Development):** поведенческие сценарии на естественном языке Gherkin во фреймворке `behave`.
* **SDD (Specification by Example):** параметризованные тесты живой спецификации конкретных примеров (`pytest`).

---

## 🚀 Быстрый старт

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Запуск программы
* **Автоматическая демонстрация (показ за 3 секунды):**
  ```bash
  python run.py --demo
  ```
* **Интерактивное консольное меню:**
  ```bash
  python run.py
  ```

---

## 🧪 Запуск тестов

* **Запуск всего набора тестов и анализ покрытия (pytest + behave):**
  ```bash
  python run.py --test
  ```

* **Запуск по отдельным методологиям:**
  - **TDD (модульные тесты):**
    ```bash
    pytest tests/test_tdd_calendar.py -v
    ```
  - **ATDD (приёмочные сценарии):**
    ```bash
    pytest tests/test_atdd_service.py -v
    ```
  - **BDD (сценарии Gherkin / Behave):**
    ```bash
    behave features/event_calendar.feature
    ```
  - **SDD (параметризованные тесты спецификации):**
    ```bash
    pytest tests/test_sdd_spec.py -v
    ```
  - **Отчёт о покрытии кода тестами (pytest-cov):**
    ```bash
    pytest tests --cov=event_calendar
    ```

---

## 📂 Структура репозитория

```text
├── event_calendar/                 # Доменный пакет приложения
│   ├── calendar_core.py            # Доменная логика расписания (EventCalendar)
│   ├── models.py                   # Модели данных (Event, EventCategory)
│   └── service.py                  # Сервисный слой API (CalendarService, ApiResponse)
├── tests/                          # Автоматизированные тесты
│   ├── test_tdd_calendar.py        # TDD юнит-тесты (13 тестов)
│   ├── test_tdd_initial_fail.py    # Тесты фазы Red
│   ├── test_atdd_service.py        # ATDD приёмочные тесты (4 теста)
│   └── test_sdd_spec.py            # SDD параметризованные тесты (11 тестов)
├── features/                       # BDD сценарии Behave
│   ├── event_calendar.feature      # Сценарии на языке Gherkin
│   └── steps/
│       └── event_calendar_steps.py # Шаги автоматизации Behave
├── specifications/                 # Живая спецификация требований (SDD)
│   └── calendar_spec.json          # Конкретные примеры расписания и валидации
├── main.py                         # Консольное приложение
├── run.py                          # Главная точка входа
└── requirements.txt                # Зависимости проекта
```
