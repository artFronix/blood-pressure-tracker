document.addEventListener('DOMContentLoaded', function() {
        // Данные из Flask
        const records = JSON.parse('{{ records|tojson|safe }}');
        
        // Подготовка данных
        const labels = records.map(r => new Date(r.date).toLocaleDateString());
        const systolicData = records.map(r => r.systolic);
        const diastolicData = records.map(r => r.diastolic);
        const pulseData = records.map(r => r.pulse);

        // График давления
        new Chart(
            document.getElementById('pressureChart'),
            {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Верхнее',
                            data: systolicData,
                            borderColor: '#ff6384',
                            tension: 0.1
                        },
                        {
                            label: 'Нижнее',
                            data: diastolicData,
                            borderColor: '#36a2eb',
                            tension: 0.1
                        }
                    ]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            suggestedMin: Math.min(...diastolicData) - 10,
                            suggestedMax: Math.max(...systolicData) + 10
                        }
                    }
                }
            }
        );

        // График пульса
        new Chart(
            document.getElementById('pulseChart'),
            {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Пульс',
                        data: pulseData,
                        borderColor: '#4bc0c0',
                        tension: 0.1
                    }]
                },
                options: { responsive: true }
            }
        );
    });