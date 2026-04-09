#!/bin/bash

apt-get update
apt-get install -y chromium chromium-driver

python bot.py
