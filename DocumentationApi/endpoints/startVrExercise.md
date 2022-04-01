[:arrow_left: Atras](../documentacion.md)

# Start Vr Exercise

Te devuelve todos los cursos de todos los centros

**URL** : `/api/start_vr_exercise/`

**Method** : `GET`

**Token required** : NO

**Data constraints**

```json
{
    "pin": "[valid pin]"
}
```

**Data example**

```json
{
    "VRtaskID": "3050"
}
```


## Success Response

**Content example**

```json
{
    "status": "OK",
    "username": "Antonio Calvo",
    "VRexerciseID": 1,
    "minExerciseVersion": 1.0
}
```

## Pin Not Found Response

**Condition** : Si el pin no existe

**Content** :

```json
{
    "status": "ERROR",
    "message": "Pin no encontrado."
}
```