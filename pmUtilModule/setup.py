from setuptools import setup, find_packages

setup(
    name='pmutils',
    version='0.0.5',
    author='Mikuas',
    author_email="email@example.com",
    packages=find_packages(),
    install_requires=[
        "pyautogui",
        "comtypes",
        "pycaw",
        "wmi"
    ]
)
