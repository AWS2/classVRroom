// $( () => {
//     $(".contenido").mouseenter( (e) => {
//         if ($(e.target).attr("class") !== 'contenido') return;
//         let icono = $(e.target).find("img");
//         let src = icono.attr('src');
//         src = src.split(".");
//         src.pop();
//         src = src.join() + '.gif';
//         icono.attr('src', src);
//     });
//     $(".contenido").mouseleave( (e) => {
//         if ($(e.target).attr("class") !== 'contenido') return;
//         let icono = $(e.target).find("img");
//         let src = icono.attr('src')
//         src = src.split(".");
//         src.pop();
//         src = src.join() + '.png';
//         icono.attr('src', src);
//     });
// });

function goToTarea(id_tarea){
    console.log(`#tarea-${id_tarea}`)
    $(`#tarea-${id_tarea}`).submit();
}