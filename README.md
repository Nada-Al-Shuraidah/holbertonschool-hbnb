# 🚩 HBNB - Layered Architecture (Task 0)

This documentation explains the layered architecture used in the HBNB project. It is structured based on the concept of **package diagrams** where each layer is encapsulated in its own logical package. This approach allows for better separation of concerns, maintainability, and scalability.

---

## 🔶 Presentation Layer

### 📌 Purpose:
This is the **interface layer** that interacts with users or external systems. Its main responsibility is to **handle HTTP requests**, delegate them to the business layer, and return appropriate HTTP responses.

It does **not** contain any business logic. Instead, it serves as a clean entry point for the application.

### ⚙️ Components:
- `UserAPI`
- `PlaceAPI`
- `ReviewAPI`
- `AmenityAPI`

### 💡 Why These Components?
Each API corresponds to a major resource in the HBNB application (users, places, reviews, and amenities). These components are split to follow **RESTful principles**, where each API provides access to a specific resource.

For example:
- `UserAPI` handles `/users` routes and delegates user-related operations to the business logic layer.

These APIs expose **endpoints** such as:
- `GET /users`
- `POST /places`
- `DELETE /reviews/<id>`

---

## 🟦 Business Logic Layer 

### 📌 Purpose:
This layer **processes all the core logic** of the system. It takes care of validations, coordinating between objects, applying rules, and preparing data before persistence or response.

It acts as a **mediator** between the presentation and persistence layers.

### ⚙️ Components:
- `User`
- `Place`
- `Review`
- `Amenity`
- `FacadeService`

### 💡 Why These Components?
Each class (`User`, `Place`, etc.) represents a domain entity with associated logic. For example:
- `User` might check for valid emails before creating a user.
- `Place` might calculate availability based on bookings.

The `FacadeService` is a key design element here. It provides a **unified interface** for the APIs to interact with the business logic, hiding the complexity of multiple services or entities. This simplifies the Presentation Layer and helps isolate changes.

---

## 🟢 Persistence Layer 
### 📌 Purpose:
This is the **data access layer**. It is responsible for all communication with the storage engine (e.g., database, file system).

It provides a consistent interface to store and retrieve data.

### ⚙️ Components:
- `DatabaseAccess`
  - `saveData()`
  - `retrieveData()`

### 💡 Why These Components?
This abstraction allows us to change the storage backend (e.g., switch from file to database) **without modifying business logic**. It also supports better testability by mocking the data access in unit tests.

In the HBNB project, this layer typically interacts with the `models` package (e.g., BaseModel) and the storage engine (`DBStorage` or `FileStorage`).

---

## 🧩 Why RESTful API?

HBNB uses a **RESTful API** style because it naturally maps HTTP methods (GET, POST, PUT, DELETE) to CRUD operations (Create, Read, Update, Delete).

It simplifies interaction between the front-end and back-end, supports **stateless** communication, and improves scalability.

Example:
```
GET /users → fetch all users
POST /places → create a new place
DELETE /reviews/<id> → delete a specific review
```

---

## 🏗️ Summary of Layer Interactions

```
🔶 Presentation Layer
    ↓ (calls)
🟦 Business Logic Layer (via Facade)
    ↓ (calls)
🟢 Persistence Layer (Data Access)
```
