# Simple TCP Load Balancer (Round Robin)

This project is a **simple TCP-based load balancer** implemented in Python. It distributes incoming client traffic to multiple backend TCP servers using the **Round Robin** scheduling algorithm.

> ⚠️ **Note:** This project is in an early stage and is intended for learning and experimentation purposes only.

---

## 📌 Features

* TCP reverse proxy / load balancer
* Round Robin traffic distribution
* Multiple backend servers
* Simple client to test load balancing behavior

---

## 🧰 Prerequisites

* Python **3.x** installed on your system

You can verify Python installation using:

```bash
python3 --version
```

---

## 📁 Project Structure

After cloning the repository, you will find the following files:

1. **`loadbalancer.py`** – TCP load balancer (reverse proxy)
2. **`server.py`** – Backend TCP server
3. **`client.py`** – Test client to generate TCP requests

---

## 🚀 How It Works

* The **load balancer** listens on port **8080**.
* Multiple backend **TCP servers** listen on different ports.
* Incoming client requests are forwarded to backend servers using **Round Robin**.
* Each request is handled by a different server in sequence.

---

## ▶️ Running the Project

### 1️⃣ Start the Load Balancer

Run the following command:

```bash
python3 loadbalancer.py
```

This will start a TCP load balancer on:

```
localhost:8080
```

---

### 2️⃣ Start Backend Servers

Open **three separate terminals** and run the servers on different ports.

Example:

```bash
python3 server.py 8088
python3 server.py 8077
python3 server.py 8070
```

These servers will receive traffic from the load balancer.

---

### 3️⃣ Run the Client

Now run the client to send TCP requests:

```bash
python3 client.py
```

* The client sends **10 TCP requests** to the load balancer.
* The load balancer forwards each request to a backend server.
* You will observe responses coming from **different servers**, proving Round Robin distribution.

---

## ✅ Expected Output

When running the client, you should see responses like:

```
Response from server running on port 8088
Response from server running on port 8077
Response from server running on port 8070
...
```

Each response will come from a different backend server in sequence.

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
