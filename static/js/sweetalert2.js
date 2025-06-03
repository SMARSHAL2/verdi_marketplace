function getCSRFToken() {
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [name, value] = cookie.trim().split('=');
    if (name === 'csrftoken') return decodeURIComponent(value);
  }
  return '';
}

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.checkbox-ativar-promocao').forEach(function (checkbox) {
    checkbox.addEventListener('change', function () {
      const promocaoId = this.getAttribute('data-promocao-id');
      const isChecked = this.checked;

      Swal.fire({
        title: isChecked ? 'Ativar promoção?' : 'Desativar promoção?',
        text: isChecked
          ? 'Tem certeza que deseja reativar esta promoção?'
          : 'Tem certeza que deseja desativar esta promoção agora?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: isChecked ? 'Sim, ativar' : 'Sim, desativar',
        cancelButtonText: 'Cancelar'
      }).then((result) => {
        if (result.isConfirmed) {
          fetch(`/suporte/desativar-promocao/${promocaoId}/`, {
            method: 'POST',
            headers: {
              'X-CSRFToken': getCSRFToken(),
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ ativo: isChecked })
          })
          .then(res => {
            if (!res.ok) throw new Error('Erro na requisição');
            return res.json();
          })
          .then(data => {
            if (data.status !== 'ok') throw new Error(data.mensagem || 'Erro inesperado');

            // Mostra mini loading antes do reload
            Swal.fire({
              title: 'Atualizando...',
              text: 'Aplicando alterações',
              allowOutsideClick: false,
              allowEscapeKey: false,
              showConfirmButton: false,
              didOpen: () => {
                Swal.showLoading();
              }
            });

            setTimeout(() => {
              location.reload();
            }, 800); // tempo para visualizar o loading

          })
          .catch(err => {
            Swal.fire('Erro', err.message, 'error');
            this.checked = !isChecked; // Reverte o estado
          });
        } else {
          this.checked = !isChecked;
        }
      });
    });
  });
});
