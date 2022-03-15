bind = "0.0.0.0:8080"
# или через сокет
# bind = "unix:/path/to/app.sock"
# для некоторых фреймворков можно указать worker_class
# worker_class = ‘gevent’
# воркеры которые не работают вот это время - умирают
# timeout = 60
# после получения сигнала (-HUP например) у воркера будет время завершить свою работу
# graceful_timeout = 60
# max_requests = 1000
# задержка перед увеличения счетчика max_requests
# max_requests_jitter = 42
# загружаем приложение до того как воркер процессы форкнутся
# preload_app = True

# Обычно, число worker считается вот так: 2xCPUs + 1
# workers = 5
# worker_connections = 1
# Максимальное число открытых ожидающих коннектов
#backlog = 2048
# задаем переменные окружения
#raw_env = [
#     'FIELD=VALUE'
# ]
# пользователь под которым все будет запущено
#user = "www"
#group = "www"
# путь до логов
logfile = "/home/alameda/PycharmProjects/app_chat/logs/unicorn.log"
loglevel = "info"
# proc_name = "example"
# путь до pid файла
#pidfile = "/path/to/gunicorn.pid"
# gunicorn -c settings.py example:app



