# Hiearchy Api 
#### _Please read General API Information first_



## **1. Who Am I**

```http
GET /api/whoami
```
* Authorization: Access token

**Returns:** UserType

**Example:**
* Response:
```json
{
    "ok": true,
    "description": "Got user details.",
    "result": {
        "id": 1,
        "external_id": "96d9ea73ec584aa79956a8a52cd406df",
        "email": "baby",
        "first_name": "Baby",
        "last_name": null,
        "companies": [
            {
                "name": "Amazon1",
                "owner_id": 1,
                "avatar": null
            }
        ],
        "phone_number": "30369",
        "role": "user",
        "is_admin": false,
        "registered_on": 1677435291.304674,
        "is_active": true,
        "is_online": false,
        "avatar": null,
        "confirmed_on": 1677435291.769746
    }
}
```



## **2. Refresh the token**

```http
GET /api/refresh
```
* Authorization: Refresh token

**Returns:** AccessTokenType  

**Example:**
* Response:
```json
{
    "ok": true,
    "description": "",
    "result": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3NzQzNTQ4NywianRpIjoiZjFkNGEyN2EtMThhZC00YTk1LWE3ODktYjg4ZDNmNTU4MmY3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Ijk2ZDllYTczZWM1ODRhYTc5OTU2YThhNTJjZDQwNmRmIiwibmJmIjoxNjc3NDM1NDg3LCJleHAiOjE2Nzc0MzcyODd9.OxPxTJ0KxHxpoHFijZSozKOvY413-a9sBHqE3lATHhk"
    }
}
```

