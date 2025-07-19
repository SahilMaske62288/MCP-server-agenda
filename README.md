# 🔥 MCP Server Agenda

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Uvicorn-0A9396?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Relational_DB-blue?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)
![AWS](https://img.shields.io/badge/AWS-EC2-orange?logo=amazon-aws)
![Status](https://img.shields.io/badge/Deployed-LIVE-green)
![Maintained](https://img.shields.io/badge/Maintained-YES-brightgreen)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 🚀 About the Project

This project is a robust **MCP (Model Context Protocol Server)** backend created with FastAPI, PostgreSQL, and containerized with Docker, then deployed on **AWS EC2** with full production readiness.

It represents a **collaborative build** between cloud engineering and API design/data management excellence.

---

## 📂 Key File Highlights

### 🧠 `mcp/server/fastmcp/server.py`
- Defines `FastMCP` class and `Context` logic
- Uses `pydantic`, `starlette`, and generic types
- Handles session, request, and lifespan for modular backends
- Acts as a foundation for the tool/prompt system

---

### 🧩 `postgres.py`
- Integrates PostgreSQL connection and operations
- Decorated with custom `@mcp.tool()` and `@mcp.prompt()` methods
- Used as a command interface for database interactions via API
- Registered directly into FastAPI for smart orchestration

---

## 🛠️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/SahilMaske62288/MCP-server-agenda.git
cd MCP-server-agenda
```

### 2. Build Docker Image

```bash
docker build -t mcp-image .
```

### 3. Run the Docker Container

```bash
docker run --rm -p 8000:8000 mcp-image
```

### 4. Access the App

```
http://<your-ec2-public-ip>:8000
```

✅ Make sure **port 8000** is open in EC2 Security Group!



## 📦 Project Structure

```
MCP-server-agenda/
│
├── mcp/
│   └── server/
│       └── fastmcp/
│            └── server.py
│
├── postgres.py
├── Dockerfile
├── env.txt
└── README.md
```
---
## 🖼️ TEST WITH MCP INSPECTOR

> MCP Server

###

![Initial(https://github.com/SahilMaske62288/MCP-server-agenda/assets/your-initial-img-id)

---

###

![Middal(https://github.com/SahilMaske62288/MCP-server-agenda/assets/your-mid-img-id)

---

### 

![Test(https://github.com/SahilMaske62288/MCP-server-agenda/assets/your-final-img-id)

---

## 👥 Collaborators

| 👤 Name              | 🌐 GitHub Username                                          | 🛠️ Role                        |
|----------------------|------------------------------------------------------------|-------------------------------|
| Pratiksha Kachole    | [pratikshakachole](https://github.com/pratikshakachole)   | Code + Data  + MCP Server     |
| Sahil Maske  | [SahilMaske62288](https://github.com/SahilMaske62288)     | EC2 + Docker + Deploy    |

---

## 🔧 Tech Stack

- [x] Python 3.10 🐍
- [x] FastAPI ⚡
- [x] MCP Server⚙️
- [x] PostgreSQL 🛢️
- [x] Docker 🐳
- [x] AWS EC2 ☁️

---

## 💡 Learnings / Highlights

- Containerization with `Docker`
- Cloud deployment on `AWS EC2`
- Building modular, typed APIs with `FastAPI`
- Using `Uvicorn` for blazing-fast ASGI server setup
- Multi-developer, GitHub-based collaboration

---


## 💡 Acknowledgements


Built with  by Pratiksha Kachole and Sahil Maske
Special thanks to the sleepless nights, endless debugging, and EC2 reboots

---
## 📬 Contact


For any questions or collaborations:



📧 [pratikshakachole19@gmail.com]


📧 [sahilmaske143@gmail.com]

