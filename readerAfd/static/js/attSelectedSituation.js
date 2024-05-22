var alteracoes = {};

// Seleciona todos os selects
var selects = document.querySelectorAll('.default-select');

// Seleciona o botão "Salvar Alterações"
var botao = document.querySelector('#salvar-alteracoes');

selects.forEach(function(selectElement) {
    selectElement.addEventListener('change', function(event) {
        var date = selectElement.getAttribute('data-date');
        var situacao = event.target.value;

        // Se a data não existir no objeto alteracoes, cria um novo objeto para ela
        if (!alteracoes[date]) {
            alteracoes[date] = {};
        }

        // Reseta todas as situações para false
        alteracoes[date]['normal'] = false;
        alteracoes[date]['ferias'] = false;
        alteracoes[date]['atestado'] = false;
        alteracoes[date]['folga'] = false;
        alteracoes[date]['pagar'] = false;

        // Define a situação selecionada para true
        alteracoes[date][situacao] = true;

        if (situacao == 'delete') {
            botao.classList.add('hidden');  // Ocultar o botão com Tailwind CSS
        } else {
            botao.classList.remove('hidden');  // Mostrar o botão com Tailwind CSS se a opção 'delete' não estiver selecionada
        }
    });
});

botao.classList.add('hidden');
botao.addEventListener('click', function() {
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
    $.ajax({
        url: '/' + funcionarioId + '/alterar_registro/',
        type: 'POST',
        data: JSON.stringify(alteracoes),
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
        success: function(response) {
            window.location.reload(true);

        }
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