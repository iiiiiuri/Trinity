function deleteDatabase() {
    if (confirm("Tem certeza que deseja continuar com essa operação?")) {
        const csrfToken = getCookies("csrftoken"); // Assuming getCookies is a valid function in Django
        fetch("/reset_database/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({}),
        })
            .then((response) => {
                location.href = '/fileupload/';
            })
            .catch((error) => {
                // Handle any errors here
            });
    } else {
        // Abort the post
    }
}

function getCookies(name) {
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