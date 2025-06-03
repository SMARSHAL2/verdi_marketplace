document.addEventListener('DOMContentLoaded', function () {
  flatpickr("#data_inicio", {
    dateFormat: "Y-m-d",       
    altInput: true,       
    altFormat: "d/m/Y",
    locale: "pt"
  });

  flatpickr("#data_fim", {
    dateFormat: "Y-m-d",       
    altInput: true,       
    altFormat: "d/m/Y",
    locale: "pt"
  });
});
