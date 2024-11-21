fetch('http://127.0.0.1:5000', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        first_name: 'John',
        last_name: 'Doe',
        blood_group: 'A+',
        hla_type: 'A24,B27',
        phone: '1234567890',
    }),
})
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
