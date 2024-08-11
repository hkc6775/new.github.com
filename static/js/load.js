window.addEventListener('load', (e) => {
    let page = document.querySelector('.loading_page');
    let time = parseInt(e.timeStamp.toFixed())

    if (time) {
        page.style.display = 'none';
    }
})