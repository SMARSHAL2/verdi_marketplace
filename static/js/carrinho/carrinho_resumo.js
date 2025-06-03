document.addEventListener('DOMContentLoaded', function() {
    const carrinhoBotao = document.getElementById('verdi-menu-botao-carrinho');
    const carrinhoDropdown = document.getElementById('verdi-menu-carrinho-dropdown');

    carrinhoBotao.addEventListener('click', function(e) {
        e.preventDefault();

        fetch('/carrinho/resumo-menu/')
        .then(response => response.json())
        .then(data => {
            carrinhoDropdown.innerHTML = data.html;
            carrinhoDropdown.style.display = 'block';
        });
    });

    // Fecha o carrinho clicando fora
    document.addEventListener('click', function(event) {
        if (!carrinhoDropdown.contains(event.target) && !carrinhoBotao.contains(event.target)) {
            carrinhoDropdown.style.display = 'none';
        }
    });
});
