const entrega = JSON.parse(document.getElementById('entrega').textContent);
const ejercicio = JSON.parse(document.getElementById('ejercicio').textContent);


const app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            ejercicio: {},
            entrega: {},
            test: 'hola'
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
    },
    mounted() {
        console.log("mounted")
        this.ejercicio = ejercicio;
        console.log(this.ejercicio);
        this.entrega = entrega;
        console.log(this.entrega);
    }
});
app.mount('#app');