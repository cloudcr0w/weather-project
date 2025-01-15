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
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        const weatherDataContainer = document.getElementById("weather-data");
        const dateElement = document.getElementById("date").querySelector("span");
        const weatherIconElement = document.getElementById("weather-icon");
        const tempElement = document.getElementById("temp").querySelector("span");
        const tempMinElement = document.getElementById("temp-min").querySelector("span");
        const tempMaxElement = document.getElementById("temp-max").querySelector("span");

        // Check if data is available
        if (data.length >= 1) {
            const todayData = data[0]; // Assuming first element is today's weather

            // Update HTML elements with weather data
            dateElement.innerText = todayData.Date || "Brak danych";
            weatherIconElement.src = weatherIcons[todayData.weather] || weatherIcons.Clear;
            tempElement.innerText = todayData.temp || "Brak danych";
            tempMinElement.innerText = todayData.temp_min || "Brak danych";
            tempMaxElement.innerText = todayData.temp_max || "Brak danych";
        } else {
            weatherDataContainer.innerText = "Brak wystarczających danych pogodowych.";
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
