const form = document.getElementById('uploadForm');
const imgInput = document.getElementById('imageInput');
const kInput = document.getElementById('kInput');
const kValue = document.getElementById('kValue');
const sInput = document.getElementById('sInput');
const sValue = document.getElementById('sValue');
const originalImg = document.getElementById('originalImg');
const processedImg = document.getElementById('processedImg');

kInput.addEventListener('input', () => {
  kValue.textContent = kInput.value;
});

sInput.addEventListener('input', () => {
  sValue.textContent = sInput.value;
});

imgInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) {
    originalImg.src = URL.createObjectURL(file);
  }
});

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(form);

  processedImg.style.opacity = 0.5;
  processedImg.src = "";

  const response = await fetch('/compress', { method: 'POST', body: formData });

  if (response.ok) {
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    processedImg.src = url;
    processedImg.onload = () => processedImg.style.opacity = 1;
  } else {
    alert('Error processing image!');
  }
});
