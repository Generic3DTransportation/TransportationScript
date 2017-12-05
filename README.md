# TransportationScript
**How to install MayaCharm**
--------
Maya integration with run and debug configurations for Maya. MayaCharm lets you execute the current document or
arbitrary code as if it was in Maya from PyCharm. For users of the professional version of PyCharm it will also setup
and connect the pydev debugger to Maya as well.

For those simply just wanting the compiled version, you are best to just search for it, in the plugin repository of PyCharm.
https://plugins.jetbrains.com/plugin/8218?pr=pycharm

**Verbindung zwischen Maya und PyCharm herstellen**
--------
Unter <Laufwerk>\Users\<user>\Documents\maya\2018\scripts ein Script namens userSetup.py reinhauen:
```
    import maya.cmds as cmds
    if not cmds.commandPort(':4434', q=True):
      cmds.commandPort(n=':4434') 
``` 

**Script vorbereiten für Maya**
--------
Beim File das Script angeben und dann sollte das offene Maya File Änderungen des Scripts ändern.
![MayaCharm Debugger Panel](http://rightsomegoodgames.ca/assets/images/MayaCharm/MCDebuggerConfig.PNG)
