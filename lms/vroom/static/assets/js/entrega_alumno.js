const entregas = JSON.parse(document.getElementById('entregas').textContent);
const tarea = JSON.parse(document.getElementById('tarea').textContent);
const calificacion = JSON.parse(document.getElementById('calificacion').textContent);


const app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            tarea: {},
            entregas: [],
            calificacion: {},
        }
    },
    methods: {
        formato_fecha(fecha) {
            try {
                let fecha2 = `${fecha.split("T")[0].split("-")[2]}/${fecha.split("T")[0].split("-")[1]}/${fecha.split("T")[0].split("-")[0]}`
                let hora = `${fecha.split("T")[1].split("Z")[0].split(':')[0]}:${fecha.split("T")[1].split("Z")[0].split(':')[1]}`
                return fecha2 + '-' + hora
            } catch (error) {
                return "No hay fecha"
            }
        },
        guardar(id_entrega) {
            var myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");

            console.log($(`#comentario${id_entrega}`).val())

            var raw = JSON.stringify({
                "comentario": $(`#comentario${id_entrega}`).val(),
                "entrega_id": id_entrega,
            });
            
            var requestOptions = {
                method: 'POST',
                headers: myHeaders,
                body: raw      
            };

            console.log(requestOptions)
            fetch(`/api/entrega_alumno/${this.tarea.id}/`, requestOptions)
            .then(respuesta => respuesta.json())
            .then((res) => {
                console.log(res)
                let alerta = $(`<div class='alert alert-${res.tipo}' role='alert'>${res.msg}</div>`);
                alerta.appendTo($('body'));
                alerta.fadeIn();
                setTimeout(
                    function() {
                        alerta.fadeOut( () => alerta.remove())
                    }, 2000);
                })
                .catch(error => console.log(error));
        }
    },
    mounted() {
        this.tarea = tarea;
        console.log(this.tarea)
        this.entregas = entregas;
        console.log(this.entregas)
        this.calificacion = calificacion
        console.log(this.calificacion)
    }
});
app.mount('#app');