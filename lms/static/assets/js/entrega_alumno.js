const entrega = JSON.parse(document.getElementById('entrega').textContent);
const ejercicio = JSON.parse(document.getElementById('ejercicio').textContent);


const app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            ejercicio: {},
            entrega: {},
            test: 'hola',
            comentario: '',
        }
    },
    methods: {
        nombre_archivo() {
            return this.entrega.archivo.split('/').pop();
        },
        formato_fecha(fecha) {
            try {
                let fecha2 = `${fecha.split("T")[0].split("-")[2]}/${fecha.split("T")[0].split("-")[1]}/${fecha.split("T")[0].split("-")[0]}`
                let hora = `${fecha.split("T")[1].split("Z")[0].split(':')[0]}:${fecha.split("T")[1].split("Z")[0].split(':')[1]}`
                return fecha2 + '-' + hora
            } catch (error) {
                return "No hay fecha"
            }
        },
        guardar() {
            var myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");

            var raw = JSON.stringify({
                "comentario": this.comentario,
            });

            var requestOptions = {
                method: 'POST',
                headers: myHeaders,
                body: raw      
            };
            fetch(`/api/entrega_alumno/${this.ejercicio.id}/`, requestOptions)
            .then(respuesta => respuesta.json())
            .then((res) => {
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
        console.log("mounted")
        this.ejercicio = ejercicio;
        console.log(this.ejercicio);
        this.entrega = entrega;
        console.log(this.entrega);
        this.comentario = entrega.comentario_alumno;
    }
});
app.mount('#app');