document.addEventListener('DOMContentLoaded', function () {
    // Permite abrir modais dinamicamente (ex: editar endereço)
    const hash = window.location.hash;
    if (hash && document.querySelector(hash)) {
        const modalElement = document.querySelector(hash);
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
    }

    // Fecha modais e limpa hash da URL
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('hidden.bs.modal', () => {
            if (window.location.hash === '#' + modal.id) {
                history.replaceState(null, null, ' ');
            }
        });
    });
});