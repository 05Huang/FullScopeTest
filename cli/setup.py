"""FullScopeTest CLI 安装配置"""

from setuptools import setup, find_packages

setup(
    name='fst-cli',
    version='1.0.0',
    description='FullScopeTest CLI - 测试平台命令行工具',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'requests>=2.28.0',
    ],
    entry_points={
        'console_scripts': [
            'fst=cli.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
