#!/bin/sh

if [ ! -f "./bin/activate" ]; then
  virtualenv .
fi

INVENV=$(python -c 'import sys; print ("1" if hasattr(sys, "real_prefix") else "0")')

echo "INVENV $INVENV"

if [ $INVENV -eq 0 ]; then
  source ./bin/activate
else
  echo "virtualenv already active"
fi
