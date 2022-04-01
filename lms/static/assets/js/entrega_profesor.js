const alumnos = JSON.parse(document.getElementById('alumnos').textContent);
const tarea = JSON.parse(document.getElementById('tarea').textContent);


const app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            alumnos: [],
            alumnos_copia: [],
            tarea: {},
            calificaciones: {},

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
        estado_td (alumno) {
            id = alumno.id;
            if (this.calificaciones.id){
                return "<span class='calificado'> Calificado </span>"
            } else {
                if (alumno.ultima_entrega) {
                    return "<span class='porCalificar'> Por calificar </span>"
                } else {
                    return "<span class='sinEntregar'> Sin entregar </span>"
                }
            }
        },
        calificacion_td (alumno) {
            id = alumno.id;
            if (this.calificaciones.id == null) {
                return `<textarea cols='3' rows='1' class='txtNota'></textarea>/${this.tarea.nota_maxima}`
            } else {
                return `<textarea cols='3' rows='1' class='txtNota'>[[calificaciones.alumno_id.nota]]</textarea>/${this.tarea.nota_maxima}`
            }
        },
        comentario_td (alumno) {
            id = alumno.id;
            if (this.calificaciones.id == null) {
                return `<textarea cols='15' rows='2' class='txtComentario'></textarea>`
            } else {
                return `<textarea cols='15' rows='2' class='txtComentario'>${this.calificaciones.id.comentario}</textarea>`
            }
        },
        fecha_entrega_td (alumno) {
            if (alumno.ultima_entrega) {
                return this.formato_fecha(alumno.ultima_entrega)
            } else {
                return `Sin fecha`
            }
        },
        fecha_calificacion_td (alumno) {
            id = alumno.id;
            if (this.calificaciones.id == null) {
                return `Sin fecha`
            } else {
                return this.formato_fecha(this.calificaciones.id.fecha_calificacion)
            }  
        },
        nombre_archivo(archivo) {
            return archivo.split("/").slice(-1).pop();
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
        get_calificaciones() {

            //ME HE QUEDADO AQUI NO CONSIGO HACER EL MAPA DE CALIFICACIONES
              fetch(`/api/calificaciones/${tarea.id}`, {method: 'GET'})
                .then(response => response.json())
                .then((result) => {
                    let calificaciones = result.data;
                    for (let index = 0; index < calificaciones.length; index++) {
                        const calificacion = calificaciones[index];
                        this.calificaciones.calificacion.alumno_id = calificacion;
                    }
                    console.log(calificaciones)
                    console.log('calis', this.calificaciones)
                })
                .catch(error => this.calificaciones={});
        },
        guardar(alumno) {
        
        },
    },
    mounted() {

        //recojer tarea de la template
        this.tarea = tarea;
        console.log(this.tarea)
        //recojer alumnos de la template
        this.alumnos = alumnos;
        this.alumnos_copia = alumnos
        console.log('alumnos', this.alumnos)
        //fetch entregas de los alumnos
        this.get_calificaciones();
        //se ordena por primera vez
        this.ordenar_nombre();

    }
});
app.mount('#app');