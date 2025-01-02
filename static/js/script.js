// Displaying the current date in the format: 25 Dec 2024
const now = new Date();
const dateOptions = { day: "2-digit", month: "short", year: "numeric" };
document.getElementById("date").innerHTML = now.toLocaleDateString(undefined, dateOptions);
document.getElementById("mobile_date").innerHTML = now.toLocaleDateString(undefined, dateOptions);

// Displaying the current time in the format: 03:45 PM
const timeOptions = { hour: "2-digit", minute: "2-digit", hour12: false };
document.getElementById("time").innerHTML = now.toLocaleTimeString(undefined, timeOptions);
document.getElementById("mobile_time").innerHTML = now.toLocaleTimeString(undefined, timeOptions);

//Refresh the page on submit 
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("input_form_town");
    if (form) {
        form.addEventListener("submit", function () {
            location.reload();
        });
    } else {
        console.error("Form with ID 'input_form_town' not found.");
    }
});

// Mapping of weather conditions to background images
document.addEventListener("DOMContentLoaded", () => {
    // Weather condition-to-background mapping
    const weatherBackgrounds = {
        "clear sky": "/static/img/clear_sky.jpg",
        "mainly clear": "/static/img/mainly_clear.jpg",
        "partly cloudy": "/static/img/partly_cloudy.jpg",
        "overcast": "/static/img/overcast.jpg",
        "fog": "/static/img/fog.jpg",
        "depositing rime fog": "/static/img/fog.jpg",
        "light drizzle": "/static/img/drizzle.jpg",
        "moderate drizzle": "/static/img/drizzle.jpg",
        "dense drizzle": "/static/img/drizzle.jpg",
        "freezing drizzle (moderate)": "/static/img/drizzle.jpg",
        "freezing drizzle (heavy)": "/static/img/drizzle.jpg",
        "light rain": "/static/img/rain.jpg",
        "moderate rain": "/static/img/rain.jpg",
        "heavy rain": "/static/img/heavy_rain.jpg",
        "Light freezing rain": "/static/img/freezing_rain.jpg",
        "Heavy freezing rain": "/static/img/freezing_rain.jpg",
        "Light snow": "/static/img/snowing.jpg",
        "Moderate snow": "/static/img/snowing.jpg",
        "Heavy snow": "/static/img/snowing.jpg",
        "Snow grains": "/static/img/snow_grains.jpg",
        "Light rain showers": "/static/img/rain_shower.jpg",
        "Moderate rain showers": "/static/img/rain_shower.jpg",
        "Violent rain showers": "/static/img/rain_shower.jpg",
        "Light snow showers": "/static/img/snow_shower.jpg",
        "Heavy snow showers": "/static/img/snow_shower.jpg",
        "Slight thunderstorm": "/static/img/thunderstorm.jpg",
        "Moderate thunderstorm": "/static/img/thunderstorm.jpg",
        "Thunderstorm with hail": "/static/img/thunderstorm.jpg",
    };

    // Function to update the background image
    function updateBackground() {
        const weatherInfoElement = document.querySelector(".weather_info");
        const body = document.body;

        if (!weatherInfoElement) {
            console.error("Weather info element not found.");
            return;
        }

        // Get the current weather text
        const currentWeather = weatherInfoElement.textContent.toLowerCase().trim();
        //console.log("Detected weather:", currentWeather); // Debugging log

        // Match the weather to the background image
        const backgroundImage = weatherBackgrounds[currentWeather] || "/static/img/default.jpg";
        //console.log(currentWeather)
        // Update the body background
        body.style.backgroundImage = `url('${backgroundImage}')`;
        body.style.backgroundSize = "cover";
        body.style.backgroundRepeat = "no-repeat";
        body.style.overflow = "hidden";

        //console.log("Background updated to:", backgroundImage); // Debugging log
    }

    // Delay the background update for dynamic rendering
    setTimeout(updateBackground, 100); // Adjust timing if necessary
});