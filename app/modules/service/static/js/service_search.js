document.addEventListener('DOMContentLoaded', () => {


    // 2. Parallax Effect cho Header Text (Bay theo chuột)
    const heroSection = document.getElementById('heroSection');
    const parallaxText = document.getElementById('parallaxText');

    if (heroSection && parallaxText) {
        heroSection.addEventListener('mousemove', (e) => {
            const x = (window.innerWidth - e.pageX * 2) / 100;
            const y = (window.innerHeight - e.pageY * 2) / 100;
            parallaxText.style.transform = `translateX(${x}px) translateY(${y}px)`;
        });

        // Reset vị trí khi chuột rời đi
        heroSection.addEventListener('mouseleave', () => {
            parallaxText.style.transform = 'translate(0,0)';
            parallaxText.style.transition = 'transform 0.5s ease';
            setTimeout(() => {
                parallaxText.style.transition = 'none';
            }, 500);
        });
    }

    // 3. Load More Button Logic
    const loadMoreBtn = document.querySelector('.btn-outline-accent');
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', function (e) {
            e.preventDefault(); // Ngăn load lại trang
            const originalText = this.innerText;
            this.innerText = 'Loading...';
            this.classList.add('disabled');

            setTimeout(() => {
                alert('Đã tải thêm dịch vụ (Demo)');
                this.innerText = originalText;
                this.classList.remove('disabled');
            }, 1000);
        });
    }
    //Render list mới
    const searchForm = document.getElementById('searchForm');
    const resultContainer = document.getElementById('serviceResultContainer');


    if (searchForm && resultContainer) {

        /**
         * Hàm Debounce: Giúp trì hoãn việc gửi request khi người dùng đang gõ phím
         * (Chỉ gửi request sau khi ngừng gõ 500ms)
         */
        function debounce(func, wait) {
            let timeout;
            return function (...args) {
                clearTimeout(timeout);
                timeout = setTimeout(() => func.apply(this, args), wait);
            };
        }

        /**
         * Hàm chính: Gửi request lên server và cập nhật lại danh sách (Render HTML mới)
         * @param {string} targetUrl - URL cụ thể để fetch (dùng cho phân trang), nếu null thì lấy từ form
         */
        function fetchAndRender(targetUrl = null) {
            let url = targetUrl;

            // Nếu không có URL cụ thể, tạo URL từ dữ liệu trong Form
            if (!url) {
                const formData = new FormData(searchForm);
                const params = new URLSearchParams(formData);
                // Reset về trang 1 khi filter thay đổi (để tránh lỗi đang ở trang 2 mà filter ra ít kết quả)
                params.set('page', 1);
                url = `${searchForm.action}?${params.toString()}`;
            }

            // Hiệu ứng UX: Làm mờ nhẹ danh sách khi đang load
            resultContainer.style.opacity = '0.5';
            resultContainer.style.pointerEvents = 'none';

            fetch(url)
                .then(response => response.text())
                .then(html => {
                    // Dùng DOMParser để "mổ xẻ" HTML trả về
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');

                    // Lấy nội dung mới của container kết quả
                    const newContent = doc.getElementById('serviceResultContainer').innerHTML;

                    // Thay thế nội dung cũ bằng nội dung mới
                    resultContainer.innerHTML = newContent;

                    // Cập nhật URL trên trình duyệt (để F5 vẫn giữ kết quả)
                    window.history.pushState({}, '', url);

                    // Re-init các hiệu ứng (như AOS animation) nếu có
                    if (typeof AOS !== 'undefined') {
                        AOS.refreshHard();
                    }
                })
                .catch(error => {
                    console.error('Lỗi khi tải dữ liệu:', error);
                })
                .finally(() => {
                    // Gỡ bỏ hiệu ứng loading
                    resultContainer.style.opacity = '1';
                    resultContainer.style.pointerEvents = 'auto';
                });
        }

        // --- GẮN SỰ KIỆN (EVENT LISTENERS) ---

        // A. Sự kiện thay đổi Select Box (Category, Duration, Sort...)
        const selects = searchForm.querySelectorAll('select');
        selects.forEach(select => {
            select.addEventListener('change', () => {
                fetchAndRender(); // Gọi hàm load ngay lập tức
            });
        });

        // B. Sự kiện nhập liệu ô Search Text (Dùng debounce)
        const searchInput = searchForm.querySelector('input[name="q"]');
        if (searchInput) {
            searchInput.addEventListener('input', debounce(() => {
                fetchAndRender();
            }, 500)); // Chờ 500ms sau khi ngừng gõ mới load
        }

        // C. Sự kiện click vào Phân trang (Pagination)
        // Dùng Event Delegation vì các nút phân trang được sinh ra động sau mỗi lần Ajax
        resultContainer.addEventListener('click', function (e) {
            const pageLink = e.target.closest('.page-link');

            // Nếu click vào thẻ a.page-link và không bị disabled
            if (pageLink && !pageLink.parentElement.classList.contains('disabled')) {
                e.preventDefault(); // Ngăn chuyển trang theo cách truyền thống
                const url = pageLink.href;
                if (url && url !== '#') {
                    fetchAndRender(url); // Gọi Ajax với URL của trang đó
                }
            }
        });

        document.addEventListener("DOMContentLoaded", function () {
            // Tìm phần tử đang active trong pagination
            var activePage = document.querySelector('#myPagination .page-item.active');

            if (activePage) {
                // Hàm này sẽ cuộn thanh ngang sao cho nút active nằm giữa màn hình
                activePage.scrollIntoView({
                    behavior: 'auto', // Hoặc 'smooth' nếu muốn thấy nó chạy từ từ
                    block: 'nearest',
                    inline: 'center'  // Quan trọng: Căn giữa theo chiều ngang
                });
            }
        });
    }
});
