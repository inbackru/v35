
// Clear existing comparisons and add test data
localStorage.setItem('comparisons', JSON.stringify(['1', '2', '3']));
console.log('Test comparison data added:', localStorage.getItem('comparisons'));

// Force reload comparison content
if (typeof loadComparisonContent === 'function') {
    loadComparisonContent();
    console.log('Comparison content reloaded');
}
