document.getElementById('previous_day').addEventListener('click', function(event) {
    event.preventDefault();
    let currentUrl = window.location.href;
    let urlParts = currentUrl.split('/');
    let dateParts = urlParts[6].split('-');
    let currentDate = new Date(dateParts[0], dateParts[1] - 1, dateParts[2]);
    currentDate.setDate(currentDate.getDate() - 1);
    let newDateString = currentDate.toISOString().split('T')[0];
    urlParts[6] = newDateString;
    window.location.href = urlParts.join('/');
});

document.getElementById('last_day').addEventListener('click', function(event) {
    event.preventDefault();
    let currentUrl = window.location.href;
    let urlParts = currentUrl.split('/');
    let dateParts = urlParts[-1].split('-');
    let currentDate = new Date(dateParts[0], dateParts[1] - 1, dateParts[2]);
    currentDate.setDate(currentDate.getDate() + 1);
    let newDateString = currentDate.toISOString().split('T')[0];
    urlParts[6] = newDateString;
    window.location.href = urlParts.join('/');
});