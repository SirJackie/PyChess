import ctypes


def EnableHighDPISupport():
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    scalingFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
    return scalingFactor


def EnableTkinterHighDPISupport(root, scalingFactor):
    root.tk.call('tk', 'scaling', scalingFactor / 75)


def GetScreenResolution():
    user32 = ctypes.windll.user32
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
