# SublimeText Nautilus Extension
#
# Place me in ~/.local/share/nautilus-python/extensions/,
# ensure you have python-nautilus package, restrart Nautilus, and enjoy :)
#
# Based on cra0zy's script for VSCode.
# Modified for Sublime by Przemas.

from gi import require_version

require_version("Gtk", "3.0")
require_version("Nautilus", "3.0")
from gi.repository import Nautilus, GObject
from subprocess import call
import os

# path to vscode
SUBL = "subl"

# what name do you want to see in the context menu?
SUBLNAME = "SublimeText"

# always create new window?
NEWWINDOW = True


class SublimeTextExtension(GObject.GObject, Nautilus.MenuProvider):
    def launch_sublime(self, menu, files):
        safepaths = ""
        args = ""

        for file in files:
            filepath = file.get_location().get_path()
            safepaths += '"' + filepath + '" '

            # If one of the files we are trying to open is a folder
            # create a new instance of vscode
            if os.path.isdir(filepath) and os.path.exists(filepath):
                args = "-wn "

        if NEWWINDOW:
            args = "-wn "

        call(SUBL + " " + args + safepaths + "&", shell=True)

    def get_file_items(self, window, files):
        item = Nautilus.MenuItem(
            name="SublimeTextOpen",
            label="Open In " + SUBLNAME,
            tip="Opens the selected files with SublimeText",
        )
        item.connect("activate", self.launch_sublime, files)

        return [item]

    def get_background_items(self, window, file_):
        item = Nautilus.MenuItem(
            name="SublimeOpenBackground",
            label="Open in " + SUBLNAME,
            tip="Opens SublimeText in the current directory",
        )
        item.connect("activate", self.launch_sublime, [file_])

        return [item]
