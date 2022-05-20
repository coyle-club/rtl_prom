#!/usr/bin/env python

from distutils.core import setup

setup(
    name="rtl_prom",
    version="1.0",
    description="Surface rtl_433 data to Prometheus",
    author="Tom Petr",
    author_email="trpetr@gmail.com",
    packages=["rtl_prom"],
    install_requires=["click", "prometheus-client"],
    entry_points={"console_scripts": ["rtl_prom=rtl_prom:main"]},
)
