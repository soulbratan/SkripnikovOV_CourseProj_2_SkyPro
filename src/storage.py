import json
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from draft_vacancies import Vacancy


class VacancyStorage(ABC):
    """Абстрактный класс для работы с хранилищем вакансий"""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Dict[str, Any]) -> List[Vacancy]:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        pass