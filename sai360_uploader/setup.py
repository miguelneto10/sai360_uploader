from setuptools import setup, find_packages

setup(
    name='sai360_uploader',
    version='0.1.0',
    description='SAI360 XML Data Uploader',
    author='Miguel Neto',
    author_email='miguel.neto@ambipar.com',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'sai360-upload=sai360_uploader.uploader:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ]
)
