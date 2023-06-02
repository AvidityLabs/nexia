web: gunicorn core.wsgi --log-file -
release: bash release.sh
beat: celery -A core.celeryapp:app beat -S redbeat.RedBeatScheduler  --loglevel=DEBUG --pidfile /tmp/celerybeat.pid
worker: celery -A core.celeryapp:app  worker -Q default -n core.%%h --without-gossip --without-mingle --without-heartbeat --loglevel=INFO --max-memory-per-child=512000 --concurrency=1