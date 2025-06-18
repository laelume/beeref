from setuptools import setup

setup(
    entry_points={
        'console_scripts': [
            'beeref=beeref.main:main',
            'beeref-cli=beeref.cli:cli_main',
        ],
    }
)
