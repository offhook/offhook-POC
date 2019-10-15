#!/bin/bash
# Source: https://askubuntu.com/questions/80665#answer-80692

apt install --download-only -o Dir::Cache::archives=$DOWNLOAD_DIR $*