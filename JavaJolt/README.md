**JavaJolt — Backend API**

A RESTful Java backend for a coding learning platform, enabling user authentication, course management, exercise tracking and progress persistence via a layered architecture. Developed as a 3rd semester portfolio project at CPH Business Academy.

**Tech Stack:**

| **Layer**    | **Technology**                        |
|----------|-----------------------------------|
| Language | Java 17                           |
| Framework | Javalin 7                         |
| ORM      | Hibernate 6 / JPA                 |
| Database | PostgreSQL 16                     |
| Security | JWT (JJWT 0.12.3) + BCrypt        |
| Testing  | JUnit 5, Rest Assured 5, Hamcrest |
| Build    | Maven 3                           |
| Logging  | SLF4J + Logback                   |

**Architecture**

The project follows a layered architecture with separation of concerns across five layers:

**HTTP Request → ApplicationConfig (Javalin + JWT before-filter) → Routes → Controllers → Services (business logic) → DAOs (database access) → PostgreSQL**

**Controllers** receive HTTP requests, extract parameters, delegate to the service layer and return responses. They contain no business logic.

Services contain all business logic — input validation, orchestration between DAOs and domain exception throwing. They have no knowledge of HTTP context.

**DAOs** handle all database operations via Hibernate EntityManager. BaseDAO provides generic CRUD via reflection. Each DAO extends it with entity-specific JPQL queries.

**Entities** are JPA-annotated classes mapped to PostgreSQL tables. All implement soft delete via isDeleted and carry a createdAt timestamp set on persist.

**DTOs** decouple the API contract from the persistence model, preventing internal entity structure from leaking into HTTP responses.