from colormath.color_conversions import convert_color
from colormath.color_objects import HSVColor, sRGBColor
import json


class ThemeConverter:

    odp2ansi = {
        1: "error",         # red
        2: "green",         # green
        3: "chalky",        # yellow
        4: "malibu",        # blue
        5: "purple",        # magenta
        6: "fountainBlue",  # cyan
        7: "lightDark",     # white
    }

    def __init__(self, colorsJSON, variant="classic"):
        colors = json.loads(colorsJSON)[variant]
        self.rgb = {}

        # Create all the colors that are directly taken from One Dark Pro.
        for i, name in self.odp2ansi.items():
            self.rgb[i] = sRGBColor.new_from_rgb_hex(colors[name])

        # Create other colors based on the predefined ones.
        # The original "white" (rather "lightDark") is not light enough.
        # Also, make it warmer by messing with the hue.
        # TODO: Changing hue by _factor_ is nonsense, this could use a better API.
        self.rgb[7] = self.modHSV(self.rgb[7], hFac=0.2, sFac=0.5, vFac=1.7)
        # Background color (aka "black") is based on white.
        self.rgb[0] = self.modHSV(self.rgb[7], sFac=2, vFac=.15)

        # Crank up saturation to the max to increase color-on-colored-background contrast.
        # To compensate, make it darker.
        for i in range(1, 8):
            self.rgb[i] = self.modHSV(self.rgb[i], sFac=2.5, vFac=0.85)

        # "Light" versions are computed from the non-light ones.
        for i in range(1, 7):
            self.rgb[i + 8] = self.modHSV(self.rgb[i], vFac=1.5)
        # Black and white need to be handled specially though to look decent.
        for i in [0, 7]:
            self.rgb[i + 8] = self.modHSV(self.rgb[i], sFac=0.85, vFac=2.3)

        # Finally, create a greenish cursor color.
        self.rgb[16] = self.modHSV(self.rgb[2], sFac=2.5, vFac=1.5)

    def modHSV(self, srgb, hFac=1, sFac=1, vFac=1):
        """Do HSV factor multiplications on a given sRGB color."""
        hsv = convert_color(srgb, HSVColor)
        modified = HSVColor(
            hsv.hsv_h * hFac,
            min(1, hsv.hsv_s * sFac),
            min(1, hsv.hsv_v * vFac),
        )
        return convert_color(modified, sRGBColor)

    def sRGB2dWord(self, srgb):
        """Create a dword value (for Windows registry entries)."""
        tup = srgb.get_upscaled_value_tuple()
        return "dword:{0:08x}".format(tup[0] + (tup[1] << 8) + (tup[2] << 16))

    def toKeyValue(
        self,
        specials={},
        normalFormat="{0}: {1}\n",
        specialFormat='"{0}": {1}\n',
    ):
        result = ""
        for name, idx in specials.items():
            result += specialFormat.format(name, self.rgb[idx].get_rgb_hex())
        for idx in range(16):
            result += normalFormat.format(idx, self.rgb[idx].get_rgb_hex())
        return result

    def toTermux(self):
        return self.toKeyValue(
            specials={
                "cursor": 16,
                "background": 0,
                "foreground": 7,
            },
            normalFormat="color{0}={1}\n",
            specialFormat="{0}={1}\n",
        )

    def toWindowsConsole(self):
        # Console is swapping red and blue as well as yellow and cyan around.
        mapping = [0, 4, 2, 6, 1, 5, 3, 7, 8, 12, 10, 14, 9, 13, 11, 15]
        result = "Windows Registry Editor Version 5.00\r\n" \
            "[HKEY_CURRENT_USER\\Console]\r\n"
        for idx in range(16):
            result += '"ColorTable{0:02d}"={1}\r\n'.format(
                idx, self.sRGB2dWord(self.rgb[mapping[idx]])
            )
        result += '"CursorColor"={0}\r\n'.format(self.sRGB2dWord(self.rgb[16]))
        result += '"ScreenColors"=dword:00000007\r\n'\
            '"PopupColors=dword:00000083\r\n'
        return result

    def toXresources(self):
        return self.toKeyValue(
            specials={
                "cursorColor": 16,
                "background": 0,
                "foreground": 7,
            },
            normalFormat="*.color{0}: {1}\n",
            specialFormat="*.{0}: {1}\n",
        )

    def updateWindowsConsole(self):
        # Update Windows Console colors in-place as an OSC sequence:
        # ESC ] 4 ; <index> ; "rgb:" <rr> "/" <gg> "/" <bb> ESC \
        for idx in range(16):
            hexval = self.rgb[idx].get_rgb_hex()
            print("\x1b]4;{0};rgb:{1}/{2}/{3}\x1b\\".format(idx, hexval[1:3], hexval[3:5], hexval[5:7]), end="")


if __name__ == "__main__":
    from os import makedirs
    conversions = {
        "sihaya.termux.properties": ThemeConverter.toTermux,
        "sihaya.reg": ThemeConverter.toWindowsConsole,
        "sihaya.Xresources": ThemeConverter.toXresources,
    }
    print("Reading input file ...")
    with open("onedark-pro/src/color.json", "r") as file:
        tc = ThemeConverter(file.read())
    makedirs("out", exist_ok=True)
    for filename, method in conversions.items():
        print("Creating " + filename + " ...")
        with open("out/" + filename, "w") as file:
            file.write(method(tc))
