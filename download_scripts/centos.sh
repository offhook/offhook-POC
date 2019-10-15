#!/bin/bash
# Source: https://access.redhat.com/solutions/10154

# TODO: Enable EPEL repository

#(RHEL5)
# yum install yum-downloadonly

#(RHEL6)
# yum install yum-plugin-downloadonly

yum install --downloadonly --downloaddir=$DOWNLOAD_DIR $*
