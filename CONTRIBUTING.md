# Contributing to core-python

Thank you for your interest in contributing to core-python! We welcome contributions from the community and want to make the process as smooth as possible.

## How to Contribute

1. **Fork the repository** and create your branch from `master`.
2. **Create descriptive branches**: Use meaningful names, e.g., `feature/add-logging` or `bugfix/fix-typo-in-readme`.
3. **Write clear, concise commit messages** that explain your changes.
4. **Open a Pull Request** (PR) against the `master` branch. Please fill out the PR template and link any related issues.

## Code Style & Quality

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for code style.
- Use [type hints](https://docs.python.org/3/library/typing.html) where appropriate.
- Document public methods and classes with docstrings.

## Supported Versions

We support all current supported versions of Python. When introducing new dependencies or syntax, please ensure they are available and function correctly across all supported Python versions. 
If code requires version-specific logic, use clear and well-documented conditional statements. Please verify changes using the test suite in each supported Python environment.


## Testing

- All new features and bugfixes must include tests.
- We use [pytest](https://docs.pytest.org/) for testing. Add your tests in the `tests/` directory.
- Ensure your code passes all tests before submitting a PR:
  ```
  pytest
  ```
- We expect **100% test coverage** for new code (exceptions may be discussed in PRs).

## Pull Request Expectations

- Keep PRs focused and small; make unrelated changes in separate PRs.
- Address all automated review comments and code style checks.
- Add/Update documentation as needed for your changes.

## Reporting Issues

- Use the [issue tracker](https://github.com/part-os/core-python/issues) for bugs, feature requests, or questions.
- Provide as much context as possible, including steps to reproduce problems.
