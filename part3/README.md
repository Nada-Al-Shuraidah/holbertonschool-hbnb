# ⭕ HBnB – Part 3 Technical Documentation

Welcome to the **technical documentation** for **Part 3** of the HBnB Project. In this phase, we extended our simple Airbnb clone with:

- **JWT-based authentication & role-based authorization**  
- **Persistent storage** using **SQLAlchemy** + **SQLite** (dev) and prepared for **MySQL** (prod)  
- **Entity mapping** & **relationships** via the ORM  
- **Database schema visualization** with Mermaid.js  

---

# 🚩 Application Factory & Configuration

## 🔶 Purpose  
Wire up Flask’s Application Factory pattern so we can swap configurations (development vs. production) easily.

### Components  
- `create_app(config_object)` in `app/__init__.py`  
- `Config`, `DevelopmentConfig`, `ProductionConfig` in `app/config.py`  

### Flow  
1. Call `create_app()` with the right config.  
2. SQLAlchemy and JWT extensions are initialized.  
3. App is ready to register Blueprints and CLI commands.

---

# 🛠️ Password Hashing

## 🔶 Purpose  
Securely store user passwords by hashing with **Flask-Bcrypt**.

### Changes  
- **User** model’s `password` field accepts plaintext only in registration.  
- `hash_password()` method converts it to a bcrypt hash.  
- No plaintext password is ever returned by the API.

---

# 🔐 JWT Authentication

## 🔶 Purpose  
Authenticate users statelessly using **Flask-JWT-Extended**.

### Workflow  
1. **Login endpoint** (`POST /api/v1/auth/login`) accepts `email` + `password`.  
2. On success, issues a JWT with claims (`user_id`, `is_admin`).  
3. Client includes `Authorization: Bearer <token>` in subsequent requests.

---

# 👮 Role-Based Authorization

## 🔶 Purpose  
Enforce **access control** based on the `is_admin` flag.

### Rules  
- **Authenticated users** can CRUD their own Places & Reviews.  
- **Admins** can CRUD **any** resource (Users, Places, Reviews, Amenities).  
- Public endpoints (`GET /api/v1/places`, `GET /api/v1/amenities`) remain open.

---

# 🗄️ SQLAlchemy Repository & Model Mapping

## 🔶 Purpose  
Replace in-memory storage with a **SQLite** database via **SQLAlchemy ORM**.

### Steps  
1. Create `SQLAlchemyRepository` implementing the same interface as the old in-memory repo.  
2. Map **`User`, `Place`, `Review`, `Amenity`** entities to `db.Model` subclasses.  
3. Define **one-to-many** and **many-to-many** relationships in the models.  
4. Prepare separate configs for **SQLite** (development) vs **MySQL** (production).

---

# 🖼️ Database Schema Visualization

View the ER diagram here: [ER Diagram (Mermaid)](./er_diagram.mmd)
---

# ✅ Summary of Endpoints

| Resource   | Method | URL                             | Auth       | Roles           |
| ---------- | ------ | ------------------------------- | ---------- | --------------- |
| Register   | POST   | `/api/v1/users`                 | Public     | —               |
| Login      | POST   | `/api/v1/auth/login`            | Public     | —               |
| Users      | GET    | `/api/v1/users/<id>`            | JWT        | Admin only      |
| Users      | DELETE | `/api/v1/users/<id>`            | JWT        | Admin only      |
| Places     | CRUD   | `/api/v1/places`                | JWT/Public | Owner / Admin   |
| Places     | CRUD   | `/api/v1/places/<id>`           | JWT/Public | Owner / Admin   |
| Reviews    | CRUD   | `/api/v1/places/<place_id>/reviews` | JWT/Public | Owner / Admin   |
| Amenities  | CRUD   | `/api/v1/amenities`             | JWT        | Admin only      |
| Amenities  | CRUD   | `/api/v1/amenities/<id>`        | JWT        | Admin only      |

---

© 2025 – Holberton School & Tuwaiq Academy  
