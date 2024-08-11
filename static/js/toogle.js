window.addEventListener('load', () => {
    let icon = document.querySelectorAll('.icon');
    let champ = document.querySelectorAll('.xvfrt');
    let menu = document.querySelector('.logo_menu');
    let flex = document.querySelector('.zone_a');


    for (let i = 0; i < icon.length; i++) {
        icon[i].addEventListener('click', () => {
            champ[i].classList.toggle('activate');
            console.log('click', i);
        })
    }

    menu.addEventListener('click', () => {
        flex.classList.toggle('active');
        console.log('men deroulant');
    })
})