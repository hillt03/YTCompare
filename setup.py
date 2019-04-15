from cx_Freeze import setup, Executable
import os.path

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

buildOptions = dict(excludes = ["tkinter"], includes =["idna.idnadata"], optimize=1)

setup(
      options = dict(build_exe = buildOptions),
      name="YTCompare",
      version="1.0",
      description="A GUI tool to compare YouTube playlist songs to songs on" +
                  " your local machine and outputs a text file with" +
                  " links to missing songs.",
       executables = [Executable(script="YTCompare.py", base="Win32GUI")]
       )
