import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from src.vacancies import Vacancy


class VacancyStorage(ABC):
    """Абстрактный класс для работы с хранилищем вакансий"""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        pass    # pragma: no cover

    @abstractmethod
    def get_vacancies(self) -> list:
        pass    # pragma: no cover

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        pass    # pragma: no cover


class JSONSaver(VacancyStorage):
    """Класс для сохранения вакансий в JSON-файл"""

    __slots__ = ("__filename",)

    def __init__(self, filename: str = "vacancies.json"):
        self.__filename = filename
        if not os.path.exists(self.__filename):
            with open(self.__filename, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _is_duplicate(self, new_vacancy: Vacancy | dict, existing_data: List[Dict[str, Any]]) -> bool:
        """Проверка на дубликаты вакансий"""
        if isinstance(new_vacancy, Vacancy):
            new_vacancy = new_vacancy.to_dict()
        for vacancy in existing_data:
            if (
                vacancy["title"] == new_vacancy["title"]
                and vacancy["url"] == new_vacancy["url"]
                and vacancy["salary"] == new_vacancy["salary"]
            ):
                return True
        return False

    def safe_from_api(self, api_vacancies: list[dict]) -> None:
        """Сохранение списка вакансий по необходимым атрибутам в JSON-файл"""
        with open(self.__filename, "r+", encoding="utf-8") as f:
            try:
                result = json.load(f)
            except json.JSONDecodeError:
                result = []
            for vacancy in api_vacancies:
                if vacancy.get("salary", None) is None:
                    salary = {"from": 0, "to": 0, "currency": "не указана"}
                else:
                    from_vac = vacancy["salary"].get("from", 0) or 0
                    to_vac = vacancy["salary"].get("to", 0) or from_vac
                    currency = vacancy["salary"].get("currency", "Не указана") or "Не указана"
                    salary = {"from": from_vac, "to": to_vac, "currency": currency}
                title = vacancy.get("name", "Название не указано") or "Название не указано"
                url = vacancy.get("alternate_url", vacancy.get("url", "Ссылка не указана")) or ""
                snippet = vacancy.get("snippet", {})
                description = snippet.get("responsibility", "Описание не указано") or "Описание не указано"
                temp_vac = {"title": title, "url": url, "salary": salary, "description": description}
                if not self._is_duplicate(temp_vac, result):
                    result.append(temp_vac)
                f.seek(0)
                json.dump(result, f, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии в файл"""
        with open(self.__filename, "r+", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

            if not self._is_duplicate(vacancy, data):
                data.append(vacancy.to_dict())
                f.seek(0)
                json.dump(data, f, ensure_ascii=False, indent=4)

    def get_vacancies(self) -> list:
        """Получение вакансий из json файла"""
        with open(self.__filename, "r", encoding="utf-8") as f:
            try:
                data: list = json.load(f)
            except json.JSONDecodeError:
                data = []
        # data = [Vacancy.from_dict(item) for item in data]
        return data

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаление вакансии из файла"""
        vacancy_dict: dict = vacancy.to_dict()
        with open(self.__filename, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

        new_data = [
            item
            for item in data
            if not (
                item["title"] == vacancy_dict["title"]
                and item["url"] == vacancy_dict["url"]
                and item["salary"] == vacancy_dict["salary"]
            )
        ]

        with open(self.__filename, "w", encoding="utf-8") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)
