from setuptools import setup

package_name = 'hscr'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='suzuki',
    maintainer_email='suzuki@todo.todo',
    description='TODO: Package description',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pub = hscr.20231016_pub_test:main',
            'pub_voice_txt = hscr.pub_voice_enter:main',
            'sub = hscr.20231016_sub_test:main',
            'speech = hscr.20231204_speech:main',
            'sub_gpt = hscr.sub_gpt:main',
        ],
    },
)
