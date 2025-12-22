function initDashboardCharts() {
    if (typeof ApexCharts === 'undefined' || !document.querySelector("#revenueChart")) {
        console.warn("ApexCharts chưa sẵn sàng hoặc không tìm thấy thẻ DIV");
        return;
    }

    const revenueData = {
        week: {
            data: [15, 22, 18, 30, 25, 40, 35],
            categories: ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'CN']
        },
        month: {
            data: [120, 150, 180, 220],
            categories: ['Tuần 1', 'Tuần 2', 'Tuần 3', 'Tuần 4']
        },
        year: {
            data: [0, 0, 0, 1, 0, 2, 0, 3, 0, 0, 0, 0],
            categories: ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12']
        }
    };

    var revenueOptions = {
        series: [{
            name: 'Doanh thu (triệu VNĐ)',
            data: revenueData.week.data
        }],
        chart: {
            height: 350,
            type: 'area',
            toolbar: {show: false},
            animations: {enabled: true}
        },
        colors: ['#3C50E0'],
        dataLabels: {enabled: false},
        stroke: {curve: 'smooth', width: 2},
        xaxis: {
            categories: revenueData.week.categories,
            axisBorder: {show: false},
            axisTicks: {show: false},
        },
        grid: {
            strokeDashArray: 4,
            yaxis: {lines: {show: true}}
        },
        fill: {
            type: 'gradient',
            gradient: {shadeIntensity: 1, opacityFrom: 0.5, opacityTo: 0.05, stops: [0, 90, 100]}
        },
        tooltip: {
            y: {
                formatter: function (val) {
                    return val + " triệu"
                }
            }
        }
    };


    if (window.revenueChartInstance) {
        window.revenueChartInstance.destroy();
    }
    window.revenueChartInstance = new ApexCharts(document.querySelector("#revenueChart"), revenueOptions);
    window.revenueChartInstance.render();

    window.updateRevenue = function (type) {
        window.revenueChartInstance.updateOptions({
            xaxis: {categories: revenueData[type].categories}
        });
        window.revenueChartInstance.updateSeries([{
            data: revenueData[type].data
        }]);

        const buttons = ['btn-week', 'btn-month', 'btn-year'];
        buttons.forEach(btnId => {
            const btn = document.getElementById(btnId);
            if (btn) { // Kiểm tra null
                if (btnId === 'btn-' + type) {
                    btn.classList.add('chart-tab-active');
                    btn.classList.remove('chart-tab-inactive', 'bg-gray-100', 'text-gray-500');
                } else {
                    btn.classList.remove('chart-tab-active');
                    btn.classList.add('chart-tab-inactive');
                }
            }
        });
    };

    var statusOptions = {
        series: [1024, 128, 15],
        labels: ['Hoàn thành', 'Đang đặt', 'Bị hủy'],
        chart: {type: 'donut', height: 320},
        colors: ['#10B981', '#3C50E0', '#FB5454'],
        plotOptions: {
            pie: {
                donut: {
                    size: '70%',
                    labels: {
                        show: true,
                        total: {
                            show: true,
                            label: 'Tổng lịch',
                            fontSize: '16px',
                            fontWeight: 600,
                            color: '#64748B',
                            formatter: function (w) {
                                return w.globals.seriesTotals.reduce((a, b) => {
                                    return a + b
                                }, 0)
                            }
                        }
                    }
                }
            }
        },
        legend: {show: false},
        dataLabels: {enabled: false}
    };

    const statusChart = new ApexCharts(document.querySelector("#statusChart"), statusOptions);
    statusChart.render();


    var peakHourOptions = {
        series: [{name: 'Số lượt đặt', data: [5, 12, 25, 18, 10, 20, 35, 40]}],
        chart: {type: 'bar', height: 300, toolbar: {show: false}},
        plotOptions: {bar: {borderRadius: 4, horizontal: false, columnWidth: '50%'}},
        colors: ['#80CAEE'],
        dataLabels: {enabled: false},
        xaxis: {
            categories: ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00'],
            title: {text: 'Giờ trong ngày'}
        },
        tooltip: {
            y: {
                formatter: function (val) {
                    return val + " khách"
                }
            }
        }
    };
    new ApexCharts(document.querySelector("#peakHourChart"), peakHourOptions).render();


    var frequencyOptions = {
        series: [{name: 'Lượt khách', data: [45, 50, 48, 60, 85, 110, 95]}],
        chart: {height: 300, type: 'area', toolbar: {show: false}},
        colors: ['#F59E0B'],
        stroke: {curve: 'smooth', width: 3},
        xaxis: {categories: ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'CN']},
        grid: {borderColor: '#f1f1f1'},
        fill: {
            type: 'gradient',
            gradient: {shadeIntensity: 1, opacityFrom: 0.6, opacityTo: 0.1, stops: [0, 90, 100]}
        }
    };
    new ApexCharts(document.querySelector("#weeklyFrequencyChart"), frequencyOptions).render();
}

function initVoucherPage() {
    const modalElement = document.getElementById('voucherModal');

    if (modalElement) {
        window.openModal = function() {
            modalElement.classList.remove('hidden');
        }

        window.closeModal = function() {
            modalElement.classList.add('hidden');
        }
    }

    if (typeof ApexCharts === 'undefined') {
        console.warn("ApexCharts chưa được tải");
        return;
    }

    const usageChartEl = document.querySelector("#usageChart");
    if (usageChartEl) {
        var usageOptions = {
            series: [{
                name: 'Lượt dùng',
                data: [30, 40, 35, 50, 49, 60, 70, 91, 125, 100, 140, 160]
            }],
            chart: {
                height: 300,
                type: 'area',
                toolbar: { show: false },
                animations: { enabled: true }
            },
            colors: ['#3C50E0'],
            fill: {
                type: 'gradient',
                gradient: { shadeIntensity: 1, opacityFrom: 0.7, opacityTo: 0.1, stops: [0, 90, 100] }
            },
            dataLabels: { enabled: false },
            stroke: { curve: 'smooth', width: 2 },
            xaxis: {
                categories: ['01/12', '03/12', '05/12', '07/12', '09/12', '11/12', '13/12', '15/12', '17/12', '19/12', '21/12', '23/12']
            },
            tooltip: {
                y: { formatter: function (val) { return val + " lượt" } }
            }
        };

        if (window.usageChartInstance) {
            window.usageChartInstance.destroy();
        }
        window.usageChartInstance = new ApexCharts(usageChartEl, usageOptions);
        window.usageChartInstance.render();
    }

    const typeChartEl = document.querySelector("#typeChart");
    if (typeChartEl) {
        var typeOptions = {
            series: [65, 35], // Percent vs Fixed
            labels: ['Theo %', 'Cố định'],
            chart: {
                type: 'donut',
                height: 320,
            },
            colors: ['#3C50E0', '#80CAEE'],
            plotOptions: {
                pie: {
                    donut: {
                        size: '65%',
                        labels: {
                            show: true,
                            total: {
                                show: true,
                                label: 'Tổng',
                                fontSize: '16px',
                                fontWeight: 600,
                                color: '#64748B',
                                formatter: function (w) {
                                    return w.globals.seriesTotals.reduce((a, b) => { return a + b }, 0) + "%"
                                }
                            }
                        }
                    }
                }
            },
            legend: { position: 'bottom' },
            dataLabels: { enabled: false }
        };

        if (window.typeChartInstance) {
            window.typeChartInstance.destroy();
        }
        window.typeChartInstance = new ApexCharts(typeChartEl, typeOptions);
        window.typeChartInstance.render();
    }
}

async function loadTab(url, element) {
    const container = document.getElementById('tab-admin');
    container.innerHTML = `<div class="flex items-center justify-center h-[60vh]">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#C18C5D]"></div>
            </div>\``
    if (element) {
        const allMenus = document.querySelectorAll('.menu-item');
        allMenus.forEach(el => {
            el.classList.remove('text-[#C18C5D]', 'bg-[#F7F5F2]', 'border-r-4', 'border-[#C18C5D]');
            el.classList.add('text-gray-600', 'hover:bg-gray-50', 'border-r-4', 'border-transparent');
        })

        element.classList.remove('text-gray-600', 'hover:bg-gray-50', 'border-transparent');
        element.classList.add('text-[#C18C5D]', 'bg-[#F7F5F2]', 'border-[#C18C5D]');
    }

    localStorage.setItem('last_active_url', url);

    try {
        const response = await fetch(url);
        if (!response.ok) {
            Swal.fire({
                icon: 'error',
                title: 'Error load page',
                timer: 2000,
                showConfirmButton: false
            })
        } else {
            const result = await response.text()
            container.innerHTML = result;
            if (typeof initDashboardCharts === 'function') {
                initDashboardCharts();
            }

             if (typeof initVoucherPage === 'function') {
                initVoucherPage();
            }
        }

    } catch (error) {
        if (typeof Swal !== 'undefined') {
            Swal.fire({
                icon: 'error',
                title: 'Error Connect',
                text: error,
                confirmButtonColor: '#C18C5D'
            });
        }
    }
}
