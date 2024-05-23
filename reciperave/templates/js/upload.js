document.getElementById('addIngredientButton').addEventListener('click', addIngredientRow);

let rowCount = 1;

function addIngredientRow() {
  rowCount++;
  const container = document.getElementById('ingredientsContainer');
  const newRow = document.createElement('div');
  newRow.className = 'ingredient-row';

  newRow.innerHTML = `
        <label for="amount${rowCount}">Amount</label>
        <input type="number" id="amount${rowCount}" name="amount[]" min="0" step="any" placeholder="e.g., 1.5">
        <label for="ingredient${rowCount}">Ingredient</label>
        <input type="text" id="ingredient${rowCount}" name="ingredient[]" placeholder="e.g., Sugar">
    `;

  container.appendChild(newRow);
}