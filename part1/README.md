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

This diagram illustrates the internal structure of the **Business Logic Layer**. It models all key entities, their attributes, and the relationships between them using correct UML practices.

---

## 🧬 Inheritance

All entities inherit from a shared `BaseModel`, which provides:
- `id: UUID`
- `created_at: dateTime`
- `updated_at: dateTime`

This ensures consistency and avoids repeating shared attributes in every class.

---

## 📌 Main Entities and Relationships

### 👤 **User**
- **Attributes:** `first_name`, `last_name`, `email`, `password`, `is_admin`
- **Methods:** `register()`, `updateProfile()`, `deleteAccount()`, `displayPlaces()`
- **Relationships:**
  - 🔗 **Composition** with `Place` (a user owns one or more places)
  - ➕ **Association** with `Review` (a user writes reviews)

---

### 🏠 **Place**
- **Attributes:** `owner_id`, `title`, `description`, `price`, `latitude`, `longitude`
- **Methods:** `createPlace()`, `updatePlace()`, `deletePlace()`, `displayReviews()`
- **Relationships:**
  - 🔗 Composed by a `User`
  - ➕ Associated with multiple `Review` entries
  - 🔁 Linked to `Amenity` through the `PlaceAmenity` class (many-to-many)

---

### ✨ **Amenity**
- **Attributes:** `name`, `description`
- **Methods:** `createAmenity()`, `updateAmenity()`, `deleteAmenity()`
- **Relationships:**
  - 🔁 Linked to `Place` through the `PlaceAmenity` class (many-to-many)

---

### 📝 **Review**
- **Attributes:** `user_id`, `place_id`, `rating`, `comment`
- **Methods:** `submitReview()`, `editReview()`, `deleteReview()`
- **Relationships:**
  - ➕ Associated with one `User`
  - ➕ Associated with one `Place`

---

### 🖇️ **PlaceAmenity**
- **Purpose:** Represents the many-to-many relationship between `Place` and `Amenity`.
- **Attributes:** `place_id`, `amenity_id`
- **Methods:** `addAmenityToPlace()`, `deleteAmenityFromPlace()`
- **Relationships:**
  - 🔄 Links a single `Place` with a single `Amenity`

---

## 🖼️ Class Diagram 

🖱️ Click to view: **[UML/Class_Diagram.svg](./UML/Class_Diagram.svg)**

---

# 🔁 Task 2: API Sequence Diagrams

This Sequence diagrams illustrate how requests move across the system layers when specific API calls are made. It visualizes the internal flow using the **Facade pattern**.

---

## 🔶 Purpose:
Show the **step-by-step interaction** between:
- `Presentation Layer` (APIs)
- `Business Logic Layer` (Services)
- `Persistence Layer` (Repositories)

For each use case, we describe how the layers communicate to fulfill the request.

---

## ⚙️ API Calls Covered:

- **👤 User Registration:**

🖱️ Click to view: **[UML/User_Registration_Sequence_Diagram.svg](./UML/User_Registration_Sequence_Diagram.svg)**

- **🔐 User Login :** 

🖱️ Click to view: **[UML/Login_Sequence_Diagram.svg](./UML/Login_Sequence_Diagram.svg)**
 
- **🏠 Place Creation:**  

🖱️ Click to view: **[UML/Create_Place_Sequence_Diagram.svg](./UML/Create_Place_Sequence_Diagram.svg)**

  
- **📝 Review Submission:**  
 
🖱️ Click to view: **[UML/Submit_Review_Sequence_Diagram.svg](./UML/Submit_Review_Sequence_Diagram.svg)**

---

## 💡 Facade Role:
Each API delegates to a **facade service**, which hides complexity and ensures clean interaction with the business logic. This keeps the APIs lightweight and maintainable.

---

## 🔗 Mermaid.js code for all the Sequence diagrams:

🖱️ Click to view: **[code/](./code/)**

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
│   └── Create_Place_Sequence_Diagram.svg
│   └── User_Registration_Sequence_Diagram.svg
├── Code/
│   └── Login_Sequence_Diagram.mmd
│   └── Submit_Review_Sequence_Diagram.mmd
│   └── Create_Place_Sequence_Diagram.mmd
│   └── User_Registration_Sequence_Diagram.mmd

```

## 👩‍💻 Authors

- **Haneen Aldawood** 
 (https://github.com/hyvuz))
- **Nada Alshuraidah** 
 (https://github.com/Nada-Al-Shuraidah))
- **Bushra Alshulail** 
 (https://github.com/Bushraalshulail))
  

© 2025 – Holberton School & Tuwaiq Academy
