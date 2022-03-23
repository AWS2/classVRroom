$(document).ready(()=>{

    var $header = $('.header-container')

    $(document).scroll(()=>{

        var scrollTop = $(document).scrollTop();
        
        
        if(scrollTop>1){
            $header.addClass('shrink');
        }else{
            $header.removeClass('shrink');
        }


    });

});