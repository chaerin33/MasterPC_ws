from setuptools import find_packages, setup

package_name = 'sml_system_pkg'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='todo',
    maintainer_email='todo@todo.com',
    description='SML 시스템 노드 패키지',
    license='TODO',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'planning_node = sml_system_pkg.planning_node:main',
            'order_server  = sml_system_pkg.order_server:main',
        ],
    },
)
