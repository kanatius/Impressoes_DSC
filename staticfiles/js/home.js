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
    //grayscale no primeiro slide
    setTimeout(carouselToGrayscale, 4000);
    //passa os slides
    setInterval(autoplay, 9000);
    /* Function for dropdown use in mobile or on small screens*/
    $('.sidenav').sidenav();
  });