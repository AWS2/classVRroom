[:arrow_left: Atras](../documentacion.md)

# Pin Request

Usado para generar un PIN que relaciona el ejercicio y el usuario

**URL** : `/api/pin_request/`

**Method** : `GET`

**Token required** : SI

**Data constraints**

```json
{
    "VRtaskID": "[valid VRtask id]"
}
```

**Data example**

```json
{
    "VRtaskID": "2"
}
```

## Success Response

**Content example**

```json
{
    "status": "OK",
    "message": "Pin generado.",
    "PIN": 8492
}
```

## Error Response

**Condition** : Si ya existe el pin para ese usuario en ese ejercicio

**Content** :

```json
{
    "status": "ERROR",
    "message": "Ya existe un pin para este usuario."
}
```