import objc
from Cocoa import *
from threading import Event

from .utils import check_running_tahoe
from .exceptions import UnsupportedOSVersionError, NoNSGlassEffectViewError
from .variants import LiquidGlassVariant


class LiquidGlass():
    def __init__(self):
        self.view_registry = {}
        self._view_id_counter = [0]

        if not check_running_tahoe():
            raise UnsupportedOSVersionError()

        try:
            self.NSGlassEffectView = objc.lookUpClass("NSGlassEffectView")
        except Exception:
            raise NoNSGlassEffectViewError()

    def _next_id(self):
        self._view_id_counter[0] += 1
        return self._view_id_counter[0]

    def _color_from_hex(self, hex_str):
        hex_str = hex_str.strip().lstrip("#").upper()
        if len(hex_str) not in (6, 8):
            return None
        try:
            rgba = int(hex_str, 16)
        except:
            return None

        if len(hex_str) == 6:
            r = ((rgba & 0xFF0000) >> 16) / 255.0
            g = ((rgba & 0x00FF00) >> 8) / 255.0
            b = (rgba & 0x0000FF) / 255.0
            a = 1.0
        else:
            r = ((rgba & 0xFF000000) >> 24) / 255.0
            g = ((rgba & 0x00FF0000) >> 16) / 255.0
            b = ((rgba & 0x0000FF00) >> 8) / 255.0
            a = (rgba & 0x000000FF) / 255.0

        return NSColor.colorWithRed_green_blue_alpha_(r, g, b, a)

    def _resolve_setter(self, obj, key: str):
        for sel_name in [f"set_{key}:", f"set{key.capitalize()}:"]:
            if obj.respondsToSelector_(sel_name):
                return sel_name
        return None


    def _run_on_main_thread(self, func):
        if NSThread.isMainThread():
            func()
        else:
            import threading
            evt = threading.Event()

            def wrapper():
                func()
                evt.set()

            dispatch_sync = objc.dispatch_sync
            dispatch_get_main_queue = objc.dispatch_get_main_queue
            dispatch_sync(dispatch_get_main_queue(), wrapper)
            evt.wait()

    def _create_glass_view(self, window: NSWindow, corner_radius, tint_color_hex):
        content_view = window.contentView()
        frame = content_view.frame()

        glass_view = self.NSGlassEffectView.alloc().initWithFrame_(frame)
        glass_view.setAutoresizingMask_(NSViewWidthSizable | NSViewHeightSizable)

        if corner_radius > 0:
            glass_view.setWantsLayer_(True)
            glass_view.layer().setCornerRadius_(corner_radius)
            glass_view.layer().setMasksToBounds_(True)

        if tint_color_hex:
            color = self._color_from_hex(tint_color_hex)
            if color:
                if hasattr(glass_view, "setTintColor_"):
                    glass_view.setTintColor_(color)
                else:
                    glass_view.setWantsLayer_(True)
                    glass_view.layer().setBackgroundColor_(color.CGColor())

        content_view.addSubview_(glass_view)
        return glass_view

    def add_view(self, window: NSWindow, corner_radius=0.0, tint_color_hex=None) -> int:
        glass_view_container = {}

        def task():
            glass_view_container['view'] = self._create_glass_view(window, corner_radius, tint_color_hex)

        self._run_on_main_thread(task)

        glass_view = glass_view_container.get('view')
        if glass_view is None:
            raise RuntimeError("Failed to create glass view")

        vid = self._next_id()
        self.view_registry[vid] = glass_view
        return vid

    def set_variant(self, view_or_id, variant: int):
        if isinstance(view_or_id, int):
            view = self.view_registry.get(view_or_id)
            if not view:
                raise ValueError(f"No view found for id {view_or_id}")
        else:
            view = view_or_id

        sel = self._resolve_setter(view, "variant")

        if sel:
            method = getattr(view, sel, None)
            if method:
                method(variant)
        else:
            print(f"set_variant: No setter found for 'variant' on {view}")