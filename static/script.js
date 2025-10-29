const uploadForm = document.getElementById("uploadForm");
const imageInput = document.getElementById("imageInput");
const originalImg = document.getElementById("originalImg");
const processedImg = document.getElementById("processedImg");
const spinner = document.getElementById("spinner");

const kInput = document.getElementById("kInput");
const sInput = document.getElementById("sInput");
const kValue = document.getElementById("kValue");
const sValue = document.getElementById("sValue");
const incK = document.getElementById("incK");
const decK = document.getElementById("decK");
const incS = document.getElementById("incS");
const decS = document.getElementById("decS");

// Slider display updates
kInput.addEventListener("input", () => (kValue.textContent = kInput.value));
sInput.addEventListener("input", () => (sValue.textContent = sInput.value));

// Increment and decrement logic
incK.addEventListener("click", () => {
  if (parseInt(kInput.value) < parseInt(kInput.max)) {
    kInput.value = parseInt(kInput.value) + 1;
    kValue.textContent = kInput.value;
  }
});

decK.addEventListener("click", () => {
  if (parseInt(kInput.value) > parseInt(kInput.min)) {
    kInput.value = parseInt(kInput.value) - 1;
    kValue.textContent = kInput.value;
  }
});

incS.addEventListener("click", () => {
  if (parseInt(sInput.value) < parseInt(sInput.max)) {
    sInput.value = parseInt(sInput.value) + 1;
    sValue.textContent = sInput.value;
  }
});

decS.addEventListener("click", () => {
  if (parseInt(sInput.value) > parseInt(sInput.min)) {
    sInput.value = parseInt(sInput.value) - 1;
    sValue.textContent = sInput.value;
  }
});

// Preview the original image
imageInput.addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (file) {
    originalImg.src = URL.createObjectURL(file);
  }
});

// Upload and process image
uploadForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(uploadForm);

  spinner.classList.add("active"); // show spinner

  try {
    const response = await fetch("/compress", {
      method: "POST",
      body: formData
    });
    const blob = await response.blob();
    processedImg.src = URL.createObjectURL(blob);
  } catch (err) {
    alert("Error processing image!");
    console.error(err);
  } finally {
    spinner.classList.remove("active"); // hide spinner
  }
});


// Zoom feature
document.querySelectorAll(".preview img").forEach(img => {
  img.addEventListener("click", () => zoomImage(img.src));
});

function zoomImage(src) {
  let modal = document.getElementById("zoomModal");
  if (!modal) {
    modal = document.createElement("div");
    modal.id = "zoomModal";
    modal.innerHTML = `<img src="${src}" alt="Zoomed image">`;
    document.body.appendChild(modal);
  } else {
    modal.querySelector("img").src = src;
  }

  modal.classList.add("show");
  modal.addEventListener("click", () => modal.classList.remove("show"));
}
