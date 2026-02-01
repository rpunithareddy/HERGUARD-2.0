const BASE_URL = "http://127.0.0.1:5000";
setInterval(() => {
  const now = new Date();
  document.getElementById("currentTime").innerText =
    now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}, 1000);

let sosTimer;

const sosBtn = document.getElementById("sosBtn");
const floatingSos = document.getElementById("floatingSos");
const sosModal = document.getElementById("sosModal");

function triggerSOS() {
  sosModal.classList.remove("hidden");

  navigator.geolocation.getCurrentPosition(pos => {
    fetch(`${BASE_URL}/sos`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        latitude: pos.coords.latitude,
        longitude: pos.coords.longitude
      })
    });
  });
}

sosBtn.addEventListener("mousedown", () => {
  sosTimer = setTimeout(triggerSOS, 3000);
});

sosBtn.addEventListener("mouseup", () => clearTimeout(sosTimer));
floatingSos.addEventListener("click", triggerSOS);

function cancelSOS() {
  sosModal.classList.add("hidden");
}

function shareLocation() {
  navigator.geolocation.getCurrentPosition(pos => {
    fetch(`${BASE_URL}/share-location`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        latitude: pos.coords.latitude,
        longitude: pos.coords.longitude
      })
    }).then(() => alert("Location shared successfully"));
  });
}

function triggerFakeCall() {
  document.getElementById("fakeCallModal").classList.remove("hidden");
}

function closeFakeCall() {
  document.getElementById("fakeCallModal").classList.add("hidden");
}
function showHelplines() {
  alert("Women Helpline: 1091\nEmergency: 112");
}
function safeRoute() {
  alert("Safe route feature coming soon");
}