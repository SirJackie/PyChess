import ctypes
import os
import tkinter as tk


osType = None

if os.name == "nt":
    osType = "Windows"
elif os.name == "posix":
    osType = "Linux"
else:
    osType = "Others"


def GetScalingFactor():
    if osType == "Windows":
        scalingFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        return scalingFactor / 100
    else:
        # Linux has no compatibility mode, High DPI is always enabled, so no need to scale
        return 100 / 100


def EnableHighDPIMode():
    if osType == "Windows":
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    else:
        # Linux has no compatibility mode, High DPI is always enabled
        pass


def IsHighDPIModeOpened():
    if osType == "Windows":
        awareness = ctypes.c_int()
        errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
        if awareness.value == 0:
            return False
        else:
            return True
    else:
        # Linux has no compatibility mode, High DPI is always enabled
        return True


def GetScreenResolutionUsingTkinterDPI():
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    return screen_width, screen_height


def GetScreenLowDPIResolution():
    if osType == "Windows":
        # Use Win32 API to get resolution
        user32 = ctypes.windll.user32
        return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    else:
        # Use Tkinter API to get resolution
        return GetScreenResolutionUsingTkinterDPI()


def GetScreenResolution():
    if osType == "Windows":

        # Windows' Window has 2 modes:
        # 1. Low DPI Mode (Compatibility Mode)
        # 2. High DPI Mode (Modern Mode)
        # When in mode 1, GetScreenLowDPIResolution() will return fake resolution (compatible resolution)
        #     We need to first sf = GetScalingFactor(), then do GetScreenLowDPIResolution() * sf
        # When in mode 2, GetScreenLowDPIResolution() will return true resolution
        # Moreover, we need to judge which mode we are inside (using IsHighDPIModeOpened())

        mode = IsHighDPIModeOpened()
        if mode is True:
            # Inside: 2. High DPI Mode (Modern Mode)
            return GetScreenLowDPIResolution()

        elif mode is False:
            # Inside: 1. Low DPI Mode (Compatibility Mode)
            sf = GetScalingFactor()
            w, h = GetScreenLowDPIResolution()
            w *= sf
            h *= sf
            w = int(w)
            h = int(h)
            return w, h

    else:
        # Linux has no compatibility mode, High DPI is always enabled
        # No mode judging issue, so just return GetScreenLowDPIResolution()
        return GetScreenLowDPIResolution()
