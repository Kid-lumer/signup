let cartOpen = false;

function toggleCart() {
    const cartDropdown = document.getElementById('cartDropdown');
    cartOpen = !cartOpen;
    if (cartOpen) {
        cartDropdown.style.display = 'block';
    } else {
        cartDropdown.style.display = 'none';
    }
}

// Example function to update cart count
function updateCartCount(count) {
    const cartCount = document.querySelector('#cartCount');
    cartCount.textContent = count;
}

let cartCount = 0;

function addToCart() {
    cartCount++;
    updateCartCount(cartCount);
}

function updateCartCount(count) {
    document.getElementById('cartCount').innerText = count;
}
