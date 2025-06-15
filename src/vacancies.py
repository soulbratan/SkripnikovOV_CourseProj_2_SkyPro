from typing import Any, Dict, List, Optional


class Vacancy:
    """Класс для представления вакансии"""

    __slots__ = ("title", "url", "salary", "description")

    def __init__(
        self,
        title: str,
        url: str,
        salary: Optional[Dict[str, Any]],
        description: str,
    ):
        self.title = title
        self.url = url
        self.salary = self.__validate_salary(salary)
        self.description = description

    def __validate_salary(self, salary: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Приватный метод валидации данных о зарплате"""
        if not salary:
            return {"from": 0, "to": 0, "currency": "не указана"}

        salary_from: int | Any = salary.get("from") if salary.get("from") is not None else 0
        salary_to: int | Any = salary.get("to") if salary.get("to") is not None else 0
        if salary_from > salary_to:
            salary_to = salary_from
        currency = salary.get("currency", "не указана").upper()

        return {"from": salary_from, "to": salary_to, "currency": currency}

    @property
    def avg_salary(self) -> float | Any:
        """Средняя зарплата для сравнения"""
        if self.salary["from"] and self.salary["to"]:
            return (self.salary["from"] + self.salary["to"]) / 2
        elif self.salary["from"]:
            return self.salary["from"]
        elif self.salary["to"]:
            return self.salary["to"]
        return 0.0

    def __str__(self) -> str:
        salary_info = (
            f"{self.salary['from']}-{self.salary['to']} {self.salary['currency']}"
            if self.salary["from"] or self.salary["to"]
            else "Зарплата не указана"
        )
        return (
            f"Вакансия: {self.title}\n"
            f"Ссылка: {self.url}\n"
            f"Зарплата: {salary_info}\n"
            f"Описание: {self.description[:100] if type(self.description) is str else "Описание не указано"}...\n"
        )

    def __repr__(self) -> str:
        return f"Vacancy({self.title}, {self.url}, {self.salary})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary == other.avg_salary

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary < other.avg_salary

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary <= other.avg_salary

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование вакансии в словарь для сохранения"""
        return {"title": self.title, "url": self.url, "salary": self.salary, "description": self.description}

    @classmethod
    def from_dict(cls, vacancy_dict: Dict[str, Any]) -> "Vacancy":
        """Создание вакансии из словаря"""
        return cls(
            title=vacancy_dict["title"],
            url=vacancy_dict["url"],
            salary=vacancy_dict["salary"],
            description=vacancy_dict["description"],
        )

    @classmethod
    def cast_to_object_list(cls, vacancies: List[Dict[str, Any]]) -> List["Vacancy"]:
        """Преобразование списка вакансий из JSON в список объектов"""
        result = []
        for vacancy in vacancies:
            salary = vacancy.get("salary")
            title = vacancy.get("title", "Название не указано")
            url = vacancy.get("alternate_url", vacancy.get("url", "Ссылка не указана"))
            description = vacancy.get("description", "Описание не указано") or "Описание не указано"

            result.append(
                cls(
                    title=title,
                    url=url,
                    salary=salary,
                    description=description,
                )
            )
        return result
