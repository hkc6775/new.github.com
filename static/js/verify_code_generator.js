window.addEventListener('load', () => {
    const inputG = document.querySelector('.ixtr_val');
    const btn = document.querySelector('#dfrty');

    btn.style.display = "none";

    function genereted() {
        let date = new Date();
        let codeI = Math.random() * date.getSeconds() * date.getSeconds() * 3;
        let newcode = Math.round(codeI).toString();
        var code = newcode < 1000 ? '1960' : newcode.slice(0, 4);
        return code;
    }

    inputG.innerHTML = genereted();

    let transmettreCode = setInterval(() => {
        return inputG.innerHTML = genereted();
    }, 9000);

    document.querySelector('#verify_result').addEventListener('focus', () => {
        clearInterval(transmettreCode);

        document.querySelector('#verify_result').addEventListener('keyup', () => {
            let value = document.querySelector('#verify_result').value;
            let valInputG = inputG.innerHTML;
            let newval = value.replace(' ', '');
            let newvalInpuTG = valInputG.replace(' ', '');
            let valConvertirToInt = parseInt(newval);
            let valInputgConvertirToInt = parseInt(newvalInpuTG);
            const result = valConvertirToInt != valInputgConvertirToInt ? false : true;

            if (result) { btn.style.display = "flex"; } else { btn.style.display = "none"; };
        });
    })
})