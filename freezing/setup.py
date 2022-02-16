from cx_Freeze import setup, Executable

setup(
    name="examplescript",
    version="1",
    description="Freezing example",
    executables=[Executable("script.py")]
)
