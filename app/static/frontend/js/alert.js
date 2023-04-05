const alertBox = document.querySelector('.alertBox');

const toggleAlert = (msg, status, action = 'show') => {
    if (action === "show") {
        // create the alert element
        const alert = document.createElement('div');
        alert.classList.add('alert', 'fade', status);
        alert.innerHTML = `
            <div class="alertTxt">
                ${msg}
            </div>
            <a class="close" data-dismiss="alert">&times;</a>
        `;
        // add the alert element to the alert box
        alertBox.appendChild(alert);

        // animate the alert
        requestAnimationFrame(() => alert.classList.add('visible'));

        // close the alert automatically after 3000ms
        setTimeout(() => {
            toggleAlert(alert.querySelector('.close'), '', 'hide');
        }, 6000);

    } else if (action === 'hide') {
        const alert = msg.closest('.alert');
        if (alert) {
            // animate the alert
            requestAnimationFrame(() => {
                alert.classList.remove('visible');
                alert.addEventListener('transitionend', () => {
                    alertBox.removeChild(alert);
                }, { once: true })
            });
        }
    }
};

alertBox.addEventListener('click', (event) => {
    const closeBtn = event.target.closest('.close');
    if (closeBtn) {
        toggleAlert(closeBtn, '', 'hide');
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert');
    if (alerts) {
        alerts.forEach((alert) => {
            setTimeout(() => {
                toggleAlert(alert.querySelector('.close'), '', 'hide');
            }, 5000);
        });
    }
});