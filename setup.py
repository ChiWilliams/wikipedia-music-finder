from setuptools import setup, find_packages

setup(
    name="wiki_music",
    version="0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires = [
        'requests',  # for API calls
        'blingfire', # for sentence splitting
        'google-genai', # for Gemini
    ],
    extras_require = [
        'analysis': [
            'numpy',
            'matplotlib'
        ],
        'dev': [
            'pytest',
            'python-dotenv',
            'openai',
        ]
    ]
)
