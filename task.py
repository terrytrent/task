"""
task.py
A very basic to-do list command line application. It works by adding and removing tasks from
a text file that is specified by the `filename` variable in the `main` function.
"""
import argparse
import sys

def main():
    filename = '' # tasks file that stores all the tasks
    parser = argparse.ArgumentParser(description='basic command line to-do application')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--list', action='store_true',
                       help='list all stored tasks')
    group.add_argument('-a', '--add', nargs='+',
                       help='tasks to be added separated by whitespace')
    group.add_argument('-r', '--remove', nargs='+', dest='remove_args',
                       help='remove by listing individual task numbers separated ' +
                       'by whitespace or a range which is of the format a..b where '+
                       'a and b are both integers')
    args = parser.parse_args()

    if args.list:
        list_tasks(filename)
    elif args.add:
        add_tasks(filename, args.add)
    elif args.remove_args:
        remove_tasks(filename, args.remove_args)

def list_tasks(filename):
    """
    List all the tasks presently stored in `filename`.
    """
    input_file = open(filename)
    tasks = input_file.read().split('\n')
    tasks.pop()
    input_file.close()
    if len(tasks) == 0:
        print('=> no tasks')
    else:
        counter = 1
        for task in tasks:
            print('{} => {}'.format(counter, task))
            counter += 1

def add_tasks(filename, tasks):
    """
    Add all the tasks that are stored in `tasks` into the tasks file.
    """
    output_file = open(filename, 'a')
    for task in tasks:
        output_file.write(task + '\n')
        print('=> added task \'{}\''.format(task))
    output_file.close()

def remove_tasks(filename, remove_args):
    """
    Removes tasks depending on what the --remove argument has received from the command line.
    Removes either by task numbers or by a 'task range' that is of the format a..b
    """
    if remove_args[0] == 'all':
        input_file = open(filename)
        tasks = input_file.read().split('\n')
        tasks.pop()
        input_file.close()
        if len(tasks) == 0:
            print('=> no tasks to remove, already empty')
        else:
            output_file = open(filename, 'w')
            output_file.write('')
            output_file.close()
            print('=> removed all tasks')
    else:
        if '..' in remove_args[0]:
            unique_task_numbers = set()
            dot_start_i = remove_args[0].index('..')
            try:
                start_num = int(remove_args[0][0:dot_start_i])
                end_num = int(remove_args[0][dot_start_i+2:])
                if end_num > start_num:
                    unique_task_numbers = {str(x) for x in
                        range(start_num, end_num + 1)}
                else:
                    print("=> warning: invalid range numbers")
                    print("=> end number must be greater than start number")
                    return 1
            except ValueError:
                print("=> warning: only integers allowed for range")
                return 1
        else:
            unique_task_numbers = set(remove_args[0:])
        input_file = open(filename)
        tasks = input_file.read().split('\n')
        tasks.pop()
        input_file.close()
        if len(tasks) == 0:
            print('=> no tasks to remove, already empty')
        else:
            for task_num_str in unique_task_numbers:
                try:
                    task_num = int(task_num_str)
                except ValueError:
                    print("=> warning: '{}' is not a task number nor a range".format(task_num_str))
                    continue
                if (task_num < 1):
                    print('=> warning: only positive task numbers allowed ({:d})'.format(task_num))
                    continue
                try:
                    tasks[task_num - 1] = None
                    print('=> removed task {:d}'.format(task_num))
                except IndexError:
                    print('=> invalid task number: {:d}'.format(task_num))
            tasks = [task for task in tasks if task != None]
            output_file = open(filename, 'w')
            for task in tasks:
                output_file.write(task + '\n')
            output_file.close()

if __name__ == '__main__':
    main()
