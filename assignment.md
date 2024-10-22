Технологии: FastApi, docker-compose, PostgreSQL, SQLAlchemy, Телеграм бот

Реализовать микросервисное веб приложение для мониторинга цен на любом сайте, например, мвидео.

Необходимо предусмотреть следующий функционал:

1. Модуль HTTP API  С использованием библиотеки FastApi

Он должен содержать следующие маршруты:

1) Добавление нового товара на мониторинг (ссылка на товар)

2) Удаление товара

3) Получение списка товаров на мониторинге

4) Получение истории цен на товар.

2. Телеграм бот с аналогичным функционалом

3. Модуль мониторинга, который будет периодически получать новую цену товара:

При добавлении товара, необходимо получать только его название, описание и рейтинг (если есть).

Получать информацию можно просто через requests.

Записывать цену на товар необходимо раз в час.

4. БД для хранения информации (PostgreSQL)

Запуск кода через docker-compose, каждый модуль в отдельном контейнере. Как минимум модуль БД должен иметь volume для сохранения информации в нем.

Для работы с базой использовать либу SQLAlchemy.

Если будет время и желание, то кроме маршрутов бекенда, можно ещё сделать странички для этих маршрутов с помощью шаблонов Jinja2 и обмазать bootstrapовскими классами для красоты, но это вообще не обязательно.