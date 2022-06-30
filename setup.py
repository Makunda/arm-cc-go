from setuptools import setup

setup(
    name='ARM-CC-GO',
    packages=['ARM-CC-GO'],
    include_package_data=True,
    install_requires=[
        'flask',
        'checksumdir',
        'python-dotenv'
    ],
)