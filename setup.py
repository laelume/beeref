from setuptools import setup

setup(
    entry_points={
    'gui_scripts': [
        'beeref=beeref.__main__:main',  # existing
    ],
    'console_scripts': [
        'beeref-cli=beeref.cli:cli_main',  # NEW LINE
    ],
}
)
