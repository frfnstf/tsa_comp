import sys
from desktop_gui import setup_desktop_app
from mobile_gui import setup_mobile_app

# User decides whether to use the mobile or desktop version
if len(sys.argv) > 1:
    if sys.argv[1] == "desktop":
        # Open the desktop application, starting with the homepage screen
        setup_desktop_app(True)
    elif sys.argv[1] == "mobile":
        # Open the mobile application, starting with the homepage screen
        setup_mobile_app(True)
    else:
        print("Invalid command. Use \'desktop\' or \'mobile\'.")
else:
    # Must specify version
    print("Usage: python3 main.py <version>")