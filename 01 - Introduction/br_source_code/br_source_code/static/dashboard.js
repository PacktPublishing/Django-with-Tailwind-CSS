console.log('hello world dashboard')

const dashboardBox = document.getElementById('dashboard-box')

$.ajax({
    type: 'GET',
    url: '/chart-data',
    success: (resp) => {
        const { data } = resp

        for (let i=0; i < data.length; i++) {
            const ctx = document.getElementById(`chart-box${i+1}`)
            const descriptionBox = document.getElementById(`desc-box${i+1}`)
            const { labels, data:d, description, type } = data[i]
            console.log(labels, d, description)
            descriptionBox.innerHTML = description
            
            new Chart(ctx, {
                type: type,
                data: {
                    labels: labels,
                    datasets:[{
                        data: d, 
                        borderWidth: 1,
                    }]
                },
                options : {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    },
                    plugins : {
                        legend: {
                            display: type === 'pie' && true,
                        }
                    }
                },
            })
        }
    },
    error: (err) => console.log(err)
})