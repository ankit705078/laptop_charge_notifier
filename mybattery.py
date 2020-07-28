import psutil
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import threading
import winsound
import gc

#pycaw initialization for getting sound devices and interfacesa
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

frequency = 2500                          # Setting Frequency To 2500 Hertz
duration = 1000                           # Setting Duration To 1000 ms == 1 second

#function to check and alarm when battery reaches 35% and is not charging
def mainfunc():
    batteryobj=psutil.sensors_battery()
    pluggedinstatus=False
    batterypercentage=0
    threading.Timer(5.0,mainfunc).start()                       #every 5 seconds
    pluggedinstatus = batteryobj.power_plugged
    batterypercentage = int(str(batteryobj.percent))

    if(batterypercentage <=40 and pluggedinstatus==False ):      #if battery falls below or to 35% sound will be made
        volume.SetMute(0, None)                                 #unmuted
        volume.SetMasterVolumeLevel(-1.0, None)                  # 0.0 ->100%   -1 --> less than 100 and so on
        winsound.Beep(frequency, duration)
        print("PLUG IN THE CHARGER BATTERY IS: ",batterypercentage)

    del batteryobj
    del batterypercentage
    del pluggedinstatus
    gc.collect()


mainfunc()