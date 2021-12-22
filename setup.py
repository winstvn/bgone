from distutils.core import setup

setup(name='bgone',
      version='0.1',
      packages=['utility', 'cogs'],
      package_dir={
            'utility': 'bgone/utility',
            'cogs': 'bgone/cogs'
      }
     )
