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