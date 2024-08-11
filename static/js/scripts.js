window.addEventListener('load', () => {
    let contentImg = document.querySelectorAll('.content_img');

    for (let i = 0; i < contentImg.length; i++) {
        contentImg[i].addEventListener('click', (e) => {
            const tab = [];
            let centerImage = contentImg[i].parentElement.querySelector('.image-one').src;
            tab.push(centerImage, e.target.src);

            contentImg[i].parentElement.querySelector('.image-one').setAttribute('src', tab[1]);
            e.target.setAttribute('src', tab[0]);
        })
    }
    let p = document.querySelectorAll('.descrip');
    let selection = Splitting({ target: p, by: "chars", whitespace: true });
    gsap.registerPlugin(ScrollTrigger);

    for (let i = 0; i < p.length; i++) {
        gsap.from(selection[i].words, {
            color: 'white',
            rotation: '360',
            stagger: 0.5,
            scrollTrigger: {
                trigger: p[i],
                start: "top 97%",
                end: "bottom bottom",
                scrub: true,
            }
        })
    }

    const lenis = new Lenis();

    lenis.on('scroll', ScrollTrigger.update);

    gsap.ticker.add((time) => {
        lenis.raf(time * 600);
    });

    gsap.ticker.lagSmoothing(0);
})