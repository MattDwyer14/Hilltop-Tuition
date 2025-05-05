document.addEventListener('DOMContentLoaded', () => {
    const track = document.querySelector('.carousel-track');
    const slides = Array.from(track.children);
    const prevButton = document.querySelector('.prev-button');
    const nextButton = document.querySelector('.next-button');

    let currentSlide = 0;
    const totalSlides = slides.length;
    const intervalTime = 1000; // 1 second per slide

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

    let slideInterval = setInterval(() => {
        currentSlide = (currentSlide + 1) % totalSlides;
        updateSlidePosition();
    }, intervalTime);

    window.addEventListener('resize', () => {
        clearInterval(slideInterval);
        slideInterval = setInterval(() => {
            currentSlide = (currentSlide + 1) % totalSlides;
            updateSlidePosition();
        }, intervalTime);
    });
});
