document.addEventListener('DOMContentLoaded', function() {
    const drink1Input = document.getElementById('drink1');
    const drink2Input = document.getElementById('drink2');
    const statusSwitch = document.getElementById('statusSwitch');
    const statusText = document.getElementById('statusText');
    const statusInput = document.createElement('input');
    statusInput.type = 'hidden';
    statusInput.name = 'status';
    document.getElementById('drinkForm').appendChild(statusInput);

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
        })
        .catch(error => console.error('Error:', error));
    }

    function updateStatus(status) {
        statusText.textContent = status ? 'ВКЛЮЧЕН' : 'ВЫКЛЮЧЕН';
        statusText.style.color = status ? 'green' : 'red';
        console.log('statusSwitch.checked:', statusSwitch.checked, status);
        statusSwitch.checked = status;
        statusInput.value = status; // Обновим значение скрытого поля
    }

    console.log('drink1Input,  drink2Input:', drink1Input.value, drink2Input.value);

    if (drink1Input && drink2Input && statusInput) {
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
    } else {
        console.error('One or more elements are missing in the DOM.');
    }
});
