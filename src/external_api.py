from abc import ABC, abstractmethod

import requests


class VacancyAPI(ABC):
    """Абстрактный класс для работы с API сервисов вакансий"""

    @abstractmethod
    def get_vacancies(self, search_text: str) -> list[dict]:
        """Абстрактный метод для подключения и получения вакансий по ключевому слову"""
        pass        # pragma: no cover


class HeadHunterAPI(VacancyAPI):
    """Класс для работы с API HeadHunter"""

    def __init__(self) -> None:
        self.__base_url = "https://api.hh.ru/vacancies"
        self.__connect_to_api()

    def __connect_to_api(self) -> bool:
        """Приватный метод подключения к API hh.ru с проверкой доступности"""
        try:
            response = requests.get(self.__base_url)
            response.raise_for_status()  # Проверка статус-кода
            return True
        except requests.RequestException as e:
            print(f"Ошибка подключения к API hh.ru: {e}")
            return False

    def get_vacancies(self, search_text: str) -> list[dict]:
        """
        Получает вакансии по ключевому слову
        search_text: Ключевое слово для поиска вакансий
        Возвращает список словарей с информацией о вакансиях
        """
        if not self.__connect_to_api():
            return []

        params = {"text": search_text, "per_page": 100, "page": 0}  # Количество вакансий на странице и номер страницы

        try:
            response = requests.get(self.__base_url, params=params)  # type: ignore
            response.raise_for_status()
            vacancies: list[dict] = response.json().get("items", [])
            return vacancies
        except requests.RequestException as e:
            print(f"Ошибка при получении вакансий: {e}")
            return []
