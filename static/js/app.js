document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.password-toggle').forEach(function (toggleButton) {
        const passwordField = toggleButton.closest('.password-field');
        const passwordInput = passwordField ? passwordField.querySelector('input') : null;

        if (passwordInput) {
            toggleButton.addEventListener('click', function () {
                const isPassword = passwordInput.type === 'password';
                passwordInput.type = isPassword ? 'text' : 'password';
                const icon = toggleButton.querySelector('i');
                if (icon) {
                    icon.classList.toggle('bi-eye', isPassword);
                    icon.classList.toggle('bi-eye-slash', !isPassword);
                }
                toggleButton.setAttribute('aria-label', isPassword ? 'Hide password' : 'Show password');
            });
        }
    });

    const mobileMenu = document.querySelector('.mobile-menu');
    const sidebar = document.querySelector('.sidebar');

    if (mobileMenu && sidebar) {
        mobileMenu.addEventListener('click', function () {
            sidebar.classList.toggle('d-none');
        });
    }

    if (document.getElementById('salesChart') && typeof salesChartData !== 'undefined') {
        const labels = salesChartData.map(item => item.label);
        const values = salesChartData.map(item => item.value);

        new Chart(document.getElementById('salesChart'), {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Sales (₦)',
                    data: values,
                    backgroundColor: 'rgba(139, 94, 60, 0.18)',
                    borderColor: '#8b5e3c',
                    borderWidth: 3,
                    tension: 0.35,
                    fill: true,
                }]
            },
            options: {
                maintainAspectRatio: false,
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    const addRowBtn = document.getElementById('add-item-row');
    const itemTable = document.getElementById('sale-items');

    if (addRowBtn && itemTable) {
        addRowBtn.addEventListener('click', function (event) {
            event.preventDefault();
            const row = document.querySelector('.product-row').cloneNode(true);
            row.querySelectorAll('input, select').forEach(input => {
                input.value = input.tagName === 'INPUT' ? '' : input.options[0].value;
            });
            itemTable.appendChild(row);
        });
    }

    document.addEventListener('click', function (event) {
        if (event.target.closest('.remove-row')) {
            const row = event.target.closest('.product-row');
            if (row && document.querySelectorAll('.product-row').length > 1) {
                row.remove();
            }
        }
    });
});
