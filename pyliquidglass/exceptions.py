class UnsupportedOSVersionError(Exception):
    def __str__(self):
        return "Unsupported macOS version. Check that you are running macOS 26 or later."

class NoNSGlassEffectViewError(Exception):
    def __str__(self):
        return "Cannot find NSGlassEffectView class. Check that you are running macOS 26 or later."