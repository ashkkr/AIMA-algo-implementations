# Python on this system 
Apple mac comes with its own installation of Python which is installed in Developer/CommandLineTools but it's 3.9.6 which is not supported by many systems like Black formatter. 
I have also installed another Python with version 3.11.9 in the pyenv folder. 

# Why do we install python?
So python installation contains the interpreter that interprets the language, the module manager pip and other essential stuff. 

# Why does the formatter Black needs python interpreter to work?
So black is itself a python package and needs an interpreter to run it. That is why we tell it what interpreter to use in user settings. This extension launches a small server using the interpreter

# Why a server anyways?
Server is just a program that stays alive. So we need not cold start it every time we need to format. Also, more importantly, it runs all the time, so it can provide real time recommendations and auto completes while coding. 