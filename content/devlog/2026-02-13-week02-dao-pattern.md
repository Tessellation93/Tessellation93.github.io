---
title: "Week 02–03 - IDAO Interface, BaseDAO & All Entities"
date: 2026-02-13
draft: false
tags: ["JavaJolt", "DAO", "BCrypt", "SoftDelete", "JPA"]
---

## Task

Extend the data model to cover all entities and establish a consistent pattern for database access across the whole project.

## What was built

Five entities: `User`, `Course`, `Lesson`, `Exercise`, `Progress`. One shared interface `IDAO<T>`, one generic `BaseDAO<T>` implementing it, and specific DAOs that extend BaseDAO and add entity-specific methods.
```java
public interface IDAO<T> {
    T findById(Long id);
    List<T> findAll();
    T save(T entity);
    T update(T entity);
    void delete(Long id);
}
```

`BaseDAO` implements this for any entity type. Each specific DAO extends it and only adds what's unique, f.eks. `UserDAO.findByEmail()`.

## Soft Delete

Every entity has `is_deleted`. The `delete()` method in each DAO sets this flag instead of removing the row:
```java
public void delete(Long id) {
    try (EntityManager em = HibernateConfig.getEntityManagerFactory().createEntityManager()) {
        em.getTransaction().begin();
        User user = em.find(User.class, id);
        if (user != null) {
            user.setDeleted(true);
            em.merge(user);
        }
        em.getTransaction().commit();
    }
}
```

`findAll()` filters them out:
```java
return em.createQuery(
    "SELECT u FROM User u WHERE u.isDeleted = false", User.class
).getResultList();
```

## BCrypt Password Hashing

Passwords are hashed in the `User` constructor, it's impossible to accidentally create a user with a plain text password:
```java
public User(String username, String email, String password, boolean isAdmin) {
    this.username = username;
    this.email = email;
    this.password = BCrypt.hashpw(password, BCrypt.gensalt(12));
    this.isAdmin = isAdmin;
}

public boolean verifyPassword(String plainText) {
    return BCrypt.checkpw(plainText, this.password);
}
```

The hash looks like: `$2a$12$N9qo8uLOickgx2ZMRZoMye...`  the `12` is the cost factor (2^12 = 4096 hashing rounds). Higher cost = slower brute force. 

## Generic interface

Early in the project there were too many overlapping interfaces: `IGenericDAO`, `ICRUD`, and others with duplicate method signatures. It created confusion about which one to implement. Collapsed everything into a single `IDAO<T>`, to ensure that any code that depends on it works with any entity without knowing which one. This makes mocking in tests straightforward too.
