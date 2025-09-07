#!/bin/bash
#
ps awux |grep ssh|grep albator|grep -v grep|awk '{print "kill " $2}'|bash
