#!/usr/bin/env python
import os, sys
import re
import time
import math

from glob import glob
from datetime import datetime


#-----------------------------------------------------------------------------------------------------------
# move pics to archive
#-----------------------------------------------------------------------------------------------------------
def move_pics_archive(pwd, newdir):
    for ext in ('jpg', 'jpeg', 'png', 'gif', 'jfif'):
        for file in glob(f'*.{ext}'):
            print(f'moved pic... {file}')
            
            dest = rf'{pwd}\{newdir}\{file}'
            # print(dest)

            # handles case if filename already exist
            try:
                os.rename(file, dest)
            except:
                os.remove(dest)

                os.rename(file, dest)

    print('>> cleaned')


#-----------------------------------------------------------------------------------------------------------
# move packages to downloads
#-----------------------------------------------------------------------------------------------------------
def move_packs_dl(pwd):
    for ext in ('exe', ''):
        for file in glob(f'*.{ext}'):
            print(f'moved package... {file}')

            newdir2 = 'Downloads'

            try:
                os.mkdir(newdir2)
            except:
                pass

            pwd1 = pwd.replace('Desktop', newdir2)

            dest = rf'{pwd1}\{file}'
            # print(dest)

            # handles case if filename already exist
            try:
                os.rename(file, dest)
            except:
                os.remove(dest)

                os.rename(file, dest)

    print('>> cleaned')


#-----------------------------------------------------------------------------------------------------------
# remove duplicate files
#-----------------------------------------------------------------------------------------------------------
def del_dup_files():
    for i in range(1, 50):
        for file in glob(f'*({i}).*'):
            print(f'removed duplicate file... {file}')
            os.remove(file)

    print('>> cleaned')


#-----------------------------------------------------------------------------------------------------------
# move past pdf to archive
#-----------------------------------------------------------------------------------------------------------
def move_past_pdf(weeks, pwd, newdir1):
    c = 0

    for ext in ('pdf', ''):
        for file in glob(f'*.{ext}'):
            # print(file)
            path = rf'{pwd}\{file}'
            # print(path)

            create_epoch = os.path.getctime(path)
            mod_epoch = os.path.getmtime(path)

            now_epoch = datetime.now().timestamp()

            diff_days_create = math.floor((now_epoch - create_epoch) / (60 * 60 * 24))
            diff_days_modify = math.floor((now_epoch - mod_epoch) / (60 * 60 * 24))



            if diff_days_modify >= weeks * 7:
                c += 1

                # print(file)
                # print(f'days since create: {diff_days_create}')
                # print(f'days since modify: {diff_days_mod}')
                # print('-' * 100)

                print(f'moved pdf... {file}')

                dest = rf'{pwd}\{newdir1}\{file}'
                # print(dest)

                # handles case if filename already exist
                try:
                    os.rename(file, dest)
                except:
                    os.remove(dest)

                    os.rename(file, dest)

    # print(c)
    print('>> cleaned')


def main():
    pwd = os.getcwd()
    # print(pwd)

    newdir = 'archive_pic'
    try:
        os.mkdir(newdir)
    except:
        pass
        
    newdir1 = 'archive_pdf'
    try:
        os.mkdir(newdir1)
    except:
        pass

    #-----------------------------------------------------------------------------------------------------------
    # execute fns
    #-----------------------------------------------------------------------------------------------------------
    ip0 = input('Delete duplicate files? (y/n) ')
    if ip0 == 'y':
        del_dup_files()
        
    ip1 = input('Move all pictures to archive? (y/n) ')
    if ip1 == 'y':
        move_pics_archive(pwd, newdir)

    ip2 = input('Move all Exes to downloads? (y/n) ')
    if ip2 == 'y':
        move_packs_dl(pwd)

    wk = 2    ## SPECIFY past weeks as criteria to move
    num_word = {
        1: 'one'
        , 2: 'two'
        , 3: 'three'
        , 4: 'four'
        , 5: 'five'
        , 6: 'six'
        , 7: 'seven'
        , 8: 'eight'
        , 9: 'nine'
        , 10: 'ten'
    }

    ip3 = input(f'Move {num_word[wk]} weeks and older PDFs to archive? (y/n) ')
    if ip3 == 'y':
        move_past_pdf(wk, pwd, newdir1)


    input('\n\nPress any key to exit...')


if __name__ == '__main__':
    main()

