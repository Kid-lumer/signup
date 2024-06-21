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
function confirmRemove() {
    return confirm("Are you sure you want to remove the selected items from the cart?");
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
    document.addEventListener('DOMContentLoaded', function() {
        const quantitySelectors = document.querySelectorAll('.quantity-selector select');
        
        quantitySelectors.forEach(selector => {
            selector.addEventListener('change', function() {
                const itemId = this.closest('form').querySelector('input[name="id"]').value;
                const newQuantity = this.value;
                updateCart(itemId, newQuantity);
            });
        });
    });
    
    function updateCart(itemId, newQuantity) {
        fetch('/update_quantity', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrf_token') // Ensure CSRF token is included if your framework requires it
            },
            body: JSON.stringify({
                id: itemId,
                quantity: newQuantity
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateUI(itemId, data.item_price, data.total_price);
            } else {
                alert('Error updating cart');
            }
        })
        .catch(error => console.error('Error:', error));
    }
    
    function updateUI(itemId, itemPrice, totalPrice) {
        // Update the item price in the UI
        const itemRow = document.querySelector(`tr[data-id="${itemId}"]`);
        itemRow.querySelector('.item-price').textContent = `R${itemPrice.toFixed(2)}`;
        
        // Update the total price in the UI
        document.getElementById('total_price').textContent = `R${totalPrice.toFixed(2)}`;
    }
    
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    
    