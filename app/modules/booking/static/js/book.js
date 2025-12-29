document.addEventListener("DOMContentLoaded", function () {
    const inputDate = document.getElementById("inputDate")
    inputDate.addEventListener("change", checkUnlockNextStep)

    const dropdownItems = document.querySelectorAll('.time-part-select')
    dropdownItems.forEach(item => {
        item.addEventListener('click', function (e) {
            e.preventDefault();

            const wrapper = this.closest('.custom-select-wrapper');
            const buttonSpan = wrapper.querySelector('.selected-text')

            if (buttonSpan) {
                buttonSpan.textContent = this.getAttribute('data-value');
            }

            wrapper.querySelectorAll('.time-part-select').forEach(el => el.classList.remove('active-selected'));
            this.classList.add('active-selected');

            updateHiddenTime();
        })
    })
})

function updateHiddenTime() {
    const hourItem = document.querySelector('#hourWrapper .active-selected');
    const minuteItem = document.querySelector('#minuteWrapper .active-selected');
    const inputTime = document.getElementById('inputTime');

    if (hourItem && minuteItem) {
        const hour = hourItem.getAttribute('data-value');
        const minute = minuteItem.getAttribute('data-value');

        inputTime.value = `${hour}:${minute}`;

    } else {
        inputTime.value = "";
    }
    checkUnlockNextStep();
}

function checkUnlockNextStep() {
    const dateValue = document.getElementById('inputDate').value;
    const timeValue = document.getElementById('inputTime').value;
    const step2 = document.getElementById('step-2');

    if (dateValue && timeValue && timeValue.length > 3) {
        step2.classList.remove('disabled');
        htmx.trigger('#step-2', 'load_timeline');
    } else {
        step2.classList.add('disabled');
    }
}