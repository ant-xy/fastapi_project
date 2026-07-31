# Create User
- send a JSON `POST` request to the API endpoint with the following body:

```json
{
  "username": "string",
  "password": "string"
}
```

## Returns
- hashed password: just for ease of use and testing (i know you do not do that in prod).
- username: the username you entered.
- account id: the id of the acccount you entered.

## Checks
- **UNIQUE** `username` only.
- returns a "Something went wrong, try again later" message if integrity checks fail.

# Check User
- send a `GET` request to the API endpoint `/user/` with the query parameter `user_id` having the value of the ID of the user you want to check.

## Returns
- If the user ID is found, returns a `Payload` object with the `data` containing `key, value` pairs of the username and id.
- If the user ID is NOT found, returns a `Payload` object with `data` containing a list of all users in the database.
  - key value pairs being "username" and "id"

# Login User

- send a JSON `POST` request containing the following body:
```json
{
  "username": "string",
  "password": "string"
}
```

## Returns
- object `Token` or "Username or password incorrect"
- the JSON response contains:
```json
{
  "jwt": <jwt token>,
  "token_type": <token type>
}
```

## JSON Web Token Contents
- the JWT token contains the `user` (username of the user logging in) and the `exp` (expiry) of the token.
