const app = Vue.createApp({
  delimiters: ['[[', ']]'],
  data() {
      return {
          id_entrega: '',

          curso: '',
          ejercicio: '',
          nombre: '',
          correo: '',
          archivo: '',
          comentario_alumno: '',
          comentario_profesor: '',
          fecha_publicacion: '',
          fecha_edicion: '',
          nota: '',
          nota_maxima: '',
          enviar_notificacion: false
      };
  },
  watch: {

    id_entrega: {
      handler(id) {
        this.get_data(id);
      }
    }

  },
  methods: {

    get_data(id) {
      
      fetch(`/api/entrega/${id}`, {method: 'GET'})
        .then(response => response.json())
        .then((result) => {
          let entrega = result.data[0];

          this.archivo = entrega.archivo;
          this.comentario_alumno = entrega.comentario_alumno;
          this.comentario_profesor = entrega.comentario_profesor;
          this.fecha_publicacion = entrega.fecha_publicacion;
          this.fecha_edicion = entrega.fecha_edicion;
          this.nota = entrega.nota;

          fetch(`/api/usuario/${entrega.autor_id}`, {method: 'GET'})
            .then(response => response.json())
            .then((result) => {
              let usuario = result.data[0];

              this.nombre = `${usuario.first_name} ${usuario.last_name}`;
              this.correo = usuario.email;

            });

          fetch(`/api/ejercicio/${entrega.ejercicio_id}`, {method: 'GET'})
            .then(response => response.json())
            .then((result) => {
              let ejercicio = result.data[0];

              this.ejercicio = ejercicio.titulo;
              this.nota_maxima = ejercicio.nota_maxima;

              fetch(`/api/curso/${ejercicio.curso_id}`, {method: 'GET'})
                .then(response => response.json())
                .then((result) => {
                  let curso = result.data[0];

                  this.curso = curso.titulo;

                })

            })

        })
        .catch(error => console.log('error', error));
    },

    set_entrega(id_entrega) {
      this.id_entrega = id_entrega;
    }

  },
  mounted() {
    this.set_entrega(1);
  }
});
app.mount('#app');