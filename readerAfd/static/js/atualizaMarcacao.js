function atualizarHora(elemento, hora, pis, linha) {
    var novaHora = elemento.textContent.trim();

    // Se novaHora é igual a hora, não fazer nada e retornar
    if (novaHora === hora) {
        return;
    }

    // Obter todas as células na mesma linha, exceto a célula atual
    var celulasNaMesmaLinha = Array.from(linha.cells).filter((td, index) => td !== elemento && [2, 3, 4, 5].includes(index));

    // Verificar se novaHora já existe na mesma linha
    if (celulasNaMesmaLinha.some(td => td.textContent.trim() === novaHora) && novaHora !== '-') {
        alert('Esta hora já existe para esta linha.');
        elemento.textContent = hora;  // Restaurar a hora original
        return;
    }

    // Obter a data da célula correspondente na tabela
    var data = linha.cells[0].innerText;
    // Remover as barras da data
    data = data.replace(/\//g, '');

    var url = '/atualizar_horario/';
    var method = 'POST';
        if (novaHora == '' && hora == '-') {
            alert('Não é possível deletar uma marcação Inexistente.');
        } else if (hora == '-') {
            url = '/criar_nova_marcacao/';
            method = 'POST';
        } else if (novaHora == '') {
            url = '/delete_marcacao_unica/';
            method = 'POST';
        } else {
            url = '/atualizar_horario/';
            method = 'POST';
        }

    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // função para obter o cookie CSRF
        },
        body: JSON.stringify({
            'data': data,
            'hora': hora,
            'pis': pis,
            'novaHora': novaHora
        })
    })
    .then(response => {
        if (response.ok) {
            window.location.reload(true);
        } else {
            console.error('Erro ao atualizar a hora: ', response.statusText);
        }
    })
    .catch(error => {
        console.error('Erro ao atualizar a hora: ', error);
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Verifica se a string do cookie começa com o nome que queremos
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}