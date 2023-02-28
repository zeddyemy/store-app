function closeAlert(alert) {
    alert.style.opacity = '0';
    alert.style.margin = '0%';
    alert.querySelector('.alert-txt').style.padding = '0%';
    alert.querySelector('.alert-txt').style.fontSize = '0%';
    alert.querySelector('.close').style.fontSize = '0%';
    setTimeout(() => alert.remove(), 1000);
}

document.querySelectorAll('.alert .close').forEach(closeBtn => {
    closeBtn.addEventListener('click', (e) => {
        const alert = e.target.closest('.alert');
        closeAlert(alert);
    });
});
