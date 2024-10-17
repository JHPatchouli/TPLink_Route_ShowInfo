from setuptools import setup

setup(
name='TPShow',
packages=['TPShow'],
entry_points={
'console_scripts': ['TPShow=TPShow.TPlinkShow:main']
}
)