## Shenase

![GitHub repo status](https://img.shields.io/badge/status-active-green?style=flat)
![GitHub license](https://img.shields.io/github/license/sheikhartin/shenase)
![GitHub contributors](https://img.shields.io/github/contributors/sheikhartin/shenase)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/sheikhartin/shenase)
![GitHub repo size](https://img.shields.io/github/repo-size/sheikhartin/shenase)
![GitHub workflow status](https://github.com/sheikhartin/shenase/actions/workflows/python-app.yml/badge.svg)

System for managing user access and permissions.

### How to Use

Install the dependencies:

```
poetry install
```

Test it first:

```
poetry run pytest -rP
```

Run the server:

```
poetry run uvicorn shenase.main:app --reload --port 8808 --log-config log_config.json
```

Then navigate to http://127.0.0.1:8808/docs.

### License

This project is licensed under the MIT license found in the [LICENSE](LICENSE) file in the root directory of this repository.
