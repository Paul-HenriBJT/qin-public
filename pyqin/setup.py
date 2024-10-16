from setuptools import setup, find_packages

setup(
    name='ws_audio_client',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'websockets>=10.0',
        'pyaudio>=0.2.11',
        'numpy>=1.18.5',
        'requests>=2.25.1'
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A client package to interact with the websocket audio server.',
    url='https://github.com/yourusername/ws_audio_client',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
