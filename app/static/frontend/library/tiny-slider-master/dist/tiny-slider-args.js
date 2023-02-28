var slider = tns({
  container: ".my-slider",
  items: 1,
  gutter: 20,
  slideBy: 1,
  controlsPosition: "bottom",
  nav: false,
  navPosition: "bottom",
  mouseDrag: true,
  autoplay: true,
  autoplayButtonOutput: false,
  controlsContainer: "#custom-control",
  speed: 800,
  responsive: {
    0: {
      items: 1,
      nav: false
    },
    768: {
      items: 1,
      nav: true
    },
    1440: {
      items: 2
    }
  }
  // mode: 'gallery',
  // speed: 2000,
  // animateIn: "scale",
  // controls: false,
  // nav: false,
  // edgePadding: 20,
  // loop: false,
});