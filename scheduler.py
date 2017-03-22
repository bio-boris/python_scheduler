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

def run(args):
    with open(args.jobsfile) as f:
	jobs_list = f.readlines()

    with open(args.hostfile) as f:
	hosts_list = f.read().splitlines()

    resources = {}
    for host in hosts_list:
    	resources[host] = getResourceForHost(host)
	max_proc = calcMaxProcs(resources[host],args)
	print("Max # of jobs on this node =",max_proc)

	


def calcMaxProcs(resources,args):
	if args.mem is None:
		return resources.cpu // args.cpu
	return min(resources.memory // args.mem, resources.cpu // args.cpu)

def getResourceForHost(hostName):
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
