import os
import tomllib


def load_config():
    try:
        base_directory = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.normpath(
            os.path.join(base_directory, "../config.toml")
        )

        if not os.path.exists(config_file_path):
            raise FileNotFoundError(f"Config file not found: {config_file_path}")

        with open(config_file_path, "rb") as config_file:
            config = tomllib.load(config_file)
            server = config.get("server")[0].get("listen")
            forward_server = config.get("server")[0].get("forward")
            proxy_server = {"host": server.split(":")[0], "port": server.split(":")[1]}
            forward_servers = []
            for server in forward_server[0].get("backends"):
                server_address = server.get("address")
                forward_servers.append({
                    "host": server_address.split(":")[0],
                    "port": server_address.split(":")[1]
                })
            print(proxy_server, forward_servers)
            return proxy_server, forward_servers
    except Exception as e:
        print(f"Unable to load config file due to {str(e)}")
