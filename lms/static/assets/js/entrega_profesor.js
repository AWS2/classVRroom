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

            orden: 'desc',
            filtro: ''
        }
    },
    computed: {
        usuario_th: function () {
            if (this.orden == 'desc') {
                return 'Usuario ▲'
            } else {
                return 'Usuario ▼'
            }
        }
    },
    watch: {

        orden: {
            handler() {
                this.ordenar();
            }
        },

        filtro: {
            handler() {
                this.filtrar();
            }
        }
    
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
        cambiarOrden() {
            if (this.orden == 'desc') {
                this.orden = 'asc';
            } else {
                this.orden = 'desc';
            }
        },
        ordenar() {
            let alumnos = this.alumnos;

            let mayor = (this.orden=='desc') ? 1 : -1 
            let menor= (this.orden=='desc') ? -1 : 1

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
        filtrar() {

            let alumnos = this.alumnos_copia;
            let filtrado = [];

            alumnos.forEach( (alumno) => {
                let cond1 = alumno.first_name.toLowerCase().indexOf(this.filtro.toLowerCase()) != -1;
                let cond2 = alumno.last_name.toLowerCase().indexOf(this.filtro.toLowerCase()) != -1;
                let cond3 = (alumno.first_name + ' ' + alumno.last_name).toLowerCase().indexOf(this.filtro.toLowerCase()) != -1;
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
        this.ordenar();

    }
});
app.mount('#app');