// URL API Gateway
const apiUrl = "https://6yd3aewsd4.execute-api.us-east-1.amazonaws.com/weather";

// Fetch data from API
fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
        // Przypisanie danych do odpowiednich sekcji
        const yesterday = document.getElementById("yesterday");
        const today = document.getElementById("today");

        // Zakładam, że dane są tablicą obiektów
        if (data.length >= 2) {
            const [day1, day2] = data; // Przykład podziału danych

            yesterday.innerHTML = `
                <h3>Wczoraj</h3>
                <p><strong>Temperatura:</strong> ${day1.temp}°C</p>
                <p><strong>Min:</strong> ${day1.temp_min}°C</p>
                <p><strong>Max:</strong> ${day1.temp_max}°C</p>
                <p><strong>Data:</strong> ${day1.Date}</p>
            `;

            today.innerHTML = `
                <h3>Dzisiaj</h3>
                <p><strong>Temperatura:</strong> ${day2.temp}°C</p>
                <p><strong>Min:</strong> ${day2.temp_min}°C</p>
                <p><strong>Max:</strong> ${day2.temp_max}°C</p>
                <p><strong>Data:</strong> ${day2.Date}</p>
            `;
        } else {
            document.getElementById("weather-data").innerText = "Brak wystarczających danych.";
        }
    })
    .catch(error => {
        console.error("Error fetching weather data:", error);
        document.getElementById("weather-data").innerText = "Nie udało się załadować danych pogodowych.";
    });
// elementy językowe
const langPlElements = document.querySelectorAll('.lang-pl');
const langEnElements = document.querySelectorAll('.lang-en');

// Przyciski do zmiany języka
const switchPl = document.getElementById('switch-pl');
const switchEn = document.getElementById('switch-en');

// Funkcja zmiany języka
function switchLanguage(language) {
    if (language === 'pl') {
        langPlElements.forEach(el => el.style.display = '');
        langEnElements.forEach(el => el.style.display = 'none');
        switchPl.classList.add('active');
        switchEn.classList.remove('active');
    } else {
        langPlElements.forEach(el => el.style.display = 'none');
        langEnElements.forEach(el => el.style.display = '');
        switchPl.classList.remove('active');
        switchEn.classList.add('active');
    }
}

// Event listeners 
switchPl.addEventListener('click', () => switchLanguage('pl'));
switchEn.addEventListener('click', () => switchLanguage('en'));
