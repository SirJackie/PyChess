set objShell=wscript.createObject("wscript.shell")
iReturn=objShell.Run("cmd.exe /C python .\\ChessUI\\TkinterControlee.py", 0, TRUE)
