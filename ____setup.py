from setuptools import setup, find_packages

setup(
    name='Nexia API',
    version='1.0.0',
    description='API used to generate text prompts and manage prompts. Intergrated with openai and huggingface.',
    author='Philip Mutua',
    packages=find_packages(),
    packages=find_packages(include=['core', 'core.*']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
