# Information-hub
Django based news crration platform

### Installation
To run the application locally, you will first need to run the following comamnds to install a virtual environment to load the requirements
```
pip install virtualenv
virtualenv venv
./venv/Scripts/activate
```
The above works for windows, the only change if you are running the application on linux is that when you activate the venv, you would instead run

```
source venv/bin/activate
```

from there, you can then install the dependencies by running the following command

```
pip install -r requirements.txt
```
Once the dependencies have been installed, you can then run the application by writing the following command
```
python manage.py runserver 
```
For the above to work, you have to make sure that you're in the directory where manage.py is located

### Testing

To run the unit tests, you have to make sure that the installation is done and that you can run the application correctly. If that's the case, you can run the unit tests by running the command
```
python manage.py test 
```

If you want to see the total test coverage from the tests instead, the commands are a bit different
```
coverage manage.py test 
coverage report
```
you should then be able to see the coverage of each file within the project. 