# python-build-cli-planner-app

In this project you will implement a simple reminder app with a command line interface (CLI). While doing so, you will learn how to use inheritance and abstract base classes to make your code modular and to ensure a contract between your classes.

First, we will guide you through implementing simple text reminders. Then, you will have reminders with a deadline, which is either a date, or a date and a time. As each of these have their own class, you will see how these can play together nicely. This basis makes it easy for you to go beyond the course scope and implement other types of reminders, such as recurrent ones.

## Installation

This project requires `python3.8` or higher. Once you have this installed, follow the instructions below to setup a virtual environment for this project, which ensures that its dependencies will not conflict with other projects of yours.

Note that you may have to use `python3` instead of `python` depending on how you have installed python.

First, regardless of your platform, open up a terminal and navigate to the project directory:
```
$ cd <path/to/project/root>
```

Then, create a virtual environment `reminders-venv`:
```
$ python -m venv reminders-venv
```
You will have to use this whenever you want to work on this project, to ensure that you have the right dependencies.
To activate your environment, run:

- Windows
```
> reminders-venv\Scripts\activate.bat
```
- macOS / Linux
```
$ source reminders-venv/bin/activate
```
Please ensure that your shell confirms the activation of the virtual environment before proceeding. This typically means that the shell displays something similar to ```(reminders-venv)``` at the beginning of each line.

Then, if you need to work on a different project, you can deactivate your environment by running `deactivate` at the command prompt.

Finally, install the dependencies:
```
python -m pip install -r requirements.txt
```

If you see a warning about `pip` being outdated, that's OK; `pip` updates frequently.

## Verify Setup

At the root of your project, run
```
$ pytest
```
You should see all tests failing in the beginning, but no error about `pytest` itself. If so, you are ready to start making your app.

As you progress through the tasks you can re-run the above command to check the tasks. The error messages should give you a hint as to why a test is failing.

## Previewing Your Work

Start playing with your app by running `python app.py`. Try adding a couple of reminders such as `Drink water` and `Complete the Reminders project`.  :)
