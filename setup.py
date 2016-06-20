from setuptools import setup
import rusty_game
with open('requirements.txt') as r:
      requirements = r.read().splitlines()
setup(name='rusty_game',
      version=rusty_game.__version__,
      description='basic adventure game',
      url='http://github.com/martyni/rusty_game',
      author='martyni',
      author_email='martynjamespratt@gmail.com',
      license='MIT',
      packages=['rusty_game'],
      install_requires=requirements,
      zip_safe=False,
      entry_points = {
         'console_scripts': ['rusty_game=rusty_game.main:main'],
      },
      include_package_data=True
      )

