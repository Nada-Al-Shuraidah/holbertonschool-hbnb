# ⭕ HBnB – Part 2 Technical Documentation

Welcome to the technical documentation for **Part 2** of the HBnB Project. Here, we implemented and tested the Business Logic and Presentation layers for our Airbnb clone.

---

## 🔨 What We Did

- **Project Structure:** Organized into `app/api`, `app/models`, `app/services`, and `tests` for a clean, modular architecture.  
- **Core Models:** Built `BaseModel`, `User`, `Place`, `Review`, and `Amenity` classes with UUIDs, timestamps, and validation rules.  
- **Services Layer:** Developed Facade services to encapsulate business logic and simplify API endpoints.  
- **API Endpoints:** Created Flask-RESTx routes for CRUD operations on Users, Amenities, Places, and Reviews.  
- **Data Serialization:** Ensured responses include related details (owner info, amenities lists, review collections).  
- **Testing & Validation:** Wrote unit tests for models and endpoints, tested APIs manually with cURL/Postman, and generated Swagger docs for interactive exploration.

---

## ✅ Key Outcomes

- A fully functional Flask application with in-memory data handling, ready for database integration in Part 3.  
- Clear separation of concerns between API, services, and models layers.  
- Comprehensive test coverage and interactive API documentation.

---

© 2025 – Holberton School & Tuwaiq Academy
