# Simple Load Balancer support TCP/HTTP based routing (Round Robin)/ Reverse proxy / Static server

This project is a **simple TCP-based load balancer** implemented in Python. It distributes incoming client traffic to multiple backend TCP servers using the **Round Robin** scheduling algorithm. Configuration is managed through a TOML file.

> ⚠️ **Note:** This project is in an early stage and is intended for learning and experimentation purposes only.

---

## 📌 Features

* TCP reverse proxy / load balancer
* Round Robin traffic distribution
* Multiple backend servers
* TOML-based configuration (`config.toml`)
* Simple client to test load balancing behavior

---

## 🧰 Prerequisites

* Python **3.11+** (required for the built-in `tomllib` module used to parse `config.toml`)

You can verify your Python version using:

```bash
python3 --version
```

---

## 📁 Project Structure

```
.
├── config.toml          # Load balancer configuration (listen address, backends)
├── server.py            # Backend TCP server
├── client.py            # Test client to generate TCP requests
└── src/
    ├── loadbalancer.py  # TCP load balancer (reverse proxy)
    └── read_config.py   # Config parser for config.toml
```

---

## ⚙️ Configuration

The load balancer is configured via `config.toml` in the project root. The default configuration looks like this:

```toml
[[server]]
listen = "0.0.0.0:8200"

[[server.forward]]
algorithm = "WRR"
backends = [
    { address = "127.0.0.1:8080" },
    { address = "127.0.0.1:8081" },
    { address = "127.0.0.1:8082" },
]
```

* **`listen`** – The address and port the load balancer binds to.
* **`algorithm`** – The balancing algorithm (currently configured as `WRR`; the implementation uses Round Robin).
* **`backends`** – The list of backend servers that receive forwarded traffic.

You can edit `config.toml` to change the listen port or add/remove backend servers.

---

## 🚀 How It Works

* The **load balancer** reads `config.toml` and listens on the configured address (default **`0.0.0.0:8200`**).
* Multiple backend **TCP servers** listen on the ports specified in the config.
* Incoming client requests are forwarded to backend servers using **Round Robin**.
* Each request is handled by a different server in sequence.

---

## ▶️ Setup & Running the Project

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/suman1buie/PLBY.git
cd PLBY
```

### 2️⃣ Start Backend Servers

Open **three separate terminals** and start a server on each port listed in `config.toml`:

```bash
python3 server.py 8080
python3 server.py 8081
python3 server.py 8082
```

Each server will print a message like:

```
Server running on port 8080...
```

### 3️⃣ Start the Load Balancer

In a new terminal, run:

```bash
cd src
python3 loadbalancer.py
```

This will start the load balancer on the address configured in `config.toml` (default `0.0.0.0:8200`):

```
Load balancer listening on port 8200...
```

### 4️⃣ Run the Client

In another terminal, send test requests:

```bash
python3 client.py
```

> **Note:** The client is currently hardcoded to connect to `localhost:8081`. To test through the load balancer, update the port in `client.py` to match the load balancer's listen port (default `8200`).

---

## ✅ Expected Output

When running the client through the load balancer, you should see responses like:

```
Hi from server 8080
Hi from server 8081
Hi from server 8082
Hi from server 8080
...
```

Each response comes from a different backend server in Round Robin sequence.

---

## 🔒 Future Improvements

This is just the beginning. Planned enhancements include:

* Security improvements
* Fault tolerance
* Health checks for backend servers
* Configurable server pools
* Better error handling

---

## 📄 Disclaimer

This project is for **educational purposes only** and is not production-ready.

---

Happy Coding 🚀
