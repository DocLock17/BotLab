# Final Setup
echo " " &&
echo "Starting Installation ..." &&
echo " " &&
echo "Updating ..." &&
echo " " &&
sudo apt-get update && sudo apt-get upgrade -y && sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y &&
echo " " &&
echo "Installing dependencies ..." &&
echo " " &&
sudo apt-get install software-properties-common build-essential cmake pkg-config python3-dev libatlas-base-dev -y &&
echo " " &&
sudo apt-get install libjasper-dev libqtgui4 python3-pyqt5 libhdf5-dev libhdf5-103 libhdf5-dev -y &&
echo " " &&
sudo apt-get install libjpeg-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libxvidcore-dev -y &&
echo " " &&
sudo apt-get install liblapack-dev libblas-dev libgirepository1.0-dev libpango1.0-dev libv4l-dev -y &&
echo " " &&
sudo apt-get install libx264-dev libtiff5-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev -y &&
echo " " &&
sudo apt-get install libgtk-3-dev libgtk2.0-dev libqtwebkit4 libqt4-test libgl1-mesa-glx libegl1-mesa -y &&
echo " " &&
sudo apt-get install libxtst6 libpango1.0-0 hdf5-tools gconf2-common gvfs-bin gfortran xclip -y &&
echo " " &&
# Bot Specific?
# sudo pip3 install pillow
# sudo pip3 install numpy
sudo apt-get install libopenjp2-7 -y &&
sudo apt install libtiff -y &&
sudo apt install libtiff5 -y &&
# sudo apt-get install libatlas-base-dev
# sudo apt-get install python3-pip
# sudo pip3 install RPi.GPIO
echo " " &&
echo "Installing utilities ..." &&
echo " " &&
sudo apt-get install nodejs npm  tilix  figlet screen links2 elinks hddtemp lm-sensors pv -y &&
echo " " &&
sudo python3 -m pip install --user --upgrade pip &&
echo " " &&
sudo python3 -m pip install --user virtualenv &&
echo " " &&
python3 -m venv env &&
echo " " &&
echo "Installing virtual environment ..." &&
echo " " &&
source env/bin/activate &&
#echo " " >> ~/.bashrc &&
echo "export PATH=/root/.local/bin:$PATH" >> ~/.bashrc &&
echo " " &&
echo "Adding virtual environment to the PATH ..." &&
echo " " &&
echo "Installing virtual environment resources ..." &&
echo " " &&
pip3 install -r packagelist.txt &&
#pip3 install -r https://raw.githubusercontent.com/DocLock17/CameraProject/main/packagelist.txt &&
echo " " &&
pip3 install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-linux_armv7l.whl &&
#pip3 install opencv-contrib-python==4.1.0.25 &&
#pip3 install jupyterlab &&
# jupyter config
echo " " &&
echo "Installing jupyter configuration ..." &&
echo " " &&
jupyter-lab --generate-config -y &&
echo "c.JupyterApp.open_browser = True" >> /home/pi/.jupyter/jupyter_notebook_config.py &&
echo "c.JupyterApp.allow_remote_access = True" >> /home/pi/.jupyter/jupyter_notebook_config.py &&
echo "c.JupyterApp.ip = '10.0.0.201'" >> /home/pi/.jupyter/jupyter_notebook_config.py &&
#echo "c.JupyterApp.ip = 'localhost'" >> /home/pi/.jupyter/jupyter_notebook_config.py &&
echo "c.JupyterApp.port = 8888" >> /home/pi/.jupyter/jupyter_notebook_config.py &&
echo "c.JupyterApp.password = ''" >> /home/pi/.jupyter/jupyter_notebook_config.py
echo " " &&
echo "You will need to restart before changes can take effect ..." &&
echo " " &&
echo "Installation Complete!" &&
echo " "
