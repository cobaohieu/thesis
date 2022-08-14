#!/bin/bash

cd /home/$SUDO_USER/Pictures/


if [ -d /home/$SUDO_USER/Pictures/C922 ] && [ -d /home/$SUDO_USER/Videos/C922]; then
    echo "Directory already exists"
    echo "Can't make directory C922 and Do not need to create!"
    chmod -R 777 /home/$SUDO_USER/Pictures/C922 /home/$SUDO_USER/Videos/C922

else
    echo "Can't find any directory C922"
    sudo mkdir -v /home/$SUDO_USER/Pictures/C922 /home/$SUDO_USER/Videos/C922 # Shorter version. Shell will complain if you put braces here though
    chmod -R 777 /home/$SUDO_USER/Pictures/C922 /home/$SUDO_USER/Videos/C922
fi
cd - 
pwd
set OPENCV_LOG_LEVEL=OFF
sudo python3 main.py