from draft_vacancies import Vacancy


def print_enumerated_list(func):
    def wrapper(*args, **kwargs):
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


def f_by_kwrd(list_vac, kwrd):
    """Фильтрация по ключевым словам"""
    filt_list = list()
    for vac in list_vac:
        for word in kwrd:
            if word in vac.description or word in vac.title:
                filt_list.append(vac)
    return filt_list


def salary_range(list_vac: list[dict]) -> list[dict]:
    try:
        salary_from = int(input("Введите минимальную зарплату: ").replace(" ", ""))
    except ValueError:
        salary_from = 0
        print(f"Некорректно введено число. Минимальная зарплата: 0")
    try:
        salary_to = int(input("Введите максимальную зарплату: ").replace(" ", ""))
    except ValueError:
        salary_to = 0
        print(f"Некорректно введено число. Максимальная зарплата: 300000")
    filtered_vacancies = list()
    for vac in list_vac:
        if isinstance(vac, Vacancy):
            if (vac.salary.get("from", 0) >= salary_from) and (vac.salary.get("to", 0) <= salary_to):
                filtered_vacancies.append(vac)
        elif isinstance(vac, dict):
            if (vac["salary"].get("from", 0) >= salary_from) and (vac["salary"].get("to", 0) <= salary_to):
                filtered_vacancies.append(vac)
    return filtered_vacancies


@print_enumerated_list
def top_vacancies(list_vac, top_n=10):
    sorted_vacancies = sorted(list_vac, reverse=True)
    top_vacancies = sorted_vacancies[:top_n]
    return top_vacancies