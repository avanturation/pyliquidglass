import objc
import time
from Cocoa import *

from pyliquidglass import LiquidGlass

if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    glass = LiquidGlass()
    screen = NSScreen.mainScreen()
    frame = screen.frame()

    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        frame,
        NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskResizable,
        NSBackingStoreBuffered,
        False,
    )

    window.setTitle_("Testing")
    window.setOpaque_(False)
    window.setBackgroundColor_(NSColor.clearColor())
    window.center()
    window.makeKeyAndOrderFront_(None)

    view_id = glass.add_view(window)
    glass.set_variant(view_id, 8)

    app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
    app.activateIgnoringOtherApps_(True)
    app.run()

    