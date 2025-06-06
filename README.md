# Django Fitness Class Booking API

This project is a Django-based API for booking fitness classes. Users can book slots using their email address without authentication. Duplicate bookings are prevented, and slot availability is checked. Tests are written using `pytest`.

---

## Setup Guide

### 1. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
python3 manage.py makemigration
python3 manage.py migrate
```
### 4. Inject sample data for testing

```bash
python3 manage.py shell < api/helper.py
```

### 5. Start the Server

```bash
python3 manage.py runserver
```

Visit: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Running Tests with Pytest

### 1. Run Tests

```bash
pytest --cov=api
```

---

## API Info

### Endpoint

```
POST /api/book/
```

### Payload

```json
{
  "class_id": "<uuid>",
  "email": "user@example.com",
  "cleint_name":"username"
}
```

### Optional Query Param

```
?timezone=Asia/Kolkata
```

---


