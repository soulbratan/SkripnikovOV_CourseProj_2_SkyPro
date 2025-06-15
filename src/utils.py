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