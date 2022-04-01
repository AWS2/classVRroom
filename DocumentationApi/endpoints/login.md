[:arrow_left: Atras](../documentacion.md)

# Login

Usado para cojer el Token asignado a un usuario registrado.

**URL** : `/api/login/`

**Method** : `GET`

**Token required** : NO

**Data constraints**

```json
{
    "username": "[valid email address]",
    "password": "[password in plain text]"
}
```

**Data example**

```json
{
    "username": "iloveauth@example.com",
    "password": "abcd1234"
}
```

## Success Response

**Content example**

```json
{
    "status": "OK",
    "message": "Autenticado con éxito.",
    "token": "3d3fb2a2993aabada7741197d34c6e8b8061e70a"
}
```

## Error Response

**Condition** : Si el email o la contraseña falta o no son correctos

**Content** :

```json
{
    "status": "ERROR",
    "message": "Authentication error."
}
```