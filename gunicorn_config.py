# gunicorn_config.py

bind = "0.0.0.0:8080"
workers = 2
worker_tmp_dir = "/dev/shm"
