import rumps
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QSettings
import cv2
from Menu_ui import Ui_Dialog
from datetime import datetime
import os, getpass, time, random
import numpy as np

app = QApplication([])

username = getpass.getuser()
config = "/Users/" + username + "/Snappy/config.txt"

def apply_warm_sepia(img):
    # Warmer sepia transformation matrix
    img_sepia = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
    img_sepia = np.array(img_sepia, dtype = np.float64)
    img_sepia = cv2.transform(img_sepia, np.matrix([[0.393, 0.769, 0.189],
                                                    [0.349, 0.686, 0.168],
                                                    [0.272, 0.534, 0.131]]))
    
    img_sepia = np.clip(img_sepia, 0, 255)
    img_sepia = np.array(img_sepia, dtype = np.uint8)
    img_sepia = cv2.cvtColor(img_sepia, cv2.COLOR_RGB2BGR)

    return img_sepia
def replaceline(filepath, line, newtext):
    with open(filepath, 'r') as file: 
        data = file.readlines() 
    data[line-1] = newtext + "\n"
    with open(filepath, 'w') as file: 
        file.writelines(data)

def apply_vignette(img, level = 2):
    height, width = img.shape[:2]  
    
    # Generate vignette mask using Gaussian kernels.
    X_resultant_kernel = cv2.getGaussianKernel(width, width/level)
    Y_resultant_kernel = cv2.getGaussianKernel(height, height/level)
        
    # Generating resultant_kernel matrix.
    kernel = Y_resultant_kernel * X_resultant_kernel.T 
    mask = kernel / kernel.max()
    
    img_vignette = np.copy(img)
        
    # Applying the mask to each channel in the input image.
    for i in range(3):
        img_vignette[:,:,i] = img_vignette[:,:,i] * mask
    
    return img_vignette

def embossed_edges(img):
    
    kernel = np.array([[0, -3, -3], 
                       [3,  0, -3], 
                       [3,  3,  0]])
    
    img_emboss = cv2.filter2D(img, -1, kernel=kernel)
    return img_emboss

def pixelate(img):
    height, width = img.shape[:2]

    w, h = (150, 150)

    # Resize input to "pixelated" size
    temp = cv2.resize(img, (w, h), interpolation=cv2.INTER_LINEAR)

    # Initialize output image
    output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)

    return output


if not os.path.exists("/Users/" + username + "/Snappy"):
    os.makedirs("/Users/" + username + "/Snappy")

if not os.path.exists(config):
    with open(config, 'w') as file:
        file.write("/Users/" + username + "/Snappy\n")
        file.write("Days\n")
        file.write("1\n")
        file.write("0\n")
        file.write("True")
    
else:
    # If the file exists, read the existing values
    with open(config, 'r') as file:
        lines = file.readlines()
        # Set the default folder path if it's not present
        if not lines or not lines[0].strip():
            replaceline(config, 1, "/Users/" + username + "/Snappy")




def replaceline(filepath, line, newtext):
    with open(filepath, 'r') as file: 
        data = file.readlines() 
    data[line-1] = newtext + "\n"
    with open(filepath, 'w') as file: 
        file.writelines(data)

with open(config, 'r') as file:
        lines = file.readlines()

timetype = lines[1].rstrip()
timeitry = lines[2]




if timetype == "Days":
    print("Days")
    countdown = int(timeitry)*86400


if timetype == "Hours":
    print("Hours")
    countdown = int(timeitry)*3600
            




class SettingsMenu(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.ui = Ui_Dialog()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)
        self.ui.browse.clicked.connect(self.browsefiles)
        self.ui.Save.clicked.connect(self.savesettings)
        self.load_settings()

    def browsefiles(self):
        # with open(config, 'r') as file:
        #     firstLine = file.readline().rstrip()
        fname = QFileDialog.getExistingDirectory(self, "choose folder")
        if not fname == "":
            self.ui.filename.setText(fname)

    def savesettings(self):
        folderpath = self.ui.filename.text()
        print("This is the folderpath" + folderpath)

        cameratype = self.ui.CameraType.value()
        delay = self.ui.DelayTime.value()

        if self.ui.days.isChecked():
            time_type = "Days"
        elif self.ui.hours.isChecked():
            time_type = "Hours"

        filters_enabled = self.ui.filters.isChecked()


        

        print("Time Type:   ", time_type)
        print("Folderpath:  ", folderpath)
        print("cameratype:  ", cameratype)
        print("delay:       ", delay)
        print("Filters:     ", "Enabled" if filters_enabled else "Disabled")

        settings = QSettings("Egloo", "Snappy")
        settings.setValue("FolderPath", folderpath)
        settings.setValue("DelayTime", delay)
        settings.setValue("CameraType", cameratype)
        settings.setValue("TimeType", time_type)
        settings.setValue("FiltersEnabled", filters_enabled)


        replaceline(config, 1, folderpath)
        replaceline(config, 2, time_type)
        replaceline(config, 3, str(delay))
        replaceline(config, 4, str(cameratype))
        replaceline(config, 5, str(filters_enabled))



    def load_settings(self):
        settings = QSettings("Egloo", "Snappy")
        folderpath = settings.value(
            "FolderPath", "/Users/" + username + "/Snappy")
        delay_time = settings.value("DelayTime", 1)
        cameratype = settings.value("CameraType", 0)
        time_type = settings.value("TimeType", "Days")
        filters_enabled = settings.value("FiltersEnabled", False, bool)

        # Set the values in the UI
        self.ui.filename.setText(folderpath)
        self.ui.DelayTime.setValue(int(delay_time))
        self.ui.CameraType.setValue(int(cameratype))
        self.ui.filters.setChecked(filters_enabled)

        if time_type == "Days":
            self.ui.days.setChecked(True)
        elif time_type == "Hours":
            self.ui.hours.setChecked(True)


class AwesomeStatusBarApp(rumps.App):
    def __init__(self):
        super(AwesomeStatusBarApp, self).__init__("📌", icon = "icon.png", template=True)
        self.repeating_timer = rumps.Timer(self.take_picture, countdown)
        self.repeating_timer.start()

    @rumps.clicked("quick pic")
    def quickpic(self, _):
        with open(config, 'r') as file:
            firstLine = file.readline().rstrip()

        with open(config, 'r') as file:
            lines = file.readlines()


        cap = cv2.VideoCapture(0)
        time.sleep(2)
        ret, frame = cap.read()

        Filters = lines[4].rstrip()
        if Filters == "True":
            filtered_frame = self.apply_random_filter(frame)
        else:
            filtered_frame = frame


        today = datetime.now()
        date = today.strftime("%d-%m-%Y-%H_%M_%S")
        print("save area:   ", firstLine + "/"+date + '.jpg')
        cv2.imwrite(firstLine + "/"+date + '.jpg', filtered_frame)
        cap.release()


    @rumps.clicked("Preferences")
    def settings(self, _):
        dlg = SettingsMenu()
        dlg.exec()
        

    def take_picture(self, _):
        print("timer is a go")
        with open(config, 'r') as file:
                lines = file.readlines()

        directory = lines[0].rstrip()
        cameratype = lines[3].rstrip()
        Filters = lines[4].rstrip()
        print(cameratype)

    

        cap = cv2.VideoCapture(int(cameratype))
        time.sleep(2)
        ret, frame = cap.read()

        if Filters == "True":
            filtered_frame = self.apply_random_filter(frame)
        else:
            filtered_frame = frame

        today = datetime.now()
        date = today.strftime("%d-%m-%Y-%H_%M_%S")
        print("save area", directory + "/"+date + '.jpg')
        cv2.imwrite(directory + "/"+date + '.jpg', filtered_frame)
        cap.release()

    def apply_random_filter(self, frame):
            filters = [
                ("Gray", lambda img: cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)),
                ("Canny", lambda img: cv2.Canny(img, 100, 200)),
                ("Threshold", lambda img: cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 128, 255, cv2.THRESH_BINARY)[1]),
                ("Adaptive_Mean", lambda img: cv2.adaptiveThreshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)),
                ("Solarize", lambda img: cv2.bitwise_not(img)),
                ("Pixelate", lambda img: pixelate(img)),
                ("Warm_Sepia", lambda img: apply_warm_sepia(img)),
                ("Vignette", lambda img: apply_vignette(img)),
                ("Embossed", lambda img: embossed_edges(img)),
            ]

            # Randomly select a filter from the list
            selected_filter_name, selected_filter = random.choice(filters)

            # Apply the selected filter
            return selected_filter(frame)
        

if __name__ == "__main__":
    AwesomeStatusBarApp().run()



