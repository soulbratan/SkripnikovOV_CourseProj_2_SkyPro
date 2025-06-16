from typing import Any, List, Union, Callable

from src.vacancies import Vacancy


def print_enumerated_list(func: Any) -> Callable:
    """Декоратор для"""

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Вызываем исходную функцию
        result = func(*args, **kwargs)

        # Проверяем, что результат является списком или итерируемым объектом
        if isinstance(result, (list, tuple)):
            # print("Результат функции (пронумерованный список):")
            for index, value in enumerate(result, start=1):
                # print(f"{index}. {value}")
                print(f"{index}---------------------------------------")
                print(value)
        else:
            print("Функция вернула не список. Результат:")
            print(result)

        return result

    return wrapper


def f_by_kwrd(list_vac: List[Union[Vacancy, dict]], kwrd: Union[str, List[str]]) -> List[Union[Vacancy, dict]]:
    """
    Фильтрация вакансий по ключевым словам в названии или описании

    Args:
        list_vac: Список вакансий (объекты Vacancy или словари)
        kwrd: Ключевое слово или список ключевых слов для поиска

    Returns:
        Отфильтрованный список вакансий, содержащих ключевые слова
    """
    if not list_vac or not kwrd:
        return []

    # Нормализуем входные ключевые слова
    if isinstance(kwrd, str):
        keywords = [kwrd.lower()]
    else:
        keywords = [k.lower() for k in kwrd if k]

    filtered_list = []
    seen_vacancies = set()  # Для отслеживания дубликатов

    for vac in list_vac:
        # Для объектов Vacancy
        if isinstance(vac, Vacancy):
            title = vac.title.lower()
            description = vac.description.lower()
            vac_id = (vac.title, vac.url, str(vac.salary))
        # Для словарей
        elif isinstance(vac, dict):
            title = vac.get("title", "").lower()
            description = vac.get("description", "").lower()
            vac_id = (vac.get("title"), vac.get("url"), str(vac.get("salary")))     # type: ignore
        else:
            continue

        # Проверяем дубликаты
        if vac_id in seen_vacancies:
            continue

        # Проверяем наличие хотя бы одного ключевого слова
        for keyword in keywords:
            if keyword in title or keyword in description:
                filtered_list.append(vac)
                seen_vacancies.add(vac_id)
                break  # Не проверяем остальные ключи, если уже нашли совпадение

    return filtered_list


def salary_range(list_vac: list[dict]) -> list[dict]:
    try:
        salary_from = int(input("Введите минимальную зарплату: ").replace(" ", ""))
    except ValueError:
        salary_from = 0
        print("Некорректно введено число. Минимальная зарплата: 0")
    try:
        salary_to = int(input("Введите максимальную зарплату: ").replace(" ", ""))
        if salary_to <= 0:  # Добавляем проверку на отрицательные значения
            salary_to = 300000
            print("Максимальная зарплата: 300000")
    except ValueError:
        salary_to = 300000
        print("Некорректно введено число. Максимальная зарплата: 300000")
    filtered_vacancies: list = list()
    for vac in list_vac:
        if isinstance(vac, Vacancy):
            if (vac.salary.get("from", 0) >= salary_from) and (vac.salary.get("to", 0) <= salary_to):
                filtered_vacancies.append(vac)
        elif isinstance(vac, dict):
            if (vac["salary"].get("from", 0) >= salary_from) and (vac["salary"].get("to", 0) <= salary_to):
                filtered_vacancies.append(vac)
    return filtered_vacancies


@print_enumerated_list
def top_vacancies(list_vac: list, top_n: int = 10) -> list:
    sorted_vacancies = sorted(list_vac, reverse=True)
    if not isinstance(top_n, int):
        top_n = 10
    top_vacancies = sorted_vacancies[:top_n]
    return top_vacancies
