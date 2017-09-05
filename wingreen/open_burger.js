

jQuery(document).ready(function ($) {
    $(document).ready(function(){
      
    $('#nav-icon1').click(function(){
          
      $(this).toggleClass('open');
      $('.menu-topmenu-container').toggleClass('open');
      $('#page').toggleClass('open');
    });
  });
  
});
