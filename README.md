# 🏠 HBNB Evolution – Part 1 Documentation

Welcome to the technical documentation for **HBnB Evolution**, a simplified version of the Airbnb application. This file summarizes the architecture and design decisions made in Part 1 of the project. It includes UML diagrams, entity descriptions, and interaction flows between system layers.

---

## 📌 Overview

This project is organized using a **three-layer architecture**:

- **Presentation Layer:** Exposes APIs to users.
- **Business Logic Layer:** Manages application rules and operations.
- **Persistence Layer:** Handles data storage and retrieval.

The **Facade Pattern** is used to simplify communication between layers.

---

## 📦 Task 0: High-Level Package Diagram

This diagram shows the three-layer architecture and how the components interact.

📎 **[View Package Diagram](../UML/package_diagram.svg)**

- **Presentation Layer:** Contains UserAPI, PlaceAPI, etc.
- **Business Logic Layer:** Includes the core models and the FacadeService.
- **Persistence Layer:** Communicates with the database using Repositories.

---

## 🧩 Task 1: Class Diagram – Business Logic Layer

This diagram shows the main entities and their relationships.

📎 **[View Class Diagram (Mermaid.js)](../Code/Class_Diagram.mmd)**

- `User`: Has first name, last name, email, password, is_admin.
- `Place`: Belongs to a user, includes title, description, price, location.
- `Amenity`: Can be attached to multiple places.
- `Review`: Connected to both Place and User.

Entities follow business rules such as one-to-many or many-to-many relationships.

---

## 🔁 Task 2: Sequence Diagrams (API Interaction)

Sequence diagrams showing request/response flows across all layers.

### 🔐 Login Flow
📎 **[View Login Sequence](../Code/sequence_login.mmd)**

### ✍️ Submit Review Flow
📎 **[View Submit Review Sequence](../Code/sequence_submit_review.mmd)**

More diagrams like Place Creation and Fetching Places can be added similarly.

---

## 📚 Summary

- ✅ **Layered architecture** improves separation of concerns.
- ✅ **Facade pattern** simplifies access to core services.
- ✅ UML diagrams make the design clear and easy to implement.

This documentation will guide the development of the full application in upcoming phases.

---

© 2025 – Holberton School | Tuwaiq Academy
