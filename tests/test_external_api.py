from unittest.mock import MagicMock, patch

import pytest
import requests

from src.external_api import HeadHunterAPI


@pytest.fixture
def hh_api() -> HeadHunterAPI:
    """Фикстура для создания экземпляра HeadHunterAPI"""
    return HeadHunterAPI()


@patch("src.external_api.requests.get")
def test_connect_to_api_success(mock_get: MagicMock, hh_api: HeadHunterAPI) -> None:
    """Тест успешного подключения к API"""
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = hh_api._HeadHunterAPI__connect_to_api()  # type: ignore

    assert result is True
    mock_get.assert_called_once_with("https://api.hh.ru/vacancies")


@patch("src.external_api.requests.get")
def test_connect_to_api_failure(mock_get: MagicMock, hh_api: HeadHunterAPI) -> None:
    """Тест неудачного подключения к API"""
    mock_get.side_effect = requests.RequestException("Connection error")

    result = hh_api._HeadHunterAPI__connect_to_api()  # type: ignore

    assert result is False


@patch("src.external_api.requests.get")
def test_get_vacancies_success(mock_get: MagicMock, hh_api: HeadHunterAPI) -> None:
    """Тест успешного получения вакансий"""
    mock_response_connect = MagicMock()
    mock_response_connect.raise_for_status.return_value = None

    mock_response_vacancies = MagicMock()
    mock_response_vacancies.raise_for_status.return_value = None
    mock_response_vacancies.json.return_value = {
        "items": [{"id": "1", "name": "Python Developer"}, {"id": "2", "name": "Data Scientist"}]
    }

    mock_get.side_effect = [mock_response_connect, mock_response_vacancies]

    vacancies = hh_api.get_vacancies("Python")

    assert len(vacancies) == 2
    assert vacancies[0]["name"] == "Python Developer"
    mock_get.assert_called_with("https://api.hh.ru/vacancies", params={"text": "Python", "per_page": 100, "page": 0})


@patch("src.external_api.requests.get")
def test_get_vacancies_connection_failed(mock_get: MagicMock, hh_api: HeadHunterAPI) -> None:
    """Тест получения вакансий при неудачном подключении"""
    mock_get.side_effect = requests.RequestException("Connection error")

    vacancies = hh_api.get_vacancies("Python")

    assert vacancies == []


@patch("src.external_api.requests.get")
def test_get_vacancies_request_failed(mock_get: MagicMock, hh_api: HeadHunterAPI) -> None:
    """Тест получения вакансий при ошибке запроса"""
    mock_response_connect = MagicMock()
    mock_response_connect.raise_for_status.return_value = None

    mock_get.side_effect = [mock_response_connect, requests.RequestException("API error")]

    vacancies = hh_api.get_vacancies("Python")

    assert vacancies == []


@patch("src.external_api.requests.get")
def test_get_vacancies_empty_response(mock_get: MagicMock, hh_api: HeadHunterAPI) -> None:
    """Тест получения вакансий с пустым ответом"""
    mock_response_connect = MagicMock()
    mock_response_connect.raise_for_status.return_value = None

    mock_response_vacancies = MagicMock()
    mock_response_vacancies.raise_for_status.return_value = None
    mock_response_vacancies.json.return_value = {"items": []}

    mock_get.side_effect = [mock_response_connect, mock_response_vacancies]

    vacancies = hh_api.get_vacancies("NonExistentPosition")

    assert vacancies == []
