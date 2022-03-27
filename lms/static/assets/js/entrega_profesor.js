const entregas = JSON.parse(document.getElementById('entregas').textContent);
const ejercicio = JSON.parse(document.getElementById('ejercicio').textContent);


const app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            entregas: [],
            ejercicio: {}
        }
    },
    methods: {
        nombre_archivo(archivo) {
            return archivo.split("/").slice(-1).pop();
        },
        formato_fecha(fecha) {
            try {
                
                return `${fecha.split("T")[0].split("-")[2]}/${fecha.split("T")[0].split("-")[1]}/${fecha.split("T")[0].split("-")[0]}-${fecha.split("T")[1].split("Z")[0]}`
            } catch (error) {
                return "No hay fecha"
            }
        }
    },
    mounted() {
        this.entregas = entregas;
        this.ejercicio = ejercicio;
        console.log(this.entregas);
        console.log(this.ejercicio)
    }
});
app.mount('#app');