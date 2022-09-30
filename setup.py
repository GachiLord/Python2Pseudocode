from setuptools import setup

setup(name='Python2Pseudocode',
      version='0.5',
      description='CLI-tool and Lib to translate python to c-styled pseudocode for code2flow site',
      url='',
      author='GachiLord',
      author_email='name50525@gmail.com',
      license='GPL-3.0',
      packages=['Python2Pseudocode'],
      install_requires=["pyperclip"],
      zip_safe=False,
      entry_points={
        'console_scripts': [
            'py2ps = Python2Pseudocode.__main__:main'
        ]
      }
      )