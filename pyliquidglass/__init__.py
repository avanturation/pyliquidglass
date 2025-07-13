import objc
from Cocoa import *

try:
    NSGlassEffectView = objc.lookUpClass("NSGlassEffectView")
except Exception:
    NSGlassEffectView = None

class GlassWindow(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        screen = NSScreen.mainScreen()
        frame = screen.frame()
        
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            frame,
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskResizable,
            NSBackingStoreBuffered,
            False,
        )
        self.window.setTitle_("macOS 26 NSGlassEffectView Demo")
        self.window.setOpaque_(False)
        self.window.setBackgroundColor_(NSColor.clearColor())
        self.window.center()
        self.window.makeKeyAndOrderFront_(None)

        content_view = self.window.contentView()

        if NSGlassEffectView:
            glass = NSGlassEffectView.alloc().initWithFrame_(frame)
            glass.setAutoresizingMask_(NSViewWidthSizable | NSViewHeightSizable)
            content_view.addSubview_(glass)
            print("Good")
        else:
            print("No NSGlassEffectView")

if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = GlassWindow.alloc().init()
    NSApp().setDelegate_(delegate)
    app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
    app.activateIgnoringOtherApps_(True)
    app.run()