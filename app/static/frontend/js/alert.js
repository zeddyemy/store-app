function closeAlert(alert, alertBox) {
    alert.style.opacity = '0';
    alert.style.margin = '0%';
    alert.querySelector('.alert-txt').style.padding = '0%';
    alert.querySelector('.alert-txt').style.fontSize = '0%';
    alert.querySelector('.close').style.fontSize = '0%';
    setTimeout(() => alertBox.remove(), 1000);
}

document.querySelectorAll('.close').forEach(closeBtn => {
    closeBtn.addEventListener('click', (e) => {
        const alert = e.target.closest('.alert');
        const alertBox = alert.closest('.alert-box');
        closeAlert(alert, alertBox);
    });
});
