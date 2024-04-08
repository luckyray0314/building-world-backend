# Registrations Api 
#### _Please read General API Information first_





## **1. User Log in**

```http
POST /api/login
```

**Parameters:** 

Name | Type | Required | Values(default) | Description
------------ | ------------ | ------------ | ------------ | ------------
email | str | YES |     | 
password | str | YES |     | 
remember_me | bool | NO |   false  | If True, RT expires after a month, otherwise a day




**Example:**
* Body:
```json
{
    "email": "baby",
    "password": "baby",
    "remember_me": true
}
```
* Response:
```json
{
    "ok": true,
    "description": "Logged in successfully",
    "result": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3ODgxNjIzNywianRpIjoiZTQ3MmNjZTctNGQ5OS00ZjE1LTk4ZDctZGIyNTY4NTM1MWYzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Ijg0MTE4MjdiYjUxYzQxOTc5YWZkNmJkNDE1YTM2MmE4IiwibmJmIjoxNjc4ODE2MjM3LCJleHAiOjE2Nzg4MTc0Mzd9.tzmZgiIJknCec_utxBMlW1ESp4TMPO4cyjzUPcXRELc",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3ODgxNjIzNywianRpIjoiN2MyYjIwYzQtMmRjMi00NDY0LWI4OTAtMDMzOGE3OTA3MDIwIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiI4NDExODI3YmI1MWM0MTk3OWFmZDZiZDQxNWEzNjJhOCIsIm5iZiI6MTY3ODgxNjIzNywiZXhwIjoxNjgxNDA4MjM3fQ.SpFF_9_Tp00AHUscihg_I02VyJsYpZAy0Nc0-wvVhZs"
    }
}
```





## **2. Create a company**

```http
POST /api/create/company
```
* Authorization: Access token

**Parameters:** 

Name | Type | Required | Values(default) | Description
------------ | ------------ | ------------ | ------------ | ------------
name | str | YES |     | 
name_in_law | str | YES |     | 
login | str | YES |     | 
email | str | YES |     | 
phone_number | str | YES |     | 





**Example:**
* Body:
```json
{
    "name": "Amazon3",
    "name_in_law": "Amazon3 LLC",
    "login": "a3",
    "email": "amazon3@gmail.com",
    "phone_number": "+1235"
}
```
* Response:
```json
{
    "ok": true,
    "description": "Created successfully",
    "result": {
        "id": 4,
        "external_id": "7abbc90f50ab45ecab9a17ff63adf56e",
        "token_id": "9e195f7ca69575be30d4af0fddf6002d5080e83a1b21e037123ea530de8ff9c7",
        "name": "Amazon3",
        "name_in_law ": "Amazon3 LLC",
        "owner_id": 1
    }
}
```



