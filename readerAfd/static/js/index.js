function loadBox(boxId) {
    // Lista de todas as boxes
    var allBoxes = ['boxEmpresa', 'boxFuncionario', 'boxCalendario'];

    // Oculta todas as boxes
    for (var i = 0; i < allBoxes.length; i++) {
        document.getElementById(allBoxes[i]).classList.add('hidden');
    }

    // Mostra a box desejada
    document.getElementById(boxId).classList.remove('hidden');
}