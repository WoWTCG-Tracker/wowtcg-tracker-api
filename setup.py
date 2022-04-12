from setuptools import setup

setup(
    name='wowtcg-tracker-api',
    version='0.1',
    description='A simple API for WoWTCG cards',
    license='GNU General Public License v3.0',
    license_file='LICENSE',
    author='Karel Bašta',
    author_email='bastakka@email.cz',
    url='https://github.com/bastakka/wowtcg-tracker',
    platforms=['any'],
    packages=['api'],
    include_package_data=True,
    install_requires=[
        'flask',
        'prisma'
    ],
    scripts=[
    ],
)
