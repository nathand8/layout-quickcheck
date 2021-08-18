# Grizzly Setup

import setuptools

setuptools.setup(
    name='layoutquickcheck-adapter',
    package_dir={
        "lqc": "src"
    },
    # packages=setuptools.find_packages("lqc"),
    packages=[
        "lqc", 
        "lqc.grizzly", 
        "lqc.web_page_creation", 
        "lqc.web_page_creation.javascript_with_debugging_tools",
        "lqc.web_page_creation.javascript_minimal",
        "lqc.web_page_creation.javascript_grizzly",
        "lqc.web_page_creation.html_body",
        "lqc.web_page_creation.ui_tools",
        "lqc.css_generators",
        "lqc.css_generators.util",
        ],
    version='0.0.1',
    install_requires=[
        'grizzly-framework',
    ],
    entry_points={
       "grizzly_adapters": ["lqc = lqc.grizzly.lqc_adapter:LayoutQuickCheckAdapter"]
    },
)