document.addEventListener('DOMContentLoaded', () => {
    const menuBtn = document.getElementById('menu-btn');
    const closeBtn = document.getElementById('close-btn');
    const sidebar = document.getElementById('sidebar');
    const modal = document.getElementById('modal');
    const modalContents = document.querySelectorAll('.modal-content');
    const closeModalBtn = document.getElementById('close-modal');
    const openModalLinks = document.querySelectorAll('.open-modal');

    function toggleSidebar() {
        sidebar.classList.toggle('translate-x-full');
        menuBtn.classList.toggle('hidden');
        closeBtn.classList.toggle('hidden');
    }

    function closeSidebar() {
        if (!sidebar.classList.contains('translate-x-full')) {
            sidebar.classList.add('translate-x-full');
            menuBtn.classList.remove('hidden');
            closeBtn.classList.add('hidden');
        }
    }

    function openModal(targetId) {
        modalContents.forEach(content => {
            content.classList.add('hidden');
        });
        const targetContent = document.getElementById(targetId);
        targetContent.classList.remove('hidden');
        modal.classList.remove('hidden');
    }

    function closeModal() {
        modal.classList.add('hidden');
    }

    menuBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleSidebar();
    });

    closeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleSidebar();
    });

    document.addEventListener('click', (e) => {
        if (!sidebar.contains(e.target) && !menuBtn.contains(e.target) && !closeBtn.contains(e.target)) {
            closeSidebar();
        }
    });

    openModalLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('data-target');
            closeSidebar();
            openModal(targetId);
        });
    });

    closeModalBtn.addEventListener('click', closeModal);

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });



});



// openModalLinks.forEach((link) => {
//     link.addEventListener("click", (e) => {
//         e.preventDefault();
//         closeSidebar();
//         openModal();
//     });
// });

//fecha modal se clicar fora
// modal.addEventListener("click", (e) => {
//     if (e.target === modal) {
//         closeModal();
//     }
// });

document.addEventListener('DOMContentLoaded', function () {
    const successMessage = document.getElementById('message_sucess');
    if (successMessage) {
        // Exibir o modal se houver uma mensagem de sucesso
        openModal();
    }
});