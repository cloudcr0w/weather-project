// URL for API Gateway
const apiUrl = 'https://6yd3aewsd4.execute-api.us-east-1.amazonaws.com/weather'

// Icons for weather conditions
const weatherIcons = {
	Clear: '/img/sun.jpg',
	Clouds: '/img/cloud.jpg',
	Rain: '/img/rain.jpg',
	Snow: '/img/snow.jpg',
	Drizzle: '/img/drizzle.jpg',
	Thunderstorm: '/img/thunderstorm.jpg',
}

// Fetch weather data from the API
fetch(apiUrl)
	.then(response => {
		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`)
		}
		return response.json()
	})
	.then(data => {
		console.log('Data from API:', data)

		// Select HTML elements
		const weatherDataContainer = document.getElementById('weather-data')
		const dateElement = document.getElementById('date').querySelector('span')
		const weatherIconElement = document.getElementById('weather-icon')
		const tempElement = document.getElementById('temp').querySelector('span')
		const tempMinElement = document.getElementById('temp-min').querySelector('span')
		const tempMaxElement = document.getElementById('temp-max').querySelector('span')

		// Find the latest data based on the date
		const latestData = data.reduce((latest, current) => {
			return new Date(current.Date) > new Date(latest.Date) ? current : latest
		}, data[0])

		console.log('Newest weather data:', latestData)

		// Check if data is available
		if (latestData) {
			// Update HTML elements with the latest data
			dateElement.innerText = latestData.Date || 'No data available'
			weatherIconElement.src = weatherIcons[latestData.weather] || weatherIcons.Clear
			tempElement.innerText = latestData.temp || 'No data available'
			tempMinElement.innerText = latestData.temp_min || 'No data available'
			tempMaxElement.innerText = latestData.temp_max || 'No data available'
		} else {
			// Display a message if no data is available
			weatherDataContainer.innerText = 'Insufficient weather data available.'
		}
	})
	.catch(error => {
		console.error('Error fetching weather data:', error)
		document.getElementById('weather-data').innerText = 'Failed to load weather data.'
	})

// Language elements
const langPlElements = document.querySelectorAll('.lang-pl')
const langEnElements = document.querySelectorAll('.lang-en')

// Language switch buttons
const switchPl = document.getElementById('switch-pl')
const switchEn = document.getElementById('switch-en')

// Function to switch language
function switchLanguage(language) {
	if (language === 'pl') {
		langPlElements.forEach(el => (el.style.display = ''))
		langEnElements.forEach(el => (el.style.display = 'none'))
		switchPl.classList.add('active')
		switchEn.classList.remove('active')
	} else {
		langPlElements.forEach(el => (el.style.display = 'none'))
		langEnElements.forEach(el => (el.style.display = ''))
		switchPl.classList.remove('active')
		switchEn.classList.add('active')
	}
}
// JavaScript to set the current year
document.getElementById('current-year').textContent = new Date().getFullYear()

// Event listeners for language switch
switchPl.addEventListener('click', () => switchLanguage('pl'))
switchEn.addEventListener('click', () => switchLanguage('en'))
