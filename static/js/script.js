// Displaying the current date in the format: 25 Dec 2024
const now = new Date();
const dateOptions = { day: "2-digit", month: "short", year: "numeric" };
// Explicitly specify the locale for proper formatting, e.g., "en-GB" for day-month-year format
document.getElementById("date").innerHTML = now.toLocaleDateString("en-GB", dateOptions);
document.getElementById("mobile_date").innerHTML = now.toLocaleDateString("en-GB", dateOptions);

// Displaying the current time in the format: 03:45 PM (24-hour format)
const timeOptions = { hour: "2-digit", minute: "2-digit", hour12: false };  // Set hour12 to false for 24-hour format
document.getElementById("time").innerHTML = now.toLocaleTimeString("en-GB", timeOptions);
document.getElementById("mobile_time").innerHTML = now.toLocaleTimeString("en-GB", timeOptions);

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
        "light freezing rain": "/static/img/freezing_rain.jpg",
        "heavy freezing rain": "/static/img/freezing_rain.jpg",
        "light snow": "/static/img/snowing.jpg",
        "moderate snow": "/static/img/snowing.jpg",
        "Heavy snow": "/static/img/snowing.jpg",
        "snow grains": "/static/img/snow_grains.jpg",
        "light rain showers": "/static/img/rain_shower.jpg",
        "moderate rain showers": "/static/img/rain_shower.jpg",
        "violent rain showers": "/static/img/rain_shower.jpg",
        "light snow showers": "/static/img/snow_shower.jpg",
        "heavy snow showers": "/static/img/snow_shower.jpg",
        "slight thunderstorm": "/static/img/thunderstorm.jpg",
        "moderate thunderstorm": "/static/img/thunderstorm.jpg",
        "thunderstorm with hail": "/static/img/thunderstorm.jpg",
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