from setuptools import setup

setup (
    name="clean-folder",
    version="0.1.0",
    packages=["clean_folder"],
    entry_points={
        "console_scripts": [
            "clean-folder = clean_folder.clean:main"
        ]
    },
)