Hey there. Thanks for downloading Snappy! Let me know what you think!

Purpose:
small little widget to rest in the macOS menu bar and take pictures on a timer for you to look back on. You have the option to change the timer and turn on photo filters.
made using rumps, cv2, and pyqt6



Since Apple is a very annoying operating system and Snappy uses your camera, the applet I created using Pyintsllaer doesn't work. (unless you're on older versions of MacOS) (Please let me know if you have a work-around)


______________________________
Way 1 - Run the native python files
Run the exec file located in the Python-Launch file

______________________________
Way 2 - Turn the Python script into a double-click exec

On Terminal, I ran which python3 and copy-pasted the result at the start of my python script, preceded with #!
Then I changed the extension of my python file to .command
On Terminal, I ran the command chmod +x fileName.command (755 instead of +x works too)

(solution provided by Sana Mumtaz on Stack Overflow)
