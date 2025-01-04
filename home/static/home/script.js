document.addEventListener('DOMContentLoaded', () => {
    const track = document.querySelector('.carousel-track');
    const slides = Array.from(track.children);
    const prevButton = document.querySelector('.prev-button');
    const nextButton = document.querySelector('.next-button');

    let currentSlide = 0;
    const totalSlides = slides.length;

    function updateSlidePosition() {
        // Slide width = container width
        // We can just shift track by `currentSlide * 100%`.
        const slideWidth = slides[0].getBoundingClientRect().width;
        track.style.transform = `translateX(-${currentSlide * slideWidth}px)`;
    }

    // Move to next slide
    nextButton.addEventListener('click', () => {
        currentSlide = (currentSlide + 1) % totalSlides; 
        // e.g. if on last slide, wrap around to 0
        updateSlidePosition();
    });

    // Move to previous slide
    prevButton.addEventListener('click', () => {
        currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
        // e.g. if on first slide (0) and you go back, wrap to last
        updateSlidePosition();
    });
});
