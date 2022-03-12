```mermaid
erDiagram
    USER ||--o{ GADGET : ""
    USER {
        int id
        varchar_128 password
        datetime_6 last_login
        tynyint_1 is_superuser
        varchar_150 username
        varchar_150 first_name
        varchar_150 last_name
        varchar_254 email
        tynyint_1 is_staff
        tynyint_1 is_active
        datetime_6 date_joined
    }
    GADGET ||--o| PURCHASE : ""
    GADGET ||--o| GIFT : ""
    GADGET ||--o{ CATALOGUE : ""
    GADGET {
        int id
        varchar name
        varchar model
        varchar brand
        enum aquisition_type
        varchar free_form
        int user_id FK
    }
    PURCHASE {
        int id
        datetime date
        int price_ati
        varchar shop
        int gadget_id FK
    }
    GIFT {
        int id
        datetime date
        varchar sender
        varchar reason
        int gadget_id FK
    }
    CATALOGUE {
        int id
        varchar url
        int gadget_id FK
    }

```