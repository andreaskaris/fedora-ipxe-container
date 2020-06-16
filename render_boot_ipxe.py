#!/usr/bin/python3

import os 
import glob
import re
import time
from inotify_simple import INotify, flags
from jinja2 import Template
from jinja2 import Environment, BaseLoader, select_autoescape

dir_path = os.path.dirname(os.path.realpath(__file__))

boot_ipxe_file_name = '/tftpboot/menu/boot.ipxe'
httpboot_dir_path = '/httpboot'
boot_menu_entry_file_name = 'boot-menu-entry'
config_path = dir_path
config_file = config_path + '/' + 'config'

'''
Watch directory /httpboot for modifications
Watch for changes in this directory, in the subdirectories and
in file boot-menu-entry
'''
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


'''
Parse config file and environment variables 
'''
class ParseConfig:
  
  cfg = {}

  def __init__(self):
      self.cfg = self.parse_config()

  """
  Parse config files with syntax key=value
  """
  def parse_config(self):
    v = {}
    self.parse_config_file(v,config_file)
    self.parse_environment(v)
    return v
  
  def parse_config_file(self, v, config_file):
      with open(config_file) as myfile:
          for line in myfile:
              name, var = line.partition("=")[::2]
              v[name.strip()] = var.strip()
  
  def parse_environment(self, v):
      for key in v:
          try:
              v[key] = os.environ[key]
          except:
              pass

'''
Take individual boot-menu-entry files, 
replace jinja2 and combine them in /tftpboot/menu/boot.ipxe
'''
class BootIPXE:

  boot_ipxe_file_name = ''
  httpboot_dir_path = ''
  boot_menu_entry_file_name = ''
  cfg = None

  def __init__(self, boot_ipxe_file_name, httpboot_dir_path, boot_menu_entry_file_name):
      self.boot_ipxe_file_name = boot_ipxe_file_name
      self.httpboot_dir_path = httpboot_dir_path
      self.boot_menu_entry_file_name = boot_menu_entry_file_name
      parse_config = ParseConfig()
      self.cfg = parse_config.cfg

  def create_boot_ipxe(self):
        menu_dirs = glob.glob(self.httpboot_dir_path + '/*')
        menu_items = ''
        menu_entries = ''
        for menu_dir in menu_dirs:
            path = menu_dir + '/' + self.boot_menu_entry_file_name
            if(os.path.isfile(path)):
                menu_entry = os.path.basename(menu_dir)
                menu_items += 'item ' + menu_entry + ' ' + menu_entry + '\n'
  
                # add menu entry header
                menu_entries += ':' + menu_entry + '\n'
                # read content from boot menu file in directory
                boot_menu_entry_file = open(path, 'r')
                boot_menu_entry_content = boot_menu_entry_file.read()
                boot_menu_entry_file.close()

                # parse any jinja2 in boot menu file and replace with cfg
                t = Environment(loader=BaseLoader()).from_string(boot_menu_entry_content)
                rendered_boot_menu_entry_content = t.render(self.cfg)
                menu_entries += rendered_boot_menu_entry_content + '\n'
            
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
  
        boot_ipxe_file = open(self.boot_ipxe_file_name,"w")
        boot_ipxe_file.write(block1)
        boot_ipxe_file.write(menu_items)
        boot_ipxe_file.write(block2)
        boot_ipxe_file.write(menu_entries)
        boot_ipxe_file.write(block3)
        boot_ipxe_file.close()

if __name__ == "__main__":
  boot_ipxe = BootIPXE(boot_ipxe_file_name, httpboot_dir_path, boot_menu_entry_file_name)
  boot_ipxe.create_boot_ipxe()
  whb = WatchHttpboot(httpboot_dir_path,boot_menu_entry_file_name, debug = False)
  while True:
      whb.add_watchers()
      time.sleep(5)
      if(whb.is_something_changed()):
          boot_ipxe.create_boot_ipxe()

