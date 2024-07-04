from setuptools import setup, find_packages

setup(
    name="Hotel Web Scraper",
    version="0.1.0",
    description="A web scraping project using Python and Selenium",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jaydeep Agravat",
    author_email="jaydeepfagravatf1@gmail.com",
    url="https://github.com/jaydeepf1/hotel_scraping_project",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=["selenium"],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "flake8",
            "mypy",
            "black",
            # 64 hotels, 138 room types
            # add other development dependencies here
        ],
    },
    python_requires=">=3.8",
)
