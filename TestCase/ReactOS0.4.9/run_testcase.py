import os
import subprocess
import re


def run_exe(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    output_re = ''
    
    while p.poll() is None:
        line = p.stdout.readline()
        output_re += line

    return output_re


def get_result(output):
    case_re = re.compile(r'([0-9]+) tests executed')
    case_list = case_re.findall(output)

    if len(case_list) == 1:
        return int(case_list[0], 10)
    else:
        #print 'Error ', output
        return 0
    

def run_path(full_path):
    case_num = 0

    print 'Start:', full_path
    
    output = run_exe(full_path)
    index = output.find('Valid test names')

    if index > 0:
        args = output[index:].split('\n')[1:]
        for arg in args:
            if len(arg.strip()) != 0:
                command = full_path.strip() + ' ' + arg.strip()
                output = run_exe(command)
                cur_num = get_result(output)
                case_num += cur_num
                print '\tSub: ' + arg + ' ' + str(cur_num)
    else:   
        case_num += get_result(output)

    print 'Total:', case_num
    return case_num


def main():
    root_dir = r'.\unit_module_test'
    case_num = 0

    test_exe_list = []

    for parents, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.exe'):
                full_path = os.path.join(parents, filename)
                test_exe_list.append(full_path)

    len_list = len(test_exe_list)

    for i in range(len_list):
        try:
            case_num += run_path(test_exe_list[i])
        except:
            pass

        if (i+1) % 20 == 0:
            print 'Up to %d, Wating for pressing key.\n Total of total: %d' % (i, case_num)
            raw_input()

    print 'Finished! Total of total:', case_num


if __name__ == "__main__":
    main()
