document.addEventListener("DOMContentLoaded", function () {
  loadSymptoms();

  document
    .querySelector(".dropdown-select")
    .addEventListener("click", toggleDropdown);
  document.querySelector("#diagnose-btn").addEventListener("click", diagnose);
});

function loadSymptoms() {
  fetch("/getsymptoms")
    .then((response) => response.json())
    .then((data) => {
      const dropdownOptions = document.getElementById("dropdown-options");
      data.forEach((item) => {
        const option = document.createElement("div");
        option.classList.add("dropdown-item");
        option.setAttribute("data-english", item.english);
        option.textContent = item.spanish;
        option.addEventListener("click", selectSymptom);
        dropdownOptions.appendChild(option);
      });
    });
}

function toggleDropdown() {
  document.getElementById("dropdown-options").classList.toggle("show");
}

function selectSymptom(event) {
  const selectedSymptoms = document.getElementById("symptoms-list");
  const symptom = event.target;
  const span = document.createElement("span");
  span.classList.add("selected-symptom");
  span.setAttribute("data-english", symptom.getAttribute("data-english"));
  span.textContent = symptom.textContent;
  selectedSymptoms.appendChild(span);

  symptom.removeEventListener("click", selectSymptom);
}

function diagnose() {
  const selectedSymptoms = document.querySelectorAll(".selected-symptom");
  const symptoms = Array.from(selectedSymptoms).map((symptom) =>
    symptom.getAttribute("data-english")
  );

  fetch("/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ symptoms: symptoms }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
    });
}
