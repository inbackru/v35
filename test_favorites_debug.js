// Debugging script for favorites system
console.log('=== FAVORITES DEBUG ===');

// Test 1: Check if user is authenticated
const authCheck = document.querySelector('a[href*="dashboard"]') || document.querySelector('.user-authenticated');
console.log('User authenticated:', authCheck !== null);

// Test 2: Check if favorites.js is loaded
console.log('FavoritesManager available:', typeof window.FavoritesManager !== 'undefined');

// Test 3: Check if favoritesManager instance exists
console.log('favoritesManager instance:', typeof window.favoritesManager !== 'undefined');

// Test 4: Test API call directly
function testFavoritesAPI() {
    console.log('Testing favorites API...');
    
    fetch('/api/favorites/toggle', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            property_id: 'debug-test-1',
            property_name: 'Debug Test Property',
            property_type: '1-комн',
            property_size: 50,
            property_price: 3000000,
            complex_name: 'Debug Complex',
            developer_name: 'Debug Developer',
            cashback_amount: 150000,
            cashback_percent: 5.0
        })
    })
    .then(response => {
        console.log('API Response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('API Response data:', data);
    })
    .catch(error => {
        console.error('API Error:', error);
    });
}

// Test 5: Check existing heart elements
const hearts = document.querySelectorAll('.favorite-heart');
console.log('Heart elements found:', hearts.length);

// Add test button to page
if (hearts.length > 0) {
    const testBtn = document.createElement('button');
    testBtn.textContent = 'Тест избранного';
    testBtn.style.cssText = 'position: fixed; top: 10px; right: 10px; z-index: 9999; background: red; color: white; padding: 10px; border: none; cursor: pointer;';
    testBtn.onclick = testFavoritesAPI;
    document.body.appendChild(testBtn);
}

console.log('=== END DEBUG ===');