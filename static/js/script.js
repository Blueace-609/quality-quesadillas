
window.setInterval(changeSlide, 5000);

let currentSlide = 1;
function changeSlide() {
  let slides = document.querySelectorAll(".slide");
  let lastSlide = currentSlide-1

  if (currentSlide >= slides.length) {
    currentSlide = 0;
  }
  if(lastSlide > -1){
    slides[lastSlide].classList.toggle("show");
  }
  slides[currentSlide].classList.toggle("show");

 currentSlide++;
}

const fileInput = document.getElementById('file-input');
const uploadedImage = document.getElementById('uploaded-image');
const predictButton = document.getElementById('predict-button');

fileInput.addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            uploadedImage.src = e.target.result;
            uploadedImage.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
});

predictButton.addEventListener('click', function () {
});