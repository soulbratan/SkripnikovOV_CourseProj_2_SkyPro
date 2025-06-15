import pytest
from src.vacancies import Vacancy


def test_vacancy_initialization():
    """Тест инициализации вакансии"""
    vacancy = Vacancy(
        title="Python Developer",
        url="https://example.com",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        description="Разработка на Python"
    )

    assert vacancy.title == "Python Developer"
    assert vacancy.url == "https://example.com"
    assert vacancy.description == "Разработка на Python"
    assert vacancy.salary == {"from": 100000, "to": 150000, "currency": "RUR"}


def test_salary_validation_no_salary():
    """Тест валидации зарплаты, когда зарплата не указана"""
    vacancy = Vacancy(
        title="Python Developer",
        url="https://example.com",
        salary=None,
        description="Разработка на Python"
    )

    assert vacancy.salary == {"from": 0, "to": 0, "currency": "не указана"}


def test_salary_validation_partial_salary():
    """Тест валидации частично указанной зарплаты"""
    vacancy = Vacancy(
        title="Python Developer",
        url="https://example.com",
        salary={"from": 100000, "currency": "USD"},
        description="Разработка на Python"
    )

    assert vacancy.salary == {"from": 100000, "to": 100000, "currency": "USD"}


def test_salary_validation_from_greater_than_to():
    """Тест валидации, когда 'from' больше 'to'"""
    vacancy = Vacancy(
        title="Python Developer",
        url="https://example.com",
        salary={"from": 200000, "to": 150000, "currency": "RUR"},
        description="Разработка на Python"
    )

    assert vacancy.salary == {"from": 200000, "to": 200000, "currency": "RUR"}


def test_avg_salary():
    """Тест расчета средней зарплаты"""
    # Оба значения указаны
    vacancy1 = Vacancy("A", "url1", {"from": 100, "to": 200, "currency": "RUR"}, "desc1")
    assert vacancy1.avg_salary == 150.0

    # Только from
    vacancy2 = Vacancy("B", "url2", {"from": 100, "currency": "RUR"}, "desc2")
    assert vacancy2.avg_salary == 100.0

    # Только to
    vacancy3 = Vacancy("C", "url3", {"to": 200, "currency": "RUR"}, "desc3")
    assert vacancy3.avg_salary == 200.0

    # Нет зарплаты
    vacancy4 = Vacancy("D", "url4", None, "desc4")
    assert vacancy4.avg_salary == 0.0


def test_str_representation():
    """Тест строкового представления вакансии"""
    vacancy = Vacancy(
        title="Python Developer",
        url="https://example.com",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        description="Разработка на Python и Django"
    )

    expected = (
        "Вакансия: Python Developer\n"
        "Ссылка: https://example.com\n"
        "Зарплата: 100000-150000 RUR\n"
        "Описание: Разработка на Python и Django...\n"
    )

    assert str(vacancy) == expected


def test_comparison_operators():
    """Тест операторов сравнения"""
    vacancy1 = Vacancy("A", "url1", {"from": 100, "to": 200}, "desc1")
    vacancy2 = Vacancy("B", "url2", {"from": 150, "to": 250}, "desc2")
    vacancy3 = Vacancy("C", "url3", {"from": 100, "to": 200}, "desc3")

    assert vacancy1 < vacancy2
    assert vacancy2 > vacancy1
    assert vacancy1 == vacancy3
    assert vacancy1 <= vacancy3
    assert vacancy2 >= vacancy1


def test_to_dict():
    """Тест преобразования вакансии в словарь"""
    vacancy = Vacancy(
        title="Python Developer",
        url="https://example.com",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        description="Разработка на Python"
    )

    expected = {
        "title": "Python Developer",
        "url": "https://example.com",
        "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
        "description": "Разработка на Python"
    }

    assert vacancy.to_dict() == expected


def test_from_dict():
    """Тест создания вакансии из словаря"""
    data = {
        "title": "Python Developer",
        "url": "https://example.com",
        "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
        "description": "Разработка на Python"
    }

    vacancy = Vacancy.from_dict(data)

    assert vacancy.title == "Python Developer"
    assert vacancy.url == "https://example.com"
    assert vacancy.salary == {"from": 100000, "to": 150000, "currency": "RUR"}
    assert vacancy.description == "Разработка на Python"


def test_cast_to_object_list():
    """Тест преобразования списка словарей в список объектов Vacancy"""
    vacancies_data = [
        {
            "name": "Python Developer",
            "alternate_url": "https://example.com/1",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "snippet": {"responsibility": "Разработка на Python"}
        },
        {
            "name": "Data Scientist",
            "url": "https://example.com/2",
            "salary": None,
            "snippet": {}
        }
    ]

    vacancies = Vacancy.cast_to_object_list(vacancies_data)

    assert len(vacancies) == 2
    assert vacancies[0].title == "Python Developer"
    assert vacancies[0].url == "https://example.com/1"
    assert vacancies[0].salary == {"from": 100000, "to": 150000, "currency": "RUR"}
    assert vacancies[0].description == "Разработка на Python"

    assert vacancies[1].title == "Data Scientist"
    assert vacancies[1].url == "https://example.com/2"
    assert vacancies[1].salary == {"from": 0, "to": 0, "currency": "не указана"}
    assert vacancies[1].description == "Описание не указано"