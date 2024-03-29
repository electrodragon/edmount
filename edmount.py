#!/usr/bin/env python3

import os
import getpass
import sys
import shutil


class Color:
    OK_BLUE = '\033[94m'
    OK_CYAN = '\033[96m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END_LINE = '\033[0m'


def get_proc_mounts_content():
    with open('/proc/mounts', 'r') as mount_proc:
        return mount_proc.readlines()


def text_blue(text):
    print(f'{Color.OK_BLUE}{text}{Color.END_LINE}')


def text_cyan(text):
    print(f'{Color.OK_CYAN}{text}{Color.END_LINE}')


def text_green(text):
    print(f'{Color.OK_GREEN}{text}{Color.END_LINE}')


def text_warning(text):
    print(f'{Color.WARNING}{text}{Color.END_LINE}')


def text_fail(text):
    print(f'{Color.FAIL}{text}{Color.END_LINE}')


class Volume:

    def __init__(self, volume, target):
        self.volume = volume
        self.target = target
        self.is_target_mounted = os.path.ismount(self.target)
        self.is_volume_mounted = False
        self.volume_mount_point = ''
        self.is_volume_mounted_on_target = False
        with open('/proc/mounts', 'r') as mount_proc:
            for lin in mount_proc.readlines():
                lin = lin.split()
                if lin[0] == self.volume:
                    self.is_volume_mounted = True
                    self.volume_mount_point = lin[1]
                    self.is_volume_mounted_on_target = lin[1] == self.target


class VolumeMountUnmount:

    def __init__(self, volume):
        self.volume = volume

    def mount(self):
        if self.volume.is_volume_mounted:
            if self.volume.is_volume_mounted_on_target:
                text_blue(f'{self.volume.volume} already mounted! @ {self.volume.target}')
            else:
                text_warning(f'{self.volume.volume} already mounted here @ {self.volume.volume_mount_point}')
        else:
            if self.volume.is_target_mounted:
                text_fail(f'{self.volume.target} is already mounted by some volume.')
            else:
                if not os.path.exists(self.volume.target):
                    os.system(f'sudo mkdir -p {self.volume.target}')

                os.system(f'sudo mount {self.volume.volume} {self.volume.target}')

                if os.path.ismount(self.volume.target):
                    text_green(f'{self.volume.volume} has been mounted at {self.volume.target}')

                    """
                    unwanted_dirs = [
                        '$Recycle.Bin',
                        'System Volume Information',
                    ]

                    for directory in os.listdir(self.volume.target):
                        if directory.lower() in list(map(lambda d: d.lower(), unwanted_dirs)):
                            unwanted_dir = os.path.join(self.volume.target, directory)
                            if os.path.exists(unwanted_dir):
                                try:
                                    shutil.rmtree(unwanted_dir)
                                    text_blue(f'Deleted Unwanted Dir -> {unwanted_dir}')
                                except OSError as e:
                                    text_blue(f'Something went wrong while deleting unwanted dir -> {unwanted_dir}')
                                    print(e.filename, e.strerror)
                            else:
                                text_blue(f'Directory Could\'t be Located for Removing -> {unwanted_dir}')
                    """

                else:
                    text_fail(f'{self.volume.volume} failed to mount at {self.volume.target}')

    def umount(self):
        if self.volume.is_volume_mounted:
            os.system(f'sudo umount {self.volume.volume}')

            if not os.path.ismount(self.volume.volume_mount_point):
                text_green(f'{self.volume.volume} un-mounted successfully!')

                if not os.path.ismount(self.volume.target):
                    os.system(f'sudo rmdir {self.volume.target}')

                    if not os.path.exists(self.volume.target):
                        text_cyan(f'{self.volume.target} -> Mount point removed!')
                    else:
                        text_fail(f'Failed to remove mount point -> {self.volume.target}')
        else:
            text_blue(f'{self.volume.target} is already un-mounted!')


EDMOUNT_VERSION = 4.0

args_list = [
    ('v', 'Displays Version'),
    ('h', 'Displays Help'),
    ('m', 'Mounts Disks'),
    ('u', 'Unmounts Disks'),
    ('s', 'Starts Lampp'),
    ('q', 'Quits Lampp')
]


def show_manual():
    print("-----------------------------------------------------")
    print("Arguments:")
    for arg, desc in args_list:
        print(f"\t-{arg}\t: {desc}")
    print("-----------------------------------------------------")


MOUNT_ROOT_DIR = f'/run/media/{getpass.getuser()}'

DISKS = [
    ('/dev/sda1', f'{MOUNT_ROOT_DIR}/c'),
    ('/dev/sda2', f'{MOUNT_ROOT_DIR}/d'),
    ('/dev/sda3', f'{MOUNT_ROOT_DIR}/e')
]

DEFAULT_ARGS = ['-ms']
args = sys.argv[1:]

if len(args) == 0:
    args = DEFAULT_ARGS

action = args[0]

if '-' in action:
    action = action.replace('-', '')

    valid_arg = False
    for arg, desc in args_list:
        if arg in action:
            valid_arg = True
            break

    if not valid_arg:
        text_warning("Invalid Argument, use -h for help")
        exit()

    for i in range(0, len(action)):
        if 'h' in action[i]:
            show_manual()
            exit()

        if 'v' in action[i]:
            print(f"Edmount Version: {EDMOUNT_VERSION}")
            exit()

        if 'm' in action[i]:
            for disk, target_path in DISKS:
                VolumeMountUnmount(Volume(disk, target_path)).mount()

        if 'u' in action[i]:
            for disk, target_path in DISKS:
                VolumeMountUnmount(Volume(disk, target_path)).umount()

        if 's' in action[i]:
            os.system('sudo /opt/lampp/lampp start')

        if 'q' in action[i]:
            os.system('sudo /opt/lampp/lampp stop')

else:
    text_warning("Invalid Argument, use -h for help")
