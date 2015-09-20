#! /usr/bin/env python

__author__ = 'Josef Ludvicek <josef.ludvicek.cz@gmail.com>'

import subprocess
import re

import socket
import sys

IPv4_REGEX = re.compile(r'.*inet (\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3})', re.MULTILINE)

# check ifconfig and type name of your network interface (maybe it's eth0 ?)
# optionally interface name can be passed as first argument when executing script
DEFAULT_INTERFACE_NAME = 'enp0s25'


def get_interface_name():
    """
    Get interface name from script argument or use default one

    :return: network interface name (eg. eth0)
    """

    ifce = DEFAULT_INTERFACE_NAME
    if len(sys.argv) > 1:
        ifce = sys.argv[1]
    print "Setting hostname for interface: %s" % ifce
    return ifce


def exec_bash(command):
    """
    Execute given command in bash

    :param command: command to invoke in bash
    :return: stdout string of executed command
    """
    bash_result = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()
    if len(bash_result) < 1:
        raise Exception("failed to execute command %s", command)

    return bash_result[0]


interface = get_interface_name()

result = exec_bash('ifconfig')

result = result.split('\n\n')
result = map(lambda line: tuple(line.split(': ')), result)
result = filter(lambda x: len(x) == 2, result)

interfaces = {}
for ifce, cfg in result:
    ips = IPv4_REGEX.findall(cfg)
    if len(ips) > 0:
        interfaces[ifce] = ips[0]

print "found interfaces: %s" % interfaces

ip = interfaces.get(interface, None)
if ip is None:
    raise Exception("interface %s not found" % interface)

print ip
hostname = socket.gethostbyaddr(ip)[0]
print "resolved hostname: %s" % hostname

subprocess.Popen(['hostname', hostname])

print "hostname is:"
subprocess.Popen('hostname')
