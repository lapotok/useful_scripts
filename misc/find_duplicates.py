import sys
import pathlib, glob

def md5sum(filename):
    import subprocess
    result = subprocess.run(f'md5 {filename}', shell=True, capture_output=True)
    return result.stdout.decode().strip().split(' ')[-1]

def find_duplicates(dir_list):
    
    md5_fn_dict = {}
    
    for dir_i in dir_list:

        files = glob.glob(dir_i + '/**/*', recursive=True)
        total_n = len(files)

        current_n = 1
        sys.stderr.write(f'# Dir: {dir_i}\n')
        for f in files:
            md5_f = md5sum(f)
            if not md5_f in md5_fn_dict:
                md5_fn_dict[md5_f] = []
            md5_fn_dict[md5_f].append(f)
            if current_n % 500 == 0:
                sys.stderr.write(f'Processing #{current_n} of {total_n}\n')
            current_n += 1
        sys.stderr.write('Done.\n\n')

    duplicates = [v for v in md5_fn_dict.values() if len(v)>1]
    
    if len(duplicates)>0:
        print('Duplicates found:')
        count = 0
        for d in duplicates:
            count += 1
            prefix = '' if count == 1 else '\n'
            print(f"{prefix}Group #{count}")
            print('\n'.join(d))

if __name__ == '__main__':

    if len(sys.argv)<2:
        print('Not enough args!')
        sys.exit(2)

    dir_list = sys.argv[1:]

    find_duplicates(dir_list)
