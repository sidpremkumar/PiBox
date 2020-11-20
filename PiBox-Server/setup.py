from setuptools import setup
import os

with open('requirements.txt', 'rb') as f:
    install_requires = f.read().decode('utf-8').split('\n')

setup(
    name='PiBox-Server',
    version=1.0,
    # description="Sync pagure and github issues to jira, via fedmsg",
    # author='Ralph Bean',
    # author_email='rbean@redhat.com',
    # url='https://pagure.io/sync-to-jira',
    # license='LGPLv2+',
    # classifiers=[
    #     "Development Status :: 5 - Production/Stable",
    #     "License :: OSI Approved :: GNU Lesser General "
    #         "Public License v2 or later (LGPLv2+)",
    #     "Intended Audience :: Developers",
    #     "Intended Audience :: System Administrators",
    #     "Programming Language :: Python :: 3",
    # ],
    install_requires=install_requires,
    packages=[
        'PiBoxServer',
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            "pibox-server=PiBoxServer.main:main",
        ],
    },
)