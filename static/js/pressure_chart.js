document.addEventListener('DOMContentLoaded', function() {
    const records = JSON.parse('{{ records_json|tojson|safe }}');
    
    // Форматирование дат
    const labels = records.map(r => {
        const date = new Date(r.date);
        return date.toLocaleDateString('ru-RU', {
            day: 'numeric',
            month: 'short',
            year: 'numeric'
        });
    });

    // График давления
    const pressureCtx = document.getElementById('pressureChart').getContext('2d');
    new Chart(pressureCtx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Верхнее',
                    data: records.map(r => r.systolic),
                    borderColor: '#ff6384',
                    backgroundColor: 'rgba(255, 99, 132, 0.1)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: true
                },
                {
                    label: 'Нижнее',
                    data: records.map(r => r.diastolic),
                    borderColor: '#36a2eb',
                    backgroundColor: 'rgba(54, 162, 235, 0.1)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: true
                }
            ]
        },
        options: getChartOptions('мм рт. ст.')
    });

    // График пульса
    const pulseCtx = document.getElementById('pulseChart').getContext('2d');
    new Chart(pulseCtx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Пульс',
                data: records.map(r => r.pulse),
                borderColor: '#4bc0c0',
                backgroundColor: 'rgba(75, 192, 192, 0.1)',
                borderWidth: 2,
                tension: 0.3,
                fill: true
            }]
        },
        options: getChartOptions('уд/мин')
    });

    function getChartOptions(unit) {
        return {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    mode: 'index',
                    intersect: false
                },
                legend: {
                    position: 'top',
                }
            },
            scales: {
                y: {
                    title: {
                        display: true,
                        text: unit
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        };
    }
});