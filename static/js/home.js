const menuBtn = document.getElementById("menu-btn");
const closeBtn = document.getElementById("close-btn");
const sidebar = document.getElementById("sidebar");
const mainContent = document.getElementById("main-content");
const modal = document.getElementById("modal-user");
const closeModalBtn = document.getElementById("close-modal");
const openModalLinks = document.querySelectorAll(".open-modal");
const perfilUser = document.getElementById("perfil-user");

function toggleSidebar() {
    sidebar.classList.toggle("translate-x-full");
}

function closeSidebar() {
    if (!sidebar.classList.contains("translate-x-full")) {
        sidebar.classList.add("translate-x-full");

    }
}

function openModal() {
    modal.classList.remove("hidden");
}

function closeModal() {
    modal.classList.add("hidden");
    location.reload();
}

menuBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    toggleSidebar();
});

closeBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    toggleSidebar();
});

document.addEventListener("click", (e) => {
    if (
        !sidebar.contains(e.target) &&
        !menuBtn.contains(e.target) &&
        !closeBtn.contains(e.target)
    ) {
        closeSidebar();
    }
});

openModalLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
        e.preventDefault();
        closeSidebar();
        openModal();
    });
});

perfilUser.addEventListener("click", (e) => {
    e.preventDefault();
    closeSidebar();
    openModal();
});


closeModalBtn.addEventListener("click", closeModal);

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