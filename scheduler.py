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
Slots = namedtuple("Slots",'max used')

class Slots(object):
    def __init__(self,max,used):
        self.max = max
        self.used = used
    def __repr__(self):
        return "Slots(%r,%r)" % (self.max, self.used);


def run(args):
    with open(args.jobsfile) as f:
        jobs_list = f.read().splitlines()

    with open(args.hostfile) as f:
        hosts_list = f.read().splitlines()

    resources = calc_resources(args,hosts_list)

    running_jobs = []
    while jobs_list:
        avail_slots = get_available_slots(resources)
        if avail_slots:
            for host in avail_slots:
                if jobs_list:
                    resources[host]['slots'].used +=1;
                    job = jobs_list.pop();
                    running_jobs.append( (host,job) )
                    schedule(host,job)
        for host,job in running_jobs:
            if is_finished(job) :
                resources[host]['slots'].used -= 1; #Free Up Slot

def is_finished(j0b):
    return True
    


def get_available_slots(resources):
    avail_hosts = []
    for node_name,node_info in resources.items():
        if node_info['slots'].used < node_info['slots'].max:
            number_of_slots = node_info['slots'].max - node_info['slots'].used
            avail_hosts.extend([node_name] * number_of_slots)

    return avail_hosts
        
    

def schedule(node_name,job):
    #"ssh node_name ; job";
    #popen(job);
    print(node_name, job)

    
#Checking available resources for each node
# Return Resources
# Resources contains a dict of 
#

def calc_resources(args,hosts_list):    
    resources = {}
    for host in hosts_list:
        host_resources= get_resource_for_host(host)
        max_proc = calc_max_procs(host_resources,args)
        resources[host] = dict(resources=host_resources,slots=Slots(max_proc,0))
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
