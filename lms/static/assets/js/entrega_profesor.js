const alumnos = JSON.parse(document.getElementById('alumnos').textContent);
const ejercicio = JSON.parse(document.getElementById('ejercicio').textContent);


const app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            entregas: [],
            alumnos: [],
            alumnos_copia: [],
            ejercicio: {},

            orden_nombre: 'desc',
            filtro_nombre: '',
            
            orden_estado: 'desc',
            filtro_estado: '',

        }
    },
    computed: {
        usuario_th: function () {
            if (this.orden_nombre == 'desc') {
                return 'Usuario ▲'
            } else {
                return 'Usuario ▼'
            }
        },
        estado_th: function () {
            if (this.orden_estado == 'desc') {
                return 'Estado ▲'
            } else {
                return 'Estado ▼'
            }
        },
    },
    watch: {

        orden_nombre: {
            handler() {
                this.ordenar_nombre();
            }
        },

        filtro_nombre: {
            handler() {
                this.filtrar_nombre();
            }
        },

        orden_estado: {
            handler() {
                this.ordenar_estado();
            }
        },
    
    },
    methods: {
        nombre_archivo(archivo) {
            return archivo
            // return archivo.split("/").slice(-1).pop();
        },
        formato_fecha(fecha) {
            try {
                
                return `${fecha.split("T")[0].split("-")[2]}/${fecha.split("T")[0].split("-")[1]}/${fecha.split("T")[0].split("-")[0]}-${fecha.split("T")[1].split("Z")[0]}`
            } catch (error) {
                return "No hay fecha"
            }
        },
        cambiarOrden_nombre() {
            if (this.orden_nombre == 'desc') {
                this.orden_nombre = 'asc';
            } else {
                this.orden_nombre = 'desc';
            }
        },
        cambiarOrden_estado() {
            if (this.orden_estado == 'desc') {
                this.orden_estado = 'asc';
            } else {
                this.orden_estado = 'desc';
            }
        },
        ordenar_nombre() {
            let alumnos = this.alumnos;

            let mayor = (this.orden_nombre=='desc') ? 1 : -1 
            let menor= (this.orden_nombre=='desc') ? -1 : 1

            alumnos.sort( (a, b) => {
                if (a["first_name"] > b["first_name"]) {
                    return mayor;
                } else if (a["first_name"] < b["first_name"]) {
                    return menor;
                } else {
                    return 0
                }
            })

            this.alumnos = alumnos;
            console.log(alumnos)
        },
        ordenar_estado() {
            let alumnos = this.alumnos;

            alumnos.forEach(alumno => {
                let entrega = this.entregas.find(entrega => entrega.autor_id == alumno.id)
                if (entrega) {
                    if (entrega.nota || entrega.nota == 0) {
                        alumno.estado = 2;
                    } else {
                        alumno.estado = 0;
                    }
                } else {
                    alumno.estado = 1;
                }
            });


            let mayor = (this.orden_estado=='desc') ? 1 : -1
            let menor= (this.orden_estado=='desc') ? -1 : 1

            mapa = {
                "Por calificar": 0,
                "No entregado": 1,
                "Calificado": 2,
            }

            alumnos.sort( (a, b) => {
                if (a["estado"] > b["estado"]) {
                    return mayor;
                } else if (a["estado"] < b["estado"]) {
                    return menor;
                } else {
                    return 0
                }
            })

            this.alumnos = alumnos;
            console.log(alumnos)
        },
        filtrar_nombre() {

            let alumnos = this.alumnos_copia;
            let filtrado = [];

            alumnos.forEach( (alumno) => {
                let cond1 = alumno.first_name.toLowerCase().indexOf(this.filtro_nombre.toLowerCase()) != -1;
                let cond2 = alumno.last_name.toLowerCase().indexOf(this.filtro_nombre.toLowerCase()) != -1;
                let cond3 = (alumno.first_name + ' ' + alumno.last_name).toLowerCase().indexOf(this.filtro_nombre.toLowerCase()) != -1;
                if ( cond1 || cond2 || cond3 ) {
                    filtrado.push(alumno)
                }
            });

            this.alumnos = filtrado;

        },
        get_entregas() {

              fetch(`/api/entregas/${ejercicio.id}`, {method: 'GET'})
                .then(response => response.json())
                .then((result) => {
                    let entregas = result.data;
                    this.entregas = entregas;
                    console.log(this.entregas)
                })
                .catch(error => console.log('error', error));
        },
        get_entrega(alumno) {
            
            for (let i = 0; i < this.entregas.length; i++) {
                const entrega = this.entregas[i];
                if (entrega.autor_id === alumno.id) {
                    return entrega;
                }
            }
            return false
        },
        guardar(alumno) {

            var myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");
            if (!this.get_entrega(alumno)) {

                var raw = JSON.stringify({
                    "new_note": document.getElementById("nota"+alumno.id).value,
                    "comment_prof": document.getElementById("comentario"+alumno.id).value,
                    "autor": alumno.id,
                });

                var requestOptions = {
                    method: 'POST',
                    headers: myHeaders,
                    body: raw      
                };

                fetch(`/api/entrega_nueva_cal/${this.ejercicio.id}/`, requestOptions)
                .then(respuesta => respuesta.json())
                .then((res) => {
                    console.log('res:', res)
                    let alerta = $(`<div class='alert alert-${res.tipo}' role='alert'>${res.msg}</div>`);
                    alerta.appendTo($('body'));
                    alerta.fadeIn();
                    setTimeout(
                        function() {
                            alerta.fadeOut( () => alerta.remove())
                        }, 2000);
                    })
                    .catch(error => console.log(error));
                    this.get_entregas()

            } else {

                let entrega = this.get_entrega(alumno);

                var raw = JSON.stringify({
                    "new_note": document.getElementById("nota"+alumno.id).value,
                    "comment_prof": document.getElementById("comentario"+alumno.id).value,
                  });

                var requestOptions = {
                    method: 'PUT',
                    headers: myHeaders,
                    body: raw      
                };

                fetch(`/api/entrega/${entrega.id}`, requestOptions)
                .then(respuesta => respuesta.json())
                .then((res) => {
                    console.log('res:', res)
                    let alerta = $(`<div class='alert alert-${res.tipo}' role='alert'>${res.msg}</div>`);
                    alerta.appendTo($('body'));
                    alerta.fadeIn();
                    setTimeout(
                        function() {
                            alerta.fadeOut( () => alerta.remove())
                    }, 2000);
                })
                .catch(error => console.log(error));

                this.get_entregas()
            }
        }  
    },
    mounted() {

        //recojer ejercicio de la template
        this.ejercicio = ejercicio;
        //recojer alumnos de la template
        this.alumnos = alumnos;
        this.alumnos_copia = alumnos
        //fetch entregas de los alumnos
        this.get_entregas();
        //se ordena por primera vez
        this.ordenar_nombre();

    }
});
app.mount('#app');