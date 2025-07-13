import objc
from Cocoa import *

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

    def _resolve_setter(self, obj, key: str):
        for sel_name in [f"set_{key}:", f"set{key.capitalize()}:"]:
            try:
                sel = objc.sel_registerName(sel_name.encode("utf-8"))
                if obj.respondsToSelector_(sel):
                    return sel
            except:
                continue
        return None


    def add_view(self, window: NSWindow) -> int:
        '''
        Addes NSGlassEffectView into frame.
        '''
        frame = window.contentView().frame()
        view = self.NSGlassEffectView.alloc().initWithFrame_(frame)
        view.setAutoresizingMask_(NSViewWidthSizable | NSViewHeightSizable)
        window.contentView().addSubview_(view)

        #self.set_variant(view, 1)

        vid = self._next_id()
        self.view_registry[vid] = view
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
            objc.objc_msgSend(view, sel, variant)
