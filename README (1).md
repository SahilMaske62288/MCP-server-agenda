# MCP Server Agenda 🚀

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-🚀-green?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-DB-blue?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)
![AWS](https://img.shields.io/badge/AWS-EC2-orange?logo=amazon-aws)
![Deployed](https://img.shields.io/badge/Deployed-Live-green)
![Maintained](https://img.shields.io/badge/Maintained-yes-brightgreen)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

A collaborative project built using FastAPI, PostgreSQL, and Docker — deployed on AWS EC2.  
This repo represents a clean backend setup with containerization and cloud deployment.

---

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

## ⚙️ Setup Instructions

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

### 4. Visit the App

Open in browser:

```
http://<your-ec2-public-ip>:8000
```

✅ Make sure **port 8000** is open in your EC2 **Security Group's inbound rules**.

---

## 👥 Collaborators

| Name               | GitHub Username                                          | Role                            |
|--------------------|----------------------------------------------------------|---------------------------------|
| Pratiksha Kachole  | [pratikshakachole](https://github.com/pratikshakachole) | Code + Data                     |
| Sahil Maske        | [SahilMaske62288](https://github.com/SahilMaske62288)   | AWS EC2 + Docker Deployment     |

---

## 🛠️ Technologies Used

- **Python**
- **FastAPI**
- **PostgreSQL**
- **Docker**
- **AWS EC2**
- **Uvicorn**
- **Git & GitHub**

---

## 📌 Notes

- Add your environment variables to `env.txt`
- Make sure PostgreSQL DB is running and reachable from the Docker container
- Ensure correct file/module structure (`__init__.py`) to avoid import issues

---

## 💡 Acknowledgements

Built with 💙 by [Pratiksha Kachole](https://github.com/pratikshakachole) and [Sahil Maske](https://github.com/SahilMaske62288)  
Special thanks to the sleepless nights, endless debugging, and EC2 reboots 😅

---
