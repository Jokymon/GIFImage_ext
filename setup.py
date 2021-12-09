import pathlib
from setuptools import setup, Command
from shutil import rmtree

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()


class CleanDistCommand(Command):
    """Command to clean out any previous build products."""

    description = 'Remove any previous build products'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            rmtree(HERE / 'pygame_animatedgif.egg-info')
            rmtree(HERE / 'build')
            rmtree(HERE / 'dist')
        except OSError:
            pass


setup(
    name="pygame-animatedgif",
    version="0.1.0",
    description="A sprite based PyGame class to use animated GIFs",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Jokymon/GIFImage_ext",
    author="Silvan Wegmann",
    author_email="pygame_animatedgif@narf.ch",
    license="",
    classifiers=[
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: pygame",
    ],
    packages=["pygame_animatedgif"],
    include_package_data=True,
    install_requires=["pygame", "Pillow"],
    cmdclass={
        'cleandist': CleanDistCommand,
    },
)
