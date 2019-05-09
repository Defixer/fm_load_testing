This is a sample `LocustIO` script [MAC]

## Requirements
* Homebrew
* Python 2.7, 3.5 or 3.6
* Pip
* Virtualenv 
* LocustIO 

## Installing Homebrew
```
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

## Installing python
```
$ brew install python
```

## Installing pip
```
$ sudo easy_install pip
```

## Installing Pyenv via
```
$ brew install pyenv
```

## Installing specific python versions
```
$ pyenv install 3.x.x
```
`3.x.x` - x's represents the version number

## Using Pyenv
```
//Lists all python installed
$ pyenv versions

//Switches the current python version to be used
$ pyenv global 3.x.x

//Creating virtual environment
$ mkdir ~/.virtual_envs
$ cd ~/.virtual_envs
$ pyenv virtualenv 3.x.x <environment_name>
```  

_it will create a virtual environment with your current python installed; if it's `Python 3.7` it will already have `pip` as well_  
_it will be created to the current directory that terminal is in_  
_reference: https://amaral.northwestern.edu/resources/guides/pyenv-tutorial_

## Activating/Deactivating virtual environment
```
$ source /[env directory]/bin/activate
$ deactivate

//Using Pyenv
$ pyenv activate <virtual environment name>
$ source deactivate
```

##### Adding aliases
```
$ sudo nano ~/.bash_profile  
$ alias venvpy3.6up="source /[virtual_env_directory]/bin/activate"  
Ctrl+O //to save  
Ctrl+X //to exit  

//Activate updated bash_profile
$ source ~/.bash_profile  
$ venvpy3.6up //[in terminal] will automatically activate your virtual environment  
(venvpy3.6) $ //virtual environment name should be included in the prompt when it is activated

//Using Pyenv  
$ alias venvpy3.6up="pyenv activate venvpy3.6"  
```

## Installing Locustio
```
$ pip install locustio
``` 
see [Locustio Installation](https://docs.locust.io/en/stable/installation.html)  
#use Python 2.7, 3.5 or 3.6. Incompatible with Python 3.7 as of February 2019

## Running script
`$ locust -f [locust_filename]` 

_In web browser_

`localhost:8089` is the locust web GUI: input the number of user as well as number of users per second and start swarming  

`$ locust -f [locust_filename] --no-web -c 1 -r 1 --print-stats` #disables GUI and purely outputs in _terminal_  
