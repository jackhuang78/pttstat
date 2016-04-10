#!/bin/sh

echo "====================================="
echo "==   Install Python Dependencies   =="
echo "====================================="
pip install --user -r requirements.txt
chmod a+x bin/*
