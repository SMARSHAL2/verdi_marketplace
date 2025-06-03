document.addEventListener('DOMContentLoaded', function () {
  const buscaWrappers = document.querySelectorAll('.verdi-menu-form-busca-wrapper');

  buscaWrappers.forEach(wrapper => {
    const input = wrapper.querySelector('input');
    const icon = wrapper.querySelector('.verdi-menu-busca-icon');

    // 🔍 Clique no ícone ativa a busca
    icon.addEventListener('click', function () {
      if (input.value.trim() !== '') {
        enviarBusca(input.value);
      }
    });

    // ⌨️ Enter ativa a busca
    input.addEventListener('keypress', function (e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        if (input.value.trim() !== '') {
          enviarBusca(input.value);
        }
      }
    });
  });

  function enviarBusca(valor) {
    const form = document.createElement('form');
    form.method = 'GET';
    form.action = '/buscar/';

    const campo = document.createElement('input');
    campo.type = 'hidden';
    campo.name = 'q';
    campo.value = valor;

    form.appendChild(campo);
    document.body.appendChild(form);
    form.submit();
  }
});
