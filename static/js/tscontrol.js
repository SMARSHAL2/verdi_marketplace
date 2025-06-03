function initTomSelect() {
  document.querySelectorAll('select.tomselect').forEach(function (selectElement) {
    // 🔹 Placeholder único definido no JS
    const placeholder = 'Selecione uma ou mais categorias';

    const ts = new TomSelect(selectElement, {
      plugins: ['remove_button'],
      create: false,
      persist: false,
      render: {
        control: function (data, escape) {
          return `<div class="ts-control verdi-ts-control">${data.input}</div>`;
        }
      },
      onFocus: function () {
        this.wrapper.classList.add('has-focus');
      },
      onBlur: function () {
        this.wrapper.classList.remove('has-focus');
      }
    });

    // 🔹 Injeta o placeholder como atributo para uso do CSS
    requestAnimationFrame(() => {
      const tsControl = ts.wrapper.querySelector('.ts-control');
      if (tsControl) {
        tsControl.setAttribute('data-placeholder', placeholder);
      }
    });
  });
}

document.addEventListener('DOMContentLoaded', initTomSelect);

