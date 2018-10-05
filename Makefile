FLASK_PID_FILE=./flask.pid
VENV=./bgg-sim-venv/bin
ENV?=dev
export AWS_PROFILE=zappa

# ---------------
#   DEPENDENCIES
# ---------------
.PHONY: update-requirements
update-requirements:
	(conda env update && \
	source activate bgg-similarity && \
	pip freeze > requirements.txt)


# ---------------
#   VIRTUALENV
# ---------------
.PHONY: init
init:
	rm -rf bgg-sim-venv
	virtualenv bgg-sim-venv
	(source $(VENV)/activate && pip install -r requirements.txt)


# ---------------
#   FLASK Locally
# ---------------
.PHONY: start
start:
	$(VENV)/python bg_similarity.py & echo $$! > $(FLASK_PID_FILE);
	sleep 1 && \
	$(VENV)/python -m webbrowser "http://127.0.0.1:5000/" &

.PHONY: stop
stop:
	kill `cat $(FLASK_PID_FILE)` && rm $(FLASK_PID_FILE)

.PHONY: restart
restart: stop start

# command to find flask PIDs in use to kill missed processes
.PHONY: find-pid
find-pid:
	sudo lsof -i :5000


# ---------------
#   ZAPPA
# ---------------
.PHONY: deploy
deploy:
	(source $(VENV)/activate && zappa deploy $(ENV))

.PHONY: redeploy
redeploy:
	(source $(VENV)/activate && zappa update $(ENV))

.PHONY: remove
remove:
	(source $(VENV)/activate && zappa undeploy $(ENV))

.PHONY: logs
logs:
	(source $(VENV)/activate && zappa tail $(ENV))

# ------------
#  TESTING
# ------------
.PHONY: test
test:
	$(VENV)/python test_bg_similarity.py


# -------------
#  LSH Training
# -------------
# The input to this is a gzip data file containing a pandas dataframe of
# collected game data
.PHONY: train
train:
	$(VENV)/python lsh_train.py ${DATA_FILE}
