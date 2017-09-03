"""
task.py
A very basic to-do list command line application. It works by adding and removing tasks from
a database located under ~/.task/task.db.
"""
from datetime import datetime
from models import Base, tasks
import argparse
from os import mkdir, path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def connect_db():
    """
    Creates the database, populates tables, and creates a DB connection.
    """
    home_path = path.expanduser("~")
    app_path = path.join(home_path, '.task')

    if not path.exists(app_path):
        mkdir(app_path)

    sqlite_file = "sqlite:///{0}/task.db".format(app_path)
    engine = create_engine(sqlite_file)

    session = sessionmaker(bind=engine)

    if not engine.dialect.has_table(engine, "tasks"):
        Base.metadata.create_all(engine)

    return session()


def main():
    """
    Returns help information and decides which function to call depending on arguments.
    """
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
        list_tasks()
    elif args.add:
        add_task(args.add)
    elif args.remove_args:
        remove_task(args.remove_args)
    else:
        parser.print_help()

def list_tasks():
    """
    List all the tasks presently stored in the database and are not marked for deletion.
    """
    all_tasks = session.query(tasks).filter_by(deleted_at=None).all()

    if len(all_tasks) == 0:
        print "=> no tasks"

    else:
        for task_number in range(0,len(all_tasks)):
            print "{0} => {1}".format(task_number+1, all_tasks[task_number].task)


def add_task(task_items):
    """
    Add all the tasks that are stored in `tasks` into the database.
    """
    created_at = datetime.today()
    for task_item in task_items:
        task = tasks(task=task_item, created_at=created_at, modified_at=created_at, deleted_at=None)

        session.add(task)
        session.commit()

        print "Task Added: \n    ID: {0}\n    Task: {1}\n    Created At: {2}\n    Modified At: {3}".format(task.id,
                                                                                                       task.task,
                                                                                                       task.created_at,
                                                                                                       task.modified_at)


def remove_task(remove_args):
    """
    Removes tasks depending on what the --remove argument has received from the command line.
    Removes either by task numbers or by a 'task range' that is of the format a..b
    """
    all_tasks = session.query(tasks).filter_by(deleted_at=None).all()

    if remove_args[0] == 'all':
        if len(all_tasks) == 0:
            print('=> no tasks to remove, already empty')
        else:
            for task_number in range(0, len(all_tasks)):
                deleted_at = datetime.today()
                task_to_delete_id = all_tasks[task_number].id
                task_to_delete = session.query(tasks).filter_by(id=task_to_delete_id).first()
                task_to_delete.deleted_at = deleted_at

                session.add(task_to_delete)
                session.commit()
            print('=> removed all tasks')

    else:
        if '..' in remove_args[0]:
            dot_start_i = remove_args[0].index('..')
            try:
                start_num = int(remove_args[0][0:dot_start_i])
                end_num = int(remove_args[0][dot_start_i+2:])
                if end_num > start_num:
                    unique_task_numbers = {str(x) for x in range(start_num, end_num + 1)}
                else:
                    print("=> warning: invalid range numbers")
                    print("=> end number must be greater than start number")
                    return 1
            except ValueError:
                print("=> warning: only integers allowed for range")
                return 1
        else:
            unique_task_numbers = set(remove_args[0])

        if len(all_tasks) == 0:
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
                    deleted_at = datetime.today()
                    task_to_delete = session.query(tasks).filter_by(id=all_tasks[task_num - 1].id).first()
                    task_to_delete.deleted_at = deleted_at

                    session.add(task_to_delete)
                    session.commit()

                    print('=> removed task {:d}'.format(task_num))

                except IndexError:
                    print('=> invalid task number: {:d}'.format(task_num))


if __name__ == '__main__':
    session = connect_db()

    main()
