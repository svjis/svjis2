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
                borderWidth: 2,
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


function sortDataInPlace(data) {
    const pairs = data.labels.map((label, index) => ({
        label: label,
        value: data.values[index]
    }));

    pairs.sort((a, b) => b.value - a.value);

    data.labels.length = 0;
    data.values.length = 0;

    pairs.forEach(pair => {
        data.labels.push(pair.label);
        data.values.push(pair.value);
    });

    return data;
}
