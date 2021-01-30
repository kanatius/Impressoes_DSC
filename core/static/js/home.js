function carouselToGrayscale() {
    $('.carousel').css({
      "filter": "grayscale(100)"
    });
  }

  function carouselToColorsacale() {
    $('.carousel').carousel('next').css({
      "filter": "grayscale(0)",
    });
  }
  $(document).ready(function(){
    $('.modal').modal();
  });
  $("#login").css({
    "color" : "#0277bd"
  });
  function autoplay() {
    carouselToColorsacale();
    // Deixa o carrosel colorido após passar a imagem
    setTimeout(carouselToGrayscale, 5000);
  }

  $(document).ready(function () {
    $('.carousel.carousel-slider').carousel({
      fullWidth: true,
      indicators: false,
      duration: 500
    });
    $(".titles_carrousel").css({
      "font-size": 40,
      'font-weight': 'bold',
      'color': '#0277bd'
    });
    $(".carousel-item p").css({
      "font-size": 25,
      'color': '#0277bd'
    });
    $(".blue_color").css({
      'color': "#0277bd"
    });
    //grayscale no primeiro slide
    setTimeout(carouselToGrayscale, 4000);
    //passa os slides
    setInterval(autoplay, 9000);
    /* Function for dropdown use in mobile or on small screens*/
    $('.sidenav').sidenav();
  });