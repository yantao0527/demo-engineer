from setuptools import find_packages, setup

setup(
    name="engineerai",
    version="0.0.0.1",
    url="https://github.com/yantao0527/demo-engineer",
    author="Frank Yan",
    author_email="yantao0527@gmail.com",
    description="Description of my package",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["tiktoken", "langchain", "openai", "python-dotenv"],
    package_data={"prompt_based": ["prompts.txt"]},
    entry_points={
        "console_scripts": [
            "engineerai = engineer.cli:app",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
