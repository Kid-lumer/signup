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

    // Function to show confirmation dialog
 function confirmRemoval(event) {
        event.preventDefault(); // Prevent the form from submitting immediately
        const userConfirmed = confirm("Are you sure you want to remove this item from your cart?");
        if (userConfirmed) {
            event.target.closest('form').submit(); // Submit the form if the user confirmed
        }
    }
