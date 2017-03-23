#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Job Launcher/Scheduler Tool
"""

from __future__ import print_function, absolute_import, division
import os
import subprocess
import re
from collections import namedtuple
import math

Resources = namedtuple("Resources",'cpu memory')
Job = namedtuple("Job",'cmd status')
Node = namedtuple("Node",'slots_max slots_used')

def run(args):
    with open(args.jobsfile) as f:
	jobs_list = f.readlines()

    with open(args.hostfile) as f:
	hosts_list = f.read().splitlines()

    resources = calc_resources(args,hosts_list)

    while jobs_list:
	schedule(resources,jobs_list.pop())

def schedule(resources,job):
	pass
	
#Checking available resources for each node
#

    	




def calc_resources(args,hosts_list):	
    resources = {}
    for host in hosts_list:
    	host_resources= get_resource_for_host(host)
	max_proc = calc_max_procs(host_resources,args)
	resources[host] = dict(resources=host_resources,max_jobs=max_proc)
    return resources

def calc_max_procs(resources,args):
	if args.mem is None:
		return resources.cpu // args.cpu
	return min(resources.memory // args.mem, resources.cpu // args.cpu)

def get_resource_for_host(hostName):
	resourceCommand = "cat /proc/meminfo /proc/cpuinfo"

	cmd = "ssh {0} {1} ".format(hostName,resourceCommand)
	output = subprocess.check_output(cmd.split())

	procs = len(re.findall("processor", output))
	memory = re.findall("MemFree:\s+(\d+)",output)[0]
	memory = int(int(memory) /1024) 

	print( "# of procs = ", procs )	
	print( "# of mem = ", memory )

	return Resources(int(procs),memory)


if '__main__' == __name__:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hostfile', default=os.getenv('PBS_NODEFILE'))
    parser.add_argument('--cpu', default=1, type=int, help='cpus required for the task/cmd')
    parser.add_argument('--mem', type=int, help='memory required for each task/cmd')
    parser.add_argument('jobsfile', help='tab separated file "directory command"')

    args = parser.parse_args()
    if not args.hostfile:
        parser.error('Use --hostfile or set $PBS_NODEFILE (you might be on the head node)')
    if args.cpu <=0:
        parser.error('# of cores < 1')
    	


    run(args)
