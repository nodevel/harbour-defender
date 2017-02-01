#!/usr/bin/python3


APP_NAME = 'defender'
APP_DIR = '/usr/share/harbour-' + APP_NAME + '/qml/python'

import sys
sys.path.insert(0, APP_DIR)
from python_hosts import Hosts, HostsEntry
from copy import deepcopy
import os
import configparser
from shutil import copyfile
import json
import time
from subprocess import check_output


#APP_DIR = '/opt/sdk/harbour-' + APP_NAME + '/usr/share/harbour-' + APP_NAME + '/qml/python''

CONFIG_HOME_DIR = '/home/nemo/.config/harbour-' + APP_NAME
CONFIG_ETC_DIR = '/etc'

CONFIG_ETC_PATH = CONFIG_ETC_DIR + '/' + APP_NAME + '.conf'
CONFIG_HOME_PATH = CONFIG_HOME_DIR + '/' + APP_NAME + '.conf'
CONFIG_APP_PATH = APP_DIR + '/' + APP_NAME + '_default.conf'

UPDATE_FILE_PATH = CONFIG_HOME_DIR + '/' + 'update'

LOGFILE_LAST = '/var/log/'+ APP_NAME +'_last.json'


whitelist = []
urls = []
whitelist_priority = True # whether the whitelist should surpass the blacklist in .editable files
sanitize = True

tmp_dir = '/tmp'
tmp_hosts = '/tmp/hosts'
native_dir="/etc"
native_hosts="/etc/hosts"
android1_dir="/system/etc"
android1_hosts="/system/etc/hosts"
android2_dir="/opt/alien/system/etc"
android2_hosts="/opt/alien/system/etc/hosts"


def load_sources():
    urls = []
    #zip_urls = []
    config_etc = configparser.ConfigParser()
    config_etc.read(CONFIG_ETC_PATH)
    config_home = configparser.ConfigParser()
    config_home.read(CONFIG_HOME_PATH)
    whitelist = []
    whitelist_priority = True
    sanitize = True

    for entry in config_etc.sections():
        if entry in ['SETTINGS', 'DEFAULT']:
            wlan_only = config_home.getboolean("SETTINGS", "WlanOnly", fallback = config_etc.getboolean("SETTINGS", "WlanOnly", fallback = True))            
            whitelist = config_etc.get("SETTINGS", "HostsWhitelist", fallback = '')
            if whitelist:
                whitelist = whitelist.split(',')
            whitelist_priority = config_etc.getboolean("SETTINGS", "HostsWhitelistPriority", fallback = True)
            sanitize = config_etc.getboolean("SETTINGS", "SanitizeSourcedAddresses", fallback = True)
        else:
            print(config_etc.get(entry, 'Url'))
            print(config_etc.getboolean(entry, 'sourceenabled', fallback=None))
            print(config_home.getboolean(entry, 'sourceenabled', fallback=None))
            enabled = config_home.getboolean(entry, 'sourceenabled', fallback = config_etc.getboolean(entry, 'sourceenabled', fallback = False))
            if enabled:
                urls.append(config_etc[entry]['Url'])
    if len(urls) > 0:
        # getting remote urls
        if wlan_only and "Not connected" in check_output(["iw", "dev", "wlan0", "link"]).decode("utf-8"):
            print("WLAN not connected")
            urls = []
    return urls, whitelist, whitelist_priority, sanitize

urls, whitelist, whitelist_priority, sanitize = load_sources()

def write_hosts(hosts, path, editable_path=None, whitelist=whitelist):
    if not editable_path:
        editable_path = path + ".editable"
    check_hosts(editable_path)
    hosts_obj = deepcopy(hosts)
    if whitelist_priority:
        hosts_obj.import_file(editable_path)
    # whitelist functionality
    for entry in whitelist:
        hosts_obj.remove_all_matching(name=entry)
    if not whitelist_priority:
        hosts_obj.import_file(editable_path)
    hosts_obj.write(path=path)
    return True

def rebuild_hosts(path, android=False):
    new_hosts = Hosts()
    #new_hosts.add(entry_type = 'comment', comment = ">> created by hosts-adblock-plus <<")
    if not android:
        new_hosts.add(entries = [
            HostsEntry(entry_type = 'ipv4',
                       address = '127.0.0.1', names = ['localhost.localdomain', 'localhost']),
            HostsEntry(entry_type = 'ipv6',
                       address = '::1', names = ['localhost6.localdomain6', 'localhost6'])
        ])
    new_hosts.write(path)

def check_hosts(path, android=False):
    if android1_hosts in path:
        android = True
    if not os.path.isfile(path):
        rebuild_hosts(path, android)

def update(remote_urls = urls):
    """
    Main update function - takes a list of remote source URLs, writes all available hosts and returns 0.
    """
    hosts = Hosts(path=tmp_hosts)
    # Adding the default entries for all host files
    hosts.add(entries = [
        HostsEntry(entry_type = 'ipv4',
                    address = '127.0.0.1', names = ['localhost.localdomain', 'localhost'])
    ])
    # Adding remote sources
    for url in remote_urls:
        print(url)
        hosts.import_url(url=url, sanitize = sanitize)
    write_hosts(deepcopy(hosts), android1_hosts)
    write_hosts(deepcopy(hosts), android2_hosts)
    
    # Adding the default entries for the native host file
    hosts.add(entries = [
        HostsEntry(entry_type = 'ipv6',
                    address = '::1', names = ['localhost6.localdomain6', 'localhost6'])
    ])
    write_hosts(deepcopy(hosts), native_hosts)
    if os.path.isfile(tmp_hosts):
        os.remove(tmp_hosts)
    data = {
        'time': time.time(),
        'sources': len(remote_urls)
        }
    with open(LOGFILE_LAST, 'w') as outfile:
        json.dump(data, outfile)
    return 0

def reset_hosts():
    return update(remote_urls = [])



if __name__ == '__main__':
    if not os.path.isfile(CONFIG_ETC_PATH):
        copyfile(CONFIG_APP_PATH, CONFIG_ETC_PATH)
    update(urls)
    if os.path.isfile(UPDATE_FILE_PATH):
        os.remove(UPDATE_FILE_PATH)
