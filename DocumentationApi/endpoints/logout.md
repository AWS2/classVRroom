[:arrow_left: Atras](../documentacion.md)

# Logout

Usado para deslogear un usuario y eliminar el token de la base de datos

**URL** : `/api/logout/`

**Method** : `GET`

**Token required** : SI


## Success Response

**Content example**

```json
{
    "status": "OK",
    "message": "Sesión cerrada."
}
```

## Error Response

**Condition** : Si el token no existe o no es correcto

**Content** :

```json
{
    "detail": "Invalid token."
}
```