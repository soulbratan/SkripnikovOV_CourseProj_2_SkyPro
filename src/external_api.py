from abc import ABC, abstractmethod


class VacancyAPI(ABC):
    """Абстрактный класс для работы с API сервисов вакансий"""

    @abstractmethod
    def get_vacancies(self, search_text: str):
        """Абстрактный метод для подключения и получения вакансий по ключевому слову"""
        pass
