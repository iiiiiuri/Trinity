var deletarLinhaButton = document.getElementById('deletar-linha');
deletarLinhaButton.classList.add('hidden');  // Ocultar o botão inicialmente com Tailwind CSS

var selectElements = document.querySelectorAll('select[name="situacao"]');
var data, pis;

selectElements.forEach(function(selectElement) {
    selectElement.addEventListener('change', function(event) {
        if (event.target.value === 'delete') {
            deletarLinhaButton.classList.remove('hidden');  // Mostrar o botão com Tailwind CSS

            data = event.target.getAttribute('data-date').replace(/\//g, '');
            pis = event.target.getAttribute('data-pis');
        } else {
            deletarLinhaButton.classList.add('hidden');  // Ocultar o botão com Tailwind CSS se a opção 'delete' não estiver selecionada
        }
    });
});

deletarLinhaButton.addEventListener('click', function() {
    // Pega o caminho da URL atual
    var path = window.location.pathname;
    // Divide o caminho por '/' para obter os segmentos da URL
    var pathSegments = path.split('/');
    // Remove o último segmento (que é uma string vazia devido ao trailing slash)
    pathSegments.pop();
    // Pega o ID do funcionário
    var funcionarioId = pathSegments.pop();

    // Pega o token CSRF
    var csrftoken = getCookie('csrftoken');

    // Envia uma requisição POST para a rota desejada
    fetch('/deletar_marcacao/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken  // função para obter o cookie CSRF
        },
        body: JSON.stringify({
            'data': data,
            'pis': pis
        })
    })
    .then(response => {
        if (response.ok) {
            location.reload();
        } else {
            console.error('Erro ao remover a marcação: ', response.statusText);
        }
    })
    .catch(error => {
        console.error('Erro ao remover a marcação: ', error);
    });
});

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