var width=$(".bannerbox").width();
var i=-1;
var timer=0;
$(document).ready(function () {
    move();
    timer=setInterval("move()",3000);
    $(".bannerbox ul li").hover(function(){
        clearInterval(timer);
    },function(){
        timer=setInterval("move()",9000);
    })
    $('.nav ul li').click(function(){
        var ddIndex=$(this).index()-1;
        i=ddIndex;
        move();
    })
})
function move(){
    i++;
    $('.baner-01-a').css({"top":"100px",opacity:0});
    $('.baner-01-b').css({"top":"400px",opacity:0});
    $('.banner2-02,.banner2-03').css({opacity:0});
    $('.banner2-01').css({opacity:0,"left":"-100px"});
    $('.banner3-04').css({opacity:0,"bottom":"100px"});
    $('.banner3-01').css({opacity:0});
    $('.banner3-02').css({opacity:0});
    $('.banner3-03').css({opacity:0});
    if(i>=3){
        i=0;
    }
    if(i<3){
        if(i==0){
            //$('.fst-li').fadeIn(100).siblings().fadeOut(100);
            $('.nav ul li').eq(i).addClass('bg').siblings().removeClass('bg');
            $('.bannerbox ul li').eq(i).fadeIn(100).siblings().fadeOut();
            $('.baner-01-a').animate({"top":"174px",opacity:1},450,function(){
                $('.baner-01-b').animate({"top":"400px",opacity:1},450)
            });
        }
        if(i==1){
            //$(".sec-li").fadeIn(100).siblings().fadeOut(100);
            $('.nav ul li').eq(i).addClass('bg').siblings().removeClass('bg');
            $('.bannerbox ul li').eq(i).fadeIn(100).siblings().fadeOut();
            $('.banner2-02').animate({opacity:1},300,function(){
                $('.banner2-03').animate({opacity:1},300,function(){
                    $('.banner2-01').animate({opacity:1,"left":0},300);
                });
            });
        }
        if(i==2){
            $('.nav ul li').eq(i).addClass('bg').siblings().removeClass('bg');
            $('.bannerbox ul li').eq(i).fadeIn(100).siblings().fadeOut();
            $('.banner3-04').animate({opacity:1,"bottom":"0"},225,function(){
                $('.banner3-01').animate({opacity:1,"margin-left":"-360px"},225,function(){
                    $('.banner3-02').animate({opacity:1,"margin-left":"-305px"},225,function(){
                        $('.banner3-03').animate({opacity:1,"margin-left":"-107px"},225);
                    });
                });
            });
        }
    }
}

