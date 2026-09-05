const question = document.getElementById('question');
const message = document.getElementById('message');
const yesBtn = document.getElementById('yesBtn');
const noBtn = document.getElementById('noBtn');
const datePickerWrap = document.getElementById('datePickerWrap');
const dateInput = document.getElementById('dateInput');
const confirmDateBtn = document.getElementById('confirmDateBtn');
const mainImage = document.getElementById("mainImage");

const celebration = document.getElementById("celebration");
const card = document.getElementById("card");
const celebrationGif = document.getElementById("celebrationGif");


const noScenes = [
    {
        text: "Think again muffin...",
        image: "images/Please-8.jpg"
    },
    {
        text: "Are you really sure muffin?",
        image: "images/Please-2.jpg"
    },
    {
        text: "I even planned the restaurant muffin 🥺",
        image: "images/Please-3.jpg"
    },
    {
        text: "I'll let you steal ice cream muffin.",
        image: "images/Please-4.jpg"
    },
    {
        text: "I'll pay 70 percent muffin😌",
        image: "images/Please-5.jpg"
    },
    {
        text: "Pleaseeeee muffin?",
        image: "images/Please-6.jpg"
    },
    {
        text: "Last chance muffin...",
        image: "images/Please-7.jpg"
    },
    {
        text: "Guess what i'm not giving up muffin 😤",
        image: "images/Please-9.jpg"
    },
    {
        text: "Okay your choice of place muffin.",
        image: "images/Please-10.jpg"
    }
];

// Preload all images
const imagesToPreload = [
    "images/happy.jpg",
    "images/dance.gif",
    ...noScenes.map(scene => scene.image)
];

imagesToPreload.forEach(src => {
    const img = new Image();
    img.src = src;
});

let noStep = 0;
let dateChosen = false;

function showDatePicker() {
  datePickerWrap.classList.remove('hidden');
  question.textContent = 'Yay! Pick the date for our dinner.';
  message.textContent = 'Your date is almost confirmed!';
  mainImage.src = "images/happy.jpg";
  console.log(mainImage.src);
}


function handleNo() {

    const current = noScenes[noStep % noScenes.length];

    question.textContent = current.text;
    mainImage.src = current.image;

    noStep++;

}

yesBtn.addEventListener('click', () => {
  showDatePicker();
});

noBtn.addEventListener('click', () => {
  handleNo();
});


confirmDateBtn.addEventListener("click", () => {

    if (!dateInput.value) {
        message.textContent = "Please choose a date first.";
        return;
    }

    // Hide the card
    card.style.display = "none";

    // Load the GIF only now
    celebrationGif.src = "images/dance.gif";

    // Show celebration screen
    celebration.classList.remove("hidden");

});