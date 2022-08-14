# install command line tools
$ xcode-select --install

brew install python3

# if pip not installed
$ sudo easy_install pip
 
# show current pip version
$ pip --version
 
# upgrade pip
——check USB port
system_profiler SPUSBDataType
—install
brew update && brew tap jlhonora/lsusb && brew install lsusb
brew install libusb-compat libusb
sudo pip install python-usb python3-usb
sudo pip install pyusb pywinusb websocket portalocker micropython-fcntl colour termcolor PySimpleGUI PyQt5-sip PyQt5 wiringpi2 pynetworktables pyudev


/——————————————————————/
This is a guide for installing GCC 5.1 on a Mac using MacPorts. It will likely work for later versions of GCC as well. Just substitute "gccx" for "gcc5", where "x" is the desired version.

Download and install Xcode from the Mac App Store.

Download and install the MacPorts "pkg" installer appropriate for your OS version (e.g., Mavericks is 10.9. Go to "Apple menu > About This Mac" if unsure): Installing MacPorts (http://www.macports.org/install.php)

Open a Terminal window and enter "sudo port -v selfupdate".

Enter your password, and wait for the update to finish.

Once it finishes, enter "sudo port install gcc5".

Enter your password if needed. It may take an hour or longer for the download and compile to complete.

Once the install completes, attempt to compile a C++14 source file using the following command: "g++-mp-5 -Wall -std=c++14 Program.cc -o Program". Note there is a hypen between "g++" and "mp".

Thanks to Julius O for the initial instructions!
--------------------


https://osdn.net/projects/mingw/releases/p15691
--------------------

https://github.com/Gadgetoid/WiringPi2-Python

