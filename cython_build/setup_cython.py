from setuptools import setup, Extension
from Cython.Build import cythonize
import os

pyx_path = os.path.join("projects", "demo_project", "modules", "image_filter", "image_filter.pyx")

extensions = [
    Extension(
        name="projects.demo_project.modules.image_filter.image_filter",
        sources=[pyx_path],
    )
]

setup(
    name="image_filter_cython_build",
    ext_modules=cythonize(extensions, compiler_directives={'language_level': "3"}),
    zip_safe=False,
)
