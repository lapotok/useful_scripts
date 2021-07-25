#!/usr/bin/python3

import sys, os
import pathlib, glob
from joblib import Memory

memory = Memory('_joblib_cache_', verbose=0)

@memory.cache
def md5sum(filename):
    import subprocess
    result = subprocess.run(f"md5 '{filename}'", shell=True, capture_output=True)
    return result.stdout.decode().strip().split(' ')[-1]

def find_duplicates(dir_list, method='md5'): # or filename
    
    key_dict = {}
    
    for dir_i in dir_list:

        files = glob.glob(dir_i + '/**/*', recursive=True)
        total_n = len(files)

        current_n = 1
        sys.stderr.write(f'# Dir: {dir_i}\n')
        for f in files:
            if os.path.isfile(f):
                key = md5sum(f) if method == 'md5' else os.path.basename(f)
                if not key in key_dict:
                    key_dict[key] = []
                key_dict[key].append(f)
                if current_n % 500 == 0:
                    sys.stderr.write(f'Processing #{current_n} of {total_n}\n')
                current_n += 1
        sys.stderr.write('Done.\n\n')

    duplicates = [v for v in key_dict.values() if len(v)>1]
    
    if len(duplicates)>0:
        print('Duplicates found:')
        count = 0
        for d in duplicates:
            count += 1
            prefix = '' if count == 1 else '\n'
            print(f"{prefix}Group #{count}")
            print('\n'.join(d))

if __name__ == '__main__':
    

    if len(sys.argv)<3:
        print(f'Not enough args!\n\nUsage: {sys.argv[0]} [-f|-m] dirs')
        sys.exit(2)

    dir_list = sys.argv[2:]

    if sys.argv[1] == '-m':
        find_duplicates(dir_list, 'md5')
    elif sys.argv[1] == '-f':
        find_duplicates(dir_list, 'filename')
    else:
        print('What method?')
        sys.exit(2)
