function createChartConfig(type, data, options = {}) {
    const total = data.values.reduce((sum, val) => sum + val, 0);

    // Generate labels with percentages
    const labelsWithPercentages = data.labels.map((label, index) => {
        const percentage = ((data.values[index] / total) * 100).toFixed(1);
        return `${label} (${percentage}%)`;
    });

    return {
        type: type,
        data: {
            labels: labelsWithPercentages,
            datasets: [{
                data: data.values,
                backgroundColor: data.colors || generateColors(data.values.length),
                borderColor: '#ffffff',
                borderWidth: 2,
                ...options.dataset
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: options.legendPosition || 'bottom'
                },
                title: {
                    display: !!options.title,
                    text: options.title
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const percentage = ((context.parsed / total) * 100).toFixed(1);
                            return `${context.label}: ${context.parsed} (${percentage}%)`;
                        }
                    }
                }
            },
        }
    };
}


function generateColors(count) {
    const colors = [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
        '#DDA0DD', '#98D8C8', '#FFB347', '#F0E68C', '#87CEEB'
    ];
    return colors.slice(0, count);
}
