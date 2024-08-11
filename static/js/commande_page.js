window.addEventListener('load', () => {
    let toogle_command = document.querySelector('#toogle_command');
    let toogle_zone = document.querySelector('.zone_btn');
    let go_form = document.querySelector('.go_form');
    let set_panier = document.querySelector('#set_panier');
    let total_price_cmmd = document.querySelector('#total_price_cmmd');
    let increments = document.querySelector('#increments');
    let decrements = document.querySelector('#decrements');
    let values = document.querySelector('#values');
    let bubles_services = document.querySelector('.zone_infos_services');
    let selects = document.querySelector('#commune');
    let livraison_price = document.querySelector('#montant_livraison');
    let prix_prod = document.querySelector('#prix_prod');
    let prod_name = document.querySelector('.prod_name');
    let storageSucces = document.querySelector('#storageSucces');
    let poids = document.querySelector('#poids');


    values.value = 1;
    livraison_price.innerHTML = selects.options[selects.selectedIndex].value;
    prix_prod.innerHTML = poids.options[poids.selectedIndex].value;

    function toggle_command_form() {
        go_form.classList.toggle('active');
        toogle_zone.style.display = "none";
        set_panier.style.display = "none";
    }

    toogle_command.addEventListener('click', toggle_command_form);

    function prixTotal() {
        const Tab = [parseInt(prix_prod.innerHTML) * parseInt(values.value), parseInt(livraison_price.innerHTML)];
        const sum = Tab.reduce((acc, entre) => acc + entre);
        total_price_cmmd.innerHTML = sum;
        document.querySelector('#sendTotal').value = sum;
    }
    prixTotal();

    function bhn() {
        if (values.value < 99) {
            values.style.width = '40px';
        } else if (values.value > 99) {
            values.style.width = '55px';
        }

        if (values.value > 999) {
            bubles_services.style.display = 'flex';
        } else if (values.value <= 999) {
            bubles_services.style.display = 'none';
        }
    }

    increments.addEventListener('click', () => {
        if (values.value >= 1) {
            values.value++;
            prixTotal();
        } else {
            window.location.reload();
        }
        bhn();
    });

    decrements.addEventListener('click', () => {
        if (values.value > 1) {
            values.value--;
            prixTotal();
        } else {
            window.location.reload();
        }
        bhn();
    });


    function createPanierVideToNavigation(panier_name) {
        let panier = [];
        existe = localStorage.getItem(panier_name);
        if (!existe) {
            localStorage.setItem(panier_name, JSON.stringify(panier));
        }
    }
    createPanierVideToNavigation(set_panier.getAttribute('class'));

    function formElement() {
        data = {
            'id_prod': prod_name.getAttribute('id'),
            'nom_prod': prod_name.textContent,
            'prix_prod': parseInt(prix_prod.innerHTML),
            'qts': values.value,
        }

        return data;
    }

    function SuccesPanier() {
        storageSucces.style.display = 'flex';

        setTimeout(() => {
            storageSucces.style.display = 'none';
        }, 5000);
    }

    function setPanierToNavigation(panier_name) {
        let panier = getPanierToNavigation(panier_name);
        let data = formElement();
        if (panier.length != 0) {
            if (data) {
                for (let i = 0; i < panier.length; i++) {
                    if (panier[i]['id_prod'] == data.id_prod) {
                        if (panier[i]['nom_prod'] != data.nom_prod) {
                            panier.push(data);
                            localStorage.setItem(panier_name, JSON.stringify(panier));
                            SuccesPanier();
                        }
                    } else {
                        panier.push(data);
                        localStorage.setItem(panier_name, JSON.stringify(panier));
                        SuccesPanier();
                    }
                }
            }
        } else {
            if (data) {
                panier.push(data);
                localStorage.setItem(panier_name, JSON.stringify(panier));
                SuccesPanier();
            }
        }
    }

    set_panier.addEventListener('click', (e) => {
        setPanierToNavigation(set_panier.getAttribute('class'));
    });


    function getPanierToNavigation(panier_name) {
        let panier = localStorage.getItem(panier_name);
        if (panier) {
            panier = JSON.parse(panier);
        } else {
            createPanierVideToNavigation(panier_name);
            window.location.reload();
        }

        return panier;
    }


    selects.addEventListener('change', (e) => {
        livraison_price.innerHTML = selects.options[selects.selectedIndex].value;
        prixTotal();
    });


    poids.addEventListener('change', (e) => {
        prix_prod.innerHTML = poids.options[poids.selectedIndex].value;
        prixTotal();
    });

})