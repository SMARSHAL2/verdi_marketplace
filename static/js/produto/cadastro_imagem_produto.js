// 🌿 Manipula mudança de arquivo
document.addEventListener('change', function (e) {
    const input = document.getElementById('anunciar-upload-input');
    if (e.target === input) {
        const file = input.files[0];
        if (!file) return;

        // Mostra a área de preview
        document.getElementById('upload-display').style.display = 'block';
        document.getElementById('file-name').textContent = file.name;
        document.getElementById('file-size').textContent = `${(file.size / 1024).toFixed(1)} KB`;

        // Simula barra de progresso
        const progressBar = document.getElementById('progress-bar');
        const progressText = document.getElementById('progress-percent');
        let progress = 0;

        const interval = setInterval(() => {
            progress += 10;
            if (progress >= 100) {
                progress = 100;
                clearInterval(interval);
            }
            progressBar.style.width = `${progress}%`;
            progressText.textContent = `${progress}%`;
        }, 50);
    }
});

// 🌿 Remover imagem
function removerUpload() {
    const input = document.getElementById('anunciar-upload-input');
    input.value = "";
    document.getElementById('upload-display').style.display = 'none';
    document.getElementById('progress-bar').style.width = '0%';
    document.getElementById('progress-percent').textContent = '0%';
    document.getElementById('file-name').textContent = '';
    document.getElementById('file-size').textContent = '';
}

// 🌿 Estiliza ao arrastar arquivo sobre o rótulo
document.addEventListener('dragover', function (e) {
    if (e.target.closest('.upload-label-box')) {
        e.preventDefault();
        e.target.closest('.upload-label-box').classList.add('dragover');
    }
});

document.addEventListener('dragleave', function (e) {
    if (e.target.closest('.upload-label-box')) {
        e.target.closest('.upload-label-box').classList.remove('dragover');
    }
});

// 🌿 Permite soltar o arquivo diretamente
document.addEventListener('drop', function (e) {
    const label = e.target.closest('.upload-label-box');
    if (label) {
        e.preventDefault();
        label.classList.remove('dragover');

        const inputId = label.getAttribute('for');
        const input = document.getElementById(inputId);

        if (input && e.dataTransfer.files.length) {
            input.files = e.dataTransfer.files;

            const changeEvent = new Event('change', { bubbles: true });
            input.dispatchEvent(changeEvent);
        }
    }
});
