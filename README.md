# task
Basic command line to-do list application.

## Video guide

[![asciicast](https://asciinema.org/a/136105.png)](https://asciinema.org/a/136105)

## How does it work?

The tasks are now stored in a database located in the users home folder under the subfolder '.task'.  For example:

`/home/user/.task/tasks.db`

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

### Viewing help

To view some basic help about the various option flags, run `python task.py -h` or `python task.py --help`.

```
usage: task [-h] [-l | -a ADD [ADD ...] | -r REMOVE_ARGS [REMOVE_ARGS ...]]

basic command line to-do application

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            list all stored tasks
  -a ADD [ADD ...], --add ADD [ADD ...]
                        tasks to be added separated by whitespace
  -r REMOVE_ARGS [REMOVE_ARGS ...], --remove REMOVE_ARGS [REMOVE_ARGS ...]
                        remove by listing individual task numbers separated by
                        whitespace or a range which is of the format a..b
                        where a and b are both integers
```
