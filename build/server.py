#!/bin/sh
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
python $SCRIPTPATH/controller.py <$1 $2 $3 $4>