window.addEventListener('load', (e) => {
    let nb = document.querySelector('.nb-notif');
    nb.style.display = 'none';
    let i = 120;
    let submit = document.querySelector('#id87');

    function an(a, result) {
        nb.style.display = 'flex';
        if (a == 0) {
            submit.style.display = 'flex';
            clearInterval(result);
            nb.innerHTML = "Je n'es pas reçu de mail. rééssayer à présent !";
        } else {
            submit.style.display = 'none';
            nb.innerHTML = "Je n'es pas reçu de mail. rééssayer dans moins de : " + parseInt(a) + ' secondes';
        }
    }

    let bubleType = document.querySelector('span');
    let getAttribute = bubleType.getAttribute('class');

    if (getAttribute == 'error') {
        console.log('Erreur de traitement !');
    } else {
        let result = setInterval(decrement, 1000);

        function decrement() {
            an(i, result);
            i -= 1;
        }
    }
})