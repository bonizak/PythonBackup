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
::    __version__ = "1.12b"
::==============================================================================================
::
:: First, ENSURE these 3 values are correct for your particular environment.#

set DRV=C:
set TKPATH=%DRV%\bin\PythonBackup\src
set CONDAPATH=%DRV%\ProgramData\Miniconda3

:: Next, Load Miniconda
CALL %CONDAPATH%\condabin\conda.bat activate

:: Now, the 'python' to be used is set in 
set PYTHONEXE=%CONDAPATH%\python.exe

::Lastly, call the PYTHON script from a new window
cd %TKPATH%
cmd.exe /i /c %PYTHONEXE% %*