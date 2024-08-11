window.addEventListener('load', () => {
    function createHeaders(keys) {
        var result = [];
        for (var i = 0; i < keys.length; i += 1) {
            result.push({
                id: keys[i],
                name: keys[i],
                prompt: keys[i],
                width: 180,
                align: "center",
                padding: 0,
            });
        }
        return result;
    }


    let btn = document.querySelectorAll('.generer_pdf');
    let recu_command = document.querySelectorAll('.recu_command');
    for (let i = 0; i < btn.length; i++) {
        btn[i].addEventListener('click', (e) => {
            function getHeaderElement() {
                let tab = [
                    recu_command[i].children[0].children[0].children[0].children[0].children[0].children[0].textContent,
                    recu_command[i].children[0].children[0].children[0].children[0].children[1].children[0].textContent,
                    recu_command[i].children[0].children[0].children[0].children[0].children[2].children[0].textContent,
                    recu_command[i].children[0].children[1].children[0].children[0].children[0].src,
                ];
                return tab;
            }


            function getFooterElement() {
                for (let o = 0; o < recu_command[i].children[2].children[0].children.length; o++) {
                    if (recu_command[i].children[2].children[0].children[o].getAttribute('class') == 'status') {
                        return recu_command[i].children[2].children[0].children[o].innerText.replace(/(\r\n|\n|\r)/gm, "");
                    }
                }
            }


            function getBodyElement() {
                for (let u = 0; u < recu_command[i].children[1].children.length; u++) {
                    if (recu_command[i].children[1].children[u].getAttribute('class') == "commands") {
                        let transform = JSON.parse(recu_command[i].children[1].children[u].value);
                        for (let x in transform) {
                            delete transform[x]['id_prod']
                        }
                        return transform;
                    } else if (recu_command[i].children[1].children[u].getAttribute('class') == "tr_tab") {
                        let element = document.querySelector('.tr_tab');
                        const tab = [];
                        const object = {
                            'nom_prod': element.children[0].textContent,
                            'prix_prod': element.children[1].textContent,
                            'qts': element.children[2].textContent,
                        }
                        tab.push(object);
                        return tab;
                    }
                }
            }

            var img = new Image();
            img.src = getHeaderElement()[3];

            console.log(img);
            var doc = new jsPDF({ putOnlyUsedFonts: true, orientation: "landscape" });
            doc.setFont("helvetica");
            doc.setFontType("bold");
            doc.text("FICHE DE COMMANDE DU SERVICE DE VENTE EN LIGNE HKCservice.ci.com", 40, 10);
            doc.setFont("courier");
            doc.text(getHeaderElement()[0], 10, 30);
            doc.setFont("courier");
            doc.text(getHeaderElement()[1], 10, 40);
            doc.setFont("courier");
            doc.text(getHeaderElement()[2], 10, 50);
            doc.setFont("courier");
            doc.text(getFooterElement(), 10, 60);
            doc.addImage(img, 'png', 225, 25, 70, 40);
            doc.table(10, 70, getBodyElement(), createHeaders(['nom_prod', 'prix_prod', 'qts']), {
                left: 10,
                top: 10,
                bottom: 10,
                width: 170,
                autoSize: true,
                printHeaders: true,
                columnWidths: 80,
            });
            var recu = "fiche_n°" + i + ".pdf";
            doc.save(recu);
        })
    }
})