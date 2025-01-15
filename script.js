// URL API Gateway
const apiUrl = "https://6yd3aewsd4.execute-api.us-east-1.amazonaws.com/weather";

// Icons for weather conditions
const weatherIcons = {
    Clear: "/img/sun.jpg",
    Clouds: "/img/cloud.jpg",
    Rain: "/img/rain.jpg",
    Snow: "/img/snow.jpg",
    Drizzle: "/img/drizzle.jpg",
    Thunderstorm: "/img/thunderstorm.jpg"
};

// Fetch weather data from API
fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
        // Select elements for yesterday and today
        const yesterday = document.getElementById("yesterday");
        const today = document.getElementById("today");

        // Check if we have at least two days of data
        if (data.length >= 2) {
            const [day1, day2] = data; // Extract yesterday and today data

            // Update the "Yesterday" section
            yesterday.innerHTML = `
                <h3 class="lang-pl">Wczoraj</h3>
                <h3 class="lang-en" style="display: none;">Yesterday</h3>
                <img src="${weatherIcons[day1.weather] || weatherIcons.Clear}" alt="Weather Icon">
                <p><strong class="lang-pl">Temperatura:</strong> <strong class="lang-en" style="display: none;">Temperature:</strong> ${day1.temp}°C</p>
                <p><strong class="lang-pl">Min:</strong> <strong class="lang-en" style="display: none;">Min:</strong> ${day1.temp_min}°C</p>
                <p><strong class="lang-pl">Max:</strong> <strong class="lang-en" style="display: none;">Max:</strong> ${day1.temp_max}°C</p>
                <p><strong class="lang-pl">Data:</strong> <strong class="lang-en" style="display: none;">Date:</strong> ${day1.Date}</p>
            `;

            // Update the "Today" section
            today.innerHTML = `
                <h3 class="lang-pl">Dzisiaj</h3>
                <h3 class="lang-en" style="display: none;">Today</h3>
                <img src="${weatherIcons[day2.weather] || weatherIcons.Clear}" alt="Weather Icon">
                <p><strong class="lang-pl">Temperatura:</strong> <strong class="lang-en" style="display: none;">Temperature:</strong> ${day2.temp}°C</p>
                <p><strong class="lang-pl">Min:</strong> <strong class="lang-en" style="display: none;">Min:</strong> ${day2.temp_min}°C</p>
                <p><strong class="lang-pl">Max:</strong> <strong class="lang-en" style="display: none;">Max:</strong> ${day2.temp_max}°C</p>
                <p><strong class="lang-pl">Data:</strong> <strong class="lang-en" style="display: none;">Date:</strong> ${day2.Date}</p>
            `;
        } else {
            // If not enough data, show an error message
            document.getElementById("weather-data").innerText = "Brak wystarczających danych.";
        }
    })
    .catch(error => {
        console.error("Error fetching weather data:", error);
        document.getElementById("weather-data").innerText = "Nie udało się załadować danych pogodowych.";
    });

// Language elements
const langPlElements = document.querySelectorAll('.lang-pl');
const langEnElements = document.querySelectorAll('.lang-en');

// Language switch buttons
const switchPl = document.getElementById('switch-pl');
const switchEn = document.getElementById('switch-en');

// Function to switch language
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

// Event listeners for language switch
switchPl.addEventListener('click', () => switchLanguage('pl'));
switchEn.addEventListener('click', () => switchLanguage('en'));
