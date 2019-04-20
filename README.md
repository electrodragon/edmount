#!/bin/bash
###########################################
# CHECK IF FOLDER EXIST, IF NOT, CREATE ONE
CFINE () {
    if [ ! -d $1 ]; then
	sudo mkdir -p $1 1> $TRASH 2> $TRASH
    fi
}
# CHECK IF DISK MOUNTED, IF NOT, MOUNT ONE
CIDMINMO () {
    if mount | grep $1 > $TRASH; then
	echo "$1 Already Mounted !"
    else
	sudo mount $1 $2
	if mount | grep $1 > $TRASH; then
	    echo "$1 Mounted @ $2"
	fi
    fi
}
# UNMOUNT FILE SYSTEMS STUFF...
isMounted () {
    if mount | grep $1 > $TRASH; then
	echo "true"
    else
	echo "false"
    fi
}
# CHECK IF DISK UNMOUNTED, IF NOT, UNMOUNT ONE
CIDUINUO () {
    if [ `isMounted $1` == "false" ]; then
	echo "$1 NOT MOUNTED !"
    else
	sudo umount $1
	if [ `isMounted $1` == "false" ]; then
	    echo "$1 UN-MOUNTED SUCCESSFULLY !"
	fi
    fi
}
# UNMOUNTS FUNCTION
UMTOBYN () {
    if [ "$2" == "y" ]; then
	CIDUINUO $1 # UNMOUNT DISK
    fi
}
# GETDUNM FUNCTON
GETDUMN () {
    if [ "$ARG1" != "c" ]; then
	read -p "UNMOUNT DISKS? (y,[n]) :" DUNM
    fi
}
# LAMPP FUNC
SISXAMPP () {
if [ "$1" == "s" ]; then
    sudo $LAMPWAY start 2> $TRASH 1> $TRASH
    echo "LAMPP Started !"
elif [ "$1" == "q" ]; then
    sudo $LAMPWAY stop 2> $TRASH 1> $TRASH
    echo "LAMPP Stopped !"
fi
}
GETLAPMP () {
    if [ "$ARG1" != "c" ]; then
	read -p "LAMPP ? (s/q) [c]:" LAMPP
    fi
}
############################################
ARG1=$1
if [ "$ARG1" == "help" ]; then
    echo "Arguments: c, help"
    echo "c - skips Unmount and Lampp Check"
    exit
fi
############################################
MYWAY="/media/`whoami`"
TRASH="/dev/null"
DISK1="/dev/sda1"
DISK2="/dev/sda2"
M1="${MYWAY}/c"
M2="${MYWAY}/d"
LAMPWAY="/opt/lampp/lampp"

CFINE $M1 # CREATE M1 FOLDER
CFINE $M2 # CREATE M2 FOLDER

CIDMINMO $DISK1 $M1 # MOUNT DISK 1
CIDMINMO $DISK2 $M2 # MOUNT DISK 2

GETDUMN ########-UNMOUNT-############
UMTOBYN $DISK1 $DUNM # UNMOUNT DISK 1
UMTOBYN $DISK2 $DUNM # UNMOUNT DISK 2

GETLAPMP #######-LAMPP-##############
SISXAMPP $LAMPP # MANAGE LAMPP
##############################################
