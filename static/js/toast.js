function showToast(title, message, type = 'success') {
    const toastEl = document.getElementById('toast-component');
    const titleEl = document.getElementById('toast-title');
    const messageEl = document.getElementById('toast-message');

    if (!toastEl || !titleEl || !messageEl) return;

    // Ganti teks di dalam HTML toast lu secara dinamis
    titleEl.textContent = title;
    messageEl.textContent = message;

    // Set class type
    toastEl.classList.remove('toast-success', 'toast-error', 'toast-hidden');
    toastEl.classList.add(`toast-${type}`);

    // Buka popover HTML-nya
    if (typeof toastEl.showPopover === 'function') {
        toastEl.showPopover();
    } else {
        toastEl.classList.remove('toast-hidden');
    }

    // Auto tutup setelah 3 detik
    setTimeout(() => {
        if (typeof toastEl.hidePopover === 'function') {
            toastEl.hidePopover();
        } else {
            toastEl.classList.add('toast-hidden');
        }
    }, 3000);
}