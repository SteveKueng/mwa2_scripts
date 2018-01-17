# mwa2_scripts
report scripts for mwa2

use munkipkg: https://github.com/munki/munki-pkg to create a pkg.
import it into munki and configure it with a postinstall script.

postscript:
```bash
#!/bin/bash

defaults write /var/root/Library/Preferences/com.github.stevekueng.munkiwebadmin.plist ServerURL -string "http://munkiwebadmin.example.com"
defaults write /var/root/Library/Preferences/com.github.stevekueng.munkiwebadmin.plist authKey -string "QmFzaWMgdGVzdDpwYXNz" #basic auth key created with: python python -c 'import base64; print "Basic %s" % base64.b64encode("USERNAME:PASSWORD")'
```

## settings
'ServerURL': 'http://munkiwebadmin',  
'authKey': '', <- basic authentication key. ```python python -c 'import base64; print "Basic %s" % base64.b64encode("USERNAME:PASSWORD")'```

- /var/root/Library/Preferences/com.github.stevekueng.munkiwebadmin.plist
- /Library/Preferences/com.github.stevekueng.munkiwebadmin.plist
