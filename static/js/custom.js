"use strict";


function CounterNumberChanger () {
  var timer = $('.timer');
  if(timer.length) {
    timer.appear(function () {
      timer.countTo();
    })
  }
}

// gallery fancybox activator 
function GalleryFancyboxActivator () {
  var galleryFcb = $('.fancybox');
  if(galleryFcb.length){
    galleryFcb.fancybox({
      openEffect  : 'elastic',
      closeEffect : 'elastic',
      helpers : {
        media : {}
      }
    });
  }
}

// revolution slider
function revolutionSliderActiver () {
  if ($('.rev_slider_wrapper #slider1').length) {
    jQuery("#slider1").revolution({
      sliderType:"standard",
      sliderLayout:"auto",
      delay:9000,
      navigation: {
        arrows:{enable:true} 
      }, 
      gridwidth:1170,
      gridheight:760 
    });
  };
}

// Google Map
function gMap () {
  if ($('.google-map').length) {
    $('.google-map').each(function () {
      // getting options from html 
      var mapName = $(this).attr('id');
      var mapLat = $(this).data('map-lat');
      var mapLng = $(this).data('map-lng');
      var iconPath = $(this).data('icon-path');
      var mapZoom = $(this).data('map-zoom');
      var mapTitle = $(this).data('map-title');

      // if zoom not defined the zoom value will be 15;
      if (!mapZoom) {
        var mapZoom = 15;
      };
      // init map
      var map;
        map = new GMaps({
            div: '#'+mapName,
            scrollwheel: false,
            lat: mapLat,
            lng: mapLng,
            zoom: mapZoom
        });
        // if icon path setted then show marker
        if(iconPath) {
        map.addMarker({
            icon: iconPath,
              lat: mapLat,
              lng: mapLng,
              title: mapTitle
          });
      }
    });  
  };
}

function contactFormValidation () {
  if($('.contact-form').length){
    $('.contact-form').validate({ // initialize the plugin
      rules: {
        name: {
          required: true
        },
        email: {
          required: true,
          email: true
        },
        message: {
          required: true
        },
        subject: {
          required: true
        }
      },
      submitHandler: function (form) { 
        // sending value with ajax request
        $.post($(form).attr('action'), $(form).serialize(), function (response) {
          $(form).parent('div').append(response);
          $(form).find('input[type="text"]').val('');
          $(form).find('input[type="email"]').val('');
          $(form).find('textarea').val('');
        });
        return false;
      }
    });
  }
}

function stickyHeader () {
  if ($('.stricky').length) {
    var strickyScrollPos = $('.stricky').next().offset().top;
    if($(window).scrollTop() > strickyScrollPos) {
      $('.stricky').addClass('stricky-fixed'); 
    }
    else if($(this).scrollTop() <= strickyScrollPos) {
      $('.stricky').removeClass('stricky-fixed');
    }
  };
}
// twitter feed widget 
//function twitterFeedWidget () {
//  if ($('.twitter').length) {
//    $.ajax({
//          method: "POST",
//          url: "includes/twitter/tweet-api.php",
//          data: {}
//      })
//      .done(function(msg) {
//          $(".twitter").append(function () {
//            return msg;
//          });
//      });
//  };
//}

function progressBarConfig () {
  var progressBar = $('.progress');
  if(progressBar.length) {
    progressBar.each(function () {
      var Self = $(this);
      Self.appear(function () {
        var progressValue = Self.data('value');

        Self.find('.progress-bar').animate({
          width:progressValue+'%'           
        }, 2000);

        Self.find('span.value').countTo({
          from: 0,
            to: progressValue,
            speed: 2000
        });
      });
    })
  }

}


function mobileMenuConfig () {
  if($('.nav_main_list').length){
    $('.navbar-toggle').on('click', function () {
      $('.nav_main_list').slideToggle();
    });
  }
}


jQuery(window).on('scroll', function() {
  (function ($) {
    stickyHeader();
  })(jQuery);  
});
jQuery(window).on('load', function() {
  (function ($) {
    twitterFeedWidget();
  })(jQuery);  
});

jQuery(document).on('ready', function() {
  (function ($) {
    revolutionSliderActiver();
    CounterNumberChanger();
    GalleryFancyboxActivator();
    gMap();
    progressBarConfig();
    mobileMenuConfig();
    contactFormValidation();


  if ($('#button').length) {
    $('#button').on('click', function(){
      $('#search').toggle(300)
    });
  };
  if ($('.custom-scroll-bar').length && $(window).width() <= 1170 ) {
    $('.custom-scroll-bar').mCustomScrollbar();
    console.log('logged!');
  };

  if ($('.mainmenu-area nav ul li.arrow_down').length) {
    $('.mainmenu-area nav ul li.arrow_down').append(function () {
      return '<i class="fa fa-bars"></i>';
    });
  };
  if ($('.mainmenu-area nav ul li.arrow_down .fa').length) {
    $('.mainmenu-area nav ul li.arrow_down .fa').on('click', function () {
      $(this).parent('li').children('div').slideToggle();
    });
  };
  if ($('#mixitup_list').length) {
    $('#mixitup_list').mixItUp(); // mix it up 
  };

  if ($(".dropdown-menu li").length) {
    $(".dropdown-menu li").on('click', function(){
      $(this).parents(".dropdown").find('.btn').html($(this).text() + ' <i class="fa fa-angle-down"></i>');
      $(this).parents(".dropdown").find('.btn').val($(this).data('value'));
    });
  };

  })(jQuery);



});



