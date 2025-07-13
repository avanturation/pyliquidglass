import platform


def check_running_tahoe() -> bool:
    mac_version = platform.mac_ver()[0]
    if int(mac_version.split(".")[0]) < 26:
        return False

    return True