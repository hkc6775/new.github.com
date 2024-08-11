window.addEventListener('load', () => {
    let recu_command = document.querySelectorAll('.recu_command')
    let commands = document.querySelectorAll('.commands')
    let zone_info_cmmd = document.querySelectorAll('.zone_info_cmmd')

    if (recu_command && commands && zone_info_cmmd) {
        for (let i = 0; i < recu_command.length; i++) {
            if (recu_command[i].childNodes[3].childNodes[3].value != undefined) {
                let tab = JSON.parse(recu_command[i].childNodes[3].childNodes[3].value);
                for (let u = 0; u < tab.length; u++) {
                    let td = `
                    <tr>
                    <td class="tdInfo">${tab[u]['nom_prod']}</td>
                    <td class="tdInfo">${tab[u]['prix_prod']}</td>
                    <td class="tdInfo">${tab[u]['qts']}</td>
                    </tr>
                    `;

                    zone_info_cmmd[i].innerHTML += td;
                }
            }
        }
    }
})