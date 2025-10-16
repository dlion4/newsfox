import { left } from "@popperjs/core";
import "../sass/project.scss";
import $ from "jquery";
import "magnific-popup";

$(function () {
    $('a.popup-youtube').magnificPopup({
        type: 'iframe',
        mainClass: 'mfp-fade',
        removalDelay: 160,
        preloader: false,
        fixedContentPos: true,
        fixedBgPos: true,
        closeOnBgClick: false,
        enableEscapeKey: false,
        disableOn: 0,
        callbacks: {
            open: function () {
                $('html, body').css({
                    overflow: 'hidden',
                    height: '100%'
                });
                $('a.popup-youtube').on('click.mfp', function (e) {
                    e.preventDefault();
                });
            },
            close: function () {
                $('html, body').css({
                    overflow: '',
                    height: ''
                });
                $('iframe.mfp-iframe').remove();
            },
            elementParse: function (item) {
                const url = item.el.attr('href');
                item.src = url;
            }
        }
    });
    $(document).on('click', 'a.popup-youtube', function (e) {
        e.preventDefault();
    });

    const date = new Date();

    const options = {
        weekday: "short",
        month: "long",
        day: "numeric"
    };
    const formattedDate = date.toLocaleDateString("en-US", options);
    $("#current-date").text(formattedDate);

    $("form.newsletter-form").on("submit", async function (e) {
        e.preventDefault();
        const emailInput = $(this).find('input[name="email"]');
        const email = emailInput.val().trim();
        const messageDiv = $(this).find('#validator-newsletter');

        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(email)) {
            messageDiv.text("Please enter a valid email address.").css("color", "red");
            return;
        }
        await new Promise((resolve, reject) => setTimeout(resolve, 500));
        messageDiv.text("Thank you for subscribing!").css("color", "green");
        emailInput.val("");
    });


async function getLocation() {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject("Geolocation not supported");
    } else {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          resolve({
            lat: pos.coords.latitude,
            lon: pos.coords.longitude
          });
        },
        (err) => reject(err.message)
      );
    }
  });
}

async function getCityName(lat, lon) {
  const response = await fetch(
    `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lon}`
  );
  const data = await response.json();
  return data.address.city || data.address.town || data.address.village || "Unknown";
}

async function updateWeather(city = "Nairobi", lat = null, lon = null) {
  let response;
  if (lat && lon) {
    // Use coordinates directly if available
    response = await fetch(`https://wttr.in/${lat},${lon}?format=j1`);
  } else {
    // Fallback to city name
    response = await fetch(`https://wttr.in/${city}?format=j1`);
  }

  const data = await response.json();
  const temp = data.current_condition[0].temp_C;
  const status = data.current_condition[0].weatherDesc[0].value;

  const cityTempDiv = document.querySelector(".city-temperature");
  cityTempDiv.querySelector("span").innerHTML = `${temp}<sup>°C</sup>`;
  cityTempDiv.querySelector("b").textContent = city;
  cityTempDiv.querySelector("i").title = status;
}

async function initWeather() {
  try {
    const { lat, lon } = await getLocation();
    const city = await getCityName(lat, lon);
    await updateWeather(city, lat, lon);

    // Refresh every 10 minutes
    setInterval(() => updateWeather(city, lat, lon), 60000 * 10);
  } catch (error) {
    console.warn("Location not available, defaulting to Nairobi:", error);
    await updateWeather("Nairobi");
    setInterval(() => updateWeather("Nairobi"), 60000 * 10);
  }
}

initWeather();



});


