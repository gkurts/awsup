from distutils.core import setup
setup(name='awsup',
      description='A script for removing SSH entries in AWS EC2 security groups and adding your current IP.',
      author='Greg Kurts',
      author_email='gkurts@gregkurts.com',
      url='https://github.com/gkurts/awsup',
      version='0.1.2',
      py_modules=['awsup'],
      install_requires=[
          'boto3',
          'requests'
      ],
      scripts=['awsup/awsup.py'],
      classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'Intended Audience :: System Administrators',
            'License :: Freely Distributable',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.7',
            'Topic :: System :: Networking',
            'Topic :: System :: Networking :: Firewalls',
            'Topic :: System :: Systems Administration',

      ]
      )
