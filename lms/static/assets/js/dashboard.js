const app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            id_usuario: id,
            
            cursos: []
        }
    },
    mounted() {

        var requestOptions = {
            method: 'GET',
            redirect: 'follow'
        };
          
        fetch(`/api/usuario_cursos/${this.id_usuario}`, requestOptions)
            .then(response => response.json())
            .then((result) => {                
                result.data.forEach( curso => {
                    console.log(curso)
                    this.cursos.push(curso)
                })
            })
            .catch(error => console.log('error', error));        

    }
  });
  app.mount('#app');