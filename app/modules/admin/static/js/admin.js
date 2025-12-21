// === CHART 1: REVENUE (Doanh thu) - Có chức năng chuyển Tab ===

// Dữ liệu giả lập
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
        data: [450, 520, 480, 600, 750, 800, 850, 900, 950, 1100, 1050, 1200],
        categories: ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12']
    }
};

var revenueOptions = {
    series: [{
        name: 'Doanh thu (triệu VNĐ)',
        data: revenueData.week.data // Mặc định là Tuần
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

var revenueChart = new ApexCharts(document.querySelector("#revenueChart"), revenueOptions);
revenueChart.render();

// Hàm xử lý khi click tab
function updateRevenue(type) {
    // Cập nhật dữ liệu biểu đồ
    revenueChart.updateOptions({
        xaxis: {categories: revenueData[type].categories}
    });
    revenueChart.updateSeries([{
        data: revenueData[type].data
    }]);

    // Cập nhật style nút bấm (Active/Inactive)
    const buttons = ['btn-week', 'btn-month', 'btn-year'];
    buttons.forEach(btnId => {
        const btn = document.getElementById(btnId);
        if (btnId === 'btn-' + type) {
            btn.classList.add('chart-tab-active');
            btn.classList.remove('chart-tab-inactive', 'bg-gray-100', 'text-gray-500');
        } else {
            btn.classList.remove('chart-tab-active');
            btn.classList.add('chart-tab-inactive');
        }
    });
}


// === CHART 2: STATUS RATIO (Tỷ lệ trạng thái - Donut) ===
var statusOptions = {
    series: [1024, 128, 15], // Hoàn thành, Đặt, Hủy
    labels: ['Hoàn thành', 'Đang đặt', 'Bị hủy'],
    chart: {
        type: 'donut',
        height: 320,
    },
    colors: ['#10B981', '#3C50E0', '#FB5454'], // Green, Blue, Red
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
    legend: {show: false}, // Đã custom legend bên ngoài bằng HTML
    dataLabels: {enabled: false}
};
var statusChart = new ApexCharts(document.querySelector("#statusChart"), statusOptions);
statusChart.render();


// === CHART 3: PEAK HOURS (Thời gian phổ biến - Bar Chart) ===
var peakHourOptions = {
    series: [{
        name: 'Số lượt đặt',
        data: [5, 12, 25, 18, 10, 20, 35, 40, 30, 15]
    }],
    chart: {
        type: 'bar',
        height: 300,
        toolbar: {show: false}
    },
    plotOptions: {
        bar: {
            borderRadius: 4,
            horizontal: false, // Cột đứng
            columnWidth: '50%'
        }
    },
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
var peakHourChart = new ApexCharts(document.querySelector("#peakHourChart"), peakHourOptions);
peakHourChart.render();


// === CHART 4: WEEKLY FREQUENCY (Tần suất trong tuần - Line/Area) ===
var frequencyOptions = {
    series: [{
        name: 'Lượt khách',
        data: [45, 50, 48, 60, 85, 110, 95] // Dữ liệu từ T2 -> CN
    }],
    chart: {
        height: 300,
        type: 'area',
        toolbar: {show: false}
    },
    colors: ['#F59E0B'], // Màu cam cho khác biệt
    stroke: {
        curve: 'smooth',
        width: 3
    },
    xaxis: {
        categories: ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'CN']
    },
    grid: {
        borderColor: '#f1f1f1',
    },
    fill: {
        type: 'gradient',
        gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.6,
            opacityTo: 0.1,
            stops: [0, 90, 100]
        }
    }
};
var weeklyChart = new ApexCharts(document.querySelector("#weeklyFrequencyChart"), frequencyOptions);
weeklyChart.render();

document.addEventListener("DOMContentLoaded", function () {
    const savedUrl = localStorage.getItem('last_active_url');
    const defaultUrl = '/booking/staff-book-view';

    console.log(savedUrl)
    let activeTab = null;
    if (savedUrl) {
        activeTab = document.querySelector(`.menu-item[onclick*="${savedUrl}"]`)
            || document.querySelector(`.menu-item[data-url="${savedUrl}"]`);
    }
    if (!activeTab) {
        activeTab = document.querySelector('.menu-item');
    }

    if (activeTab) {
        loadTab(savedUrl || defaultUrl, activeTab);
    }
})

async function loadTab(url, element) {
    const container = document.getElementById('tab-staff');
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
