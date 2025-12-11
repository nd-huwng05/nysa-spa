function toggleEditInfo(btn) {
    const inputs = document.querySelectorAll('#step-3 input, #step-3 select, #step-3 textarea');
    const isCurrentlyReadonly = document.getElementById('custName').hasAttribute('readonly');

    inputs.forEach(input => {
        if(input.id === 'custEmail') return; // Bỏ qua Email

        if(isCurrentlyReadonly) {
            input.removeAttribute('readonly');
            input.removeAttribute('disabled');
        } else {
            input.setAttribute('readonly', true);
            if(input.tagName === 'SELECT') input.setAttribute('disabled', true);
        }
    });

    if(isCurrentlyReadonly) {
        btn.innerHTML = '<i class="fas fa-save me-1"></i> Save';
        btn.classList.remove('btn-outline-primary');
        btn.classList.add('btn-primary');
    } else {
        btn.innerHTML = '<i class="fas fa-pen me-1"></i> Update';
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-outline-primary');
    }
}

function updateComboMaster(comboId, staffId) {
    const comboBox = document.querySelector(`.combo-box[data-id="${comboId}"]`);
    const childSelects = comboBox.querySelectorAll('.child-select');

    if (staffId !== 'split') {
        childSelects.forEach(select => {
            select.value = staffId;
            select.setAttribute('disabled', true);
            const serviceId = select.id.split('-')[2];
            updateAllocation(serviceId);
        });
    } else {
        childSelects.forEach(select => {
            select.removeAttribute('disabled');
        });
    }
}

function updateAllocation(serviceId) {
    const selectBox = document.getElementById(`staff-select-${serviceId}`);
    if(!selectBox) return;

    const staffName = selectBox.options[selectBox.selectedIndex].text;
    const summaryLabel = document.getElementById(`sum-staff-${serviceId}`);
    if(summaryLabel) {
        summaryLabel.innerText = staffName;
    }
}

function checkStep1() {
    const date = document.getElementById('inputDate').value;
    const time = document.getElementById('inputTime').value;
    const estimateBox = document.getElementById('timeEstimate');
    const timePlaceholder = document.getElementById('time-placeholder');
    const timelineNodes = document.querySelectorAll('.timeline-node');

    if(date && time) {
        document.getElementById('step-2').classList.remove('disabled');
        document.getElementById('step-3').classList.remove('disabled');
        document.getElementById('btnSubmit').disabled = false;
        if(timePlaceholder) timePlaceholder.classList.add('d-none');
        timelineNodes.forEach(node => node.classList.remove('d-none'));

        let currentMockTime = new Date(`2000-01-01T${time}:00`);
        let totalMinutes = 0;

        const serviceItems = document.querySelectorAll('.service-item');

        serviceItems.forEach(item => {
            const duration = parseInt(item.getAttribute('data-duration'));
            const id = item.getAttribute('data-id');

            let endTime = new Date(currentMockTime.getTime() + duration * 60000);

            const timeStr = `${formatTime(currentMockTime)} - ${formatTime(endTime)}`;

            const timeLabel = document.getElementById(`sum-time-${id}`);
            if(timeLabel) timeLabel.innerText = timeStr;

            updateAllocation(id);

            totalMinutes += duration;
            currentMockTime = endTime;
        });

        estimateBox.style.display = 'flex';
        document.getElementById('durationText').innerText = `Total duration: ${totalMinutes} mins`;
        document.getElementById('endTimeText').innerText = `Est. finish: ${formatTime(currentMockTime)}`;

        document.getElementById('sumTimeDisplay').innerText = time;
        document.getElementById('sumEndTimeDisplay').innerText = `(Est. finish at ${formatTime(currentMockTime)})`;
        const dateObj = new Date(date);
        document.getElementById('sumDateDisplay').innerText = dateObj.toLocaleDateString('en-US', {weekday: 'long', day:'numeric', month:'long'});

    } else {
        estimateBox.style.display = 'none';
        document.getElementById('btnSubmit').disabled = true;
        if(timePlaceholder) timePlaceholder.classList.remove('d-none');
        timelineNodes.forEach(node => node.classList.add('d-none'));
    }
}

function formatTime(d) {
    return d.toTimeString().substring(0, 5);
}