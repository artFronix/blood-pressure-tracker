document.addEventListener('DOMContentLoaded', function() {
    // Загрузка данных через API
    fetch('/get_records')
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(records => {
            if (records.length > 0) {
                drawCharts(records);
                setupResizeHandler();
            } else {
                console.log("Нет данных для отображения графиков");
            }
        })
        .catch(error => {
            console.error('Ошибка загрузки данных:', error);
            document.getElementById('pressureChart-container').innerHTML = 
                '<p class="chart-error">Не удалось загрузить данные</p>';
        });

    function drawCharts(records) {
        // Форматирование дат
        const labels = records.map(r => {
            const date = new Date(r.date);
            return date.toLocaleDateString('ru-RU', {
                day: 'numeric',
                month: 'short',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        });

        // Общие настройки для всех графиков
        const commonOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        font: {
                            size: 14
                        }
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0,0,0,0.7)',
                    bodyFont: {
                        size: 14
                    }
                }
            },
            elements: {
                line: {
                    tension: 0.3
                },
                point: {
                    radius: 4,
                    hoverRadius: 6
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45
                    }
                }
            }
        };

        // График давления
        const pressureCtx = document.getElementById('pressureChart');
        window.pressureChart = new Chart(pressureCtx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Верхнее давление',
                        data: records.map(r => r.systolic),
                        borderColor: '#ff6384',
                        backgroundColor: 'rgba(255, 99, 132, 0.1)',
                        borderWidth: 2,
                        fill: true
                    },
                    {
                        label: 'Нижнее давление',
                        data: records.map(r => r.diastolic),
                        borderColor: '#36a2eb',
                        backgroundColor: 'rgba(54, 162, 235, 0.1)',
                        borderWidth: 2,
                        fill: true
                    }
                ]
            },
            options: {
                ...commonOptions,
                scales: {
                    ...commonOptions.scales,
                    y: {
                        title: {
                            display: true,
                            text: 'мм рт. ст.'
                        }
                    }
                }
            }
        });

        // График пульса
        const pulseCtx = document.getElementById('pulseChart');
        window.pulseChart = new Chart(pulseCtx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Пульс',
                    data: records.map(r => r.pulse),
                    borderColor: '#4bc0c0',
                    backgroundColor: 'rgba(75, 192, 192, 0.1)',
                    borderWidth: 2,
                    fill: true
                }]
            },
            options: {
                ...commonOptions,
                scales: {
                    ...commonOptions.scales,
                    y: {
                        title: {
                            display: true,
                            text: 'уд/мин'
                        }
                    }
                }
            }
        });
    }

    function setupResizeHandler() {
        let resizeTimer;
        window.addEventListener('resize', function() {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(function() {
                if (window.pressureChart) window.pressureChart.resize();
                if (window.pulseChart) window.pulseChart.resize();
            }, 200);
        });
    }
});