#!/bin/bash

./venv/bin/gunicorn --bind 127.0.0.1:9002 api:app
