// Function to fetch suggestions from the server
function fetchSuggestions(query) {
  return fetch(`/suggest?query=${encodeURIComponent(query)}`)
      .then(response => response.json())
      .then(data => {
          console.log('Suggestions:', data);
          return data.suggestions;
      })
      .catch(error => {
          console.log('Error:', error);
      });
}

// Fetch the whole item from the database based on the suggestion
function fetchItemDetails(suggestion) {
  return fetch(`/search?name=${encodeURIComponent(suggestion)}`)
      .then(response => response.json())
      .then(data => {
          console.log('Search Results:', data)
          suggestionsContainer.innerHTML = '';
          searchInput.value = '';
          return data;
      })
      .catch(error => {
          console.log('Error:', error);
      });
}

// After the item is fetched, update and populate the table with the different components from the recipe list
function updateSearchResults(data) {
  // Clear the table and title from past searches
  tableBody.innerHTML = '';
  titleCraftItem.innerHTML = '';

  // Populate the table with the new data
  for (const item of data) {
      if (item.item_recipe) {
          // Create a table row for each recipe item
          for (const recipe of item.item_recipe) {
              console.log(recipe);
              // Create a table row
              const tableRow = document.createElement('tr');

              // Create a table cell for the IMAGE recipe item
              const recipeImageCell = document.createElement('td');
              const recipeImage = document.createElement('img');
              recipeImage.src = `data:image/png;base64,${recipe.ingredients_image}`;
              recipeImageCell.appendChild(recipeImage);
              tableRow.appendChild(recipeImageCell);

              // Create a table cell for the NAME recipe item
              const recipeNameCell = document.createElement('td');
              recipeNameCell.textContent = recipe.ingredients_name;
              tableRow.appendChild(recipeNameCell);

              // Create a table cell for the QUANTITY recipe item
              const recipeQuantityCell = document.createElement('td');
              recipeQuantityCell.textContent = recipe.ingredients_quantity;
              tableRow.appendChild(recipeQuantityCell);

              // Create a table cell for the PRICE recipe item
              const inputPriceCell = document.createElement('td');
              const inputPrice = document.createElement("input");
              inputPrice.setAttribute("type", "number");
              inputPrice.setAttribute("maxlength", "7");
              inputPrice.setAttribute("pattern", "[0-9]{1,7}");
              inputPriceCell.appendChild(inputPrice);
              tableRow.appendChild(inputPriceCell);

              // Create a table cell for the TOTAL recipe item
              const inputTotalCell = document.createElement('td');
              inputTotalCell.textContent = ''
              tableRow.appendChild(inputTotalCell);

              // Append the table row to the table body
              tableBody.appendChild(tableRow);
          }
      }
      
      // Create a link for the item name
      const a = document.createElement('a');
      a.href = `https://www.dofus.com/fr/mmorpg/encyclopedie/equipements/${item.item_id_dofus}`;
      a.textContent = item.item_name;
      titleCraftItem.appendChild(a);
  }
}

// Handle the search input
function handleSearchInput() {
  const query = searchInput.value;
  if (query.length > 0) {
      // Display the suggestions div and populate it with the suggestions
      fetchSuggestions(query)
          .then(suggestions => {
              suggestionsContainer.style.display = 'block';
              suggestionsContainer.innerHTML = '';
              // Create a div for each suggestion
              for (const suggestion of suggestions) {
                  const suggestionElement = document.createElement('div');
                  suggestionElement.textContent = suggestion;
                  suggestionElement.addEventListener('click', function() {
                      // Fetch the item details based on the suggestion by clicking on it
                      fetchItemDetails(suggestion)
                          .then(data => {
                              craftingContainer.classList.add('show');
                              suggestionsContainer.style.display = 'none';
                              updateSearchResults(data);
                          });
                  });
                  suggestionsContainer.appendChild(suggestionElement);
              }
          });
  } else {
      suggestionsContainer.innerHTML = '';
  }
}

// Call view to insert the data from the JSON to Database
function insertJsonData() {
  fetch('/insert-data', {
      method: 'POST'
  })
      .then(response => {
          console.log(response);
      })
      .catch(error => {
          console.log('Error:', error);
      });
}

// Calculate the total price of each recipe item
function calculateTotalPrice() {
  const tableRows = document.querySelectorAll('#crafting-table tbody tr');

  // For each row, get the price & total & quantity cells
  tableRows.forEach(row => {
      const priceInput = row.querySelector('td:nth-child(3) input');
      const totalCell = row.querySelector('td:nth-child(4)');
      const quantity = parseInt(row.querySelector('td:nth-child(2)').textContent);

      // Update the total cell when the price input changes
      priceInput.addEventListener('input', function() {
          const price = parseFloat(this.value);
          const total = isNaN(price) ? 0 : (price * quantity).toFixed(0);
          totalCell.textContent = parseInt(total);
          // Call the function to update the total cost input
          updateTotalCost();
          updateProfit();
      });
  });
}

// Update the total cost input
function updateTotalCost() {
  const totalCells = document.querySelectorAll('#crafting-table tbody tr td:nth-child(4)');
  let totalCost = 0;

  // For each total cell, get the total and add it to the total cost
  totalCells.forEach(cell => {
      // Get the total from the cell
      const total = parseInt(cell.textContent);
      if (!isNaN(total)) {
          totalCost += total;
      }
  });

  // Update the total cost input
  const totalCostCell = document.getElementById('total-cost');
  totalCostCell.value = totalCost;

  // Call the function to update the profit input
  updateProfit();
}

// Calculate the profit input
function updateProfit() {
  // Get the profit input, item price input, total cost input, label profit
  const profitInput = document.getElementById('profit');
  const itemPrice = parseFloat(document.getElementById('item-price-input').value);
  const totalCost = parseFloat(document.getElementById('total-cost').value);
  const labelProfit = document.getElementById('label-profit');

  const profit = ((itemPrice - totalCost) * 0.98);

  // Update the profit input
  if (profit > 0) {
      profitInput.value = profit.toFixed(0) + '';
      labelProfit.textContent = 'Profit';
      profitInput.style.color = 'green';
      labelProfit.style.color = 'green';
  } else if (profit < 0) {
      profitInput.value = profit.toFixed(0) + '';
      labelProfit.textContent = 'Loss';
      profitInput.style.color = 'red';
      labelProfit.style.color = 'red';
  } else {
      profitInput.value = 'No profit';
      profitInput.style.color = 'black';
  }
}

// Get the elements from the DOM
const searchInput = document.getElementById('search-input');
const suggestionsContainer = document.getElementById('suggestions');
const tableBody = document.querySelector('tbody');
const titleCraftItem = document.getElementById('crafted-item-title');
const insertDataButton = document.getElementById('insert-data-button');
const itemPriceInput = document.getElementById('item-price-input');
const craftingContainer = document.getElementById('crafting-container');

// Event listeners
searchInput.addEventListener('input', handleSearchInput);
insertDataButton.addEventListener('click', insertJsonData);
tableBody.addEventListener('input', calculateTotalPrice);
itemPriceInput.addEventListener('input', updateProfit);