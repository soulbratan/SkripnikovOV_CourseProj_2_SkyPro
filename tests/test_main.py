from unittest.mock import MagicMock, patch

import pytest

from main import user_interaction


@pytest.fixture
def mock_vacancy_data() -> list:
    return [
        {
            "name": "Python Developer",
            "alternate_url": "https://example.com",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "snippet": {"responsibility": "Разработка на Python"},
        }
    ]


@patch("builtins.input", side_effect=["Python", "Python", "100000", "200000", "5"])
@patch("src.external_api.HeadHunterAPI.get_vacancies", return_value=[])
@patch("builtins.print")
def test_user_interaction_no_vacancies(
    mock_print: MagicMock, mock_get_vacancies: MagicMock, mock_input: MagicMock
) -> None:
    """Тест случая, когда API не возвращает вакансий"""
    user_interaction()
    mock_print.assert_not_called


@patch("builtins.input", side_effect=["Python", "Java", "abc", "xyz", "5"])
@patch("src.external_api.HeadHunterAPI.get_vacancies")
@patch("src.storage.JSONSaver")
@patch("builtins.print")
def test_user_interaction_invalid_salary(
    mock_print: MagicMock,
    mock_json_saver: MagicMock,
    mock_get_vacancies: MagicMock,
    mock_input: MagicMock,
    mock_vacancy_data: MagicMock,
) -> None:
    """Тест обработки некорректного ввода зарплаты"""
    mock_get_vacancies.return_value = mock_vacancy_data
    json_saver_instance = mock_json_saver.return_value
    json_saver_instance.get_vacancies.return_value = mock_vacancy_data

    user_interaction()

    # Проверяем, что были сообщения о некорректном вводе
    assert any("Некорректно введено число" in str(call) for call in mock_print.call_args_list)


@patch("builtins.input", side_effect=["Python", "InvalidKeyword", "100000", "200000", "5"])
@patch("src.external_api.HeadHunterAPI.get_vacancies")
@patch("src.storage.JSONSaver")
@patch("src.utils.f_by_kwrd", return_value=[])
@patch("builtins.print")
def test_user_interaction_no_matching_keywords(
    mock_print: MagicMock,
    mock_f_by_kwrd: MagicMock,
    mock_json_saver: MagicMock,
    mock_get_vacancies: MagicMock,
    mock_input: MagicMock,
    mock_vacancy_data: MagicMock,
) -> None:
    """Тест случая, когда нет вакансий по ключевому слову"""
    mock_get_vacancies.return_value = mock_vacancy_data
    json_saver_instance = mock_json_saver.return_value
    json_saver_instance.get_vacancies.return_value = mock_vacancy_data

    user_interaction()
