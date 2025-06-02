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

### ⚙️ Components:
- `DatabaseAccess`
  - `saveData()`
  - `retrieveData()`

This abstraction layer ensures the system can switch between storage engines (like FileStorage or DBStorage) without changing core logic.

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

🖱️ Click to view: **[Code/class_diagram.mmd](../Code/class_diagram.mmd)**

---

# 🔁 Task 2: API Sequence Diagrams

We created sequence diagrams to show how API calls interact with all layers.

---

## 🔐 Login API Flow
```
User -> UserAPI: login(credentials)
UserAPI -> UserServices: authenticate(credentials)
UserServices -> UserRepository: findUserByCredentials()
UserRepository --> UserServices: User
UserServices --> UserAPI: AuthToken
UserAPI --> User: AuthToken
```
📎 [View Source](../Code/sequence_login.mmd)

---

## ✍️ Review Submission API Flow
```
User -> ReviewAPI: submit_review(reviewData, token)
ReviewAPI -> ReviewServices: submit_review(reviewData, userID)
ReviewServices -> ReviewRepository: saveReview(review)
ReviewRepository --> ReviewServices: Review
ReviewServices --> ReviewAPI: ReviewConfirmation
ReviewAPI --> User: ReviewConfirmation
```
📎 [View Source](../Code/sequence_submit_review.mmd)

---

# ✅ Summary

- Built using **Layered Architecture**
- Applied the **Facade Pattern** for clarity and modularity
- Created **UML Diagrams** to guide implementation
- Designed for easy extension in the next project phases

This documentation reflects our **real design decisions**, helping others understand the exact structure, naming, and flow of the HBnB Evolution system.

---

📁 Directory Layout
```
part1/
├── README.md
├── UML/
│   └── package_diagram.png
├── Code/
│   ├── class_diagram.mmd
│   ├── sequence_login.mmd
│   └── sequence_submit_review.mmd
```

© 2025 – Holberton School & Tuwaiq Academy
