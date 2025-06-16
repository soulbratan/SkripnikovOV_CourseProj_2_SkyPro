from unittest.mock import MagicMock, mock_open, patch

import pytest

from src.storage import JSONSaver
from src.vacancies import Vacancy


@pytest.fixture
def sample_vacancy() -> Vacancy:
    """Фикстура с примером вакансии"""
    return Vacancy(
        title="Python Developer",
        url="https://example.com",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        description="Разработка на Python",
    )


@pytest.fixture
def sample_vacancy_dict() -> dict:
    """Фикстура с примером вакансии в виде словаря"""
    return {
        "title": "Python Developer",
        "url": "https://example.com",
        "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
        "description": "Разработка на Python",
    }


@pytest.fixture
def mock_json_file() -> str:
    """Фикстура для мокирования файла"""
    return '[{"title": "Existing Vacancy", "url": "https://existing.com", "salary": {"from": 50000, "to": 70000, "currency": "RUR"}, "description": "Existing job"}]'


def test_json_saver_init_creates_file_if_not_exists() -> None:
    """Тест создания файла при инициализации, если он не существует"""
    with patch("os.path.exists", return_value=False), patch("builtins.open", mock_open()) as mock_file:
        JSONSaver("test.json")
        mock_file.assert_called_once_with("test.json", "w", encoding="utf-8")
        mock_file().write.assert_called_once_with("[]")


def test_json_saver_init_does_not_create_file_if_exists() -> None:
    """Тест, что файл не пересоздается, если уже существует"""
    with patch("os.path.exists", return_value=True), patch("builtins.open", mock_open()) as mock_file:
        JSONSaver("test.json")
        mock_file.assert_not_called()


def test_add_vacancy_new(sample_vacancy: Vacancy, mock_json_file: MagicMock) -> None:
    """Тест добавления новой вакансии"""
    m = mock_open(read_data=mock_json_file)
    with patch("builtins.open", m), patch("json.dump") as mock_dump:
        saver = JSONSaver()
        saver.add_vacancy(sample_vacancy)

        # Проверяем, что файл открывался для чтения и записи
        assert m.call_count == 2
        assert mock_dump.call_count == 2


def test_add_vacancy_duplicate(sample_vacancy: Vacancy, mock_json_file: MagicMock) -> None:
    """Тест, что дубликаты вакансий не добавляются"""
    m = mock_open(read_data=mock_json_file)
    with patch("builtins.open", m), patch("json.dump") as mock_dump:
        saver = JSONSaver()
        # Создаем вакансию, которая уже есть в моке
        existing_vacancy = Vacancy(
            title="Existing Vacancy",
            url="https://existing.com",
            salary={"from": 50000, "to": 70000, "currency": "RUR"},
            description="Existing job",
        )
        saver.add_vacancy(existing_vacancy)
        mock_dump.assert_called_once()


def test_get_vacancies(sample_vacancy_dict: dict, mock_json_file: MagicMock) -> None:
    """Тест получения списка вакансий"""
    m = mock_open(read_data=mock_json_file)
    with patch("builtins.open", m):
        saver = JSONSaver()
        vacancies = saver.get_vacancies()
        assert isinstance(vacancies, list)
        assert len(vacancies) == 1
        assert vacancies[0]["title"] == "Existing Vacancy"


def test_get_vacancies_empty_file() -> None:
    """Тест получения вакансий из пустого файла"""
    m = mock_open(read_data="")
    with patch("builtins.open", m):
        saver = JSONSaver()
        vacancies = saver.get_vacancies()
        assert vacancies == []


def test_delete_vacancy(sample_vacancy: Vacancy, mock_json_file: MagicMock) -> None:
    """Тест удаления вакансии"""
    m = mock_open(read_data=mock_json_file)
    with patch("builtins.open", m), patch("json.dump") as mock_dump:
        saver = JSONSaver()
        # Создаем вакансию, которая есть в моке
        existing_vacancy = Vacancy(
            title="Existing Vacancy",
            url="https://existing.com",
            salary={"from": 50000, "to": 70000, "currency": "RUR"},
            description="Existing job",
        )
        saver.delete_vacancy(existing_vacancy)
        assert mock_dump.call_count == 2


def test_safe_from_api(sample_vacancy_dict: dict) -> None:
    """Тест сохранения вакансий из API"""
    api_data = [
        {
            "name": "New Vacancy",
            "alternate_url": "https://new.com",
            "salary": {"from": 80000, "to": 120000, "currency": "RUR"},
            "snippet": {"responsibility": "New job description"},
        }
    ]

    m = mock_open(read_data="[]")
    with patch("builtins.open", m), patch("json.dump") as mock_dump:
        saver = JSONSaver()
        saver.safe_from_api(api_data)

        # Проверяем, что данные были записаны
        assert mock_dump.call_count == 2
        args, kwargs = mock_dump.call_args
        assert len(args[0]) == 1
        assert args[0][0]["title"] == "New Vacancy"


def test_safe_from_api_with_duplicates(sample_vacancy_dict: dict, mock_json_file: MagicMock) -> None:
    """Тест, что дубликаты из API не добавляются"""
    api_data = [
        {
            "name": "Existing Vacancy",  # Такая уже есть в моке
            "alternate_url": "https://existing.com",
            "salary": {"from": 50000, "to": 70000, "currency": "RUR"},
            "snippet": {"responsibility": "Existing job"},
        }
    ]

    m = mock_open(read_data=mock_json_file)
    with patch("builtins.open", m), patch("json.dump") as mock_dump:
        saver = JSONSaver()
        saver.safe_from_api(api_data)
        assert mock_dump.call_count == 2
