$(document).ready(function(){
	AOS.init();
});

$('.navbar-collapse a').click(function(){
    $(".navbar-collapse").collapse('hide');
});

$('.navbar-collapse a:not(.dropdown-toggle)').click(function(){
    if($(window).width() < 768 )
        $('.navbar-collapse').collapse('hide');
});

var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
  var currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    document.getElementById("navbar").style.top = "0";
    // document.getElementById("navbar").style.opacity = '1';
    document.getElementById("navbarResponsive").style.opacity = '1';
  } else {
    document.getElementById("navbar").style.top = "-90px";
    // document.getElementById("navbar").style.opacity = '0';
    document.getElementById("navbarResponsive").style.opacity = '0';
  }
  prevScrollpos = currentScrollPos;
}