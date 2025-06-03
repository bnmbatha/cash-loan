# 🚀 User Service - Cash Loan Platform

This microservice handles all **user account** operations for the Cash Loan Platform. It provides a robust and secure foundation for **registration**, **authentication**, **password management**, and **email verification**. Built with **FastAPI**, **PostgreSQL**, **JWT**, and hosted on **AWS EKS**.

---

## 🌐 Features

### ✅ User Management

* **Register** a new user
* **Get user by ID**
* **Update** user details
* **Delete** user account
* Passwords are securely hashed using **bcrypt**

### ✨ Authentication

* **JWT-based login** with access token
* Protected `/me` endpoint to fetch current user profile
* JWT tokens expire after **1 hour**

### 🔐 Email Verification

* Generates a **verification token** on registration
* `/verify/{token}` endpoint to verify email
* Updates `is_active` flag on successful verification

### 🔒 Password Reset

* **Forgot Password**: Generates JWT reset link (valid for 30 mins)
* **Reset Password**: Accepts token and new password to update DB
* Tokens are generated with HS256 algorithm using a shared secret key

### 🚀 AWS Integration

* Uses **AWS Secrets Manager** to store sensitive configs
* Accesses secrets securely using **IRSA (IAM Roles for Service Accounts)**

### 🚄 Database

* PostgreSQL via **SQLAlchemy ORM**
* Models auto-created at runtime via `Base.metadata.create_all()`
* User schema includes:

  ```sql
  id, full_name, email, hashed_password, is_active
  ```

### ⚙️ Deployment Ready

* Dockerized and Kubernetes-ready
* Includes probes, resource limits, and LoadBalancer service
* Fetches secrets dynamically from AWS at runtime

---

## 📄 Project Structure

```bash
user_service/
├── app/
│   ├── api/v1/user_routes.py       # API endpoints
│   ├── core/
│   │   ├── config.py               # Load AWS secrets
│   │   └── auth.py                 # JWT & password auth
│   ├── db/
│   │   ├── models/user.py          # SQLAlchemy user model
│   │   ├── session.py              # DB connection/session
│   │   └── base.py
│   ├── schemas/user.py             # Pydantic models
│   ├── services/user_service.py    # Business logic
│   └── main.py                     # FastAPI app
├── Dockerfile
├── requirements.txt
├── .env                            # (for local use)
└── create_db.py                    # Manual DB init
```

---

## 📝 API Reference

| Method | Endpoint           | Description             |
| ------ | ------------------ | ----------------------- |
| POST   | `/register`        | Register new user       |
| GET    | `/{user_id}`       | Get user by ID          |
| PUT    | `/{user_id}`       | Update user             |
| DELETE | `/{user_id}`       | Delete user             |
| POST   | `/login`           | User login, returns JWT |
| GET    | `/me`              | Authenticated user info |
| POST   | `/forgot-password` | Start password reset    |
| POST   | `/reset-password`  | Complete password reset |
| GET    | `/verify/{token}`  | Email verification      |

---

## 🛡️ Security Notes

* All passwords are hashed with **bcrypt**.
* JWT tokens are signed with a secret from AWS Secrets Manager.
* IRSA is used to authorize pod access to AWS APIs.
* No hardcoded credentials. Environment values come from AWS Secrets.

---

## ⚡ To-Do / Improvements

* [ ] Integrate SES or SMTP for sending verification/reset emails
* [ ] Add role support (admin, agent, etc.)
* [ ] Add automated tests
* [ ] Improve error logging and observability

---

## 🚀 Running Locally

1. Clone the repo
2. Add a `.env` file or export AWS credentials
3. Run Docker:

```
docker build -t user-service .
docker run --env-file .env -p 8000:8000 user-service
```

---

## 🛌 Contributors

This microservice was crafted as part of a broader effort to build a robust, scalable, and cloud-native cash loan platform.

---

## 🔗 License

MIT License. Feel free to use and extend!
