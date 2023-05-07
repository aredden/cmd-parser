from setuptools import setup, find_packages


setup(
    name="cmd_parser",
    version="0.0.1",
    description="Command parser for string argument parsing including unquoted string arguments.",
    author="Alex Redden",
    url="https://github.com/aredden/cmd-parse",
    packages=["cmd_parser"],
    package_dir={"cmd_parser": "cmd_parser"},
    py_modules=["cmd_parser"],
)