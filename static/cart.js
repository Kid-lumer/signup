let cartOpen = false;

function toggleCart() {
    const cartDropdown = document.getElementById('cartDropdown');
    cartOpen = !cartOpen;
    if (cartOpen) {
        // Show cart dropdown
        cartDropdown.style.display = 'block';
    } else {
        // Hide cart dropdown
        cartDropdown.style.display = 'none';
    }
}

// Example function to update cart count
function updateCartCount(count) {
    const cartCount = document.querySelector('.cart-count');
    cartCount.textContent = count;
}


let cartCount = 0;

function addToCart() {
  cartCount++;
  updateCartCount();
}

function updateCartCount() {
  document.getElementById('cartCount').innerText = cartCount;
}
