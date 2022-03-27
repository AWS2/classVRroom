$(document).ready(()=>{

    var $header = $('.header-container')

    $(document).scroll(()=>{

        var scrollTop = $(document).scrollTop();
        
        
        if(scrollTop>100){
            $header.addClass('shrink');
        }else if(scrollTop<50){
            $header.removeClass('shrink');
        }


    });


});

