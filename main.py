import os
import json

LOCAL_ENV = "env_local.json"


def init_local_env(path: str):
    if os.path.exists(path):
        with open(path) as json_file:
            data = json.load(json_file)
            for key, value in data.items():
                os.environ[key] = value


def main():
    pass


if __name__ == "__main__":
    init_local_env(LOCAL_ENV)
    main()
