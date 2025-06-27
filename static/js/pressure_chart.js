document.addEventListener('DOMContentLoaded', function() {
    fetch('/get_records')
      .then(response => response.json())
      .then(records => {
        if (records.length === 0) return;
        
        // Форматирование дат
        const labels = records.map(r => new Date(r.date).toLocaleDateString('ru-RU', {
          day: 'numeric',
          month: 'short',
          hour: '2-digit',
          minute: '2-digit'
        }));
  
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
                  data: records.map(r => r.systolic),
                  borderColor: '#2a9dff',
                  backgroundColor: 'rgba(42, 157, 255, 0.1)',
                  tension: 0.3,
                  fill: true
                },
                {
                  label: 'Нижнее',
                  data: records.map(r => r.diastolic),
                  borderColor: '#4cc9f0',
                  backgroundColor: 'rgba(76, 201, 240, 0.1)',
                  tension: 0.3,
                  fill: true
                }
              ]
            },
            options: getChartOptions('мм рт. ст.')
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
                data: records.map(r => r.pulse),
                borderColor: '#f72585',
                backgroundColor: 'rgba(247, 37, 133, 0.1)',
                tension: 0.3,
                fill: true
              }]
            },
            options: getChartOptions('уд/мин')
          }
        );
      });
  
    function getChartOptions(unit) {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top' },
          tooltip: { mode: 'index' }
        },
        scales: {
          y: { title: { display: true, text: unit } },
          x: { grid: { display: false } }
        }
      };
    }
  });