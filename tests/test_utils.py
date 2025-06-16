from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from src.utils import f_by_kwrd, print_enumerated_list, salary_range, top_vacancies
from src.vacancies import Vacancy


@pytest.fixture
def sample_vacancies_2() -> list:
    """Фикстура с примером списка вакансий"""
    return [
        Vacancy(
            title="Python Developer",
            url="https://example.com/python",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            description="Разработка на Python и Django",
        ),
        Vacancy(
            title="Java Developer",
            url="https://example.com/java",
            salary={"from": 120000, "to": 180000, "currency": "RUR"},
            description="Разработка на Java и Spring",
        ),
        Vacancy(
            title="Data Scientist",
            url="https://example.com/data",
            salary={"from": 150000, "to": 200000, "currency": "RUR"},
            description="Анализ данных на Python",
        ),
    ]


def test_f_by_kwrd(sample_vacancies_2: list) -> None:
    """Тест фильтрации по ключевым словам"""
    # Фильтрация по слову "Python"
    filtered = f_by_kwrd(sample_vacancies_2, ["Python"])
    assert len(filtered) == 2
    assert filtered[0].title == "Python Developer"
    assert filtered[1].title == "Data Scientist"

    # Фильтрация по слову "Java"
    filtered = f_by_kwrd(sample_vacancies_2, ["Java"])
    assert len(filtered) == 1
    assert filtered[0].title == "Java Developer"

    # Фильтрация по нескольким словам
    filtered = f_by_kwrd(sample_vacancies_2, ["Python", "Java"])
    assert len(filtered) == 3


@patch("builtins.input", side_effect=["100000", "200000"])
def test_salary_range_valid_input(mock_input: MagicMock, sample_vacancies_2: list) -> None:
    """Тест фильтрации по диапазону зарплат с корректным вводом"""
    filtered = salary_range(sample_vacancies_2)
    assert len(filtered) == 3
    assert filtered[0].title == "Python Developer"  # type: ignore
    assert filtered[1].title == "Java Developer"  # type: ignore
    assert filtered[2].title == "Data Scientist"  # type: ignore


@patch("builtins.input", side_effect=["abc", "xyz"])
def test_salary_range_invalid_input(mock_input: MagicMock, sample_vacancies_2: list, capsys: Any) -> None:
    """Тест фильтрации с некорректным вводом зарплат"""
    filtered = salary_range(sample_vacancies_2)
    captured = capsys.readouterr()
    # При некорректном вводе salary_from=0, salary_to=300000
    assert len(filtered) == 3


def test_top_vacancies(sample_vacancies_2: list, capsys: Any) -> None:
    """Тест вывода топ-N вакансий"""
    result = top_vacancies(sample_vacancies_2, 2)

    # Проверяем возвращаемое значение
    assert len(result) == 2
    assert result[0].title == "Data Scientist"  # Самая высокая зарплата
    assert result[1].title == "Java Developer"

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "1---------------------------------------" in captured.out
    assert "2---------------------------------------" in captured.out
    assert "Data Scientist" in captured.out
    assert "Java Developer" in captured.out


def test_print_enumerated_list_decorator(capsys: Any) -> None:
    """Тест декоратора print_enumerated_list"""

    @print_enumerated_list
    def test_func() -> list:
        return ["item1", "item2"]

    result = test_func()

    # Проверяем возвращаемое значение
    assert result == ["item1", "item2"]

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "1---------------------------------------" in captured.out
    assert "item1" in captured.out
    assert "2---------------------------------------" in captured.out
    assert "item2" in captured.out


def test_print_enumerated_list_non_iterable(capsys: Any) -> None:
    """Тест декоратора с неитерируемым результатом"""

    @print_enumerated_list
    def test_func() -> str:
        return "not a list"

    result = test_func()

    # Проверяем возвращаемое значение
    assert result == "not a list"

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "Функция вернула не список. Результат:" in captured.out
    assert "not a list" in captured.out
