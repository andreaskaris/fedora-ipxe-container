#!/usr/bin/python3

import os 
import glob
import re

dir_path = os.path.dirname(os.path.realpath(__file__))
boot_ipxe_file_name = dir_path + '/boot.ipxe'
menu_items = ''
menu_entries = ''

dir_path = '/httpboot'
menu_dirs = glob.glob(dir_path + '/*')
for menu_dir in menu_dirs:
    menu_entry = os.path.basename(menu_dir)
    menu_items += 'item ' + menu_entry + '\n'

    menu_entries += ':' + menu_entry + '\n'
    boot_menu_entry_file = open(menu_dir + '/boot-menu-entry', 'r')
    menu_entries += boot_menu_entry_file.read() + '\n'
    boot_menu_entry_file.close()

block1 = """#!ipxe

menu PXE Boot Options

"""

block2 = """
item shell iPXE shell
item exit  Exit to BIOS

choose --default exit --timeout 10000 option && goto ${option}

"""

block3 = """
:shell
shell

:exit
exit
"""

boot_ipxe_file = open(boot_ipxe_file_name,"w")
boot_ipxe_file.write(block1)
boot_ipxe_file.write(menu_items)
boot_ipxe_file.write(block2)
boot_ipxe_file.write(menu_entries)
boot_ipxe_file.write(block3)
boot_ipxe_file.close()
