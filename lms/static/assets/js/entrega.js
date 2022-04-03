// if (window.location.protocol == "https:") {
//   var ws_scheme = "wss://";
// } else {
//   var ws_scheme = "ws://"
// };

// var socket = new WebSocket(
//   ws_scheme+
//   window.location.host+
//   '/ws/entrega/'
// );

// socket.onmessage = function(e) {
//   const data = JSON.parse(e.data);
//   console.log(`entrega con id=${data.id} ha sido editada`)
//   root.update_entrega(data.id)
// }

// socket.send(JSON.stringify({
//   'id': this.id_entrega
// }))

const entregas = JSON.parse(document.getElementById('entregas').textContent);
const alumno = JSON.parse(document.getElementById('alumno').textContent);
const tarea = JSON.parse(document.getElementById('tarea').textContent);
const curso = JSON.parse(document.getElementById('curso').textContent);
const lista_entregas = JSON.parse(document.getElementById('lista_entregas').textContent);

const app = Vue.createApp({
  delimiters: ['[[', ']]'],
  data() {
      return {
        id_alumno: '',
        primera_carga: true,

        entregas: [],
        alumno: {},
        tarea: {},
        curso: {},
        calificacion: {},
        lista_entregas: {},
      };
  },
  watch: {
    id_alumno: {
      handler(id) {
        this.actualizar(id);
      }
    },
  },
  methods: {
    get_alumno(id) {
      return fetch(`/api/usuario/${id}`, {method: 'GET'})
        .then(response => response.json())
        .then((res) => {
          this.alumno = res.data[0];
        })
        .catch(error => console.error(error));  

    },
    get_entregas() {

      fetch(`/api/entregas/${this.tarea.id}?alumno=${this.alumno.id}`, {method: 'GET'})
        .then(response => response.json())
        .then((res) => {
          this.entregas = res.data;
        })
        .catch(error => {
          console.error(error)
          this.entregas = [];
        });
    },
    get_calificacion() {

      fetch(`/api/calificacion/${this.tarea.id}?alumno=${this.alumno.id}`, {methos: "GET"})
      .then(response => response.json())
      .then((res) => {
        this.calificacion = res.data
      })
      .catch(error => {
        console.error(error)
        this.calificacion = false;
      });

    },
    actualizar(id) {

      if (this.primera_carga) {
        this.primera_carga = false;
        return;
      }

      console.log("actualizando id", id)
      
      this.get_alumno(id).then( () => {
        this.get_entregas();
        this.get_calificacion();

        let url = window.location.href
        url = url.split("/")
        url.pop()
        url = url.join("/") + "/" + this.alumno.id
        window.history.pushState(null, null, url);
      })
    },
    set_anterior() {

      let indice = this.lista_entregas.indexOf(this.id_alumno);
      if (indice == 0) {
        this.id_alumno = this.lista_entregas[this.lista_entregas.length - 1];
      } else {
        this.id_alumno = this.lista_entregas[indice - 1];
      }

    },
    set_siguiente() {

      let indice = this.lista_entregas.indexOf(this.id_alumno);
      if (indice == this.lista_entregas.length - 1) {
        this.id_alumno = this.lista_entregas[0];
      } else {
        this.id_alumno = this.lista_entregas[indice + 1];
      }

    },
  },
  mounted() {

    this.lista_entregas = lista_entregas  
    console.log(this.lista_entregas)
    this.entregas = entregas;
    this.alumno = alumno;
    this.id_alumno = this.alumno.id;
    this.tarea = tarea;
    this.curso = curso;
    
    this.get_calificacion();

  }
});
const root = app.mount('#app');
