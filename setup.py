# Grizzly Setup

import setuptools

setuptools.setup(
    name='layout-quickcheck',
    package_dir={
        "": "src"
    },
    packages=setuptools.find_packages(where="src"),
    # packages=[
    #     "lqc", 
    #     "lqc_runner",
    #     "grizzly"
    #     ],
    version='1.0.0',
    install_requires=[
        'grizzly-framework',
    ],
    entry_points={
       "grizzly_adapters": ["lqc = lqc_grizzly.lqc_adapter:LayoutQuickCheckAdapter"]
    },
)
