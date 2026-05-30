#!/bin/env bash

cat << 'EOF'
-------------------------
 Needed software
-------------------------


pip3 install -r requirements.txt
EOF

echo "Setting up required packages ..."

pip3 install -r requirements.txt --break-system-packages

