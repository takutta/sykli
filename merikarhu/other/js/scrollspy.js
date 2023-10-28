$(window).on('scroll', function() {
    var scrollPos = $(document).scrollTop();
    $('#navbarToggler a').each(function() {
      var currLink = $(this);
      var refElement = $(currLink.attr('href'));
      if (
        refElement.position().top <= scrollPos &&
        refElement.position().top + refElement.height() > scrollPos
      ) {
        $('#navbarToggler ul li a').removeClass('active');
        currLink.addClass('active');
      } else {
        currLink.removeClass('active');
      }
    });
  });
  
  document.addEventListener('DOMContentLoaded', function() {
    var navTab = document.getElementById('nav-tab');
    if (navTab) {
      var tabButtons = navTab.querySelectorAll('button');
      tabButtons.forEach(function(button) {
        button.addEventListener('click', function() {
          var buttonId = button.id;
          var numericId = buttonId.replace(/\D/g, '');
          var navbarLinks = document.querySelectorAll('#navbarToggler a');
          navbarLinks.forEach(function(link) {
            var originalHash = link.getAttribute('href').split('#')[1];
            var newHref = '#' + originalHash.slice(0, -1) + numericId;
            link.href = newHref;
          });
        });
      });
    }
  
    function updateScrollSpy() {
      var scrollPos = $(document).scrollTop();
      $('#navbarToggler a').each(function() {
        var currLink = $(this);
        var refElement = $(currLink.attr('href'));
        if (
          refElement.position().top <= scrollPos &&
          refElement.position().top + refElement.height() > scrollPos
        ) {
          $('#navbarToggler ul li a').removeClass('active');
          currLink.addClass('active');
        } else {
          currLink.removeClass('active');
        }
      });
    }
  
    updateScrollSpy();
  });
  