function calcularHorasTotais() {
    let tabela = document.getElementById('espelho');

    let totalHoras = 0;

    for (let i = 1; i < tabela.rows.length; i++) {
        let linha = tabela.rows[i];
        let horasTrabalhadas = linha.cells[6].innerText.trim();

        // Verifica se as horas trabalhadas estão no formato hh:mm
        if (!/^([01]?[0-9]|2[0-3]):[0-5][0-9]$/.test(horasTrabalhadas)) {
            horasTrabalhadas = '00:00';
        }

        let [horas, minutos] = horasTrabalhadas.split(':');
        totalHoras += parseInt(horas) + parseInt(minutos) / 60;
    }

    let horas = Math.floor(totalHoras);
    let minutos = Math.round((totalHoras - horas) * 60);

    return `${horas.toString().padStart(2, '0')}:${minutos.toString().padStart(2, '0')}`;
}



function calculaHorasExtras(){
    let tabela = document.getElementById('espelho');

    let totalHoras = 0;

    for (let i = 1; i < tabela.rows.length; i++) {
        let linha = tabela.rows[i];
        let horasTrabalhadas = linha.cells[10].innerText.trim();

        if (!/^([01]?[0-9]|2[0-3]):[0-5][0-9]$/.test(horasTrabalhadas)) {
            horasTrabalhadas = '00:00';
        }

        let [horas, minutos] = horasTrabalhadas.split(':');
        totalHoras += parseInt(horas) + parseInt(minutos) / 60;
    }

    let horas = Math.floor(totalHoras);
    let minutos = Math.round((totalHoras - horas) * 60);

    return `${horas.toString().padStart(2, '0')}:${minutos.toString().padStart(2, '0')}`;
    
}

function calcularHorasFaltantes(){
    let tabela = document.getElementById('espelho');

    let totalHoras = 0;

    for (let i = 1; i < tabela.rows.length; i++) {
        let linha = tabela.rows[i];
        let horasTrabalhadas = linha.cells[9].innerText.trim();

        if (!/^([01]?[0-9]|2[0-3]):[0-5][0-9]$/.test(horasTrabalhadas)) {
            horasTrabalhadas = '00:00';
        }

        let [horas, minutos] = horasTrabalhadas.split(':');
        totalHoras += parseInt(horas) + parseInt(minutos) / 60;
    }

    let horas = Math.floor(totalHoras);
    let minutos = Math.round((totalHoras - horas) * 60);

    return `${horas.toString().padStart(2, '0')}:${minutos.toString().padStart(2, '0')}`;
}


function calculoPagar(){
    let tabela = document.getElementById('espelho');

    let totalHoras = 0;

    for (let i = 1; i < tabela.rows.length; i++) {
        let linha = tabela.rows[i];
        let horasTrabalhadas = linha.cells[11].innerText.trim();

        if (!/^([01]?[0-9]|2[0-3]):[0-5][0-9]$/.test(horasTrabalhadas)) {
            horasTrabalhadas = '00:00';
        }

        let [horas, minutos] = horasTrabalhadas.split(':');
        totalHoras += parseInt(horas) + parseInt(minutos) / 60;
    }

    let horas = Math.floor(totalHoras);
    let minutos = Math.round((totalHoras - horas) * 60);

    return `${horas.toString().padStart(2, '0')}:${minutos.toString().padStart(2, '0')}`;
}

window.onload = function() {
    document.getElementById('HorasExtras').value = calculaHorasExtras();
    document.getElementById('HorasTrabalhadas').value = calcularHorasTotais();
    document.getElementById('HorasFaltantes').value = calcularHorasFaltantes();
    document.getElementById('aPagar').value = calculoPagar();

}