# python-build-cli-planner-app

In this project you will implement a simple reminder app with a command line interface (CLI). While doing so, you will learn how to use inheritance and abstract base classes to make your code modular and to ensure a contract between your classes.

First, we will guide you through implementing simple text reminders. Then, you will have reminders with a deadline, which is either a date, or a date and a time. As each of these have their own class, you will see how these can play together nicely. This basis makes it easy for you to go beyond the course scope and implement other types of reminders, such as recurrent ones.

## Setup

You should have [Docker](https://www.docker.com/products/docker-desktop) installed, as well as `make`. These ensure the app is easy to run regardless of your platform.

### Play with the app

Now that you have all the requirements ready, you can test the app by running `make` in the root directory. You can add a new reminder, or list the ones you have already added.

Try adding a couple of reminders, such as *Drink water*, *Take a break* or *Buy some milk*.

### Test the app

To test your app, run `make test`. Since you have not implemented anything, all the tests should be failing. As you progress through the tasks, more and more of them will pass. When you are stuck, running the tests may give you a hint about your error.
