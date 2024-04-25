document.addEventListener("DOMContentLoaded", function() {
    const modal = document.getElementById('modal');
    const addToCartBtns = document.querySelectorAll('.add-to-cart-btn');
    const categoriesList = document.getElementById('categories-list');
    const priceRangeSelect = document.getElementById('price-range');
    const sortBtn = document.getElementById('sort-btn');
    let products = Array.from(document.querySelectorAll('.product'));
  
    // Filter, render products, and sort functions as before
  
    // Event listener for Add to Cart button
    addToCartBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const productDiv = btn.parentElement;
        const productName = productDiv.querySelector('h2').textContent;
        const productPrice = parseFloat(productDiv.dataset.price);
        alert(`Added "${productName}" to cart. Price: $${productPrice}`);
        // Add your cart logic here, such as updating the cart UI or sending data to a server
      });
    });
  
    // Event listeners for prescription upload, modal, and confirmation as before
  });
  