document.addEventListener('DOMContentLoaded', () => {
    //
    // 1) MARQUEE AUTO-SCROLL
    //
    const marquee = document.querySelector('.marquee');
    let marqueePos = 0;
    const marqueeSpeed = 1; // px per frame
  
    function marqueeStep() {
      marqueePos += marqueeSpeed;
      // when we’ve scrolled half the duplicated content, reset
      if (marqueePos >= marquee.scrollWidth / 2) {
        marqueePos = 0;
      }
      marquee.scrollLeft = marqueePos;
      requestAnimationFrame(marqueeStep);
    }
  
    // start marquee loop
    marqueeStep();
  
    // optional: pause on hover
    marquee.addEventListener('mouseenter', () => {
      // stop by setting speed to 0
      marqueeSpeed = 0;
    });
    marquee.addEventListener('mouseleave', () => {
      marqueeSpeed = 1;
    });
  
    //
    // 2) CAROUSEL (MANUAL ONLY)
    //
    const track = document.querySelector('.carousel-track');
    const slides = Array.from(track.children);
    const prevButton = document.querySelector('.prev-button');
    const nextButton = document.querySelector('.next-button');
    let currentSlide = 0;
    const totalSlides = slides.length;
  
    function updateSlidePosition() {
      const slideWidth = slides[0].getBoundingClientRect().width;
      track.style.transform = `translateX(-${currentSlide * slideWidth}px)`;
    }
  
    nextButton.addEventListener('click', () => {
      currentSlide = (currentSlide + 1) % totalSlides;
      updateSlidePosition();
    });
  
    prevButton.addEventListener('click', () => {
      currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
      updateSlidePosition();
    });
  
    // recalc on resize so width stays correct
    window.addEventListener('resize', updateSlidePosition);
  });
  