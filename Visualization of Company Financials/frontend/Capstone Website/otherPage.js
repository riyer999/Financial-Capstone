    // button that returns the user to the homepage
    const homeBtn = document.getElementById('homeBtn');
    homeBtn.addEventListener('click', function() {
        window.location.href = 'homePage.html';
    });

    // Display image
    const imageDiv = document.getElementById('image');
    imageDiv.innerHTML = ''; // Clear previous image
    const image = document.createElement('img');
    image.src = questions[questionIndex].image;
    imageDiv.appendChild(image);