import requests
from terminaltables import AsciiTable
from itertools import count
import os
from dotenv import load_dotenv


def predict_rub_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8
    return None


def get_vacancies_hh(language, page=0):
    area = 1
    url = 'https://api.hh.ru/vacancies'
    params = {'text': language, 'area': area, 'page': page}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_statistic_vacancies_hh():
    vacancies_by_language = {}

    languages = [
        "Python", "Java", "Javascript", "Ruby", "PHP", "C++", "C#", "C", "Go",
        "Shell"
    ]

    for language in languages:
        salary_by_vacancies = []
        for page in count(0):
            vacancies = get_vacancies_hh(language, page=page)
            if page >= vacancies["pages"] - 1:
                break
            for vacancy in vacancies["items"]:
                salary = vacancy.get('salary')
                if salary and salary['currency'] == 'RUR':
                    predicted_salary = predict_rub_salary(
                        salary.get('from'), salary.get('to'))
                    if predicted_salary:
                        salary_by_vacancies.append(predicted_salary)
        total_vacancies = vacancies["found"]
        average_salary = None
        if salary_by_vacancies:
            average_salary = int(
                sum(salary_by_vacancies) / len(salary_by_vacancies))

        vacancies_by_language[language] = {
            'vacancies_found': total_vacancies,
            'vacancies_processed': len(salary_by_vacancies),
            'average_salary': average_salary
        }

    return vacancies_by_language


def get_vacancies_sj(sj_secret_key, language="Python", page=0):
    url_sj = 'https://api.superjob.ru/2.0/vacancies/'

    headers = {'X-Api-App-Id': sj_secret_key}
    params = {
        'keyword': language,
        'town': "Moscow",
        'page': page,
        'period': 30,
        'catalogues': 48,
    }

    response = requests.get(url_sj, headers=headers, params=params)
    response.raise_for_status()

    return response.json()


def get_statistic_vacancies_sj(sj_secret_key):
    vacancies_by_language = {}

    languages = [
        "Python", "Java", "Javascript", "Ruby", "PHP", "C++", "C#", "C", "Go",
        "Shell"
    ]
    for language in languages:

        salary_by_vacancies_sj = []
        for page in count(0, 1):
            vacancies_superjob = get_vacancies_sj(sj_secret_key,
                                                  language,
                                                  page=page)

            if not vacancies_superjob['objects']:
                break

            for vacancy in vacancies_superjob['objects']:
                predicted_salary = predict_rub_salary(
                    vacancy.get('payment_from'), vacancy.get('payment_to'))

                if predicted_salary:
                    salary_by_vacancies_sj.append(predicted_salary)

        total_vacancies_sj = vacancies_superjob['total']
        average_salary = None

        if salary_by_vacancies_sj:
            average_salary = int(
                sum(salary_by_vacancies_sj) / len(salary_by_vacancies_sj))

        vacancies_by_language[language] = {
            'vacancies_found': total_vacancies_sj,
            'vacancies_processed': len(salary_by_vacancies_sj),
            'average_salary': average_salary
        }

    return vacancies_by_language


def get_table_vacancies(title, vacancies_by_language):
    table_vacancies = [[
        'Язык программирования', 'Вакансий найдено', 'Вакансий обработано',
        'Средняя зарплата'
    ]]
    for language, vacancies in vacancies_by_language.items():
        table_vacancies.append([
            language, vacancies['vacancies_found'],
            vacancies['vacancies_processed'], vacancies['average_salary']
        ])
    table = AsciiTable(table_vacancies, title)
    return table.table


def main():
    load_dotenv()
    sj_secret_key = os.environ['SJ_SECRET_KEY']
    print(
        get_table_vacancies('SuperJob Moscow',
                            get_statistic_vacancies_sj(sj_secret_key)))
    print(
        get_table_vacancies('HeadHunter Moscow', get_statistic_vacancies_hh()))


if __name__ == '__main__':
    main()