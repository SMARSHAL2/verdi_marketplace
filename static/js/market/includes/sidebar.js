        const abrirSidebar = document.getElementById('abrirSidebar');
        const fecharSidebar = document.getElementById('fecharSidebar');
        const sidebar = document.getElementById('verdiSidebar');

        if (abrirSidebar && fecharSidebar && sidebar) {
            abrirSidebar.addEventListener('click', () => {
                sidebar.classList.add('ativo');
            });

            fecharSidebar.addEventListener('click', () => {
                sidebar.classList.remove('ativo');
            });

            document.addEventListener('click', (e) => {
                if (!sidebar.contains(e.target) && !abrirSidebar.contains(e.target)) {
                    sidebar.classList.remove('ativo');
                }
            });
        }