document.addEventListener('DOMContentLoaded', function() {
    const drink1Input = document.getElementById('drink1');
    const drink2Input = document.getElementById('drink2');
    const statusSwitch = document.getElementById('statusSwitch');
    const statusText = document.getElementById('statusText');
    const statusInfo = document.getElementById('status_info');
    const statusInput = document.createElement('input');
    statusInput.type = 'hidden';
    statusInput.name = 'status';
    document.getElementById('drinkForm').appendChild(statusInput);

    const translations = {
        on: document.getElementById('trans-on').textContent,
        off: document.getElementById('trans-off').textContent,
        info: {
            0: document.getElementById('trans-info-0').textContent,
            1: document.getElementById('trans-info-1').textContent,
            2: document.getElementById('trans-info-2').textContent,
            3: document.getElementById('trans-info-3').textContent,
            4: document.getElementById('trans-info-4').textContent,
        }
    };

    function updateStatus(status) {
        statusText.textContent = status ? translations.on : translations.off;
        statusText.style.color = status ? '#0f6121' : 'red';
        statusSwitch.checked = status;
        statusInput.value = status; // Обновим значение скрытого поля
    }

    function updateStatusInfo(info) {
        const statusInfo = document.getElementById('status_info');
        const statusInfo2 = document.getElementById('status_info2');
        const statusCircle = document.getElementById('status_circle');

        statusInfo.textContent = translations.info[info];

        const color_green = '#116d25'

        switch (info) {
            case 0:
            case 1:
            case 2:
                statusInfo.style.color = color_green;
                statusInfo2.style.color = color_green;
                statusCircle.style.backgroundColor = color_green; // Светло-зеленый цвет
                break;
            case 3:
                statusInfo.style.color = 'orange';
                statusInfo2.style.color = 'orange';
                statusCircle.style.backgroundColor = 'orange';
                break;
            case 4:
                statusInfo.style.color = 'red';
                statusInfo2.style.color = 'red';
                statusCircle.style.backgroundColor = 'red';
                break;
            default:
                statusInfo.style.color = 'black'; // Сброс цвета на стандартный, если info не соответствует ни одному из случаев
                statusCircle.style.backgroundColor = 'black';
        }
    }

    function validateInput(input) {
        let value = parseFloat(input.value);

        if (isNaN(value) || input.value.trim() === '') {
            value = 0;
        } else {
            value = Math.round(value);
            if (value < 0) {
                value = 0;
            } else if (value > 500) {
                value = 500;
            }
        }
        input.value = value;

        const event = new Event('change');
        input.dispatchEvent(event);
    }

    function sendData(formData) {
        fetch('', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('Response data:', data);
            updateStatus(data.status);
            updateStatusInfo(data.info);  // Обновите status_info
        })
        .catch(error => console.error('Error:', error));
    }

    function updateData() {
        $.ajax({
            url: '/get_data/',
            method: 'GET',
            success: function(data) {
                drink1Input.value = data.drink1;
                drink2Input.value = data.drink2;
                updateStatus(data.status);
                updateStatusInfo(data.info);  // Обновите status_info
            },
            error: function(error) {
                console.error('Error fetching data:', error);
            }
        });
    }

    if (drink1Input && drink2Input && statusInput) {
        drink1Input.addEventListener('input', function() {
            validateInput(drink1Input);
        });

        drink2Input.addEventListener('input', function() {
            validateInput(drink2Input);
        });

        drink1Input.addEventListener('change', function() {
            console.log('Drink1 changed:', drink1Input.value);
            const formData = new FormData(document.getElementById('drinkForm'));
            sendData(formData);
        });

        drink2Input.addEventListener('change', function() {
            console.log('Drink2 changed:', drink2Input.value);
            const formData = new FormData(document.getElementById('drinkForm'));
            sendData(formData);
        });

        statusSwitch.addEventListener('change', function() {
            console.log('statusSwitch changed:', statusSwitch.checked);
            const formData = new FormData(document.getElementById('drinkForm'));
            formData.append('status', statusSwitch.checked);
            sendData(formData);
        });

        updateData();

    } else {
        console.error('One or more elements are missing in the DOM.');
    }

    // Обновляем данные каждые 2 секунды
    setInterval(updateData, 2000);
});
