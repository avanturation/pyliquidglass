# pyliquidglass
<div align="center">
<img width="400" alt="Example" src="https://github.com/user-attachments/assets/37326998-b22a-4649-9123-9681cd983bf6" />
  
**Binding Native `NSGlassEffectView` with Python3**
</div>

## Requirements
- macOS 26 Tahoe
- Python3
- PyObjC

## Reference

### class: `LiquidGlass`
```python
from pyliquidglass import LiquidGlass
```
- Initializes the LiquidGlass class. Raises exceptions if macOS is below version 26 (Tahoe) or NSGlassEffectView is unavailable.
- LiquidGlass 인스턴스를 초기화합니다. macOS 26 이상이 아니거나 NSGlassEffectView가 없는 경우 `UnsupportedOSVersionError`, `NoNSGlassEffectViewError`가 발생합니다.

---

### `LiquidGlass.add_view`
```python
LiquidGlass.add_view(NSWindow, corner_radius=16.0, tint_color_hex="#ff0000")
```
- Addes `NSGlassEffectView` into NSWindow.
- 인자로 들어온 `NSWindow`에 `NSGlassEffectView`를 추가합니다.

**Parameters:**

| Name            | Type              | Description (설명)                            |
|-----------------|-------------------|-----------------------------------------------|
| `window`        | `NSWindow`        | 유리 효과를 줄 대상 윈도우 (Target macOS window) |
| `corner_radius` | `float`, optional | 모서리 반경 (Corner radius)   |
| `tint_color_hex`| `str`, optional   | `#RRGGBB` 또는 `#RRGGBBAA` 색상 (Tint color)   |

---

### `LiquidGlass.set_variant`
```python
LiquidGlass.set_variant(view_id, LiquidGlassVariant.CONTROL_CENTER)
```
- Sets variant from `add_view` view id.
- `add_view`에서 리턴받은 ID의 베리언트를 설정합니다.

**Parameters:**

| Name            | Type              | Description (설명)                            |
|-----------------|-------------------|-----------------------------------------------|
| `view_or_id`        | `NSWindow`        | `add_view`에서 받은 View ID값 (View ID from `add_view`) |
| `variant` | `LiquidGlassVariant` | `LiquidGlassVariant`에서 정의된 사전 설정값 중 하나 (Enum value from `LiquidGlassVariant`)   |

---

### `LiquidGlassVariant(IntEnum)`
- Enum defining built-in NSGlassEffectView private variants for `NSGlassEffectView`.
- `NSGlassEffectView`에 내부적으로 정의된 베리언트들의 Enum입니다.

| Name | Value |
|------|-------|
| `REGULAR` | 0 |
| `CLEAR` | 1 |
| `DOCK` | 2 |
| `APP_ICONS` | 3 |
| `WIDGETS` | 4 |
| `TEXT` | 5 |
| `AV_PLAYER` | 6 |
| `FACETIME` | 7 |
| `CONTROL_CENTER` | 8 |
| `NOTIFICATION_CENTER` |
| `MONOGRAM` | 10 |
| `BUBBLES` | 11 |
| `IDENTITY` | 12 |
| `FOCUS_BORDER` | 13 |
| `FOCUS_PLATTER` | 14 |
| `KEYBOARD` | 15 |
| `SIDEBAR` | 16 |
| `ABUTTED_SIDEBAR` | 17 |
| `INSPECTOR` | 18 |
| `CONTROL` | 19 |
| `LOUPE` | 20 |
| `SLIDER` | 21 |
| `CAMERA` | 22 |
| `CARTOUCHE_POPOVER` | 23 |

## Example
```python
import objc
import time
from Cocoa import *

from pyliquidglass import LiquidGlass, LiquidGlassVariant

if __name__ == "__main__":
    glass = LiquidGlass() # Making a new LiquidGlass class

    app = NSApplication.sharedApplication()
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

    view_id = glass.add_view(window) # add NSGlassEffectView into NSWindow
    glass.set_variant(view_id, LiquidGlassVariant.CLEAR) # Sets NSGlassEffectView variants

    app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
    app.activateIgnoringOtherApps_(True)
    app.run()
```

## Contributing
저 사실 개발자 아니라서 풀리퀘 해주시면 매우 ㄱㅅㄱㅅ
