# 🚗 Car Reports Backend API (Flask)

## 📌 Project Description

Flask-based backend for car registration reports with JWT authentication, MySQL persistence, and external car dataset integration. Supports user signup/login, protected profile APIs, background processing, schema validation, and advanced search functionality.

---

## 🧠 Project Overview

This project is a production-ready RESTful backend built using **Flask**. It provides secure user authentication, car data ingestion from an external API, background task processing, data validation, and efficient search APIs. The system is designed with scalability, security, and clean architecture in mind.

Users can register, log in, receive a JWT token, and access protected APIs. Car data is fetched from an external source and stored in a MySQL database, with periodic background updates handled using Celery.

---

## 🛠️ Tech Stack

* **Backend Framework:** Flask
* **Database:** MySQL
* **Authentication:** JWT (JSON Web Tokens)
* **Task Queue:** Celery
* **Message Broker:** Redis
* **Schema Validation:** Marshmallow
* **External API:** Back4App (Car Model List)
* **API Testing:** Postman

---

## 📂 Project Structure

```text
project-root/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── models/
│   ├── routes/
│   │   ├── auth.py
│   │   ├── profile.py
│   │   ├── cars.py
│   ├── schemas/
│   ├── services/
│   └── tasks/
│
├── migrations/
├── celery_worker.py
├── run.py
├── requirements.txt
└── README.md
```

---

## 🔐 Authentication Flow (JWT)

1. **User Signup**

   * User registers using email and password
   * Password is securely hashed
   * User details are stored in MySQL

2. **User Signin**

   * Credentials are verified
   * A JWT access token is generated and returned

3. **Protected APIs**

   * JWT token is sent in the request header
   * Token is validated before accessing protected routes

---

## 👤 Profile API

* Endpoint is protected using JWT
* Retrieves authenticated user details from MySQL
* Returns user-specific information only after token verification

---

## 🚘 Car Data Integration

* Car data is fetched from:

  ```
  https://parseapi.back4app.com/classes/Car_Model_List?limit=10
  ```
* Data is normalized and stored in MySQL
* Duplicate entries are avoided

---

## 🔁 Background Processing with Celery

* Celery is used for asynchronous and scheduled tasks
* Daily background job fetches updated car data
* Ensures non-blocking API performance
* Redis is used as the message broker

---

## 📐 Data Validation with Marshmallow

* Request and response schemas defined using Marshmallow
* Automatic validation of incoming payloads
* Clear and structured validation error messages
* Improves API reliability and security

---

## 🔍 Search & Filtering API

* Search cars by:

  * Make
  * Model
  * Year
* Supports pagination
* Optimized database queries for fast results

---

## ▶️ How to Run the Project

### 1. Clone the Repository

```bash
git clone <repository-url>
cd project-root
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file and add:

```env
FLASK_ENV=development
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret
DATABASE_URL=mysql://user:password@localhost/db_name
REDIS_URL=redis://localhost:6379/0
```

### 5. Run the Application

```bash
python run.py
```

### 6. Start Celery Worker

```bash
celery -A celery_worker.celery worker --loglevel=info
```

---

## 🧪 API Testing

* Use **Postman** to test all endpoints
* Include JWT token in the `Authorization` header:

  ```
  Authorization: Bearer <token>
  ```

---

## ✅ Key Highlights

* Secure JWT-based authentication
* Clean and scalable Flask architecture
* Background processing with Celery
* Strong schema validation using Marshmallow
* Efficient search and filtering
* MySQL-backed persistent storage

---

## 📌 Conclusion

This project demonstrates real-world backend development practices including authentication, background processing, data validation, and third-party API integration. It is designed to be scalable, maintainable, and production-ready.

---

## 👨‍💻 Author

**Huzaifa**

---

