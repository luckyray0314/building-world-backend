# Profile Api

#### _Please read General API Information first_

## **1. Edit Profile**

```http
PUT /api/edit/profile
```

* Authorization: Access token

**Parameters:**

 Name  | Type | Required | Values(default)                                          | Description               
-------|------|----------|----------------------------------------------------------|---------------------------
 key   | str  | YES      | "first_name", "last_name", "avatar_link", "phone_number" | Key name of the user info 
 value | str  | YES      |                                                          | Value of the field        

**Returns:** UserType

**Example:**

* Body:

```json
{
  "key": "first_name",
  "value": "Baby Yoda"
}
```

* Response:

```json
{
  "ok": true,
  "description": "Profile edited",
  "result": {
    "id": 1,
    "external_id": "e9a9e08a422f4e3888af25a8280c71b0",
    "token_id": "2059c1aa80387619a5b058847c4be3a664aa48dd7eb871c0d402a2b983613662",
    "email": "baby",
    "first_name": "Baby Yoda",
    "last_name": null,
    "companies": [
      {
        "external_id": "1de6b9ec89e4492395be62ad2927f1e5",
        "name": "Amazon1",
        "owner_id": 1
      }
    ],
    "phone_number": null,
    "role": "user",
    "is_admin": false,
    "is_active": true
  }
}
```

## **2. Update Profile Status**

```http
PUT /api/profile/updateStatus
```

* Authorization: Access token

**Returns:** ShortUserType

**Parameters:**

| Name | Type | Required | Values(default) | Description |
|------|------|----------|-----------------|-------------|
| None |      |          |                 |             |

**Example:**

* Body:

```json
```

* Response:

```json
{
  "ok": true,
  "description": "User Online Status updated",
  "result": {
    "status": "Ok"
  }
}
```
