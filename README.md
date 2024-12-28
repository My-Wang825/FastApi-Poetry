### Python Backend Test
```
poetry_demo
├─ .gitignore
├─ app
│  ├─ agent
│  │  ├─ function_call.py
│  │  └─ __init__.py
│  ├─ api
│  │  ├─ v1
│  │  │  ├─ routers
│  │  │  │  ├─ ask_database.py
│  │  │  │  ├─ doris_test.py
│  │  │  │  ├─ test.py
│  │  │  │  └─ __init__.py
│  │  │  └─ __init_.py
│  │  └─ __init__.py
│  ├─ core
│  │  ├─ config.py
│  │  └─ __init__.py
│  ├─ curd
│  ├─ db
│  │  └─ base.py
│  ├─ models
│  ├─ server.py
│  ├─ task
│  │  ├─ cron
│  │  │  ├─ nifi_dingding_alarm.py
│  │  │  └─ __init__.py
│  │  ├─ schedule.py
│  │  └─ __init__.py
│  ├─ tests
│  ├─ utils
│  └─ __init__.py
├─ docker-compose.yml
├─ Dockerfile
├─ experiment
│  ├─ function_calling.ipynb
│  └─ vanna_doris_test.ipynb
├─ poetry.lock
├─ pyproject.toml
└─ README.md

```