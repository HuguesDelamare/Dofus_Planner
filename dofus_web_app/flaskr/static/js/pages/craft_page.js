console.log('Craft Page JS Loaded...')
    
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


// Function to fetch the whole item from the database
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


// Function to update the DOM with search results
function updateSearchResults(data) {
    tableBody.innerHTML = '';
    titleCraftItem.innerHTML = '';

    for (const item of data) {
        if (item.item_recipe) {
        for (const recipe of item.item_recipe) {
            const tableRow = document.createElement('tr');
            const recipeNameCell = document.createElement('td');
            recipeNameCell.textContent = recipe.ingredients_name;
            tableRow.appendChild(recipeNameCell);

            const recipeQuantityCell = document.createElement('td');
            recipeQuantityCell.textContent = recipe.ingredients_quantity;
            tableRow.appendChild(recipeQuantityCell);

            const inputPriceCell = document.createElement('td');
            const inputPrice = document.createElement("input");
            inputPrice.setAttribute("type", "number");
            inputPriceCell.appendChild(inputPrice);
            tableRow.appendChild(inputPriceCell);

            const inputTotalCell = document.createElement('td');
            inputTotalCell.textContent = ''
            tableRow.appendChild(inputTotalCell);

            tableBody.appendChild(tableRow);
        }
        }
        titleCraftItem.innerHTML = item.item_name;
    }
}


// Event listener function for search input
function handleSearchInput() {
    const query = searchInput.value;

    if (query.length > 0) {
    fetchSuggestions(query)
        .then(suggestions => {
        suggestionsContainer.style.display = 'block';
        suggestionsContainer.innerHTML = '';
        for (const suggestion of suggestions) {
            const suggestionElement = document.createElement('div');
            suggestionElement.textContent = suggestion;
            suggestionElement.addEventListener('click', function() {
            fetchItemDetails(suggestion)
                .then(data => {
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


function insertJsonData() {
    fetch('/insert-data', {
    method: 'POST'
    })
    .then(response => {
    console.log(response)
    })
    .catch(error => {
    console.log('Error:', error)
    })
}

    
function calculateTotalPrice() {
  const tableRows = document.querySelectorAll('#crafting-table tbody tr');

  tableRows.forEach(row => {
    const priceInput = row.querySelector('td:nth-child(3) input');
    const totalCell = row.querySelector('td:nth-child(4)');
    const quantity = parseInt(row.querySelector('td:nth-child(2)').textContent);

    priceInput.addEventListener('input', function() {
      const price = parseFloat(this.value);
      const total = isNaN(price) ? '' : (price * quantity).toFixed(0);
      totalCell.textContent = parseInt(total);
      updateTotalCost();
    });
  });
}
  
function updateTotalCost() {
  const totalCells = document.querySelectorAll('#crafting-table tbody tr td:nth-child(4)');
  let totalCost = 0;
  totalCells.forEach(cell => {
    const total = parseInt(cell.textContent);
    if (!isNaN(total)) {
      totalCost += total;
    }
  });
  const totalCostCell = document.getElementById('total-cost');
  totalCostCell.value = totalCost;
  profitCalculation();
}
  
function profitCalculation() {
  const profitInput = document.getElementById('profit');
  const itemPrice = parseFloat(document.getElementById('item-price-input').value);
  const totalCost = parseFloat(document.getElementById('total-cost').value);
  const labelProfit = document.getElementById('label-profit');

  console.log('itemPrice:', itemPrice);
  console.log('totalCost:', totalCost);

  const profit = itemPrice - totalCost;
  console.log('profit:', profit);

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

const searchInput = document.getElementById('search-input');
const suggestionsContainer = document.getElementById('suggestions');
const tableBody = document.querySelector('tbody');
const titleCraftItem = document.getElementById('crafted-item-title');
const insertDataButton = document.getElementById('insert-data-button');

searchInput.addEventListener('input', handleSearchInput);
insertDataButton.addEventListener('click', insertJsonData);
tableBody.addEventListener('input', calculateTotalPrice);
