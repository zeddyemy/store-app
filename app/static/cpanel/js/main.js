// Get a reference to the file input and avatar container
const fileInput = document.querySelector('.avatar input[type="file"]');
const avatar = document.querySelector('.avatar img');

// Add an event listener for when the file input changes
fileInput.addEventListener('change', function () {
    // Get the selected file
    const file = this.files[0];

    // Create a new FileReader object
    const reader = new FileReader();

    // Add an event listener for when the file has been loaded
    reader.addEventListener('load', function () {
        // Set the background-image property of the avatar to the data URL of the image
        avatar.src = `${this.result}`;
    });

    // Read the contents of the file as a data URL
    reader.readAsDataURL(file);
});