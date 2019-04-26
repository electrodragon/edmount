#!/bin/bash
edmVersion () {
  echo "-----------------------------------------------------"
  echo -e " !!! ==> edmount version 3.0\n"
  echo " !!! ==> https://github.com/electrodragon/edmount.git"
  echo "-----------------------------------------------------"
  exit 0
}
Show_Manual () {
  echo "-----------------------------------------------------"
  echo "Arguments:"
  echo " v   -  Shows Version !"
  echo " h   -  HELP"
  echo " m   -  Mounts Disks"
  echo " u   -  Unmounts Disks"
  echo " s   -  Starts Lampp"
  echo " q   -  Quits Lampp"
  echo " ms  -  Mounts Disks and Starts Lampp"
  echo " us  -  Unmounts Disks and Starts Lampp"
  echo " mq  -  Mounts Disks and Stops Lampp"
  echo " uq  -  Unmounts Disks and Stops Lampp"
  echo "-----------------------------------------------------"
  exit 0
}
Create_Folder () {
  if [[ "$2" == 'true' ]]; then
    if [ ! -d "$1" ]; then
      sudo mkdir -p $1 1> $TRASH 2> $TRASH
    fi
  fi
}
isMounted () {
  if mount | grep $1 > $TRASH; then
    echo "true"
  else
    echo "false"
  fi
}
Mount_Disk () {
  if [[ "$3" == "true" ]]; then
    if [[ `isMounted $1` == 'true' ]]; then
      echo "$1 is Already Mounted !"
    else
      sudo mount $1 $2
      if [[ `isMounted $1` == 'true' ]]; then
        echo "$1 has been Mounted at $2"
      else
        echo "Sorry ! SomeThing Went Wrong While Mounting $1"
      fi
    fi
  fi
}
Unmount_Disk () {
  if [[ "$2" == 'true' ]]; then
    if [[ `isMounted $1` == 'true' ]]; then
      sudo umount $1 1> $TRASH 2> $TRASH
      if [[ `isMounted $1` == 'false' ]]; then
        echo "$1 Successfully UnMounted !!!"
      else
        echo "$1 May Be Busy, Can't UnMount !"
      fi
    else
      echo "$1 is Already UnMounted !"
    fi
  fi
}
Manage_LAMPP () {
  if [[ "$2" == 'true' ]]; then
    sudo $1 start 1> $TRASH 2> $TRASH
    echo "LAMPP started !"
  elif [[ "$3" == 'true' ]]; then
    sudo $1 stop 1> $TRASH 2> $TRASH
    echo "LAMPP quitted !"
  fi
}
############################################
if [[ "$1" == "help" || "$1" == "h" ]]; then
  Show_Manual
elif [[ "$1" == "v" || "$1" == "V" ]]; then
  edmVersion
elif [[ "$1" == "" ]]; then
  DEFAULT_ARG="m"   # SET YOURS DEFAULT HERE !!!!!!!!!!!!
else
  DEFAULT_ARG=$1
fi
############################################
MountExecution='false'
UnMountExecution='false'
LamppExecution='false'
LamppQuiting='false'
case $DEFAULT_ARG in
  m)
  MountExecution='true'
    ;;
  u)
  UnMountExecution='true'
    ;;
  s)
  LamppExecution='true'
    ;;
  q)
  LamppQuiting='true'
    ;;
  ms)
  MountExecution='true'
  LamppExecution='true'
    ;;
  us)
  UnMountExecution='true'
  LamppExecution='true'
    ;;
  mq)
  MountExecution='true'
  LamppQuiting='true'
    ;;
  uq)
  UnMountExecution='true'
  LamppQuiting='true'
    ;;
  *)
  echo "Wrong Argument Entered !!!"
  Show_Manual
    ;;
esac
############################################
TRASH="/dev/null"
LAMPWAY="/opt/lampp/lampp"
#-------------------------
DISK1="/dev/sda1"
DISK2="/dev/sda2"
#-------------------------
MYWAY="/media/`whoami`"
M1="${MYWAY}/c"
M2="${MYWAY}/d"

Create_Folder $M1 $MountExecution
Create_Folder $M2 $MountExecution

Mount_Disk $DISK1 $M1 $MountExecution
Mount_Disk $DISK2 $M2 $MountExecution

Unmount_Disk $DISK1 $UnMountExecution
Unmount_Disk $DISK2 $UnMountExecution

Manage_LAMPP $LAMPWAY $LamppExecution $LamppQuiting
##############################################
