const inputContainer = document.getElementById('input-container');
const airportList = document.getElementById('airport-list');
// const inputFields = inputContainer.querySelectorAll('input[name="arrivaldeparture"]');

inputContainer.addEventListener('input', function (event) {
    if (event.target.matches('input[name="arrivaldeparture"]')) {
         handleInput(event.target).catch(error => {
            console.error('An error occurred:', error);
        });
    }
});

async function handleInput(inputField) {
    const inputValue = inputField.value;
    const response = await fetch(`/search?q=${inputValue}`);
    const airports = await response.json();
    console.log(airports);
    let html = '';

    for (let i = 0; i < airports.length; i++) {
        let airport = airports[i];
        let cityName = airport[1].replace('<', '&lt;').replace('&', '&amp;');
        let airportName = airport[0].replace('<', '&lt;').replace('&', '&amp;');
        html += '<li data-value="' + airportName + '">' + cityName + ' - ' + airportName + '</li>';
    }

    airportList.innerHTML = html;

    // Attach click event listeners to list items for autocompletion
    const listItems = airportList.querySelectorAll('li');
    listItems.forEach(item => {
        item.addEventListener('click', function (event) {
            autocompleteInput(event.target, inputField);
        });
    });
}

function autocompleteInput(clickedItem, inputField) {
    inputField.value = clickedItem.getAttribute('data-value');

    // Clear the airport list
    airportList.innerHTML = '';
}
























// const inputContainer = document.getElementById('input-container');
// inputContainer.addEventListener('input', function (event) {
//     if (event.target.matches('input[name="arrivaldeparture"]')) {
//          handleInput(event.target).catch(error => {
//             console.error('An error occurred:', error);
//         });
//     }
// });
// async function handleInput(inputField) {
//     const inputValue = inputField.value;
//     const response = await fetch(`/search?q=${inputValue}`);
//     const airports = await response.json();
//     console.log(airports);
//     let html = '';
//     for (let i = 0; i < airports.length; i++) {
//         let airport = airports[i];
//         let cityName = airport[1].replace('<', '&lt;').replace('&', '&amp;');
//         let airportName = airport[0].replace('<', '&lt;').replace('&', '&amp;');
//         html += '<li>' + cityName + ' - ' + airportName + '</li>';
//     }
//     document.querySelector('ul').innerHTML = html;
// }
