# Python utility to copy folder using shutil.copytree() method  
import os
import shutil
# Source path
src = '/home/pi/CameraProject/sampleImages'
# Destination path  
dest = '/home/pi/CameraProject/'
destinationName = 'extractableImages'
if os.path.isdir(dest+destinationName):
    destinationName+='Copy'
    
# Copytree
destination = shutil.copytree(src, dest+destinationName)  

# Report
print("Copying from: ", src," to: ", destination)
