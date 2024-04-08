
## **1. UserType**
This object represents a user.

Field | Type | Default | Description
------------ | ------------ | ------------ | ------------
id | int | | Unique identifier for a user
external_id | str | | Unique string identifier for a user, lenght is 32
email | str | | Email
first_name | str | | 
last_name | str | | 
phone_number | str | | Phone number without "+", only digits but string
registered_on | float | | Date when a user registered. Unix timestamp, so you need to convert it to the string which is human readable
confirmed_on | float | |  Date when a user confirmed his email. Unix timestamp, so you need to convert it to the string which is human readable
role | str | "user" | Role of a user in the system
is_admin | bool | false | True if a user has an administrator permission
is_active | bool | false | Turns true when a user verifies his email, if a user is blocked soon it will be false
is_online | bool | false | True if a user is online
companies | Array of ShortCompanyType | empty list | 
avatar | str | null | Base64 encoded string for the image file


