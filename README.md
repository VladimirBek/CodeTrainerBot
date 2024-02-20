# CodeTrainerBot


Этот Telegram бот позволяет пользователям получать информацию о задачах на популярном программистском ресурсе Codeforces. Он обладает следующими функциями:

- Получение подборки задач по заданной сложности и тематике с помощью команды /get_task.
- Пользователь может указать сложность задачи и тему, чтобы получить список подходящих задач.

Подборка задач загружается с внешнего ресурса по расписанию: каждый час.
## Установка

Для установки и запуска бота необходимо выполнить следующие шаги:

1. Заполнить .env файл в корне проекта согласно образцу .env.sample. Некоторые данные цже заполнены, их менять не нужно для корректной работы программы.
2. Запустить проект в docker с помощью команды

````bash 
docker compose up --build
````
