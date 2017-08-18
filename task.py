import sys

def main():
    filename = '' # tasks file that stores all the tasks
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'list' or sys.argv[1] == 'l':
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
        elif sys.argv[1] == 'add' or sys.argv[1] == 'a':
            if len(sys.argv) == 2:
                print("=> no tasks received")
            else:
                output_file = open(filename, 'a')
                for task in sys.argv[2:]:
                    output_file.write(task + '\n')
                    print('=> added task \'{}\''.format(task))
                output_file.close()
        elif sys.argv[1] == 'remove' or sys.argv[1] == 'done' or sys.argv[1] == 'r' or sys.argv[1] == 'd':
            if len(sys.argv) == 2:
                print('=> expected command \'all\' or task numbers')
            else:
                if sys.argv[2] == 'all':
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
                    if '..' in sys.argv[2]:
                        unique_task_numbers = set()
                        dot_start_i = sys.argv[2].index('..')
                        try:
                            start_num = int(sys.argv[2][0:dot_start_i])
                            end_num = int(sys.argv[2][dot_start_i+2:])
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
                        unique_task_numbers = set(sys.argv[2:])
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
        else:
            print('=> unknown command \'{}\''.format(sys.argv[1]))
            print('=> list, add, or remove expected')
    else:
        print('=> no command received')
        print('=> list, add, or remove expected')

if __name__ == '__main__':
    main()
