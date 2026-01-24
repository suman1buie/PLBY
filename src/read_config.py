import os
import tomllib


def load_config():
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.normpath(
            os.path.join(BASE_DIR, "../config.toml")
        )

        if not os.path.exists(config_file_path):
            raise FileNotFoundError(f"Config file not found: {config_file_path}")

        with open(config_file_path, "rb") as f:
            config = tomllib.load(f)
            server = config.get("server")[0].get("listen")
            forword_server = config.get("server")[0].get("forward")
            proxy_server = {"host":server.split(":")[0], "port":server.split(":")[1]}
            forword_servers = []
            for server in forword_server[0].get("backends"):
                server_address = server.get("address")
                forword_servers.append({
                    "host":server_address.split(":")[0],
                    "port":server_address.split(":")[1]
                })
            print(proxy_server, forword_servers)
            return proxy_server, forword_servers
    except Exception as e:
        print(f"Unable to load config file due to {str(e)}")
