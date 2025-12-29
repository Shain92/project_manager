# Блок-схема моделей базы данных

## Диаграмма связей моделей

```mermaid
erDiagram
    User ||--o{ Project : "ответственный (ManyToMany)"
    ProjectStatus ||--o{ Project : "имеет статус"
    
    User {
        int id PK
        string username
        string email
        string first_name
        string last_name
        datetime date_joined
        boolean is_active
        boolean is_staff
        boolean is_superuser
    }
    
    ProjectStatus {
        int id PK
        string name
        string color
    }
    
    Project {
        int id PK
        string name
        string cipher
        string code
        int completion_percent
        text note
        datetime created_at
        datetime updated_at
        int status_id FK
    }
```

## Описание моделей

### User
Кастомная модель пользователя, наследуется от AbstractUser Django.
- Связь с Project: ManyToMany (один пользователь может быть ответственным за несколько проектов)

### ProjectStatus
Модель статуса проекта.
- Поля: название, цвет (HEX формат)
- Связь с Project: OneToMany (один статус может быть у многих проектов)

### Project
Модель проекта.
- Поля: имя, шифр, код, процент готовности, примечание, даты создания/обновления
- Связь с ProjectStatus: ForeignKey (каждый проект имеет один статус)
- Связь с User: ManyToMany (у проекта может быть несколько ответственных)

