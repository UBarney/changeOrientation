# https://stackoverflow.com/questions/23768184/programmatically-rotate-monitor/23787146
import win32api as win32
import win32con


def getProfile(name=None, displayIndex=1):
    from profiles import profiles as allProfiles
    if name in allProfiles: return allProfiles[name]
    device = win32.EnumDisplayDevices(None, displayIndex)
    currentOrientation = win32.EnumDisplaySettings(
        device.DeviceName,
        win32con.ENUM_CURRENT_SETTINGS
    ).DisplayOrientation
    for p in allProfiles.values():
        if p['orientation'] != currentOrientation:
            return p

    dm = win32.EnumDisplaySettings(
        device.DeviceName, win32con.ENUM_CURRENT_SETTINGS,
    )

    return {
        "displayIndex": displayIndex,
        "orientation": (currentOrientation + 1) % 4,
        "width": dm.PelsHeight,
        "heigh": dm.PelsWidth,
    }


if __name__ == '__main__':
    profile = getProfile()
    device = win32.EnumDisplayDevices(None, profile['displayIndex'])
    print(f"Rotate device {device.DeviceString},{device.DeviceName} ")

    # https://docs.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-devmodea
    dm = win32.EnumDisplaySettings(
        device.DeviceName, win32con.ENUM_CURRENT_SETTINGS,
    )
    dm.DisplayOrientation = profile["orientation"]
    dm.PelsWidth, dm.PelsHeight = profile["width"], profile["height"]
    print("ok: ", win32.ChangeDisplaySettingsEx(device.DeviceName, dm)==0)
