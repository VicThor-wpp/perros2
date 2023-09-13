import multiprocessing

bind = "unix:/tmp/gunicorn.sock"
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 120
name = "sebuscahumano.com"
loglevel = 'info'
errorlog = 'logs/error.log'
accesslog = 'logs/access.log'
forwarded_allow_ips = '*'