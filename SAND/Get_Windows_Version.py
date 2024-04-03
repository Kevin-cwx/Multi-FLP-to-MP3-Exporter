import platform

def get_windows_version():
    version = platform.platform()
    if 'Windows' in version:
        if '10' in version:
            return 'Windows 10'
        elif '8.1' in version:
            return 'Windows 8.1'
        elif '8' in version:
            return 'Windows 8'
        elif '7' in version:
            return 'Windows 7'
        elif 'Vista' in version:
            return 'Windows Vista'
        elif 'XP' in version:
            return 'Windows XP'
        else:
            return 'Unknown Windows version'
    else:
        return 'Non-Windows OS'

# Get and print the Windows version
windows_version = get_windows_version()
print("Windows version:", windows_version)
