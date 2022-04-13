@echo off
::==============================================================================================
:: This wrapper sets the paths required to run python from the base env
:: then calls the script provided with any parameters
::
::    __author__ = "Barry Onizak"
::    __copyright__ = 'Copyright (c) 2020 IBM All rights reserved.' \
::                    ' No part of this script may be copied or translated' \
::                    ' in any form or by any means without prior written permission from IBM.'
::    __license__ = "IBM Internal Use Only"
::    __version__ = "20220410.1"
::==============================================================================================
::
:: First, ENSURE these values are correct for your particular environment.#

export ScriptPATH=/DevApps/PyCharmProjects/PythonBackup/src
export PythonPATH=/DevApps/DevTools/anaconda3

:: Next, Load Miniconda
export pythonexec=$PythonPATH/bin/python

## Check for params
[ -z "$1" ] && echo $0 - ERROR -- No Parameters provided! && return

cd $(dirname $0)
$pythonexec $@