# Loan Service API

This is a backend microservice built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. It provides endpoints for loan applications, approvals, and user-specific loan data. The app includes support for authentication, audit logging, and integration with AWS and other internal services.

---

## 🚀 Features

* Apply for a loan
* Admin can approve or reject loan applications
* View current user's loans with filtering, sorting, and pagination
* Admin can view loans for any user
* Email notification upon approval or rejection
* Auto-disbursement integration
* Audit log of all admin actions
* JWT-based authentication
* AWS Secrets Manager integration

---

## 🧱 Tech Stack

* **FastAPI** – Web framework
* **SQLAlchemy** – ORM for database access
* **PostgreSQL** – Primary database
* **Alembic** – Database migrations
* **Pydantic** – Data validation
* **Uvicorn** – ASGI server
* **Python-JOSE** – JWT handling
* **Passlib (bcrypt)** – Password hashing
* **httpx / requests** – HTTP clients for inter-service calls
* **boto3** – AWS SDK for Python
* **AWS Secrets Manager** – Secret management

---

## 📁 Project Structure

```
app/
├── api/
│   └── v1/
│       └── endpoints/
│           ├── loan.py         # Apply/view loans
│           └── approval.py     # Admin approves/rejects loans
├── core/
│   └── config.py               # App settings from environment
│   └── loan_logic.py           # Monthly payment calculation
├── db/
│   ├── models/
│   │   ├── loan.py             # Loan DB model
│   │   └── loan_audit_log.py   # Audit log model
│   └── session.py              # DB engine and session setup
├── schemas/
│   └── loan.py                 # Pydantic models (LoanCreate, LoanOut, etc.)
│   └── approval.py             # Pydantic model for loan approval
common_libs/
├── auth/
│   └── dependencies.py         # JWT auth and role-based access
├── disbursement.py             # Fund disbursement logic
├── notifications.py            # Email notification logic
├── users.py                    # User service integration
main.py                         # FastAPI app setup and route registration
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/loan-service.git
cd loan-service
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
DB_HOST=your-db-host
DB_PORT=5432
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_NAME=your-db-name
SECRET_KEY=your-secret-key
aws_region=your-region
aws_secret_name=your-aws-secret-name
user_service_url=http://user-service:8000
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
uvicorn main:app --reload
```

### 5. Access API Docs

Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📌 Example Endpoints

* `POST /api/v1/loans/apply` - Submit a loan application
* `GET /api/v1/loans/me` - List logged-in user's loans
* `GET /api/v1/loans/{loan_id}` - View specific loan details
* `PUT /api/v1/loans/{loan_id}/approve` - Admin approves a loan
* `PUT /api/v1/loans/{loan_id}/reject` - Admin rejects a loan

---

## 🛡 Authentication

* JWT tokens are required for protected routes.
* Admin-only routes (e.g., approval) require the user to have role `"admin"`.

---

## 🗃 Database

* PostgreSQL is used as the relational database.
* Alembic can be configured for migrations.

---

## 📜 License

This project is licensed under the MIT License.

---

## 🙋‍♂️ Contributions

Feel free to fork this repo and submit a PR or open an issue. All contributions are welcome.
