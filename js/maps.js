/* ==========================================
   js/maps.js
   Google Maps Redirect Buttons
========================================== */

document.addEventListener("DOMContentLoaded", () => {

  /* ========================
     Find All Map Buttons
  ======================== */
  const mapButtons = document.querySelectorAll(".map-btn");

  /* ========================
     Open Google Maps Search
  ======================== */
  function openMaps(query) {

    const url =
      `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(query)}`;

    window.open(url, "_blank");
  }

  /* ========================
     Attach Click Events
  ======================== */
  mapButtons.forEach(button => {

    button.addEventListener("click", () => {

      const query = button.getAttribute("data-query");

      if (query) {
        openMaps(query);
      }

    });

  });

  /* ========================
     Optional Auto Geolocation
  ======================== */
  const locationBtn = document.getElementById("useLocation");

  if (locationBtn) {

    locationBtn.addEventListener("click", () => {

      if (!navigator.geolocation) {
        alert("Geolocation is not supported on this browser.");
        return;
      }

      locationBtn.innerText = "Detecting...";

      navigator.geolocation.getCurrentPosition(
        (position) => {

          const lat = position.coords.latitude;
          const lng = position.coords.longitude;

          const url =
            `https://www.google.com/maps/search/?api=1&query=${lat},${lng}`;

          window.open(url, "_blank");

          locationBtn.innerText = "Use My Location";
        },

        () => {
          alert("Unable to access your location.");
          locationBtn.innerText = "Use My Location";
        }
      );

    });

  }

  /* ========================
     Nearby Search Helpers
  ======================== */
  const quickSearch = {
    gold: "gold shop near me",
    broker: "stock broker near me",
    bank: "bank near me",
    atm: "ATM near me",
    exchange: "currency exchange near me",
    insurance: "insurance office near me"
  };

  /* Example Usage:
     openMaps(quickSearch.gold);
  */

});