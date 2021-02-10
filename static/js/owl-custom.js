// owl-carousel 
$(document).ready(function() {
 
  $("#owl").owlCarousel({
 
      navigation : false, // Show next and prev buttons
      slideSpeed : 100,
      paginationSpeed : 400,
      singleItem:true,
      autoPlay : 3000,
      rewindSpeed:100,
      stopOnHover: true
 
      // "singleItem:true" is a shortcut for:
      // items : 1, 
      // itemsDesktop : false,
      // itemsDesktopSmall : false,
      // itemsTablet: false,
      // itemsMobile : false
  });
});