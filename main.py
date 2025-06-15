from src.external_api import HeadHunterAPI
from src.storage import JSONSaver
from src.utils import f_by_kwrd, salary_range, top_vacancies
from src.vacancies import Vacancy


def user_interaction() -> None:
    """Функция взаимодействия с пользователем"""
    search_query = input("Введите поисковый запрос: ")
    hh_api = HeadHunterAPI()
    hh_vacancies = hh_api.get_vacancies(search_query)
    json_saver = JSONSaver()
    json_saver.safe_from_api(hh_vacancies)

    data_from_file = json_saver.get_vacancies()
    vacancies_from_file = Vacancy.cast_to_object_list(data_from_file)

    user_keyword = input("Введите ключевое слово для поиска: ")
    result_filt_by_keyword = f_by_kwrd(vacancies_from_file, user_keyword)

    filt_by_salary = salary_range(result_filt_by_keyword)

    top_n = int(input("Введите количество вакансий для вывода в топ N: "))

    top_vacancies(filt_by_salary, top_n)


if __name__ == "__main__":
    user_interaction()
