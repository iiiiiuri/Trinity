var changeData = null;

function storeChange(event, dia, campo, valorAntigo) {
    var novoValor = event.target.value.trim();
    changeData = {
        dia: dia,
        campo: campo.toLowerCase(),
        antigo: valorAntigo,
        novoValor: novoValor
    };
    document.getElementById('saveButton').classList.remove('hidden');
}

function sendChange() {
    if (changeData) {
        var csrftoken = getCookie('csrftoken');
        fetch('/atualizar_configuracao/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(changeData),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            document.getElementById('saveButton').classList.add('hidden');
            changeData = null;
            window.location.reload(true);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
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