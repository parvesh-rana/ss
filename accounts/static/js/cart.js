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

// Add this function to initialize cart count
function updateCartCount(count) {
    const cartCountElements = document.querySelectorAll('.cart-count');
    cartCountElements.forEach(element => {
        element.textContent = count;
        // Show/hide the badge based on count
        element.style.display = count > 0 ? 'block' : 'none';
    });
}

// Add this function to get initial cart count
function getInitialCartCount() {
    fetch('/cart/count/')  // You'll need to create this endpoint
        .then(response => response.json())
        .then(data => {
            updateCartCount(data.cart_count);
        });
}

// Call this when page loads
document.addEventListener('DOMContentLoaded', getInitialCartCount);

function addToCart(productId, quantity = 1) {
    console.log('Adding to cart:', productId); // Debug log
    fetch('/cart/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: quantity
        })
    })
    .then(response => {
        console.log('Response:', response); // Debug log
        return response.json();
    })
    .then(data => {
        console.log('Data:', data); // Debug log
        if (data.success) {
            updateCartCount(data.cart_count);  // Use the new function
        } else {
            alert('Error: ' + (data.error || 'Could not add product to cart'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error adding product to cart');
    });
}

function updateCartItem(itemId, quantity) {
    fetch('/cart/update/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            item_id: itemId,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload(); // Refresh to update totals
        } else {
            alert('Error updating cart');
        }
    });
} 