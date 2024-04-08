# Product Api

#### _Please read General API Information first_

### check_permissions(func)

A decorator function that checks user permissions before executing an endpoint method.

#### Parameters

- `func` (function): The endpoint method to be decorated.

#### Returns

- `function`: The decorated function that checks user permissions.

#### Functionality

1. Check if user is authenticated. If not, log a warning and abort with a 401 (Unauthorized) status code.
2. Check if the user has access to the company associated with the resource. If not, log a warning and abort with a
   403 (
   Forbidden) status code.
3. Check if user has pipeline permission in the navbar. If not, log a warning and abort with a 403 (Forbidden) status
   code.
4. If all checks are passed, execute the endpoint method.

Note: This decorator assumes that the `current_user` variable is available, which should be an instance of the `User`
model. Additionally, it requires that the endpoint method being decorated has a `company_id` keyword argument, which is
used to determine which company the resource belongs to.

# **ProductsResource**

## **1. Edit Products**

```http
GET /api/products/<int:product_id>/edit
```

- Authorization: Access token

**Request Body:**

| Name           | Type        | Required | Values(default) | Description                     |
|----------------|-------------|----------|-----------------|---------------------------------|
| product_id     | int         | YES      | None            | Id of the product to be edited. |
| avatar         | str         | NO       | None            | Avatar of the product.          |
| name           | str         | NO       | None            | Name of the product.            |
| price          | float       | NO       | None            | Price of the product.           |
| currency       | str         | NO       | None            | Currency of the product.        |
| description    | str         | NO       | None            | Description of the product.     |
| product_images | List of str | NO       | None            | Images of the product.          |

**Returns:** ShortProductType

**Example:**

- URL:

```url
GET /api/products/1/edit
```

- Request Body:

```json
{
  "avatar": "New avatar",
  "name": "New name",
  "price": 1,
  "currency": "New currency",
  "description": "New description",
  "product_images": [
    "New img1",
    "New img2",
    "New img3",
    "New img4"
  ]
}
```

```json
{
  "ok": true,
  "description": "Product data Updated",
  "result": {
    "avatar": "New avatar",
    "name": "New name",
    "price": 1.0,
    "currency": "New currency",
    "description": "New description",
    "images": [
      {
        "image": "New img1"
      },
      {
        "image": "New img2"
      },
      {
        "image": "New img3"
      },
      {
        "image": "New img4"
      }
    ]
  }
}
```