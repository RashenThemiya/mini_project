document.addEventListener('DOMContentLoaded', function() {
  var ctx = document.getElementById('agricultureChart').getContext('2d');
  if (ctx) {
      new Chart(ctx, {
          type: 'pie',
          data: {
              labels: ['Rice', 'Tea', 'Coconut', 'Rubber'],
              datasets: [{
                  label: 'Agricultural Production in Sri Lanka',
                  data: [40, 30, 20, 10],
                  backgroundColor: ['#4bc0c0', '#ffce56', '#36a2eb', '#ff6384'],
                  borderColor: ['#4bc0c0', '#ffce56', '#36a2eb', '#ff6384'],
                  borderWidth: 1
              }]
          },
          options: {
              responsive: true,
              plugins: {
                  legend: {
                      position: 'top',
                  },
                  title: {
                      display: true,
                      text: 'Agricultural Production in Sri Lanka'
                  }
              }
          }
      });
  } else {
      console.log('Chart element not found');
  }
});
