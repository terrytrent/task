# task
Basic command line to-do application.

## How does it work?

Make sure the variable `filename` inside `task.py` is set to a file name that you would like to store the tasks in.

### Adding tasks

`$ python task.py --add 'task one'`

This will add a task called 'task one' to the tasks file. Multiple tasks can be added at once by passing multiple arguments to `python task.py --add`.

### Listing tasks

To list all the tasks, simply run `python task.py --list`.

### Removing tasks

Removal of tasks is done by the command `python task.py --remove`. Task numbers are listed after `--remove`.
All tasks can be removed at once by running `python task.py --remove all`.
A "range" can also be specified for removing tasks. A range has the form `a..b` where `a` and `b` are both integers. `b` has to be greater than `a`.
For example, `python task.py --remove 3..7` removes the tasks 3 through 7.
