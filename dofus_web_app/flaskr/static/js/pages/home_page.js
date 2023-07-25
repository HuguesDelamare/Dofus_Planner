document.addEventListener("DOMContentLoaded", function() {
    // Fetch the data from the server
    fetch('/fetch_almanax_data')
      .then(response => response.json())
      .then(data => {
        // Update the webpage with the fetched data
        // You can use this data in your HTML and render it using Jinja
        console.log(data);
      });
  });
  