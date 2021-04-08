from setuptools import setup

setup(
    name='CoT_Trackserver',
    version='1.0',
    packages=['CoT_Trackserver'],
    url='',
    license='',
    author='Sven Meuleman',
    author_email='sven.meuleman@telenet.be',
    description='Trackserver GPS trackers to Cursos-on-Target converter',
    keywords=[
        "Cursor on Target", "ATAK", "TAK", "CoT","Trackserver"
    ],
    install_requires=[
        "asyncio"
    ]
)
