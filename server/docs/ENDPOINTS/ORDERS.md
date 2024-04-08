# Orders Api

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
4. If all checks are passed, execute the endpoint method.

Note: This decorator assumes that the `current_user` variable is available, which should be an instance of the `User`
model. Additionally, it requires that the endpoint method being decorated has a `company_id` keyword argument, which is
used to determine which company the resource belongs to.

# **OrderResource**

## **1. Get Orders of a company**

```http
GET /api/company/providers/provider_id/orders
```

- Authorization: Access token

**Request Body:**

| Name       | Type | Required | Values(default) | Description                                         |
|------------|------|----------|-----------------|-----------------------------------------------------|
| company_id | int  | Yes      | None            | Id of the company who's orders we are getting.      |
| status     | str  | NO       | None            | Status of the order (Paid, Pending, Refunded, etc). |

**Returns:** List of ShortOrderType

**Example:**

- URL:

```url
GET /api/company/providers/1/orders
```

- Request Body:

```
```

```json
{
  "ok": true,
  "description": "Got Company Order(s)",
  "result": [
    {
      "provider_id": 3,
      "order_price": 35.0,
      "status": "paid",
      "tracking_status": "in_transit",
      "ordered_date": 1684061398.038104,
      "order_items": []
    },
    {
      "provider_id": 3,
      "order_price": 30.0,
      "status": "paid",
      "tracking_status": "ordered",
      "ordered_date": 1684061398.036362,
      "order_items": []
    },
    {
      "provider_id": 3,
      "order_price": 25.0,
      "status": "pending",
      "tracking_status": "ordered",
      "ordered_date": 1684061398.034565,
      "order_items": []
    },
    {
      "provider_id": 3,
      "order_price": 45.0,
      "status": "refunded",
      "tracking_status": "delivered",
      "ordered_date": 1684061398.032719,
      "order_items": []
    },
    {
      "provider_id": 2,
      "order_price": 35.0,
      "status": "paid",
      "tracking_status": "in_transit",
      "ordered_date": 1684061398.030924,
      "order_items": []
    },
    {
      "provider_id": 2,
      "order_price": 30.0,
      "status": "paid",
      "tracking_status": "ordered",
      "ordered_date": 1684061398.028954,
      "order_items": []
    },
    {
      "provider_id": 2,
      "order_price": 25.0,
      "status": "pending",
      "tracking_status": "ordered",
      "ordered_date": 1684061398.026862,
      "order_items": []
    },
    {
      "provider_id": 1,
      "order_price": 45.0,
      "status": "refunded",
      "tracking_status": "delivered",
      "ordered_date": 1684061398.0244,
      "order_items": []
    },
    {
      "provider_id": 1,
      "order_price": 35.0,
      "status": "paid",
      "tracking_status": "in_transit",
      "ordered_date": 1684061398.021929,
      "order_items": []
    },
    {
      "provider_id": 1,
      "order_price": 30.0,
      "status": "paid",
      "tracking_status": "ordered",
      "ordered_date": 1684061398.020043,
      "order_items": [
        {
          "product_id": 2,
          "product_quantity": 3,
          "product": {
            "avatar": "Avatar",
            "name": "Sugar",
            "price": 25.0,
            "currency": "USD",
            "description": "10lb Sugar"
          }
        },
        {
          "product_id": 4,
          "product_quantity": 7,
          "product": {
            "avatar": "Avatar",
            "name": "Cola",
            "price": 2.5,
            "currency": "USD",
            "description": "Can of soda"
          }
        },
        {
          "product_id": 2,
          "product_quantity": 3,
          "product": {
            "avatar": "Avatar",
            "name": "Sugar",
            "price": 25.0,
            "currency": "USD",
            "description": "10lb Sugar"
          }
        },
        {
          "product_id": 4,
          "product_quantity": 5,
          "product": {
            "avatar": "Avatar",
            "name": "Cola",
            "price": 2.5,
            "currency": "USD",
            "description": "Can of soda"
          }
        },
        {
          "product_id": 2,
          "product_quantity": 1,
          "product": {
            "avatar": "Avatar",
            "name": "Sugar",
            "price": 25.0,
            "currency": "USD",
            "description": "10lb Sugar"
          }
        }
      ]
    }
  ]
}
```

- URL:

```url
GET api/company/providers/1/orders?status=paid
```

- Request Body:

```
```

```json
{
  "ok": true,
  "description": "Got Company Order(s)",
  "result": [
    [
      {
        "provider_id": 3,
        "order_price": 35.0,
        "status": "paid",
        "tracking_status": "in_transit",
        "ordered_date": 1684061398.038104,
        "order_items": []
      },
      {
        "provider_id": 3,
        "order_price": 30.0,
        "status": "paid",
        "tracking_status": "ordered",
        "ordered_date": 1684061398.036362,
        "order_items": []
      },
      {
        "provider_id": 2,
        "order_price": 35.0,
        "status": "paid",
        "tracking_status": "in_transit",
        "ordered_date": 1684061398.030924,
        "order_items": []
      },
      {
        "provider_id": 2,
        "order_price": 30.0,
        "status": "paid",
        "tracking_status": "ordered",
        "ordered_date": 1684061398.028954,
        "order_items": []
      },
      {
        "provider_id": 1,
        "order_price": 35.0,
        "status": "paid",
        "tracking_status": "in_transit",
        "ordered_date": 1684061398.021929,
        "order_items": []
      },
      {
        "provider_id": 1,
        "order_price": 30.0,
        "status": "paid",
        "tracking_status": "ordered",
        "ordered_date": 1684061398.020043,
        "order_items": [
          {
            "product_id": 2,
            "product_quantity": 3,
            "product": {
              "avatar": "Avatar",
              "name": "Sugar",
              "price": 25.0,
              "currency": "USD",
              "description": "10lb Sugar"
            }
          },
          {
            "product_id": 4,
            "product_quantity": 7,
            "product": {
              "avatar": "Avatar",
              "name": "Cola",
              "price": 2.5,
              "currency": "USD",
              "description": "Can of soda"
            }
          },
          {
            "product_id": 2,
            "product_quantity": 3,
            "product": {
              "avatar": "Avatar",
              "name": "Sugar",
              "price": 25.0,
              "currency": "USD",
              "description": "10lb Sugar"
            }
          },
          {
            "product_id": 4,
            "product_quantity": 5,
            "product": {
              "avatar": "Avatar",
              "name": "Cola",
              "price": 2.5,
              "currency": "USD",
              "description": "Can of soda"
            }
          },
          {
            "product_id": 2,
            "product_quantity": 1,
            "product": {
              "avatar": "Avatar",
              "name": "Sugar",
              "price": 25.0,
              "currency": "USD",
              "description": "10lb Sugar"
            }
          }
        ]
      }
    ]
  ]
}
```

## **2. Get Orders of a provider**

```http
GET /api/providers/provider_id/orders
```

- Authorization: Access token

**Request Body:**

| Name        | Type | Required | Values(default) | Description                                         |
|-------------|------|----------|-----------------|-----------------------------------------------------|
| provider_id | int  | Yes      | None            | Id of the provider whos orders we are getting.      |
| status      | str  | NO       | None            | Status of the order (Paid, Pending, Refunded, etc). |

**Returns:** List of ShortOrderType

**Example:**

- URL:

```url
GET /api/providers/1/orders
```

- Request Body:

```
```

```json
{
  "ok": true,
  "description": "Got Order(s)",
  "result": [
    {
      "provider_id": 1,
      "order_price": 45.0,
      "status": "refunded",
      "tracking_status": "delivered",
      "ordered_date": 1683773191.422812,
      "order_items": []
    },
    {
      "provider_id": 1,
      "order_price": 35.0,
      "status": "paid",
      "tracking_status": "in_transit",
      "ordered_date": 1683773191.421053,
      "order_items": []
    },
    {
      "provider_id": 1,
      "order_price": 30.0,
      "status": "paid",
      "tracking_status": "ordered",
      "ordered_date": 1683773191.41929,
      "order_items": [
        {
          "product_id": 2,
          "product_quantity": 3,
          "product": {
            "avatar": "Avatar",
            "name": "Sugar",
            "price": 25.0,
            "currency": "USD",
            "description": "10lb Sugar"
          }
        },
        {
          "product_id": 4,
          "product_quantity": 7,
          "product": {
            "avatar": "Avatar",
            "name": "Cola",
            "price": 2.5,
            "currency": "USD",
            "description": "Can of soda"
          }
        },
        {
          "product_id": 2,
          "product_quantity": 3,
          "product": {
            "avatar": "Avatar",
            "name": "Sugar",
            "price": 25.0,
            "currency": "USD",
            "description": "10lb Sugar"
          }
        },
        {
          "product_id": 4,
          "product_quantity": 5,
          "product": {
            "avatar": "Avatar",
            "name": "Cola",
            "price": 2.5,
            "currency": "USD",
            "description": "Can of soda"
          }
        },
        {
          "product_id": 2,
          "product_quantity": 1,
          "product": {
            "avatar": "Avatar",
            "name": "Sugar",
            "price": 25.0,
            "currency": "USD",
            "description": "10lb Sugar"
          }
        }
      ]
    },
    {
      "provider_id": 1,
      "order_price": 25.0,
      "status": "pending",
      "tracking_status": "ordered",
      "ordered_date": 1683773191.416942,
      "order_items": [
        {
          "product_id": 1,
          "product_quantity": 2,
          "product": {
            "avatar": "Avatar",
            "name": "Shampoo",
            "price": 10.0,
            "currency": "USD",
            "description": "Dove Shampoo"
          }
        },
        {
          "product_id": 3,
          "product_quantity": 5,
          "product": {
            "avatar": "Avatar",
            "name": "Bread",
            "price": 5.0,
            "currency": "USD",
            "description": "Sliced Bread"
          }
        },
        {
          "product_id": 1,
          "product_quantity": 1,
          "product": {
            "avatar": "Avatar",
            "name": "Shampoo",
            "price": 10.0,
            "currency": "USD",
            "description": "Dove Shampoo"
          }
        },
        {
          "product_id": 3,
          "product_quantity": 4,
          "product": {
            "avatar": "Avatar",
            "name": "Bread",
            "price": 5.0,
            "currency": "USD",
            "description": "Sliced Bread"
          }
        },
        {
          "product_id": 1,
          "product_quantity": 3,
          "product": {
            "avatar": "Avatar",
            "name": "Shampoo",
            "price": 10.0,
            "currency": "USD",
            "description": "Dove Shampoo"
          }
        },
        {
          "product_id": 3,
          "product_quantity": 2,
          "product": {
            "avatar": "Avatar",
            "name": "Bread",
            "price": 5.0,
            "currency": "USD",
            "description": "Sliced Bread"
          }
        }
      ]
    }
  ]
}
```

- URL:

```url
GET api/providers/1/orders?status=paid
```

- Request Body:

```
```

```json
{
  "ok": true,
  "description": "Got Order(s)",
  "result": [
    [
      {
        "provider_id": 1,
        "order_price": 35.0,
        "status": "paid",
        "tracking_status": "in_transit",
        "ordered_date": 1683773191.421053,
        "order_items": []
      },
      {
        "provider_id": 1,
        "order_price": 30.0,
        "status": "paid",
        "tracking_status": "ordered",
        "ordered_date": 1683773191.41929,
        "order_items": [
          {
            "product_id": 2,
            "product_quantity": 3,
            "product": {
              "avatar": "Avatar",
              "name": "Sugar",
              "price": 25.0,
              "currency": "USD",
              "description": "10lb Sugar"
            }
          },
          {
            "product_id": 4,
            "product_quantity": 7,
            "product": {
              "avatar": "Avatar",
              "name": "Cola",
              "price": 2.5,
              "currency": "USD",
              "description": "Can of soda"
            }
          },
          {
            "product_id": 2,
            "product_quantity": 3,
            "product": {
              "avatar": "Avatar",
              "name": "Sugar",
              "price": 25.0,
              "currency": "USD",
              "description": "10lb Sugar"
            }
          },
          {
            "product_id": 4,
            "product_quantity": 5,
            "product": {
              "avatar": "Avatar",
              "name": "Cola",
              "price": 2.5,
              "currency": "USD",
              "description": "Can of soda"
            }
          },
          {
            "product_id": 2,
            "product_quantity": 1,
            "product": {
              "avatar": "Avatar",
              "name": "Sugar",
              "price": 25.0,
              "currency": "USD",
              "description": "10lb Sugar"
            }
          }
        ]
      }
    ]
  ]
}
```