from setuptools import setup

setup(
    name='verificatio',
    version='0.1.0',
    description='A domain possession verification library for everyone',
    author='Fallible',
    author_email='support@vedilink.com',
    url='https://github.com/vedilink/verificatio',
    download_url='https://github.com/vedilink/verificatio/tarball/0.1',
    packages=['verificatio'],
    install_requires=[
        'dnspython',
        'requests',
        'pytest',
        'responses',
    ],
)
