window.addEventListener('load', () => {
    let panier_name = document.querySelector('#conteneur_principal');
    let selects = document.querySelector('#commune');
    let livraison_price = document.querySelector('#montant_livraison');

    function afficheProd() {
        let panier_get = panier_name.getAttribute('class');

        let panier = localStorage.getItem(panier_get);
        document.querySelector('#setCommandes').value = panier;
        panier = JSON.parse(panier);

        if (panier && panier.length != 0) {
            for (let i = 0; i < panier.length; i++) {
                const prodContent = `
                <ul class="conteneur_prod">
                        <li>Produit : ${panier[i]['nom_prod']}</li>
                        <li class="dsr">Prix : ${panier[i]['prix_prod']} frs</li>
                        <li class="dsr">Quantitées : ${panier[i]['qts']}</li>
                        <li>
                            <button type="button" class="${panier[i]['id_prod']} delete_prod" style="align-items:center;display:flex;">
                                <ion-icon name="trash" class="icom"></ion-icon>
                                supprimer
                            </button>
                        </li>
                    </ul>
                `;
                panier_name.innerHTML += prodContent;

            }
        } else if (!panier || panier.length == 0) {
            document.querySelector('#yrdtsdz').style.display = 'none';
            let bublePanierVide = `<div class='bublePanierVide'>
                <div class='icon'><ion-icon name="sad"></ion-icon></div>
                <div class='texte'>
                    <p>Ooooh ! Votre panier est vide.
                        S'il vous plait veuiller ajouter des produits à
                        votre panier.
                    </p>
                </div>
            </div>`;
            panier_name.innerHTML += bublePanierVide;
            document.querySelector('#clear_panier').style.display = 'none';
        }
    }
    afficheProd();

    let deletedProd = document.querySelectorAll('.delete_prod');

    for (let i = 0; i < deletedProd.length; i++) {
        deletedProd[i].addEventListener('click', () => {
            let attribue = deletedProd[i].getAttribute('class');
            const tab = attribue.split(' ');
            const idProd = tab[0];

            let panier_get = panier_name.getAttribute('class');

            let panier = localStorage.getItem(panier_get);
            panier = JSON.parse(panier);

            if (panier.length != 0 && panier[i]['id_prod'] == idProd) {
                const newtab = panier.filter((element, index) => index != i);
                localStorage.setItem(panier_get, JSON.stringify(newtab));
                window.location.reload();
                console.log(newtab);
            }
        })
    }

    livraison_price.innerHTML = selects.options[selects.selectedIndex].value;
    selects.addEventListener('change', (e) => {
        livraison_price.innerHTML = selects.options[selects.selectedIndex].value;
        prixTotal();
    });

    function prixTotal() {
        let panier_get = panier_name.getAttribute('class');
        let panier = localStorage.getItem(panier_get);
        if (panier) {
            panier = JSON.parse(panier);
            let newpanier = panier.map((element) => element['prix_prod'] * element['qts']);
            const sum = newpanier.reduce((acc, entre) => acc + entre);
            total_price_cmmd.innerHTML = sum + parseInt(livraison_price.innerHTML);
            document.querySelector('#setTotal').value = sum + parseInt(livraison_price.innerHTML);
        }
    }
    prixTotal();

    document.querySelector('#clear_panier').addEventListener('click', () => {
        const panier = [];
        let panier_get = panier_name.getAttribute('class');
        localStorage.setItem(panier_get, JSON.stringify(panier))
        window.location.reload();
    });

})