from cx_Freeze import setup, Executable

base = None


executables = [Executable("MainMdiProgram.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "SQL Conversion",
    options = options,
    version = "0.5",
    description = 'SQL Conversion',
    executables = executables
)