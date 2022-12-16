from dotenv import dotenv_values


def init_config_pg():
    config = {
        **dotenv_values(".env.secret")
    }
    print(config)