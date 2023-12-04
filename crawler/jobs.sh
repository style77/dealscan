#!/bin/bash

INTERVAL=5

while true; do
  echo "Refreshing feed"
  python manage.py refreshfeeds
  sleep $INTERVAL;
done