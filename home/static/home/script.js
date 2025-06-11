document.addEventListener('DOMContentLoaded', () => {
  //
  // 1) MARQUEE AUTO-SCROLL
  //
  const marquee = document.querySelector('.marquee');
  let marqueeSpeed = 1; // this must be declared outside the function to be mutable
  let marqueePos = 0;

  function marqueeStep() {
    marqueePos += marqueeSpeed;
    if (marquee && marquee.scrollWidth) {
      if (marqueePos >= marquee.scrollWidth / 2) {
        marqueePos = 0;
      }
      marquee.scrollLeft = marqueePos;
      requestAnimationFrame(marqueeStep);
    }
  }

  if (marquee) {
    marqueeStep();

    marquee.addEventListener('mouseenter', () => {
      marqueeSpeed = 0;
    });
    marquee.addEventListener('mouseleave', () => {
      marqueeSpeed = 1;
    });
  }

  //
  // 2) CAROUSELS (Multiple instances)
  //
  const carousels = document.querySelectorAll('.carousel-container');

  carousels.forEach(container => {
    const track = container.querySelector('.carousel-track');
    const slides = Array.from(track.children);
    const prevButton = container.querySelector('.prev-button');
    const nextButton = container.querySelector('.next-button');
    let currentSlide = 0;

    function updateSlidePosition() {
      const slideWidth = slides[0].getBoundingClientRect().width;
      track.style.transform = `translateX(-${currentSlide * slideWidth}px)`;
    }

    if (nextButton) {
      nextButton.addEventListener('click', () => {
        currentSlide = (currentSlide + 1) % slides.length;
        updateSlidePosition();
      });
    }

    if (prevButton) {
      prevButton.addEventListener('click', () => {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        updateSlidePosition();
      });
    }

    window.addEventListener('resize', updateSlidePosition);

    // Initialise position
    updateSlidePosition();
  });
});
