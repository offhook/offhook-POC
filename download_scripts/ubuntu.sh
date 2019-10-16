#!/bin/bash
# Source: https://askubuntu.com/questions/80665#answer-80692

apt-get update
apt-get --download-only -o Dir::Cache::archives=$DOWNLOAD_DIR install $*