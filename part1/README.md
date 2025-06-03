# ⭕ HBNB – Part 1 Technical Documentation

Welcome to the **technical documentation** for Part 1 of the **HBnB Project**, a simplified clone of Airbnb. This project is designed using a layered architecture with clear separation between the API, core logic, and data layers. This file explains the structure, diagrams, and system flow we built step-by-step to form a solid foundation for future implementation phases.

---

# 🚩 Task 0: High-Level Architecture – Package Diagram

The system follows a **three-layered architecture** using **package diagrams** for structure and the **Facade Pattern** for clean communication across layers.

---

## 🔶 Presentation Layer

### 📌 Purpose:
The entry point of the system. Handles user/API requests and responses.

### ⚙️ Components:
- `UserAPI`
- `PlaceAPI`
- `ReviewAPI`
- `AmenityAPI`

These APIs do **not** include logic. They receive HTTP requests (e.g., `POST /users`, `GET /places`) and delegate all processing to the Business Logic Layer via the **FacadeService**.

## 📌 Note: The Facade Pattern in this Architecture

### 🔷 What is the Facade Pattern?
The **Facade Pattern** is a design pattern that provides a **unified and simplified interface** to a set of complex subsystems. In our case, it's used to **isolate the API layer** from the internal business rules and operations.

> It acts like a receptionist: the API talks to the Facade, and the Facade knows how to handle everything inside without exposing the internal complexity which simplify the communication.

---

### 🧠 How We Apply It:
For each resource (`User`, `Place`, `Review`, `Amenity`), there is a corresponding **Service class**:
- `UserService`
- `PlaceService`
- `ReviewService`
- `AmenityService`

These service classes:
- Contain the business rules and validation logic
- Coordinate actions (e.g., creating, updating, or deleting objects)
- Interact with the model and repository layers
- Are the **only components** that the Presentation Layer talks to

---

### ✅ Why It’s Useful:
- Keeps the API code simple and clean
- Reduces direct coupling between layers
- Makes the logic easier to maintain and test
- Encourages **Separation of Concerns** inside the Business Logic Layer

---

## 🟦 Business Logic Layer

### 📌 Purpose:
Contains the actual logic for handling business rules, processing data, and managing relationships between objects.

### ⚙️ Components:
- `User`
- `Place`
- `Review`
- `Amenity`
- `FacadeService`

Each class handles its entity's logic (e.g., `User` validates emails, `Place` calculates pricing logic). `FacadeService` unifies access to this logic, so API routes can call it directly without dealing with all individual models.

---

## 🟢 Persistence Layer

### 📌 Purpose:
Handles **storing and retrieving** data from the database or file system.

This **abstraction layer** makes the system flexible — allowing it to switch between different storage engines (like `FileStorage` and `DBStorage`) **without affecting the core logic** of the application. That’s a key part of keeping your code clean, testable, and modular.

> This layer works as the “bridge” between the logic and the actual data source.

### ⚙️ Components:
- `PlaceRepository`
- `UserRepository`
- `ReviewRepository`
- `AmenityRepository`

Each repository class:
- Implements methods
- Communicates with the appropriate storage engine 
- Is used by the **Business Logic Layer** to persist and retrieve model instances without needing to know the storage details

---

## 🖼️ Package Diagram

🖱️ Click to view: **[UML/Package_Diagram.svg](./UML/Package_Diagram.svg)**

---

# 🧩 Task 1: Business Logic Class Diagram

This diagram illustrates the internal structure of the Business Logic Layer and how entities are related.

## 📌 Main Entities

- **User**
  - Attributes: `id`, `first_name`, `last_name`, `email`, `password`, `is_admin`, `created_at`, `updated_at`
  - Relationships: Can create Places and submit Reviews

- **Place**
  - Attributes: `id`, `title`, `description`, `price`, `latitude`, `longitude`, `created_at`, `updated_at`
  - Relationships: Belongs to a User, has many Amenities and Reviews

- **Amenity**
  - Attributes: `id`, `name`, `description`, `created_at`, `updated_at`
  - Relationships: Can belong to many Places

- **Review**
  - Attributes: `id`, `text`, `rating`, `created_at`, `updated_at`
  - Relationships: Linked to a User and a Place
 
---

## 🖼️ Class Diagram 

🖱️ Click to view: **[UML/Class_Diagram.svg](./UML/Class_Diagram.svg)**

---

## 🖼️ Source Code

🖱️ Click to view: **[code/Class_Diagram.mmd](./code/Class_Diagram.mmd)**

---

# 🔁 Task 2: API Sequence Diagrams

This diagrams shows how API calls interact with all layers.

---

## 🖼️ Sequence Diagram for Login

🖱️ Click to view: **[UML/Login_Sequence_Diagram.svg](.UML/Login_Sequence_Diagram.svg)**

---

## 🔗 Source Code for login

🖱️ Click to view: **[code/Login_Sequence_Diagram.mmd](.code/Login_Sequence_Diagram.mmd)**

---

## 🖼️ Sequence Diagram for Submit Review 

🖱️ Click to view: **[UML/Submit_Review_Sequence_Diagram.svg](.UML/Submit_Review_Sequence_Diagram.svg)**

---

## 🔗 Source Code for Submit Review 

🖱️ Click to view: **[code/Submit_Review_Sequence_Diagram.mmd](.code/Submit_Review_Sequence_Diagram.mmd)**


---

# ✅ Summary

- Built using **Layered Architecture**
- Applied the **Facade Pattern** for clarity and modularity
- Created **UML Diagrams** to guide implementation

---

📁 Directory Layout

```
part1/
├── README.md
├── UML/
│   └── Package_Diagram.svg
│   └── Class_Diagram.svg
│   └── Login_Sequence_Diagram.svg
│   └── Submit_Review_Sequence_Diagram.svg
├── Code/
│   ├── Class_Diagram.mmd
│   ├── Sequence_Login.mmd
│   └── Sequence_Submit_Review.mmd
```

© 2025 – Holberton School & Tuwaiq Academy
