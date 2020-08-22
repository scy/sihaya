# Sihaya

This is a color scheme based on the [Visual Studio Code](https://code.visualstudio.com/) [_One Dark Pro_](https://binaryify.github.io/OneDark-Pro/) colors.
It contains a full 16 color [ANSI palette](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors) for use in terminal emulators, other editors etc.

## Screenshot

![Screenshot of a color table](color-table.png)

## Design Goals

1. Create any colors needed **programmatically**, based on the original _One Dark Pro_ colors.
2. Represent **the usual ANSI colors**. There are some people who get really creative with color schemes that basically contain only three colors in different variations. This can look beautiful, but once you have a diff where the added lines are yellow and the removed lines are a slightly lighter yellow, it gets annoying.
3. Allow **creating configuration files** for all the terminal emulators the author ([@scy](https://github.com/scy)) is using.
4. If there are things that suck (according to me) in the original theme, try to **fix them**.

## Status

I'm using it on several of my machines and kind of happy with it.
Expect only minor changes to the colors, if any.
The code that generates the output files will be improved at some point.

This is pretty much a personal project, the colors have to be pleasing to _me_.
If you like them too, that’s great, and if you have improvements to suggest, file an issue.

* Bugs will probably be fixed.
* Pull requests that add support for other editors will likely be accepted.
* Pull requests that change the color values must have a good reason. Maybe file an issue first or contact me in some other way before investing too much time. That said, if you think you’re improving readability or aesthetics without diverging too much from the original colors, I’m totally interested.

## Supported Terminals/Editors

* Linux Console (text/framebuffer mode)
  * either via a shell script (by sending escape codes) or kernel command line parameters
* [Termux](https://termux.com/)
* Windows Console (`cmd.exe`)
* xterm (via `.Xresources` file)

Visual Studio Code users should instead install the original [_One Dark Pro_ extension](https://marketplace.visualstudio.com/items?itemName=zhuangtongfa.Material-theme) that this project is based on.

Planned:

* [Windows Terminal](https://github.com/Microsoft/Terminal)

## Building

Make sure to also clone the `onedark-pro` submodule when cloning this repo.
Then, make sure the [colormath](https://python-colormath.readthedocs.io/) library is available.
I'm providing [Pipenv](https://docs.pipenv.org/) files to get it.

Fire up `convert.py`.
It will create several configuration files in the `out` directory and even create that if it doesn't exist because awesome UX.

You can also access the conversion logic from your own code by `import`ing `convert`.
Read the code for more information.

## Differences to Previous Projects

This project supersedes the [_Unexciting_](https://github.com/scy/unexciting) theme only two days after its initial creation.
This is because after creating _Unexciting_, I found out that creating a VS Code theme is more work that I want to invest.
Therefore, I had to choose an existing theme and create the terminal palettes based on it.

## Previous Name

This project was called _One Dark Pro Everywhere_ until 2020-05-29.
In order to increase readability on colored backgrounds, I have modified the original color values quite a lot, and I don’t think it’s fair to still call these colors _One Dark Pro_.

The new name _Sihaya_ is a word from Frank Herbert’s _Dune_ novels and roughly translates to “desert spring”.

## License

MIT, see [LICENSE.txt](LICENSE.txt).
