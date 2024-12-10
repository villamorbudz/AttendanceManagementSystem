// Initialize all charts when the document is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();

    // Watch for theme changes
    if (window.matchMedia) {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', initializeCharts);
    }
});

function isDarkMode() {
    return document.documentElement.classList.contains('dark') || 
           (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);
}

function getThemeColors() {
    return {
        text: isDarkMode() ? '#ffffff' : '#2b2d42',
        gridLines: isDarkMode() ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.05)',
        primary: isDarkMode() ? '#98c1d9' : '#3d5a80',
        secondary: isDarkMode() ? '#ee6c4d' : '#e76f51',
        background: isDarkMode() ? '#1f2937' : '#ffffff',
        chartAreaBg: isDarkMode() ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.02)'
    };
}

function initializeCharts() {
    initializeActiveUsersChart();
    initializeAttendanceChart();
    fetchChartData();
}

function initializeActiveUsersChart() {
    const ctx = document.getElementById('activeUsersChart');
    if (!ctx) return;

    const data = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
        datasets: [{
            data: [300, 220, 150, 280, 450, 380, 420, 280, 180],
            backgroundColor: 'rgba(255, 255, 255, 0.9)',
            borderRadius: 0,
            barThickness: 8,
            borderSkipped: false,
        }]
    };

    const config = {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: {
                padding: {
                    left: -10,
                    right: -10,
                    top: 0,
                    bottom: -10
                }
            },
            scales: {
                y: {
                    display: true,
                    position: 'left',
                    max: 500,
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)',
                        font: {
                            size: 10,
                            weight: '400'
                        },
                        padding: 0,
                        stepSize: 100,
                        callback: function(value) {
                            return value === 0 ? '' : value;
                        }
                    },
                    border: {
                        display: false
                    }
                },
                x: {
                    display: false
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            }
        }
    };

    if (window.activeUsersChart) {
        window.activeUsersChart.destroy();
    }
    window.activeUsersChart = new Chart(ctx, config);
}

function initializeAttendanceChart() {
    const ctx = document.getElementById('attendanceChart');
    if (!ctx) return;

    // Create gradients
    const ctx2d = ctx.getContext('2d');
    const gradientBlue = ctx2d.createLinearGradient(0, 0, 0, ctx.height);
    gradientBlue.addColorStop(0, 'rgba(152, 193, 217, 0.4)');
    gradientBlue.addColorStop(1, 'rgba(152, 193, 217, 0.0)');

    const gradientPink = ctx2d.createLinearGradient(0, 0, 0, ctx.height);
    gradientPink.addColorStop(0, 'rgba(255, 182, 193, 0.4)');
    gradientPink.addColorStop(1, 'rgba(255, 182, 193, 0.0)');

    const data = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [{
            label: 'Present',
            data: [450, 380, 320, 280, 300, 380, 400, 360, 320, 300, 340, 360],
            borderColor: '#98c1d9',
            backgroundColor: gradientBlue,
            tension: 0.4,
            fill: true,
            borderWidth: 2,
            pointRadius: 0
        },
        {
            label: 'Absent',
            data: [300, 250, 200, 180, 220, 280, 320, 280, 240, 200, 180, 160],
            borderColor: '#e76f51',
            backgroundColor: gradientPink,
            tension: 0.4,
            fill: true,
            borderWidth: 2,
            pointRadius: 0
        }]
    };

    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: {
                padding: {
                    top: 20,
                    right: 20,
                    bottom: 0,
                    left: 0
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 500,
                    position: 'right',
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)',
                        drawBorder: false,
                        borderDash: [5, 5]
                    },
                    ticks: {
                        color: '#98c1d9',
                        font: {
                            size: 10,
                            weight: '400'
                        },
                        padding: 10,
                        stepSize: 100,
                        callback: function(value) {
                            return value === 0 ? '' : value;
                        }
                    },
                    border: {
                        display: false
                    }
                },
                x: {
                    grid: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        color: '#98c1d9',
                        font: {
                            size: 10,
                            weight: '400'
                        },
                        padding: 5
                    },
                    border: {
                        display: false
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    };

    if (window.attendanceChart) {
        window.attendanceChart.destroy();
    }
    window.attendanceChart = new Chart(ctx, config);
}

async function fetchChartData() {
    try {
        const response = await fetch('/dashboard/api/chart-data/', {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'same-origin'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Chart data received:', data); // Debug log
        
        if (data.weekly_leave_data) {
            initializeWeeklyLeaveChart(data.weekly_leave_data);
        } else {
            console.error('Weekly leave data not found in response');
        }
        
        if (data.employee_status_data) {
            initializeEmployeeStatusChart(data.employee_status_data);
        } else {
            console.error('Employee status data not found in response');
        }
        
        if (data.daily_stats_data) {
            initializeDailyStatsChart(data.daily_stats_data);
        } else {
            console.error('Daily stats data not found in response');
        }
    } catch (error) {
        console.error('Error fetching chart data:', error);
        // Display a user-friendly error message
        const charts = document.querySelectorAll('canvas');
        charts.forEach(chart => {
            const ctx = chart.getContext('2d');
            ctx.font = '14px Arial';
            ctx.fillStyle = '#666';
            ctx.textAlign = 'center';
            ctx.fillText('Unable to load chart data', chart.width / 2, chart.height / 2);
        });
    }
}

function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}

function initializeWeeklyLeaveChart(chartData) {
    const ctx = document.getElementById('weeklyLeaveChart');
    if (!ctx) return;

    const colors = getThemeColors();
    const data = {
        labels: chartData.labels,
        datasets: [{
            data: chartData.data,
            backgroundColor: colors.primary,
            barThickness: 4,
            borderRadius: 15,
        }]
    };

    new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            family: 'Poppins',
                            size: 7
                        },
                        color: colors.text
                    }
                },
                y: {
                    grid: {
                        color: colors.gridLines,
                        drawBorder: false
                    },
                    ticks: {
                        font: {
                            family: 'Poppins',
                            size: 6
                        },
                        color: colors.text,
                        stepSize: 2,
                        max: 12
                    }
                }
            }
        }
    });
}

function initializeEmployeeStatusChart(chartData) {
    const ctx = document.getElementById('employeeStatusChart');
    if (!ctx) return;

    const colors = getThemeColors();
    const data = {
        labels: chartData.labels,
        datasets: [{
            data: chartData.data,
            backgroundColor: [colors.primary, colors.secondary],
            borderWidth: 0,
        }]
    };

    new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: {
                    display: false
                }
            },
            elements: {
                arc: {
                    borderWidth: 0
                }
            }
        }
    });
}

function initializeDailyStatsChart(chartData) {
    const ctx = document.getElementById('dailyStatsChart');
    if (!ctx) return;

    const colors = getThemeColors();
    const data = {
        labels: chartData.labels,
        datasets: chartData.datasets.map((dataset, index) => ({
            label: dataset.label,
            data: dataset.data,
            backgroundColor: index === 0 ? colors.primary : colors.secondary,
            barThickness: 28.92,
            borderRadius: {
                topLeft: 10,
                topRight: 10
            }
        }))
    };

    new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    stacked: true,
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            family: 'Poppins',
                            size: 8
                        },
                        color: colors.text
                    }
                },
                y: {
                    stacked: true,
                    grid: {
                        color: colors.gridLines,
                        drawBorder: false
                    },
                    ticks: {
                        font: {
                            family: 'Poppins',
                            size: 7
                        },
                        color: colors.text,
                        stepSize: 2,
                        max: 12
                    }
                }
            }
        }
    });
}

// Update theme function for all charts
function updateChartsTheme(isDark) {
    Chart.instances.forEach(chart => {
        const options = chart.options;
        
        // Update grid colors
        if (options.scales) {
            if (options.scales.y) {
                options.scales.y.grid.color = isDark ? '#374151' : '#f6f6f6';
            }
            if (options.scales.x) {
                options.scales.x.grid.color = isDark ? '#374151' : '#f6f6f6';
            }
        }
        
        chart.update();
    });
}

// Listen for theme changes if you have a theme toggle
document.addEventListener('themeChanged', function(e) {
    updateChartsTheme(e.detail.isDark);
});
