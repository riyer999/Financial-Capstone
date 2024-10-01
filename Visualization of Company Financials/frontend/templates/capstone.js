    // Display image
    const imageDiv = document.getElementById('image');
    imageDiv.innerHTML = ''; // Clear previous image
    const image = document.createElement('img');
    image.src = questions[questionIndex].image;
    imageDiv.appendChild(image);