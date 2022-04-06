[:arrow_left: Atras](../documentacion.md)

# Finish Vr Exercise

Te devuelve todos los cursos de todos los centros

**URL** : `/api/finish_vr_exercise/`

**Method** : `POST`

**Token required** : NO

**Data constraints**

```json
{
    "pin":"[valid pin]",
    "autograde":
        {
            "passed_items":"[int]",
            "failed_items":"[int]",
            "score":"[int]",
            "comments":"[str]"
        },
    "VRexerciseID":"[int]",
    "exerciseVersionID":"[float]",
    "performance_data":
        {
            "[random data idk]":"[random data idk]"
        }
}
```

**Data example**

```json
{
    "pin":3050,
    "autograde":
        {
            "passed_items":4,
            "failed_items":3,
            "score":73,
            "comments":"...to be decided..."
        },
    "VRexerciseID":1,
    "exerciseVersionID":1.0,
    "performance_data":
        {
            "ejemplo1":"ejemplo1"
        }
}
```


## Success Response

**Content example**

```json
{
    "status": "OK",
    "message": "Entrega guardada."
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