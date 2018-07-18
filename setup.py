from distutils.core import setup
setup(name='awsup',
      version='0.1.1',
      py_modules=['awsup'],
      install_requires=[
          'boto3',
          'requests'
      ],
      scripts=['awsup/awsup.py']
      )
