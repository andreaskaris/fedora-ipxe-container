#!/usr/bin/python3

import os 
import glob
import re
import time
from inotify_simple import INotify, flags

dir_path = os.path.dirname(os.path.realpath(__file__))

boot_ipxe_file_name = '/tftpboot/menu/boot.ipxe'
httpboot_dir_path = '/httpboot'
boot_menu_entry_file_name = 'boot-menu-entry'

class WatchHttpboot:

  httpboot_dir_path = ''
  boot_menu_entry_file_name = ''
  inotify = None
  watch_flags = None
  debug = False

  def __init__(self, httpboot_dir_path, boot_menu_entry_file_name, debug = False):
      self.httpboot_dir_path = httpboot_dir_path
      self.boot_menu_entry_file_name = boot_menu_entry_file_name
      self.debug = debug

      self.inotify = INotify()
      self.watch_flags = flags.CREATE | flags.DELETE | flags.MODIFY | flags.DELETE_SELF

  def add_watchers(self):
      # need to watch httpboot in case new dirs are created
      if self.debug:
          print("Adding watcher for: " + self.httpboot_dir_path)
      wd = self.inotify.add_watch(self.httpboot_dir_path, self.watch_flags)
      menu_dirs = glob.glob(self.httpboot_dir_path + '/*')
      for menu_dir in menu_dirs:
          # need to watch sub-directory in case new boot-menu-entry is created
          if self.debug:
              print("Adding watcher for: " + menu_dir)
          wd = self.inotify.add_watch(menu_dir, self.watch_flags)
          path = menu_dir + '/' + self.boot_menu_entry_file_name
          if(os.path.isfile(path)):
              if self.debug:
                  print("Adding watcher for: " + path)
              wd = self.inotify.add_watch(path, self.watch_flags)

  def is_something_changed(self):
      changed = False
      for event in self.inotify.read():
          changed = True
          if self.debug:
              print(event)
              for flag in flags.from_mask(event.mask):
                  print('    ' + str(flag) + "\n")
          else:
              return changed
      return changed


def create_boot_ipxe(boot_ipxe_file_name, httpboot_dir_path, boot_menu_entry_file_name):
  menu_dirs = glob.glob(httpboot_dir_path + '/*')
  menu_items = ''
  menu_entries = ''
  for menu_dir in menu_dirs:
      path = menu_dir + '/' + boot_menu_entry_file_name
      if(os.path.isfile(path)):
          menu_entry = os.path.basename(menu_dir)
          menu_items += 'item ' + menu_entry + ' ' + menu_entry + '\n'

          menu_entries += ':' + menu_entry + '\n'
          boot_menu_entry_file = open(path, 'r')
          menu_entries += boot_menu_entry_file.read() + '\n'
          boot_menu_entry_file.close()
      
  block1 = "#!ipxe \n" \
           "\n" \
           "menu PXE Boot Options\n" \
           "\n" 

  block2 = "\n" \
           "item shell iPXE shell\n" \
           "item exit  Exit to BIOS\n" \
           "\n" \
           "choose --default exit --timeout 10000 option && goto ${option}\n" \
           "\n"

  block3 = "\n" \
           ":shell\n" \
           "shell\n" \
           "\n" \
           ":exit\n" \
           "exit\n"

  boot_ipxe_file = open(boot_ipxe_file_name,"w")
  boot_ipxe_file.write(block1)
  boot_ipxe_file.write(menu_items)
  boot_ipxe_file.write(block2)
  boot_ipxe_file.write(menu_entries)
  boot_ipxe_file.write(block3)
  boot_ipxe_file.close()

if __name__ == "__main__":
  create_boot_ipxe(boot_ipxe_file_name, httpboot_dir_path, boot_menu_entry_file_name)
  whb = WatchHttpboot(httpboot_dir_path,boot_menu_entry_file_name, debug = False)
  while True:
      whb.add_watchers()
      time.sleep(5)
      if(whb.is_something_changed()):
          create_boot_ipxe(boot_ipxe_file_name, httpboot_dir_path, boot_menu_entry_file_name)
