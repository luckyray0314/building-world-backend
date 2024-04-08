# Customers Api

#### _Please read General API Information first_

### check_permissions(func)

A decorator function that checks user permissions before executing an endpoint method.

#### Parameters

- `func` (function): The endpoint method to be decorated.

#### Returns

- `function`: The decorated function that checks user permissions.

#### Functionality

1. Check if user is authenticated. If not, log a warning and abort with a 401 (Unauthorized) status code.
2. Check if user has access to the company associated with the resource. If not, log a warning and abort with a 403 (
   Forbidden) status code.
3. Check if user has pipeline permission in the navbar. If not, log a warning and abort with a 403 (Forbidden) status
   code.
4. If all checks passed, execute the endpoint method.

Note: This decorator assumes that the `current_user` variable is available, which should be an instance of the `User`
model. Additionally, it requires that the endpoint method being decorated has a `company_id` keyword argument, which is
used to determine which company the resource belongs to.

# **CustomerResource**

## **1. Search for customers**

```http
GET /api/company/company_id/customers
```

- Authorization: Access token

**Request Body:**

| Name       | Type | Required | Values(default) | Description                                         |
|------------|------|----------|-----------------|-----------------------------------------------------|
| company_id | int  | Yes      | None            | Id of the company who's customers we are searching. |
| name       | str  | NO       | None            | First or Last name of the customer.                 |
| phone      | str  | NO       | None            | phone number of the customer.                       |
| email      | str  | NO       | None            | email of the customer.                              |

**Returns:** List or Single ShortCustomerType

**Example:**

- URL:

```url
GET /api/company/1/customers
```

- Request Body:

```
```

```json
{
  "ok": true,
  "description": "Got Customer(s)",
  "result": [
    {
      "customer_id": 11,
      "date": 1684319727.648047,
      "first_name": "lola",
      "last_name": "doe",
      "phone_number": "12345678910",
      "email": "lola@mail.com"
    },
    {
      "customer_id": 10,
      "date": 1684319727.646052,
      "first_name": "bron",
      "last_name": "gayer",
      "phone_number": "1234567899",
      "email": "bron@mail.com"
    },
    {
      "customer_id": 9,
      "date": 1684319727.644023,
      "first_name": "isabella",
      "last_name": "gayer",
      "phone_number": "1234567898",
      "email": "isabella@mail.com"
    },
    {
      "customer_id": 8,
      "date": 1684319727.642157,
      "first_name": "misty",
      "last_name": "girl",
      "phone_number": "1234567897",
      "email": "misty@mail.com"
    },
    {
      "customer_id": 7,
      "date": 1684319727.640399,
      "first_name": "anon",
      "last_name": "boy",
      "phone_number": "1234567896",
      "email": "anon@mail.com"
    },
    {
      "customer_id": 6,
      "date": 1684319727.638536,
      "first_name": "doe",
      "last_name": "john",
      "phone_number": "1234567895",
      "email": "john2@mail.com"
    },
    {
      "customer_id": 5,
      "date": 1684319727.636572,
      "first_name": "doe",
      "last_name": "deo",
      "phone_number": "1234567894",
      "email": "deo@mail.com"
    },
    {
      "customer_id": 4,
      "date": 1684319727.63479,
      "first_name": "john",
      "last_name": "doe",
      "phone_number": "1234567893",
      "email": "john@mail.com"
    },
    {
      "customer_id": 3,
      "date": 1684319727.632717,
      "first_name": "man",
      "last_name": "baby",
      "phone_number": "1234567892",
      "email": "man@mail.com"
    },
    {
      "customer_id": 2,
      "date": 1684319727.630923,
      "first_name": "baby",
      "last_name": "guy",
      "phone_number": "1234567891",
      "email": "guy@mail.com"
    }
  ]
}
```

- URL:

```url
GET api/company/1/customers?name=boy
```

- Request Body:

```
```

```json
{
  "ok": true,
  "description": "Got Customer(s)",
  "result": [
    {
      "customer_id": 7,
      "date": 1684319727.640399,
      "first_name": "anon",
      "last_name": "boy",
      "phone_number": "1234567896",
      "email": "anon@mail.com"
    },
    {
      "customer_id": 1,
      "date": 1684319727.628385,
      "first_name": "baby",
      "last_name": "boy",
      "phone_number": "1234567890",
      "email": "baby@mail.com"
    }
  ]
}
```

- URL:

```url
GET api/company/1/customers?phone=1234567890
```

- Request Body:

```
```

```json
{
  "ok": true,
  "description": "Got Customer(s)",
  "result": {
    "customer_id": 1,
    "date": 1684319727.628385,
    "first_name": "baby",
    "last_name": "boy",
    "phone_number": "1234567890",
    "email": "baby@mail.com"
  }
}
```

- URL:

```url
GET api/company/1/customers?email=man@mail.com
```

- Request Body:

```
```

```json
{
  "ok": true,
  "description": "Got Customer(s)",
  "result": {
    "customer_id": 3,
    "date": 1684319727.632717,
    "first_name": "man",
    "last_name": "baby",
    "phone_number": "1234567892",
    "email": "man@mail.com"
  }
}
```
