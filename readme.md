# Сравниваем вакансии программистов
## Описание
Проект создан для загрузки данных о зарплатах различных программистов, зависимости от языка программирования. Поиск производится по [hh.ru](https://hh.ru)  и [SuperJob](https://superjob.ru).
## Установка
Python3 должен быть уже установлен. Затем ```pip```(или ```pip3```, если есть конфликт с Python2) для установки зависимостей и установить зависимости. Зависимости можно установить командой, представленной ниже. Создайте бота у отца ботов. Создайте новый канал в Telegram.
```
pip install -r requirements.txt
```
## Пример запуска скрипта
Для запуска скрпита у вас должен быть установлен Python3.

Для получения таблиц с вакансиями и зарабатной платой необходимо написать:
```
python main.py
```
## Переменные окружения
Часть настроек проекта берётся из переменных окружения. Переменные окружения - это переменные, значения которых присваиваются программе Python извне. Чтобы их определить создайте файл ```.env``` рядом с ```main.py``` и запиишите туда данные в таком фармате: переменная=значение.

Пример содержания файла `.env` :
```
sj_secret_key = ['SJ_SECRET_KEY']
```

Получить токен `SJ_SECRET_KEY`  можно на сайте [API SuperJob](https://api.superjob.ru/)

## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).