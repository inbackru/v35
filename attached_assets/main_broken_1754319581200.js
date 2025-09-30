// Consolidated JavaScript for ClickBack Real Estate Platform
// Auto-generated from multiple page-specific scripts

// Utility function to safely add event listeners
function safeAddEventListener(selector, event, handler) {
    const element = document.querySelector(selector);
    if (element) {
        element.addEventListener(event, handler);
    }
}

function safeAddEventListenerAll(selector, event, handler) {
    const elements = document.querySelectorAll(selector);
    elements.forEach(element => {
        if (element) {
            element.addEventListener(event, handler);
        }
    });
}

// From script-how-it-works.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
document.addEventListener('DOMContentLoaded', function() {
const priceSlider = document.getElementById('price');
const priceInput = document.getElementById('price-input');
const percentSlider = document.getElementById('percent');
const percentInput = document.getElementById('percent-input');
const calculateBtn = document.getElementById('calculate-btn');
const resultElement = document.getElementById('result');
const resultPrice = document.getElementById('result-price');
const resultPercent = document.getElementById('result-percent');
priceSlider.addEventListener('input', function() {
priceInput.value = this.value;
calculateCashback();
});
priceInput.addEventListener('input', function() {
if (parseInt(this.value) > 50000000) this.value = 50000000;
if (parseInt(this.value) < 1000000) this.value = 1000000;
priceSlider.value = this.value;
calculateCashback();
});
percentSlider.addEventListener('input', function() {
percentInput.value = this.value;
calculateCashback();
});
percentInput.addEventListener('input', function() {
if (parseFloat(this.value) > 5) this.value = 5;
if (parseFloat(this.value) < 1) this.value = 1;
percentSlider.value = this.value;
calculateCashback();
});
calculateBtn.addEventListener('click', calculateCashback);
calculateCashback();
function formatCurrency(num) {
return new Intl.NumberFormat('ru-RU').format(num) + ' ₽';
}
function calculateCashback() {
const price = parseInt(priceInput.value);
const percent = parseFloat(percentInput.value);
const cashback = Math.round(price * percent / 100);
resultElement.textContent = formatCurrency(cashback);
resultPrice.textContent = formatCurrency(price);
resultPercent.textContent = percent.toFixed(1) + '%';
}
});
function toggleFAQ(id) {
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
function toggleDropdown(element) {
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
document.addEventListener('click', function(e) {
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
function toggleFooterMenu(header) {
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
function updateCarousel() {
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
prevBtn.addEventListener('click', () => {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
nextBtn.addEventListener('click', () => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
dot.addEventListener('click', () => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
carousel.addEventListener('mouseenter', () => clearInterval(interval));
carousel.addEventListener('mouseleave', () => {
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
function setupTypewriter() {
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
function tick() {
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
window.addEventListener('load', function() {
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
function toggleMobileMenu() {
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
function toggleSubMenu(id) {
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
function openApplicationModal() {
document.getElementById('applicationModal').classList.remove('hidden');
}
function openLoginModal() {
document.getElementById('loginModal').classList.remove('hidden');
}
function openRegisterModal() {
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
function closeModal(modalId) {
document.getElementById(modalId).classList.add('hidden');
}
function loginUser() {
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
function logoutUser() {
closeModal('accountModal');
}
document.getElementById('toggleFilters').addEventListener('click', function() {
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
function initCarousels() {
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
function nextSlide() {
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
function prevSlide() {
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
function updateDots() {
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
inner.addEventListener('transitionend', () => {
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
carousel.querySelector('.carousel-next').addEventListener('click', () => {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
carousel.querySelector('.carousel-prev').addEventListener('click', () => {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
setupDropdowns();
setupTypewriter();
initCarousels();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
btn.addEventListener('click', function() {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
function updateSelectedFilters() {
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceRange = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');
const downPaymentRange = document.getElementById('downPaymentRange');
const downPaymentValue = document.getElementById('downPaymentValue');
const termRange = document.getElementById('termRange');
const termValue = document.getElementById('termValue');
const cashbackAmount = document.getElementById('cashbackAmount');
const monthlyPayment = document.getElementById('monthlyPayment');
function updateCalculator() {
const price = parseInt(priceRange.value);
const downPayment = parseInt(downPaymentRange.value);
const downPaymentPercent = Math.round((downPayment / price) * 100);
const term = parseInt(termRange.value);
const cashbackPercent = 2.5;
priceValue.textContent = new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
downPaymentValue.textContent = new Intl.NumberFormat('ru-RU').format(downPayment) + ' ₽ (' + downPaymentPercent + '%)';
termValue.textContent = term + ' лет';
const cashback = price * cashbackPercent / 100;
cashbackAmount.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(cashback)) + ' ₽';
const loanAmount = price - downPayment;
const monthlyRate = 0.06 / 12;
const payments = term * 12;
const monthly = loanAmount * monthlyRate * Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
monthlyPayment.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(monthly)) + ' ₽';
}
priceRange.addEventListener('input', updateCalculator);
downPaymentRange.addEventListener('input', updateCalculator);
termRange.addEventListener('input', updateCalculator);
cashbackRange.addEventListener('input', updateCalculator);
updateCalculator();
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
prev.addEventListener('click', () => {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
next.addEventListener('click', () => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
modal.addEventListener('click', function(e) {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});

// From script-ipoteka.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const priceInput = document.getElementById('price-input');
const priceSlider = document.getElementById('price');
const initialInput = document.getElementById('initial-input');
const initialSlider = document.getElementById('initial');
const termInput = document.getElementById('term-input');
const termSlider = document.getElementById('term');
const rateSelect = document.getElementById('rate');
const insuranceCheck = document.getElementById('insurance');
const cashbackCheck = document.getElementById('cashback-check');
const creditSumEl = document.getElementById('credit-sum');
const downpaymentResultEl = document.getElementById('downpayment-result');
const monthlyPaymentEl = document.getElementById('monthly-payment');
const overpaymentEl = document.getElementById('overpayment');
const rateResultEl = document.getElementById('rate-result');
const cashbackEl = document.getElementById('cashback');
const selectedYearsEl = document.getElementById('selected-years');
const progressBar = document.getElementById('progress-bar');
function styleRangeInput(input) {
const value = (input.value - input.min) / (input.max - input.min) * 100;
input.style.background = `
linear-gradient(to right,
var(--thumb-color, #0088cc) 0%,
var(--thumb-color, #0088cc) ${value}%,
var(--track-color, #e5e7eb) ${value}%,
var(--track-color, #e5e7eb) 100%)
`;
}
const programLimits = {
'Базовая ипотека - 14.99%': { maxLoan: Infinity },
'Семейная ипотека - 6%': { maxLoan: 6000000 },
'IT ипотека - 6%': { maxLoan: 9000000 },
'Сельская ипотека - 3%': { maxLoan: 6000000 }
};
function formatPrice(value) {
return new Intl.NumberFormat('ru-RU').format(value);
}
function parsePrice(value) {
return parseInt(value.replace(/\s/g, ''));
}
function formatPercent(value) {
return value;
}
function connectInputAndSlider(input, slider, isPrice) {
input.addEventListener('input', function() {
let value = input.value;
if (isPrice) value = parsePrice(value);
if (!isNaN(value)) {
slider.value = value;
styleRangeInput(slider);
updateCalculator();
}
});
slider.addEventListener('input', function() {
input.value = isPrice ? formatPrice(slider.value) : slider.value;
styleRangeInput(this);
updateCalculator();
});
styleRangeInput(slider);
}
connectInputAndSlider(priceInput, priceSlider, true);
connectInputAndSlider(initialInput, initialSlider, false);
connectInputAndSlider(termInput, termSlider, false);
function calculateDownPayment(price, initialPercent, programType) {
let downPayment;
if (programType.includes('Семейная')) {
const maxLoan = 6000000;
downPayment = Math.max(price * initialPercent / 100, price - maxLoan);
}
else if (programType.includes('IT')) {
const maxLoan = 9000000;
downPayment = Math.max(price * initialPercent / 100, price - maxLoan);
}
else {
downPayment = price * initialPercent / 100;
}
return downPayment;
}
document.querySelectorAll('input[type="range"]').forEach(styleRangeInput);
try {
const price = parsePrice(priceInput.value) || 8000000;
const initialPercent = parseInt(initialSlider.value) || 15;
const termYears = parseInt(termSlider.value) || 15;
const selectedOption = rateSelect.options[rateSelect.selectedIndex].text;
let rate = parseFloat(rateSelect.value) || 14.99;
if (insuranceCheck.checked) {
rate = Math.max(0.1, rate - 0.5);
}
let downPayment;
let loanAmount;
if (selectedOption.includes('Семейная')) {
const maxLoan = 6000000;
downPayment = Math.max(price * initialPercent / 100, price - maxLoan);
}
else if (selectedOption.includes('IT')) {
const maxLoan = 9000000;
downPayment = Math.max(price * initialPercent / 100, price - maxLoan);
}
else {
downPayment = price * initialPercent / 100;
}
loanAmount = price - downPayment;
const monthlyRate = rate / 100 / 12;
const payments = termYears * 12;
const monthlyPayment = loanAmount * monthlyRate *
Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
const totalPayment = monthlyPayment * payments;
const totalOverpayment = totalPayment - loanAmount;
const cashback = cashbackCheck.checked ? price * 0.02 : 0;
document.getElementById('downpayment-result').textContent = formatPrice(Math.round(downPayment)) + ' ₽';
creditSumEl.textContent = formatPrice(Math.round(loanAmount)) + ' ₽';
document.getElementById('initial-sum').textContent = formatPrice(Math.round(downPayment)) + ' ₽';
document.getElementById('downpayment-amount').textContent = formatPrice(Math.round(downPayment)) + ' ₽';
monthlyPaymentEl.textContent = formatPrice(Math.round(monthlyPayment)) + ' ₽';
overpaymentEl.textContent = formatPrice(Math.round(totalOverpayment)) + ' ₽';
document.getElementById('rate-result').textContent = rate.toFixed(2) + '%';
cashbackEl.textContent = formatPrice(Math.round(cashback)) + ' ₽';
selectedYearsEl.textContent = termYears;
progressBar.style.width = `${(termYears / 30) * 100}%`;
} catch (error) {
console.error("Error in calculator:", error);
}
}
[
priceSlider, priceInput,
initialSlider, initialInput,
termSlider, termInput,
rateSelect, insuranceCheck, cashbackCheck
].forEach(el => {
el.addEventListener('input', updateCalculator);
el.addEventListener('change', updateCalculator);
});
updateCalculator();
const style = document.createElement('style');
style.textContent = `
input[type="range"] {
-webkit-appearance: none;
height: 6px;
background: var(--track-color, #e5e7eb);
border-radius: 3px;
}
input[type="range"]::-webkit-slider-thumb {
-webkit-appearance: none;
width: 18px;
height: 18px;
border-radius: 50%;
background: var(--thumb-color, #0088cc);
cursor: pointer;
box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
input[type="range"]::-moz-range-thumb {
width: 18px;
height: 18px;
border-radius: 50%;
background: var(--thumb-color, #0088cc);
cursor: pointer;
box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
`;
document.head.appendChild(style);
});
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
function updateActiveFiltersCount() {
const activeCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
const activeSelects = Array.from(document.querySelectorAll('select'))
.filter(select => select.value !== '');
const activeTextInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'))
.filter(input => input.value !== '');
const totalFilters = activeCheckboxes.length + activeSelects.length + activeTextInputs.length;
const badge = document.getElementById('activeFilterBadge');
if (totalFilters > 0) {
badge.textContent = totalFilters;
badge.classList.remove('hidden');
} else {
badge.classList.add('hidden');
}
}
document.querySelectorAll('input[type="checkbox"], select, input[type="text"], input[type="number"]').forEach(element => {
element.addEventListener('change', updateActiveFiltersCount);
element.addEventListener('input', updateActiveFiltersCount);
});
setupDropdowns();
setupTypewriter();
initCarousels();
updateActiveFiltersCount();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceInput = document.getElementById('price-input');
const priceSlider = document.getElementById('price');
const initialInput = document.getElementById('initial-input');
const initialSlider = document.getElementById('initial');
const termInput = document.getElementById('term-input');
const termSlider = document.getElementById('term');
const rateSelect = document.getElementById('rate');
const creditSumEl = document.getElementById('credit-sum');
const monthlyPaymentEl = document.getElementById('monthly-payment');
const overpaymentEl = document.getElementById('overpayment');
const cashbackEl = document.getElementById('cashback');
const cashbackCheckbox = document.querySelector('input[name="cashback"]');
let value = input.value.replace(/\s/g, '');
if (!isNaN(value)) {
slider.value = value;
updateCalculator();
}
});
input.value = formatFn(slider.value);
updateCalculator();
});
}
return parseInt(value).toLocaleString('ru-RU');
}
return value;
}
connectInputAndSlider(priceInput, priceSlider, formatPrice);
connectInputAndSlider(initialInput, initialSlider, formatPercent);
connectInputAndSlider(termInput, termSlider, formatPercent);
const price = parseInt(priceInput.value.replace(/\s/g, '')) || 5000000;
const initialPercent = parseInt(initialSlider.value) || 15;
const termYears = parseInt(termSlider.value) || 15;
const ratePercent = parseFloat(rateSelect.value) || 14.99;
const cashbackPercentage = 2;
let loanAmount;
const programType = rateSelect.options[rateSelect.selectedIndex].text;
if (programType.includes('Семейная') || programType.includes('Сельская')) {
const maxLoan = 6000000;
const requiredDownPayment = Math.max(0, price - maxLoan);
const calculatedDownPayment = price * initialPercent / 100;
const effectiveDownPayment = Math.max(requiredDownPayment, calculatedDownPayment);
loanAmount = price - effectiveDownPayment;
if (calculatedDownPayment < requiredDownPayment) {
initialInput.classList.add('border-red-500');
} else {
initialInput.classList.remove('border-red-500');
}
}
else if (programType.includes('IT')) {
const maxLoan = 9000000;
const requiredDownPayment = Math.max(0, price - maxLoan);
const calculatedDownPayment = price * initialPercent / 100;
const effectiveDownPayment = Math.max(requiredDownPayment, calculatedDownPayment);
loanAmount = price - effectiveDownPayment;
if (calculatedDownPayment < requiredDownPayment) {
initialInput.classList.add('border-red-500');
} else {
initialInput.classList.remove('border-red-500');
}
}
else {
loanAmount = price * (100 - initialPercent) / 100;
initialInput.classList.remove('border-red-500');
}
const monthlyRate = ratePercent / 100 / 12;
const payments = termYears * 12;
const monthlyPayment = loanAmount * monthlyRate *
Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
const totalPayment = monthlyPayment * payments;
const totalOverpayment = totalPayment - loanAmount;
let cashback = 0;
if (cashbackCheckbox.checked) {
cashback = price * cashbackPercentage / 100;
}
creditSumEl.textContent = formatPrice(Math.round(loanAmount)) + ' ₽';
monthlyPaymentEl.textContent = formatPrice(Math.round(monthlyPayment)) + ' ₽';
overpaymentEl.textContent = formatPrice(Math.round(totalOverpayment)) + ' ₽';
cashbackEl.textContent = formatPrice(Math.round(cashback)) + ' ₽';
}
[priceSlider, initialSlider, termSlider, rateSelect, cashbackCheckbox].forEach(el => {
});
updateCalculator();
});
function increaseDownPayment() {
const initialInput = document.getElementById('initial-input');
const initialSlider = document.getElementById('initial');
const currentValue = parseInt(initialInput.value) || 0;
const price = parseInt(document.getElementById('price-input').value.replace(/\s/g, '')) || 8000000;
const programType = document.getElementById('rate').options[document.getElementById('rate').selectedIndex].text;
let newValue = currentValue + 1;
let maxValue = 40;
if (programType.includes('Семейная') || programType.includes('Сельская')) {
maxValue = Math.min(40, Math.max(100 - (6000000 / price) * 100, 0));
} else if (programType.includes('IT')) {
maxValue = Math.min(40, Math.max(100 - (9000000 / price) * 100, 0));
}
if (newValue > maxValue) {
newValue = maxValue;
}
if (newValue <= maxValue) {
initialInput.value = newValue;
initialSlider.value = newValue;
document.querySelector('input[name="initial-percent"]').value = newValue;
updateCalculator();
}
}
function decreaseDownPayment() {
const initialInput = document.getElementById('initial-input');
const currentValue = parseInt(initialInput.value) || 0;
const minValue = 0;
if (currentValue > minValue) {
const newValue = currentValue - 1;
initialInput.value = newValue;
document.getElementById('initial').value = newValue;
document.querySelector('input[name="initial-percent"]').value = newValue;
updateCalculator();
}
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});
function initMap() {
const mapContainer = document.getElementById('districtMap');
const currentDistrict = "Черемушки (ЧМР)";
const districtCoords = [
[38.9730, 45.0370],
[38.9770, 45.0390],
[38.9790, 45.0340],
[38.9750, 45.0310],
[38.9710, 45.0340]
];
console.log(`Карта района "${currentDistrict}" инициализирована`);
}
document.addEventListener('DOMContentLoaded', initMap);
document.querySelectorAll('section.faq button').forEach(button => {
button.addEventListener('click', () => {
const answer = button.nextElementSibling;
const icon = button.querySelector('i');
if (answer.style.display === 'none' || !answer.style.display) {
answer.style.display = 'block';
icon.classList.remove('fa-chevron-down');
icon.classList.add('fa-chevron-up');
} else {
answer.style.display = 'none';
icon.classList.remove('fa-chevron-up');
icon.classList.add('fa-chevron-down');
}
});
});
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
anchor.addEventListener('click', function (e) {
e.preventDefault();
document.querySelector(this.getAttribute('href')).scrollIntoView({
behavior: 'smooth'
});
});
});
const initGallery = () => {
const galleryContainer = document.querySelector('.gallery-container');
const gallerySlides = document.querySelectorAll('.gallery-slide');
const galleryNavButtons = document.querySelectorAll('.gallery-nav button');
if (!galleryContainer) return;
galleryNavButtons[0].classList.add('bg-blue-600');
galleryNavButtons[0].classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryNavButtons.forEach(button => {
const slideIndex = parseInt(button.getAttribute('data-slide'));
const slide = gallerySlides[slideIndex];
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
button.classList.add('bg-blue-600');
button.classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryContainer.scrollTo({
left: slide.offsetLeft - galleryContainer.offsetLeft - 16,
behavior: 'smooth'
});
});
});
galleryContainer.addEventListener('scroll', () => {
const scrollPosition = galleryContainer.scrollLeft + galleryContainer.offsetWidth / 2;
gallerySlides.forEach((slide, index) => {
const slideStart = slide.offsetLeft - galleryContainer.offsetLeft;
const slideEnd = slideStart + slide.offsetWidth;
if (scrollPosition > slideStart && scrollPosition < slideEnd) {
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
galleryNavButtons[index].classList.add('bg-blue-600');
galleryNavButtons[index].classList.remove('bg-blue-200', 'hover:bg-blue-400');
}
});
});
let touchStartX = 0;
let touchEndX = 0;
galleryContainer.addEventListener('touchstart', e => {
touchStartX = e.changedTouches[0].screenX;
}, {passive: true});
galleryContainer.addEventListener('touchend', e => {
touchEndX = e.changedTouches[0].screenX;
handleSwipe();
}, {passive: true});
function handleSwipe() {
if (touchEndX < touchStartX - 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex < gallerySlides.length - 1) {
galleryNavButtons[currentSlideIndex + 1].click();
}
}
if (touchEndX > touchStartX + 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex > 0) {
galleryNavButtons[currentSlideIndex - 1].click();
}
}
}
};
document.addEventListener('DOMContentLoaded', () => {
initGallery();
document.getElementById('showBorder')?.addEventListener('click', () => {
alert('Функция "Показать границы" будет работать с реальным API Яндекс.Карт');
});
document.getElementById('showMarkers')?.addEventListener('click', () => {
alert('Функция "Основные объекты" будет работать с реальным API Яндекс.Карт');
});
});

// From script-it-mortgage.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
const activeCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
const activeSelects = Array.from(document.querySelectorAll('select'))
.filter(select => select.value !== '');
const activeTextInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'))
.filter(input => input.value !== '');
const totalFilters = activeCheckboxes.length + activeSelects.length + activeTextInputs.length;
const badge = document.getElementById('activeFilterBadge');
if (totalFilters > 0) {
badge.textContent = totalFilters;
badge.classList.remove('hidden');
} else {
badge.classList.add('hidden');
}
}
document.querySelectorAll('input[type="checkbox"], select, input[type="text"], input[type="number"]').forEach(element => {
});
setupDropdowns();
setupTypewriter();
initCarousels();
updateActiveFiltersCount();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceInput = document.getElementById('price-input');
const priceSlider = document.getElementById('price');
const initialInput = document.getElementById('initial-input');
const initialSlider = document.getElementById('initial');
const termInput = document.getElementById('term-input');
const termSlider = document.getElementById('term');
const rateSelect = document.getElementById('rate');
const creditSumEl = document.getElementById('credit-sum');
const monthlyPaymentEl = document.getElementById('monthly-payment');
const overpaymentEl = document.getElementById('overpayment');
const cashbackEl = document.getElementById('cashback');
const cashbackCheckbox = document.querySelector('input[name="cashback"]');
let value = input.value.replace(/\s/g, '');
if (!isNaN(value)) {
slider.value = value;
updateCalculator();
}
});
input.value = formatFn(slider.value);
updateCalculator();
});
}
return parseInt(value).toLocaleString('ru-RU');
}
return value;
}
connectInputAndSlider(priceInput, priceSlider, formatPrice);
connectInputAndSlider(initialInput, initialSlider, formatPercent);
connectInputAndSlider(termInput, termSlider, formatPercent);
const price = parseInt(priceInput.value.replace(/\s/g, '')) || 5000000;
const initialPercent = parseInt(initialSlider.value) || 15;
const termYears = parseInt(termSlider.value) || 15;
const ratePercent = parseFloat(rateSelect.value) || 14.99;
const cashbackPercentage = 2;
let loanAmount;
const programType = rateSelect.options[rateSelect.selectedIndex].text;
if (programType.includes('Семейная') || programType.includes('Сельская')) {
const maxLoan = 6000000;
const requiredDownPayment = Math.max(0, price - maxLoan);
const calculatedDownPayment = price * initialPercent / 100;
const effectiveDownPayment = Math.max(requiredDownPayment, calculatedDownPayment);
loanAmount = price - effectiveDownPayment;
if (calculatedDownPayment < requiredDownPayment) {
initialInput.classList.add('border-red-500');
} else {
initialInput.classList.remove('border-red-500');
}
}
else if (programType.includes('IT')) {
const maxLoan = 9000000;
const requiredDownPayment = Math.max(0, price - maxLoan);
const calculatedDownPayment = price * initialPercent / 100;
const effectiveDownPayment = Math.max(requiredDownPayment, calculatedDownPayment);
loanAmount = price - effectiveDownPayment;
if (calculatedDownPayment < requiredDownPayment) {
initialInput.classList.add('border-red-500');
} else {
initialInput.classList.remove('border-red-500');
}
}
else {
loanAmount = price * (100 - initialPercent) / 100;
initialInput.classList.remove('border-red-500');
}
const monthlyRate = ratePercent / 100 / 12;
const payments = termYears * 12;
const monthlyPayment = loanAmount * monthlyRate *
Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
const totalPayment = monthlyPayment * payments;
const totalOverpayment = totalPayment - loanAmount;
let cashback = 0;
if (cashbackCheckbox.checked) {
cashback = price * cashbackPercentage / 100;
}
creditSumEl.textContent = formatPrice(Math.round(loanAmount)) + ' ₽';
monthlyPaymentEl.textContent = formatPrice(Math.round(monthlyPayment)) + ' ₽';
overpaymentEl.textContent = formatPrice(Math.round(totalOverpayment)) + ' ₽';
cashbackEl.textContent = formatPrice(Math.round(cashback)) + ' ₽';
}
[priceSlider, initialSlider, termSlider, rateSelect, cashbackCheckbox].forEach(el => {
});
updateCalculator();
});
const initialInput = document.getElementById('initial-input');
const initialSlider = document.getElementById('initial');
const currentValue = parseInt(initialInput.value) || 0;
const price = parseInt(document.getElementById('price-input').value.replace(/\s/g, '')) || 8000000;
const programType = document.getElementById('rate').options[document.getElementById('rate').selectedIndex].text;
let newValue = currentValue + 1;
let maxValue = 40;
if (programType.includes('Семейная') || programType.includes('Сельская')) {
maxValue = Math.min(40, Math.max(100 - (6000000 / price) * 100, 0));
} else if (programType.includes('IT')) {
maxValue = Math.min(40, Math.max(100 - (9000000 / price) * 100, 0));
}
if (newValue > maxValue) {
newValue = maxValue;
}
if (newValue <= maxValue) {
initialInput.value = newValue;
initialSlider.value = newValue;
document.querySelector('input[name="initial-percent"]').value = newValue;
updateCalculator();
}
}
const initialInput = document.getElementById('initial-input');
const currentValue = parseInt(initialInput.value) || 0;
const minValue = 0;
if (currentValue > minValue) {
const newValue = currentValue - 1;
initialInput.value = newValue;
document.getElementById('initial').value = newValue;
document.querySelector('input[name="initial-percent"]').value = newValue;
updateCalculator();
}
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});
const mapContainer = document.getElementById('districtMap');
const currentDistrict = "Черемушки (ЧМР)";
const districtCoords = [
[38.9730, 45.0370],
[38.9770, 45.0390],
[38.9790, 45.0340],
[38.9750, 45.0310],
[38.9710, 45.0340]
];
console.log(`Карта района "${currentDistrict}" инициализирована`);
}
document.querySelectorAll('section.faq button').forEach(button => {
const answer = button.nextElementSibling;
const icon = button.querySelector('i');
if (answer.style.display === 'none' || !answer.style.display) {
answer.style.display = 'block';
icon.classList.remove('fa-chevron-down');
icon.classList.add('fa-chevron-up');
} else {
answer.style.display = 'none';
icon.classList.remove('fa-chevron-up');
icon.classList.add('fa-chevron-down');
}
});
});
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
e.preventDefault();
document.querySelector(this.getAttribute('href')).scrollIntoView({
behavior: 'smooth'
});
});
});
const initGallery = () => {
const galleryContainer = document.querySelector('.gallery-container');
const gallerySlides = document.querySelectorAll('.gallery-slide');
const galleryNavButtons = document.querySelectorAll('.gallery-nav button');
if (!galleryContainer) return;
galleryNavButtons[0].classList.add('bg-blue-600');
galleryNavButtons[0].classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryNavButtons.forEach(button => {
const slideIndex = parseInt(button.getAttribute('data-slide'));
const slide = gallerySlides[slideIndex];
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
button.classList.add('bg-blue-600');
button.classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryContainer.scrollTo({
left: slide.offsetLeft - galleryContainer.offsetLeft - 16,
behavior: 'smooth'
});
});
});
const scrollPosition = galleryContainer.scrollLeft + galleryContainer.offsetWidth / 2;
gallerySlides.forEach((slide, index) => {
const slideStart = slide.offsetLeft - galleryContainer.offsetLeft;
const slideEnd = slideStart + slide.offsetWidth;
if (scrollPosition > slideStart && scrollPosition < slideEnd) {
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
galleryNavButtons[index].classList.add('bg-blue-600');
galleryNavButtons[index].classList.remove('bg-blue-200', 'hover:bg-blue-400');
}
});
});
let touchStartX = 0;
let touchEndX = 0;
touchStartX = e.changedTouches[0].screenX;
}, {passive: true});
touchEndX = e.changedTouches[0].screenX;
handleSwipe();
}, {passive: true});
if (touchEndX < touchStartX - 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex < gallerySlides.length - 1) {
galleryNavButtons[currentSlideIndex + 1].click();
}
}
if (touchEndX > touchStartX + 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex > 0) {
galleryNavButtons[currentSlideIndex - 1].click();
}
}
}
};
initGallery();
alert('Функция "Показать границы" будет работать с реальным API Яндекс.Карт');
});
alert('Функция "Основные объекты" будет работать с реальным API Яндекс.Карт');
});
});

// From script-login.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
primary: '#0088CC',
secondary: '#39F',
dark: '#222',
light: '#F5F5F5',
accent: '#FF6B00'
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const notificationButtons = [
document.getElementById('notification-button'),
document.getElementById('notification-button-mobile')
];
const notificationBadges = [
document.getElementById('notification-badge'),
document.getElementById('notification-badge-mobile')
];
const notificationDropdown = document.getElementById('notification-dropdown');
const notificationDropdownMobile = document.getElementById('notification-dropdown-mobile');
if (dropdown.classList.contains('show')) {
dropdown.classList.remove('show');
setTimeout(() => {
dropdown.style.display = 'none';
}, 300);
} else {
dropdown.style.display = 'block';
setTimeout(() => {
dropdown.classList.add('show');
}, 10);
notificationBadges.forEach(badge => {
if (badge) badge.classList.add('hidden');
});
}
}
function toggleNotifications() {
toggleDropdown(notificationDropdown);
}
function toggleNotificationsMobile() {
toggleDropdown(notificationDropdownMobile);
}
function closeNotifications() {
if (notificationDropdown.classList.contains('show')) {
notificationDropdown.classList.remove('show');
setTimeout(() => {
notificationDropdown.style.display = 'none';
}, 300);
}
if (notificationDropdownMobile.classList.contains('show')) {
notificationDropdownMobile.classList.remove('show');
setTimeout(() => {
notificationDropdownMobile.style.display = 'none';
}, 300);
}
}
const desktopButton = document.getElementById('notification-button');
const desktopButton2 = document.getElementById('notification-button-2');
if (desktopButton) {
desktopButton.addEventListener('click', function(e) {
e.stopPropagation();
toggleNotifications();
});
}
if (desktopButton2) {
desktopButton2.addEventListener('click', function(e) {
e.stopPropagation();
toggleNotifications();
});
}
const mobileButton = document.getElementById('notification-button-mobile');
if (mobileButton) {
mobileButton.addEventListener('click', function(e) {
e.stopPropagation();
toggleNotificationsMobile();
});
}
const desktopBadge = document.getElementById('notification-badge');
const mobileBadge = document.getElementById('notification-badge-mobile');
if (desktopBadge) {
desktopBadge.addEventListener('click', function(e) {
e.stopPropagation();
toggleNotifications();
});
}
if (mobileBadge) {
mobileBadge.addEventListener('click', function(e) {
e.stopPropagation();
toggleNotificationsMobile();
});
}
document.addEventListener('click', function() {
closeNotifications();
});
notificationDropdown.addEventListener('click', function(e) {
e.stopPropagation();
});
function showNewNotifications(count) {
notificationBadge.textContent = count;
notificationBadge.classList.remove('hidden');
}
const userMenuButton = document.getElementById('user-menu-button');
const userMenu = document.getElementById('user-menu');
userMenuButton.addEventListener('click', function(e) {
e.stopPropagation();
userMenu.classList.toggle('hidden');
});
userMenu.classList.add('hidden');
});
const dropdownButton = document.getElementById('contact-dropdown-button');
const dropdownMenu = document.getElementById('contact-dropdown-menu');
dropdownButton.addEventListener('click', function(e) {
e.stopPropagation();
dropdownMenu.classList.toggle('hidden');
});
dropdownMenu.classList.add('hidden');
});
const pages = {
'cashback': document.getElementById('cashback-page'),
'applications': document.getElementById('applications-page'),
'favorites': document.getElementById('favorites-page'),
'collections': document.getElementById('collections-page'),
'settings': document.getElementById('settings-page'),
'manager': document.getElementById('manager-page'),
'documents': document.getElementById('documents-page'),
'placeholder': document.getElementById('placeholder-page'),
'cashback': document.getElementById('cashback')
};
const statsCards = document.querySelector('.grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-4.gap-4.mb-6');
const mainSections = document.querySelector('.grid.grid-cols-1.lg\\:grid-cols-3.gap-6');
function showPage(pageId) {
Object.values(pages).forEach(page => {
page.classList.add('hidden');
});
if (pages[pageId]) {
pages[pageId].classList.remove('hidden');
}
const showMainSections = !pageId;
statsCards.classList.toggle('hidden', !showMainSections);
mainSections.classList.toggle('hidden', !showMainSections);
document.querySelectorAll('.sidebar-item').forEach(item => {
item.classList.remove('active');
if (item.querySelector(`[data-page="${pageId}"]`)) {
item.classList.add('active');
}
});
}
Object.values(pages).forEach(page => {
page.classList.add('hidden');
});
if (pages[pageId]) {
pages[pageId].classList.remove('hidden');
}
const showMainCards = !pageId;
statsCards.classList.toggle('hidden', !showMainCards);
mainSections.classList.toggle('hidden', !showMainCards);
document.querySelectorAll('.sidebar-item').forEach(item => {
item.classList.remove('active');
if (item.querySelector(`[data-page="${pageId}"]`)) {
item.classList.add('active');
}
});
}
document.querySelectorAll('[data-page]').forEach(link => {
link.addEventListener('click', function(e) {
e.preventDefault();
const pageId = this.getAttribute('data-page');
showPage(pageId);
window.location.hash = pageId;
});
});
document.querySelector('.sidebar-item.active').addEventListener('click', function(e) {
if (!e.target.closest('[data-page]')) {
e.preventDefault();
showPage('');
window.location.hash = '';
}
});
window.addEventListener('hashchange', function() {
const pageId = window.location.hash.substring(1);
showPage(pageId);
});
const initialPage = window.location.hash.substring(1);
showPage(initialPage);
});
const newAppBtn = document.getElementById('new-application-btn');
const newAppDropdown = document.getElementById('new-application-dropdown');
if (newAppBtn && newAppDropdown) {
newAppBtn.addEventListener('click', function(e) {
e.stopPropagation();
newAppDropdown.classList.toggle('hidden');
});
newAppDropdown.classList.add('hidden');
});
newAppDropdown.addEventListener('click', function(e) {
e.stopPropagation();
});
}
});
document.getElementById('new-application-btn').addEventListener('click', function() {
document.getElementById('new-application-modal').classList.remove('hidden');
});
document.getElementById('close-application-modal').addEventListener('click', function() {
document.getElementById('new-application-modal').classList.add('hidden');
});
document.getElementById('new-application-modal').addEventListener('click', function(e) {
if (e.target === this) {
this.classList.add('hidden');
}
});

// From script-index.js
document.getElementById('toggleAdvanced').addEventListener('click', function() {
const panel = document.getElementById('advancedParams');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-plus-circle');
this.querySelector('i').classList.toggle('fa-minus-circle');
});
const container = document.querySelector('.property-card');
if (!container) return;
const carousel = container.querySelector('.flex');
const images = carousel.querySelectorAll('img');
const dots = container.querySelectorAll('.absolute.bottom-3 .rounded-full');
let currentIndex = 0;
const totalImages = images.length;
carousel.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('bg-opacity-70', index === currentIndex);
dot.classList.toggle('bg-opacity-30', index !== currentIndex);
});
}
container.querySelector('button:nth-of-type(1)')?.addEventListener('click', () => {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : totalImages - 1;
updateCarousel();
});
container.querySelector('button:nth-of-type(2)')?.addEventListener('click', () => {
currentIndex = (currentIndex < totalImages - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < totalImages - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const container = document.querySelector('.property-card');
if (!container) return;
const carousel = container.querySelector('.flex');
const images = carousel.querySelectorAll('img');
const dots = container.querySelectorAll('.absolute.bottom-3 .rounded-full');
let currentIndex = 0;
const totalImages = images.length;
carousel.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('bg-opacity-70', index === currentIndex);
dot.classList.toggle('bg-opacity-30', index !== currentIndex);
});
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : totalImages - 1;
updateCarousel();
});
currentIndex = (currentIndex < totalImages - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < totalImages - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const container = document.querySelector('.property-card');
if (!container) return;
const carousel = container.querySelector('.flex');
const images = carousel.querySelectorAll('img');
const dots = container.querySelectorAll('.absolute.bottom-3 .rounded-full');
let currentIndex = 0;
const totalImages = images.length;
carousel.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('bg-opacity-70', index === currentIndex);
dot.classList.toggle('bg-opacity-30', index !== currentIndex);
});
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : totalImages - 1;
updateCarousel();
});
currentIndex = (currentIndex < totalImages - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < totalImages - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
setupDropdowns();
setupTypewriter();
initCarousels();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceRange = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');
const downPaymentRange = document.getElementById('downPaymentRange');
const downPaymentValue = document.getElementById('downPaymentValue');
const termRange = document.getElementById('termRange');
const termValue = document.getElementById('termValue');
const cashbackAmount = document.getElementById('cashbackAmount');
const monthlyPayment = document.getElementById('monthlyPayment');
const price = parseInt(priceRange.value);
const downPayment = parseInt(downPaymentRange.value);
const downPaymentPercent = Math.round((downPayment / price) * 100);
const term = parseInt(termRange.value);
const cashbackPercent = 2.5;
priceValue.textContent = new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
downPaymentValue.textContent = new Intl.NumberFormat('ru-RU').format(downPayment) + ' ₽ (' + downPaymentPercent + '%)';
termValue.textContent = term + ' лет';
const cashback = price * cashbackPercent / 100;
cashbackAmount.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(cashback)) + ' ₽';
const loanAmount = price - downPayment;
const monthlyRate = 0.06 / 12;
const payments = term * 12;
const monthly = loanAmount * monthlyRate * Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
monthlyPayment.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(monthly)) + ' ₽';
}
updateCalculator();
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});
function setupDropdowns() {
document.querySelectorAll('.dropdown-btn').forEach(btn => {
btn.addEventListener('click', function(e) {
e.stopPropagation();
const menu = this.nextElementSibling;
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(m => {
if (m !== menu) {
m.classList.remove('open');
m.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
this.classList.toggle('open');
});
});
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
});
}
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const TELEGRAM_BOT_TOKEN = '7210651587:AAEx05tkpKveOIqPpDtwXOY8UGkhwYeCxmE';
const TELEGRAM_CHAT_ID = '730764738';
const EMAIL_API_URL = 'YOUR_EMAIL_SERVICE_ENDPOINT';
const modal = document.getElementById('quiz-modal');
const backdrop = document.getElementById('modal-backdrop');
const openBtns = document.querySelectorAll('.open-quiz');
const modalContainer = document.getElementById('modal-container');
function openModal() {
modalContainer.classList.remove('hidden');
backdrop.classList.remove('hidden');
modal.classList.remove('hidden');
document.body.style.overflow = 'hidden';
goToStep(0);
setTimeout(() => {
modal.classList.add('show');
}, 10);
}
modal.classList.remove('show');
setTimeout(() => {
modalContainer.classList.add('hidden');
backdrop.classList.add('hidden');
modal.classList.add('hidden');
document.body.style.overflow = '';
}, 300);
}
modal.classList.remove('show');
backdrop.classList.remove('show');
setTimeout(() => {
modalContainer.classList.add('hidden');
backdrop.classList.add('hidden');
modal.classList.add('hidden');
document.body.style.overflow = '';
}, 300);
}
document.getElementById('close-modal').addEventListener('click', closeModal);
let touchStartY = 0;
modal.addEventListener('touchstart', (e) => {
touchStartY = e.touches[0].clientY;
}, {passive: true});
modal.addEventListener('touchmove', (e) => {
const touchY = e.touches[0].clientY;
const touchDiff = touchY - touchStartY;
if (touchDiff > 50 && window.scrollY <= 0) {
closeModal();
}
}, {passive: true});
let startY = 0;
startY = e.touches[0].clientY;
}, {passive: true});
const y = e.touches[0].clientY;
if (y - startY > 100 && window.scrollY === 0) {
closeModal();
}
}, {passive: true});
openBtns.forEach(btn => {
btn.addEventListener('click', openModal);
});
backdrop.addEventListener('click', closeModal);
modalContainer.addEventListener('click', function(e) {
if (e.target === modalContainer) {
closeModal();
}
});
document.addEventListener('keydown', function(e) {
if (e.key === 'Escape' && !modalContainer.classList.contains('hidden')) {
closeModal();
}
});
const form = document.getElementById('quiz-form');
const steps = document.querySelectorAll('.step');
const nextButtons = document.querySelectorAll('.next-step');
const prevButtons = document.querySelectorAll('.prev-step');
const optionCards = document.querySelectorAll('.option-card');
const progressFill = document.getElementById('progress');
const currentStepDisplay = document.getElementById('current-step');
let currentStep = 0;
const totalSteps = steps.length - 1;
const formData = {
districts: null,
rooms: null,
completion: null,
payment: null,
name: null,
phone: null,
email: null
};
nextButtons.forEach(button => {
button.addEventListener('click', function() {
if (validateStep(currentStep)) {
goToStep(currentStep + 1);
}
});
});
prevButtons.forEach(button => {
goToStep(currentStep - 1);
});
});
optionCards.forEach(card => {
card.addEventListener('click', function() {
const stepId = this.closest('.step').id;
const value = this.getAttribute('data-value');
const allCardsInStep = this.closest('.step').querySelectorAll('.option-card');
allCardsInStep.forEach(c => c.classList.remove('selected'));
this.classList.add('selected');
switch(stepId) {
case 'step-1':
formData.districts = value;
break;
case 'step-2':
formData.rooms = value;
break;
case 'step-3':
formData.completion = value;
break;
case 'step-4':
formData.payment = value;
break;
}
});
});
function validateStep(stepIndex) {
switch(stepIndex) {
case 0:
if (!formData.districts) {
alert('Пожалуйста, выберите количество районов');
return false;
}
return true;
case 1:
if (!formData.rooms) {
alert('Пожалуйста, выберите количество комнат');
return false;
}
return true;
case 2:
if (!formData.completion) {
alert('Пожалуйста, выберите срок сдачи');
return false;
}
return true;
case 3:
if (!formData.payment) {
alert('Пожалуйста, выберите способ оплаты');
return false;
}
return true;
case 4:
const name = document.getElementById('name').value;
const phone = document.getElementById('phone').value;
const consent = document.getElementById('consent').checked;
if (!name || !phone) {
alert('Пожалуйста, заполните обязательные поля');
return false;
}
if (!consent) {
alert('Необходимо согласие на обработку данных');
return false;
}
formData.name = name;
formData.phone = phone;
formData.email = document.getElementById('email').value;
return true;
default:
return true;
}
}
function goToStep(stepIndex) {
if (stepIndex < 0 || stepIndex > totalSteps) return;
steps[currentStep].classList.remove('active');
steps[stepIndex].classList.add('active');
currentStep = stepIndex;
const progressPercent = (stepIndex / totalSteps) * 100;
progressFill.style.width = `${progressPercent}%`;
currentStepDisplay.textContent = stepIndex + 1;
window.scrollTo({ top: 0, behavior: 'smooth' });
}
form.addEventListener('submit', function(e) {
e.preventDefault();
const submitBtn = document.getElementById('submit-btn');
const submitText = document.getElementById('submit-text');
const submitSpinner = document.getElementById('submit-spinner');
submitBtn.disabled = true;
submitText.classList.add('hidden');
submitSpinner.classList.remove('hidden');
if (validateStep(currentStep)) {
const formData = {
districts: getSelectedOptionText('step-1') || 'Не указано',
rooms: getSelectedOptionText('step-2') || 'Не указано',
completion: getSelectedOptionText('step-3') || 'Не указано',
payment: getSelectedOptionText('step-4') || 'Не указано',
name: document.getElementById('name').value,
phone: document.getElementById('phone').value,
email: document.getElementById('email').value || 'Не указано'
};
const telegramMessage = `
📌 *Новая заявка на подбор жилья*:
🏙 *Районы*: ${formData.districts}
🏠 *Комнат*: ${formData.rooms}
📅 *Срок сдачи*: ${formData.completion}
💳 *Способ оплаты*: ${formData.payment}
👤 *Имя*: ${formData.name}
📞 *Телефон*: ${formData.phone}
📧 *Email*: ${formData.email}
`;
axios.post(`https:
chat_id: TELEGRAM_CHAT_ID,
text: telegramMessage,
parse_mode: 'Markdown'
})
.then(() => {
console.log('Сообщение отправлено в Telegram');
})
.catch(error => {
console.error('Ошибка отправки в Telegram:', error);
});
axios.post(EMAIL_API_URL, {
subject: 'Новая заявка на подбор жилья',
text: telegramMessage,
to: 'your@email.com',
formData: formData
})
.then(() => {
console.log('Сообщение отправлено на email');
})
.catch(error => {
console.error('Ошибка отправки на email:', error);
});
goToStep(totalSteps);
submitBtn.disabled = false;
submitText.classList.remove('hidden');
submitSpinner.classList.add('hidden');
}
});
function getSelectedOptionText(stepId) {
const step = document.getElementById(stepId);
if (!step) return null;
const selectedCard = step.querySelector('.option-card.selected');
if (!selectedCard) return null;
return selectedCard.querySelector('h3').textContent;
}
const phoneInput = document.getElementById('phone');
phoneInput.addEventListener('input', function(e) {
let x = e.target.value.replace(/\D/g, '').match(/(\d{0,1})(\d{0,3})(\d{0,3})(\d{0,2})(\d{0,2})/);
e.target.value = !x[2] ? x[1] : x[1] + ' (' + x[2] + ') ' + x[3] + (x[4] ? '-' + x[4] : '') + (x[5] ? '-' + x[5] : '');
});
});

// From script-about.js
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
setupDropdowns();
setupTypewriter();
initCarousels();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceRange = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');
const downPaymentRange = document.getElementById('downPaymentRange');
const downPaymentValue = document.getElementById('downPaymentValue');
const termRange = document.getElementById('termRange');
const termValue = document.getElementById('termValue');
const cashbackAmount = document.getElementById('cashbackAmount');
const monthlyPayment = document.getElementById('monthlyPayment');
const price = parseInt(priceRange.value);
const downPayment = parseInt(downPaymentRange.value);
const downPaymentPercent = Math.round((downPayment / price) * 100);
const term = parseInt(termRange.value);
const cashbackPercent = 2.5;
priceValue.textContent = new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
downPaymentValue.textContent = new Intl.NumberFormat('ru-RU').format(downPayment) + ' ₽ (' + downPaymentPercent + '%)';
termValue.textContent = term + ' лет';
const cashback = price * cashbackPercent / 100;
cashbackAmount.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(cashback)) + ' ₽';
const loanAmount = price - downPayment;
const monthlyRate = 0.06 / 12;
const payments = term * 12;
const monthly = loanAmount * monthlyRate * Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
monthlyPayment.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(monthly)) + ' ₽';
}
updateCalculator();
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});

// From script-blog.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
setupDropdowns();
setupTypewriter();
initCarousels();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceRange = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');
const downPaymentRange = document.getElementById('downPaymentRange');
const downPaymentValue = document.getElementById('downPaymentValue');
const termRange = document.getElementById('termRange');
const termValue = document.getElementById('termValue');
const cashbackAmount = document.getElementById('cashbackAmount');
const monthlyPayment = document.getElementById('monthlyPayment');
const price = parseInt(priceRange.value);
const downPayment = parseInt(downPaymentRange.value);
const downPaymentPercent = Math.round((downPayment / price) * 100);
const term = parseInt(termRange.value);
const cashbackPercent = 2.5;
priceValue.textContent = new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
downPaymentValue.textContent = new Intl.NumberFormat('ru-RU').format(downPayment) + ' ₽ (' + downPaymentPercent + '%)';
termValue.textContent = term + ' лет';
const cashback = price * cashbackPercent / 100;
cashbackAmount.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(cashback)) + ' ₽';
const loanAmount = price - downPayment;
const monthlyRate = 0.06 / 12;
const payments = term * 12;
const monthly = loanAmount * monthlyRate * Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
monthlyPayment.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(monthly)) + ' ₽';
}
updateCalculator();
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});

// From script-careers.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
const activeCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
const activeSelects = Array.from(document.querySelectorAll('select'))
.filter(select => select.value !== '');
const activeTextInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'))
.filter(input => input.value !== '');
const totalFilters = activeCheckboxes.length + activeSelects.length + activeTextInputs.length;
const badge = document.getElementById('activeFilterBadge');
if (totalFilters > 0) {
badge.textContent = totalFilters;
badge.classList.remove('hidden');
} else {
badge.classList.add('hidden');
}
}
document.querySelectorAll('input[type="checkbox"], select, input[type="text"], input[type="number"]').forEach(element => {
});
setupDropdowns();
setupTypewriter();
initCarousels();
updateActiveFiltersCount();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceInput = document.getElementById('price-input');
const priceSlider = document.getElementById('price');
const initialInput = document.getElementById('initial-input');
const initialSlider = document.getElementById('initial');
const termInput = document.getElementById('term-input');
const termSlider = document.getElementById('term');
const rateSelect = document.getElementById('rate');
const creditSumEl = document.getElementById('credit-sum');
const monthlyPaymentEl = document.getElementById('monthly-payment');
const overpaymentEl = document.getElementById('overpayment');
const cashbackEl = document.getElementById('cashback');
const cashbackCheckbox = document.querySelector('input[name="cashback"]');
let value = input.value.replace(/\s/g, '');
if (!isNaN(value)) {
slider.value = value;
updateCalculator();
}
});
input.value = formatFn(slider.value);
updateCalculator();
});
}
return parseInt(value).toLocaleString('ru-RU');
}
return value;
}
connectInputAndSlider(priceInput, priceSlider, formatPrice);
connectInputAndSlider(initialInput, initialSlider, formatPercent);
connectInputAndSlider(termInput, termSlider, formatPercent);
const price = parseInt(priceInput.value.replace(/\s/g, '')) || 5000000;
const initialPercent = parseInt(initialSlider.value) || 15;
const termYears = parseInt(termSlider.value) || 15;
const ratePercent = parseFloat(rateSelect.value) || 14.99;
const cashbackPercentage = 2;
let loanAmount;
const programType = rateSelect.options[rateSelect.selectedIndex].text;
if (programType.includes('Семейная') || programType.includes('Сельская')) {
const maxLoan = 6000000;
const requiredDownPayment = Math.max(0, price - maxLoan);
const calculatedDownPayment = price * initialPercent / 100;
const effectiveDownPayment = Math.max(requiredDownPayment, calculatedDownPayment);
loanAmount = price - effectiveDownPayment;
if (calculatedDownPayment < requiredDownPayment) {
initialInput.classList.add('border-red-500');
} else {
initialInput.classList.remove('border-red-500');
}
}
else if (programType.includes('IT')) {
const maxLoan = 9000000;
const requiredDownPayment = Math.max(0, price - maxLoan);
const calculatedDownPayment = price * initialPercent / 100;
const effectiveDownPayment = Math.max(requiredDownPayment, calculatedDownPayment);
loanAmount = price - effectiveDownPayment;
if (calculatedDownPayment < requiredDownPayment) {
initialInput.classList.add('border-red-500');
} else {
initialInput.classList.remove('border-red-500');
}
}
else {
loanAmount = price * (100 - initialPercent) / 100;
initialInput.classList.remove('border-red-500');
}
const monthlyRate = ratePercent / 100 / 12;
const payments = termYears * 12;
const monthlyPayment = loanAmount * monthlyRate *
Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
const totalPayment = monthlyPayment * payments;
const totalOverpayment = totalPayment - loanAmount;
let cashback = 0;
if (cashbackCheckbox.checked) {
cashback = price * cashbackPercentage / 100;
}
creditSumEl.textContent = formatPrice(Math.round(loanAmount)) + ' ₽';
monthlyPaymentEl.textContent = formatPrice(Math.round(monthlyPayment)) + ' ₽';
overpaymentEl.textContent = formatPrice(Math.round(totalOverpayment)) + ' ₽';
cashbackEl.textContent = formatPrice(Math.round(cashback)) + ' ₽';
}
[priceSlider, initialSlider, termSlider, rateSelect, cashbackCheckbox].forEach(el => {
});
updateCalculator();
});
const initialInput = document.getElementById('initial-input');
const initialSlider = document.getElementById('initial');
const currentValue = parseInt(initialInput.value) || 0;
const price = parseInt(document.getElementById('price-input').value.replace(/\s/g, '')) || 8000000;
const programType = document.getElementById('rate').options[document.getElementById('rate').selectedIndex].text;
let newValue = currentValue + 1;
let maxValue = 40;
if (programType.includes('Семейная') || programType.includes('Сельская')) {
maxValue = Math.min(40, Math.max(100 - (6000000 / price) * 100, 0));
} else if (programType.includes('IT')) {
maxValue = Math.min(40, Math.max(100 - (9000000 / price) * 100, 0));
}
if (newValue > maxValue) {
newValue = maxValue;
}
if (newValue <= maxValue) {
initialInput.value = newValue;
initialSlider.value = newValue;
document.querySelector('input[name="initial-percent"]').value = newValue;
updateCalculator();
}
}
const initialInput = document.getElementById('initial-input');
const currentValue = parseInt(initialInput.value) || 0;
const minValue = 0;
if (currentValue > minValue) {
const newValue = currentValue - 1;
initialInput.value = newValue;
document.getElementById('initial').value = newValue;
document.querySelector('input[name="initial-percent"]').value = newValue;
updateCalculator();
}
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});
const mapContainer = document.getElementById('districtMap');
const currentDistrict = "Черемушки (ЧМР)";
const districtCoords = [
[38.9730, 45.0370],
[38.9770, 45.0390],
[38.9790, 45.0340],
[38.9750, 45.0310],
[38.9710, 45.0340]
];
console.log(`Карта района "${currentDistrict}" инициализирована`);
}
document.querySelectorAll('section.faq button').forEach(button => {
const answer = button.nextElementSibling;
const icon = button.querySelector('i');
if (answer.style.display === 'none' || !answer.style.display) {
answer.style.display = 'block';
icon.classList.remove('fa-chevron-down');
icon.classList.add('fa-chevron-up');
} else {
answer.style.display = 'none';
icon.classList.remove('fa-chevron-up');
icon.classList.add('fa-chevron-down');
}
});
});
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
e.preventDefault();
document.querySelector(this.getAttribute('href')).scrollIntoView({
behavior: 'smooth'
});
});
});
const initGallery = () => {
const galleryContainer = document.querySelector('.gallery-container');
const gallerySlides = document.querySelectorAll('.gallery-slide');
const galleryNavButtons = document.querySelectorAll('.gallery-nav button');
if (!galleryContainer) return;
galleryNavButtons[0].classList.add('bg-blue-600');
galleryNavButtons[0].classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryNavButtons.forEach(button => {
const slideIndex = parseInt(button.getAttribute('data-slide'));
const slide = gallerySlides[slideIndex];
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
button.classList.add('bg-blue-600');
button.classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryContainer.scrollTo({
left: slide.offsetLeft - galleryContainer.offsetLeft - 16,
behavior: 'smooth'
});
});
});
const scrollPosition = galleryContainer.scrollLeft + galleryContainer.offsetWidth / 2;
gallerySlides.forEach((slide, index) => {
const slideStart = slide.offsetLeft - galleryContainer.offsetLeft;
const slideEnd = slideStart + slide.offsetWidth;
if (scrollPosition > slideStart && scrollPosition < slideEnd) {
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
galleryNavButtons[index].classList.add('bg-blue-600');
galleryNavButtons[index].classList.remove('bg-blue-200', 'hover:bg-blue-400');
}
});
});
let touchStartX = 0;
let touchEndX = 0;
touchStartX = e.changedTouches[0].screenX;
}, {passive: true});
touchEndX = e.changedTouches[0].screenX;
handleSwipe();
}, {passive: true});
if (touchEndX < touchStartX - 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex < gallerySlides.length - 1) {
galleryNavButtons[currentSlideIndex + 1].click();
}
}
if (touchEndX > touchStartX + 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex > 0) {
galleryNavButtons[currentSlideIndex - 1].click();
}
}
}
};
initGallery();
alert('Функция "Показать границы" будет работать с реальным API Яндекс.Карт');
});
alert('Функция "Основные объекты" будет работать с реальным API Яндекс.Карт');
});
});

// From script-contacts.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
setupDropdowns();
setupTypewriter();
initCarousels();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceRange = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');
const downPaymentRange = document.getElementById('downPaymentRange');
const downPaymentValue = document.getElementById('downPaymentValue');
const termRange = document.getElementById('termRange');
const termValue = document.getElementById('termValue');
const cashbackAmount = document.getElementById('cashbackAmount');
const monthlyPayment = document.getElementById('monthlyPayment');
const price = parseInt(priceRange.value);
const downPayment = parseInt(downPaymentRange.value);
const downPaymentPercent = Math.round((downPayment / price) * 100);
const term = parseInt(termRange.value);
const cashbackPercent = 2.5;
priceValue.textContent = new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
downPaymentValue.textContent = new Intl.NumberFormat('ru-RU').format(downPayment) + ' ₽ (' + downPaymentPercent + '%)';
termValue.textContent = term + ' лет';
const cashback = price * cashbackPercent / 100;
cashbackAmount.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(cashback)) + ' ₽';
const loanAmount = price - downPayment;
const monthlyRate = 0.06 / 12;
const payments = term * 12;
const monthly = loanAmount * monthlyRate * Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
monthlyPayment.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(monthly)) + ' ₽';
}
updateCalculator();
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});

// From script-map.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const map = L.map('map').setView([45.0355, 38.9753], 13);
L.tileLayer('https:
attribution: '&copy; <a href="https:
}).addTo(map);
const tonMarkerIcon = (hasCashback) => {
return L.divIcon({
className: 'custom-marker',
html: `
<div class="relative transform hover:scale-110 transition-transform duration-200">
${hasCashback ?
'<div class="absolute -inset-1 rounded-full bg-blue-400 opacity-20 animate-pulse"></div>' :
''}
<div class="relative rounded-full w-10 h-10 flex items-center justify-center
${hasCashback ? 'ton-gradient' : 'bg-gray-600'} shadow-md">
<span class="text-white font-semibold text-xs">${hasCashback ? 'TON' : 'APT'}</span>
</div>
<div class="absolute -bottom-2 left-1/2 transform -translate-x-1/2 w-0 h-0
border-l-8 border-r-8 border-t-8 border-l-transparent border-r-transparent
${hasCashback ? 'border-t-blue-500' : 'border-t-gray-600'}"></div>
</div>
`,
iconSize: [40, 50],
iconAnchor: [20, 50]
});
};
const randomInRange = (min, max) => Math.random() * (max - min) + min;
const generateRandomMarker = (id, isComplex) => {
const lat = randomInRange(45.01, 45.08);
const lng = randomInRange(38.95, 39.05);
const hasCashback = Math.random() > 0.3;
return {
id,
lat,
lng,
price: isComplex ? "ЖК" : `${(5 + Math.random() * 8).toFixed(1)}M`,
type: isComplex ? "ЖК" : "Квартира",
rooms: isComplex ? null : Math.floor(1 + Math.random() * 4),
hasCashback,
name: isComplex ?
`ЖК ${['Центральный', 'Фестивальный', 'Речной', 'Южный'][Math.floor(Math.random() * 4)]}` :
`${Math.floor(1 + Math.random() * 4)}-комн. кварт.`,
floor: isComplex ? "1-16" : `${Math.floor(1 + Math.random() * 15)}/${Math.floor(5 + Math.random() * 15)}`,
year: isComplex ? "2022-2024" : (2020 + Math.floor(Math.random() * 4)).toString()
};
};
const properties = [];
for (let i = 1; i <= 10; i++) {
properties.push(generateRandomMarker(i, false));
}
for (let i = 11; i <= 12; i++) {
properties.push(generateRandomMarker(i, true));
}
properties.forEach(property => {
const marker = L.marker([property.lat, property.lng], {
icon: tonMarkerIcon(property.hasCashback),
riseOnHover: true
}).addTo(map);
const popupContent = `
<div class="w-48">
<h3 class="font-bold">${property.name}</h3>
<p class="text-sm">${property.type === 'ЖК' ? 'Объекты от 6.2 млн ₽' : `${property.price} · ${property.rooms} комн.`}</p>
<p class="text-xs text-gray-500 mt-1">${property.type !== 'ЖК' ? `${property.floor} этаж · ` : ''}${property.year}</p>
${property.hasCashback ?
'<div class="mt-1 text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">Кешбек</div>' : ''}
<button onclick="showObjectDetails(${property.id})"
class="mt-2 w-full bg-blue-500 text-white py-1 rounded text-sm hover:bg-blue-600">
Подробнее
</button>
</div>
`;
marker.bindPopup(popupContent);
marker.on('click', function() {
showObjectDetails(property.id);
});
});
L.control.zoom({
position: 'bottomright'
}).addTo(map);
L.tileLayer('https:
maxZoom: 19,
attribution: '&copy; <a href="https:
errorTileUrl: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAYAAABccqhmAAAB/ElEQVR4nO3BMQEAAADCoPVPbQwfoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4K0G0wABlT6OoAAAAABJRU5ErkJggg=='
}).addTo(map);
L.control.zoom({
position: 'bottomright'
}).addTo(map);
document.getElementById('map').style.visibility = 'visible';
const propertyIcon = (property) => L.divIcon({
className: 'custom-marker',
html: `
<div class="relative transform hover:scale-110 transition-transform duration-200">
<div class="absolute -inset-1 rounded-full bg-blue-400 opacity-20 animate-pulse"></div>
<div class="relative rounded-full w-10 h-10 flex items-center justify-center ton-gradient shadow-md">
<span class="text-white font-semibold z-10 text-sm">
${property.type === 'ЖК' ? 'ЖК' : property.rooms}
</span>
</div>
<div class="absolute -bottom-2 left-1/2 transform -translate-x-1/2 w-0 h-0
border-l-8 border-r-8 border-t-8 border-l-transparent border-r-transparent
border-t-blue-500"></div>
</div>
`,
iconSize: [40, 50],
iconAnchor: [20, 50]
});
const markers = L.markerClusterGroup({
iconCreateFunction: function(cluster) {
const count = cluster.getChildCount();
return L.divIcon({
html: `
<div class="relative">
<div class="absolute inset-0 rounded-full bg-blue-500 opacity-20"></div>
<div class="relative rounded-full w-12 h-12 flex items-center justify-center ton-gradient shadow-md">
<span class="text-white font-bold">${count}</span>
</div>
</div>
`,
className: 'marker-cluster-custom',
iconSize: L.point(40, 40)
});
},
spiderfyOnMaxZoom: true,
showCoverageOnHover: false,
zoomToBoundsOnClick: true
});
const properties = [
{
lat: 45.0435,
lng: 38.9783,
price: "12.8",
count: 4,
type: "Квартира",
rooms: 4,
area: 104,
objectId: 1,
hasCashback: true
},
{
lat: 45.0330,
lng: 38.9680,
price: "8.7",
count: 5,
type: "Квартира",
rooms: 3,
area: 78,
objectId: 2,
hasCashback: true
},
{
lat: 45.0180,
lng: 38.9900,
price: "6.2",
count: 3,
type: "Квартира",
rooms: 2,
area: 54,
objectId: 3,
hasCashback: false
},
{
lat: 45.0250,
lng: 38.9600,
price: "ЖК",
count: 8,
type: "ЖК",
area: "-",
objectId: 4,
hasCashback: true
}
];
const propertyIcon = (property) => L.divIcon({
className: 'custom-marker',
html: `
<div class="relative">
<div class="marker-pulse ${property.hasCashback ? 'bg-blue-500' : 'bg-gray-500'}"></div>
<div class="marker-content ${property.hasCashback ? 'bg-blue-500' : 'bg-gray-500'}">
<span>${property.price.includes('ЖК') ? 'ЖК' : property.price}</span>
</div>
</div>
`,
iconSize: [32, 32],
iconAnchor: [16, 32]
});
properties.forEach(property => {
const marker = L.marker([property.lat, property.lng], {
icon: propertyIcon(property)
});
const popupContent = `
<div class="popup-content w-52">
<div class="bg-white rounded-xl shadow-lg overflow-hidden">
<div class="ton-gradient p-3 text-white">
<h3 class="font-bold text-lg">${property.price}${property.type === 'ЖК' ? '' : ' млн ₽'}</h3>
<p class="text-blue-100 text-sm">
${property.type === 'ЖК' ? 'Жилой комплекс' : `${property.rooms}-комн. кв., ${property.area} м²`}
</p>
</div>
<div class="p-3">
<div class="flex items-center mb-2">
<div class="w-8 h-8 rounded-full ton-gradient flex items-center justify-center text-white font-bold mr-2">
${property.type === 'ЖК' ? 'ЖК' : property.rooms}
</div>
<div>
<p class="text-gray-700 text-sm">${property.floor} этаж</p>
<p class="text-gray-400 text-xs">${property.year} год</p>
</div>
</div>
${property.hasCashback ?
'<div class="bg-blue-50 text-blue-600 text-xs px-2 py-1 rounded-full mb-3">Кешбек 3%</div>' : ''}
<button onclick="showObjectDetails(${property.objectId})"
class="w-full ton-gradient text-white py-2 rounded-lg text-sm font-medium hover:opacity-90 transition">
Подробнее
</button>
</div>
</div>
</div>
`;
marker.bindPopup(popupContent);
markers.addLayer(marker);
});
map.addLayer(markers);
function showPropertiesAtLocation(lat, lng) {
showObjectDetails(lat > 45.04 ? 1 :
lat > 45.03 ? 2 :
lat > 45.02 ? 3 : 4);
}
const mapboxToken = 'pk.eyJ1IjoidG9ucy1yZWFsLWVzdGF0ZSIsImEiOiJjbHVuY2k4aWswMnk0MmpwbmQ3ZG1pbWNvIn0.LLF3E8k3M0-XgP3-Kb1z6g';
let map;
let markers = [];
const map = L.map('map').setView([45.0355, 38.9753], 12);
L.tileLayer('https:
attribution: '&copy; <a href="https:
}).addTo(map);
loadInitialProperties();
}
function loadInitialProperties() {
const initialProperties = [
{
id: 1,
coordinates: [38.9783, 45.0435],
price: "12.8M",
color: "#0087F5",
onClick: () => showObjectDetails(1)
},
{
id: 2,
coordinates: [38.9680, 45.0330],
price: "8.7M",
color: "#0087F5",
onClick: () => showObjectDetails(2)
},
{
id: 3,
coordinates: [38.9900, 45.0180],
price: "6.2M",
color: "#0087F5",
onClick: () => showObjectDetails(3)
},
{
id: 4,
coordinates: [38.9600, 45.0250],
price: "ЖК",
color: "#0087F5",
onClick: () => showObjectDetails(4)
}
];
addMarkersToMap(initialProperties);
}
function addMarkersToMap(properties) {
clearMarkers();
properties.forEach(property => {
const el = document.createElement('div');
el.className = 'custom-marker';
el.innerHTML = `<div class="marker-pin"></div><span class="marker-price">${property.price}</span>`;
el.style.width = '40px';
el.style.height = '54px';
const marker = new mapboxgl.Marker(el)
.setLngLat(property.coordinates)
.addTo(map);
el.addEventListener('click', property.onClick);
markers.push(marker);
});
}
function clearMarkers() {
markers.forEach(marker => marker.remove());
markers = [];
}
async function searchProperties() {
const address = document.getElementById('addressInput').value;
if (!address) {
alert('Пожалуйста, введите адрес для поиска');
return;
}
try {
const response = await fetch(`https:
const data = await response.json();
if (data.features.length === 0) {
alert('Адрес не найден');
return;
}
const [lng, lat] = data.features[0].center;
map.flyTo({
center: [lng, lat],
zoom: 14
});
const nearbyProperties = await fetchNearbyProperties(lng, lat);
addMarkersToMap(nearbyProperties);
} catch (error) {
console.error('Ошибка поиска:', error);
alert('Произошла ошибка при поиске');
}
}
async function fetchNearbyProperties(lng, lat) {
const randomOffset = () => (Math.random() * 0.02 - 0.01);
return [
{
id: 101,
coordinates: [lng + randomOffset(), lat + randomOffset()],
price: `${Math.floor(5 + Math.random() * 10)}.${Math.floor(Math.random() * 9)}M`,
color: "#0087F5",
onClick: () => showObjectDetails(101)
},
{
id: 102,
coordinates: [lng + randomOffset(), lat + randomOffset()],
price: `${Math.floor(5 + Math.random() * 10)}.${Math.floor(Math.random() * 9)}M`,
color: "#0087F5",
onClick: () => showObjectDetails(102)
}
];
}
window.onload = initMap;
const objects = {
1: {
title: "4-комн. квартира, 104 м²",
price: "12 800 000 ₽",
address: "ЖК «Гранд Люкс», Краснодар, ул. Красных Партизан",
image: "https:
floor: "5/16",
year: "2019",
area: "104 м²",
cashback: "Кешбек 3%",
badge: "Кешбек 3%",
badgeColor: "amber-400",
description: "Просторная 4-комнатная квартира в современном жилом комплексе \"Гранд Люкс\". Квартира с качественным евроремонтом, готова к заселению. Большая кухня-гостиная 30 м² с панорамным остеклением. Три спальни и кабинет. Санузлы раздельные. Вся необходимая бытовая техника встроена. Двор закрыт от посторонних, детские и спортивные площадки, подземный паркинг. Развитая инфраструктура района - школы, детские сады, торговые центры в шаговой доступности. Кешбек 3% при покупке через Tons."
},
2: {
title: "3-комн. квартира, 78 м²",
price: "8 700 000 ₽",
address: "ЖК «Небесный», Краснодар, ул. 40 лет Победы",
image: "https:
floor: "15/25",
year: "2022",
area: "78 м²",
cashback: "Кешбек 2%",
badge: "Кешбек 2%",
badgeColor: "amber-400",
description: "Современная 3-комнатная квартира в новом жилом комплексе \"Небесный\". Высокий этаж с панорамным видом на город. Удобная планировка с изолированными комнатами. Кухня-гостиная 20 м². Есть балкон. Ремонт выполнен по дизайнерскому проекту. Встроенная техника, кондиционеры. Закрытая охраняемая территория, паркинг, детские площадки. Рядом парк и набережная. Кешбек 2% при покупке через Tons."
},
3: {
},
4: {
title: "2-комн. квартира, 54 м²",
price: "6 200 000 ₽",
address: "ЖК «Триумфальная Арка», Краснодар, ул. Тургенева",
image: "https:
floor: "3/9",
year: "2018",
area: "54 м²",
cashback: "",
badge: "Акция",
badgeColor: "red-500 text-white",
description: "Уютная 2-комнатная квартира в жилом комплексе \"Триумфальная Арка\". Хорошая транспортная доступность. Первый пул ремонта - стены, пол, сантехника. Возможен индивидуальный дизайн-проект. Балкон застеклен. Во дворе детская площадка, зоны отдыха. В шаговой доступности супермаркет, аптека, остановка общественного транспорта. Специальное предложение - скидка 5% при покупке до конца месяца."
},
4: {
title: "ЖК «Гранд Люкс»",
price: "12 объектов от 6.2 млн ₽",
address: "Краснодар, ул. Красных Партизан, 108",
image: "https:
floor: "5-16 этажей",
year: "2020-2024 (3 очередь)",
area: "от 33 м² до 125 м²",
cashback: "Кешбек 1%",
badge: "ЖК",
badgeColor: "blue-500 text-white",
developer: "Гарантия-Инвест",
series: "Комфорт-класс",
decoration: "Чистовая отделка",
parking: "Подземный (платный)",
ceiling: "2.7 м",
infrastructure: "Школа, детсад, магазины",
description: `
<p>Жилой комплекс бизнес-класса в экологически чистом районе Краснодара. Общая площадь 15 га.</p>
<ul class="mt-2 list-disc pl-5">
<li>7 жилых корпусов высотой 5-16 этажей</li>
<li>Собственная управляющая компания</li>
<li>Двор без машин, 70% озеленения</li>
<li>Детские и спортивные площадки</li>
<li>Фитнес-центр и SPA на территории</li>
<li>3 очереди строительства</li>
<li>Инфраструктура шаговой доступности</li>
</ul>
<p class="mt-2">Кешбек 1% при покупке квартиры через нашу платформу.</p>
`,
paymentTypes: ["Ипотека 4.8%", "Рассрочка 0%", "Trade-in"],
features: ["Панорамные окна", "Тёплые полы", "Видеонаблюдение", "Пункт охраны"]
}
};
function showObjectDetails(id) {
if (!objects[id]) {
console.error('Объект с id', id, 'не найден');
return;
}
const object = objects[id];
document.getElementById('modalTitle').textContent = object.title;
document.getElementById('modalPrice').textContent = object.price;
document.getElementById('modalAddress').textContent = object.address;
document.getElementById('modalImage').src = object.image;
document.getElementById('modalFloor').textContent = object.floor || '-';
document.getElementById('modalYear').textContent = object.year || '-';
document.getElementById('modalArea').textContent = object.area || '-';
document.getElementById('modalCashback').textContent = object.cashback || 'Нет кешбека';
document.getElementById('modalDescription').innerHTML = object.description || '';
if (object.developer) {
document.getElementById('modalDev').textContent = object.developer;
document.getElementById('modalSeries').textContent = object.series;
document.getElementById('modalDecoration').textContent = object.decoration;
document.getElementById('modalParking').textContent = object.parking;
const paymentEl = document.getElementById('modalPayment');
paymentEl.innerHTML = '';
object.paymentTypes?.forEach(type => {
const chip = document.createElement('span');
chip.className = 'bg-blue-100 text-blue-800 text-xs px-2.5 py-0.5 rounded';
chip.textContent = type;
paymentEl.appendChild(chip);
});
const featuresEl = document.getElementById('modalFeatures');
featuresEl.innerHTML = '';
object.features?.forEach(feat => {
const chip = document.createElement('span');
chip.className = 'bg-gray-100 text-gray-800 text-xs px-2.5 py-0.5 rounded';
chip.textContent = feat;
featuresEl.appendChild(chip);
});
}
const badge = document.getElementById('modalBadge');
badge.textContent = object.badge;
badge.className = `absolute top-2 right-2 bg-${object.badgeColor} text-xs font-medium px-2 py-1 rounded-full`;
const modal = document.getElementById('objectModal');
modal.classList.add('open');
document.body.style.overflow = 'hidden';
if (id === 4) {
const jkContent = document.getElementById('modalJkContent');
const regularContent = document.getElementById('modalRegularContent');
jkContent.classList.remove('hidden');
regularContent.classList.add('hidden');
document.getElementById('modalJkTitle').textContent = 'ЖК «Гранд Люкс»';
document.getElementById('modalJkPrice').textContent = '12 объектов от 6.2 млн ₽';
document.getElementById('modalJkAddress').textContent = 'Краснодар, ул. Красных Партизан, 108';
document.getElementById('modalJkYear').textContent = '2020-2024 (3 очередь)';
document.getElementById('modalJkFloors').textContent = '5-16 этажей';
document.getElementById('modalJkArea').textContent = 'от 33 м² до 125 м²';
document.getElementById('modalJkDev').textContent = 'Гарантия-Инвест';
document.getElementById('modalJkClass').textContent = 'Комфорт-класс';
document.getElementById('modalJkDescription').innerHTML = `
<p>Жилой комплекс бизнес-класса в экологически чистом районе Краснодара. Общая площадь 15 га.</p>
<ul class="mt-2 list-disc pl-5">
<li>7 жилых корпусов высотой 5-16 этажей</li>
<li>Собственная управляющая компания</li>
<li>Двор без машин, 70% озеленения</li>
<li>Детские и спортивные площадки</li>
</ul>
<p class="mt-3">Кешбек 1% при покупке квартиры через нашу платформу.</p>
`;
} else {
const jkContent = document.getElementById('modalJkContent');
const regularContent = document.getElementById('modalRegularContent');
jkContent.classList.add('hidden');
regularContent.classList.remove('hidden');
}
if (id === 1) map.setView([45.0435, 38.9783], 15);
else if (id === 2) map.setView([45.0330, 38.9680], 15);
else if (id === 3) map.setView([45.0180, 38.9900], 15);
else if (id === 4) map.setView([45.0250, 38.9600], 15);
}
function hideModal() {
const modal = document.getElementById('objectModal');
modal.classList.remove('open');
document.body.style.overflow = 'auto';
}
function changeMainImage(img) {
document.getElementById('modalImage').src = img.src;
}
document.getElementById('objectModal').addEventListener('click', function(e) {
if (e.target === this) {
hideModal();
}
});
function toggleAdvancedFilters() {
const filters = document.getElementById('advancedFilters');
filters.classList.toggle('hidden');
}
function toggleObjectList() {
const list = document.querySelector('.lg\\:w-1\\/3');
list.classList.toggle('hidden');
}
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
const activeCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
const activeSelects = Array.from(document.querySelectorAll('select'))
.filter(select => select.value !== '');
const activeTextInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'))
.filter(input => input.value !== '');
const totalFilters = activeCheckboxes.length + activeSelects.length + activeTextInputs.length;
const badge = document.getElementById('activeFilterBadge');
if (totalFilters > 0) {
badge.textContent = totalFilters;
badge.classList.remove('hidden');
} else {
badge.classList.add('hidden');
}
}
document.querySelectorAll('input[type="checkbox"], select, input[type="text"], input[type="number"]').forEach(element => {
});
setupDropdowns();
setupTypewriter();
initCarousels();
updateActiveFiltersCount();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceRange = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');
const downPaymentRange = document.getElementById('downPaymentRange');
const downPaymentValue = document.getElementById('downPaymentValue');
const termRange = document.getElementById('termRange');
const termValue = document.getElementById('termValue');
const cashbackAmount = document.getElementById('cashbackAmount');
const monthlyPayment = document.getElementById('monthlyPayment');
const price = parseInt(priceRange.value);
const downPayment = parseInt(downPaymentRange.value);
const downPaymentPercent = Math.round((downPayment / price) * 100);
const term = parseInt(termRange.value);
const cashbackPercent = 2.5;
priceValue.textContent = new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
downPaymentValue.textContent = new Intl.NumberFormat('ru-RU').format(downPayment) + ' ₽ (' + downPaymentPercent + '%)';
termValue.textContent = term + ' лет';
const cashback = price * cashbackPercent / 100;
cashbackAmount.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(cashback)) + ' ₽';
const loanAmount = price - downPayment;
const monthlyRate = 0.06 / 12;
const payments = term * 12;
const monthly = loanAmount * monthlyRate * Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
monthlyPayment.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(monthly)) + ' ₽';
}
updateCalculator();
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});

// From script-news.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
setupDropdowns();
setupTypewriter();
initCarousels();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceRange = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');
const downPaymentRange = document.getElementById('downPaymentRange');
const downPaymentValue = document.getElementById('downPaymentValue');
const termRange = document.getElementById('termRange');
const termValue = document.getElementById('termValue');
const cashbackAmount = document.getElementById('cashbackAmount');
const monthlyPayment = document.getElementById('monthlyPayment');
const price = parseInt(priceRange.value);
const downPayment = parseInt(downPaymentRange.value);
const downPaymentPercent = Math.round((downPayment / price) * 100);
const term = parseInt(termRange.value);
const cashbackPercent = 2.5;
priceValue.textContent = new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
downPaymentValue.textContent = new Intl.NumberFormat('ru-RU').format(downPayment) + ' ₽ (' + downPaymentPercent + '%)';
termValue.textContent = term + ' лет';
const cashback = price * cashbackPercent / 100;
cashbackAmount.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(cashback)) + ' ₽';
const loanAmount = price - downPayment;
const monthlyRate = 0.06 / 12;
const payments = term * 12;
const monthly = loanAmount * monthlyRate * Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
monthlyPayment.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(monthly)) + ' ₽';
}
updateCalculator();
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});

// From script-object.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
new Swiper('.heroSwiper', {
loop: true,
pagination: {
el: '.heroSwiper .swiper-pagination',
clickable: true,
},
navigation: {
nextEl: '.heroSwiper .swiper-button-next',
prevEl: '.heroSwiper .swiper-button-prev',
},
});
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
const activeCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
const activeSelects = Array.from(document.querySelectorAll('select'))
.filter(select => select.value !== '');
const activeTextInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'))
.filter(input => input.value !== '');
const totalFilters = activeCheckboxes.length + activeSelects.length + activeTextInputs.length;
const badge = document.getElementById('activeFilterBadge');
if (totalFilters > 0) {
badge.textContent = totalFilters;
badge.classList.remove('hidden');
} else {
badge.classList.add('hidden');
}
}
document.querySelectorAll('input[type="checkbox"], select, input[type="text"], input[type="number"]').forEach(element => {
});
setupDropdowns();
setupTypewriter();
initCarousels();
updateActiveFiltersCount();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceRange = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');
const downPaymentRange = document.getElementById('downPaymentRange');
const downPaymentValue = document.getElementById('downPaymentValue');
const termRange = document.getElementById('termRange');
const termValue = document.getElementById('termValue');
const cashbackAmount = document.getElementById('cashbackAmount');
const monthlyPayment = document.getElementById('monthlyPayment');
const price = parseInt(priceRange.value);
const downPayment = parseInt(downPaymentRange.value);
const downPaymentPercent = Math.round((downPayment / price) * 100);
const term = parseInt(termRange.value);
const cashbackPercent = 2.5;
priceValue.textContent = new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
downPaymentValue.textContent = new Intl.NumberFormat('ru-RU').format(downPayment) + ' ₽ (' + downPaymentPercent + '%)';
termValue.textContent = term + ' лет';
const cashback = price * cashbackPercent / 100;
cashbackAmount.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(cashback)) + ' ₽';
const loanAmount = price - downPayment;
const monthlyRate = 0.06 / 12;
const payments = term * 12;
const monthly = loanAmount * monthlyRate * Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
monthlyPayment.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(monthly)) + ' ₽';
}
updateCalculator();
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});

// From script-partners.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
setupDropdowns();
setupTypewriter();
initCarousels();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceRange = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');
const downPaymentRange = document.getElementById('downPaymentRange');
const downPaymentValue = document.getElementById('downPaymentValue');
const termRange = document.getElementById('termRange');
const termValue = document.getElementById('termValue');
const cashbackAmount = document.getElementById('cashbackAmount');
const monthlyPayment = document.getElementById('monthlyPayment');
const price = parseInt(priceRange.value);
const downPayment = parseInt(downPaymentRange.value);
const downPaymentPercent = Math.round((downPayment / price) * 100);
const term = parseInt(termRange.value);
const cashbackPercent = 2.5;
priceValue.textContent = new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
downPaymentValue.textContent = new Intl.NumberFormat('ru-RU').format(downPayment) + ' ₽ (' + downPaymentPercent + '%)';
termValue.textContent = term + ' лет';
const cashback = price * cashbackPercent / 100;
cashbackAmount.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(cashback)) + ' ₽';
const loanAmount = price - downPayment;
const monthlyRate = 0.06 / 12;
const payments = term * 12;
const monthly = loanAmount * monthlyRate * Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
monthlyPayment.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(monthly)) + ' ₽';
}
updateCalculator();
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});

// From script-properties-card.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const panel = document.getElementById('advancedParams');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-plus-circle');
this.querySelector('i').classList.toggle('fa-minus-circle');
});
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
const activeCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
const activeSelects = Array.from(document.querySelectorAll('select'))
.filter(select => select.value !== '');
const activeTextInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'))
.filter(input => input.value !== '');
const totalFilters = activeCheckboxes.length + activeSelects.length + activeTextInputs.length;
const badge = document.getElementById('activeFilterBadge');
if (totalFilters > 0) {
badge.textContent = totalFilters;
badge.classList.remove('hidden');
} else {
badge.classList.add('hidden');
}
}
document.querySelectorAll('input[type="checkbox"], select, input[type="text"], input[type="number"]').forEach(element => {
});
setupDropdowns();
setupTypewriter();
initCarousels();
updateActiveFiltersCount();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceRange = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');
const downPaymentRange = document.getElementById('downPaymentRange');
const downPaymentValue = document.getElementById('downPaymentValue');
const termRange = document.getElementById('termRange');
const termValue = document.getElementById('termValue');
const cashbackAmount = document.getElementById('cashbackAmount');
const monthlyPayment = document.getElementById('monthlyPayment');
const price = parseInt(priceRange.value);
const downPayment = parseInt(downPaymentRange.value);
const downPaymentPercent = Math.round((downPayment / price) * 100);
const term = parseInt(termRange.value);
const cashbackPercent = 2.5;
priceValue.textContent = new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
downPaymentValue.textContent = new Intl.NumberFormat('ru-RU').format(downPayment) + ' ₽ (' + downPaymentPercent + '%)';
termValue.textContent = term + ' лет';
const cashback = price * cashbackPercent / 100;
cashbackAmount.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(cashback)) + ' ₽';
const loanAmount = price - downPayment;
const monthlyRate = 0.06 / 12;
const payments = term * 12;
const monthly = loanAmount * monthlyRate * Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
monthlyPayment.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(monthly)) + ' ₽';
}
updateCalculator();
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});

// From script-properties.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const panel = document.getElementById('advancedParams');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-plus-circle');
this.querySelector('i').classList.toggle('fa-minus-circle');
});
document.querySelectorAll('.dropdown-btn').forEach(btn => {
e.stopPropagation();
const dropdown = this.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu').forEach(m => {
if (m !== menu) m.classList.add('hidden');
});
menu.classList.toggle('hidden');
});
});
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.add('hidden');
});
});
});
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
const activeCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
const activeSelects = Array.from(document.querySelectorAll('select'))
.filter(select => select.value !== '');
const activeTextInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'))
.filter(input => input.value !== '');
const totalFilters = activeCheckboxes.length + activeSelects.length + activeTextInputs.length;
const badge = document.getElementById('activeFilterBadge');
if (totalFilters > 0) {
badge.textContent = totalFilters;
badge.classList.remove('hidden');
} else {
badge.classList.add('hidden');
}
}
document.querySelectorAll('input[type="checkbox"], select, input[type="text"], input[type="number"]').forEach(element => {
});
setupDropdowns();
setupTypewriter();
initCarousels();
updateActiveFiltersCount();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceRange = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');
const downPaymentRange = document.getElementById('downPaymentRange');
const downPaymentValue = document.getElementById('downPaymentValue');
const termRange = document.getElementById('termRange');
const termValue = document.getElementById('termValue');
const cashbackAmount = document.getElementById('cashbackAmount');
const monthlyPayment = document.getElementById('monthlyPayment');
const price = parseInt(priceRange.value);
const downPayment = parseInt(downPaymentRange.value);
const downPaymentPercent = Math.round((downPayment / price) * 100);
const term = parseInt(termRange.value);
const cashbackPercent = 2.5;
priceValue.textContent = new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
downPaymentValue.textContent = new Intl.NumberFormat('ru-RU').format(downPayment) + ' ₽ (' + downPaymentPercent + '%)';
termValue.textContent = term + ' лет';
const cashback = price * cashbackPercent / 100;
cashbackAmount.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(cashback)) + ' ₽';
const loanAmount = price - downPayment;
const monthlyRate = 0.06 / 12;
const payments = term * 12;
const monthly = loanAmount * monthlyRate * Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
monthlyPayment.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(monthly)) + ' ₽';
}
updateCalculator();
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});

// From script-registrations.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
primary: '#0088cc',
secondary: '#39f',
dark: '#17212b',
light: '#f5f5f5',
accent: '#00c6ff'
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
document.getElementById('login-tab').addEventListener('click', function() {
showLoginForm();
});
document.getElementById('register-tab').addEventListener('click', function() {
showRegisterForm();
});
document.getElementById('show-register').addEventListener('click', function() {
showRegisterForm();
});
document.getElementById('show-login').addEventListener('click', function() {
showLoginForm();
});
document.getElementById('show-forgot').addEventListener('click', function() {
document.getElementById('login-form').classList.add('hidden');
document.getElementById('register-form').classList.add('hidden');
document.getElementById('forgot-form').classList.remove('hidden');
document.getElementById('login-tab').classList.remove('tab-active');
document.getElementById('register-tab').classList.remove('tab-active');
document.getElementById('login-tab').classList.add('text-gray-500');
document.getElementById('register-tab').classList.add('text-gray-500');
});
document.getElementById('back-to-login').addEventListener('click', function() {
showLoginForm();
});
function showLoginForm() {
document.getElementById('login-form').classList.remove('hidden');
document.getElementById('register-form').classList.add('hidden');
document.getElementById('forgot-form').classList.add('hidden');
document.getElementById('login-tab').classList.add('tab-active');
document.getElementById('register-tab').classList.remove('tab-active');
document.getElementById('login-tab').classList.remove('text-gray-500');
document.getElementById('register-tab').classList.add('text-gray-500');
}
function showRegisterForm() {
document.getElementById('login-form').classList.add('hidden');
document.getElementById('register-form').classList.remove('hidden');
document.getElementById('forgot-form').classList.add('hidden');
document.getElementById('login-tab').classList.remove('tab-active');
document.getElementById('register-tab').classList.add('tab-active');
document.getElementById('login-tab').classList.add('text-gray-500');
document.getElementById('register-tab').classList.remove('text-gray-500');
}
document.querySelectorAll('[class*="fa-eye"]').forEach(icon => {
icon.addEventListener('click', function() {
const input = this.closest('.relative').querySelector('input');
if (input.type === 'password') {
input.type = 'text';
this.classList.remove('fa-eye');
this.classList.add('fa-eye-slash');
} else {
input.type = 'password';
this.classList.remove('fa-eye-slash');
this.classList.add('fa-eye');
}
});
});
document.querySelector('#forgot-form button').addEventListener('click', function(e) {
e.preventDefault();
document.getElementById('forgot-form').classList.add('hidden');
document.getElementById('success-message').classList.remove('hidden');
setTimeout(() => {
showLoginForm();
document.getElementById('success-message').classList.add('hidden');
}, 3000);
});

// From script-residential.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const swiper = new Swiper('.swiper', {
loop: true,
pagination: {
el: '.swiper-pagination',
clickable: true,
},
navigation: {
nextEl: '.swiper-button-next',
prevEl: '.swiper-button-prev',
},
});
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
const activeCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
const activeSelects = Array.from(document.querySelectorAll('select'))
.filter(select => select.value !== '');
const activeTextInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'))
.filter(input => input.value !== '');
const totalFilters = activeCheckboxes.length + activeSelects.length + activeTextInputs.length;
const badge = document.getElementById('activeFilterBadge');
if (totalFilters > 0) {
badge.textContent = totalFilters;
badge.classList.remove('hidden');
} else {
badge.classList.add('hidden');
}
}
document.querySelectorAll('input[type="checkbox"], select, input[type="text"], input[type="number"]').forEach(element => {
});
setupDropdowns();
setupTypewriter();
initCarousels();
updateActiveFiltersCount();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceRange = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');
const downPaymentRange = document.getElementById('downPaymentRange');
const downPaymentValue = document.getElementById('downPaymentValue');
const termRange = document.getElementById('termRange');
const termValue = document.getElementById('termValue');
const cashbackAmount = document.getElementById('cashbackAmount');
const monthlyPayment = document.getElementById('monthlyPayment');
const price = parseInt(priceRange.value);
const downPayment = parseInt(downPaymentRange.value);
const downPaymentPercent = Math.round((downPayment / price) * 100);
const term = parseInt(termRange.value);
const cashbackPercent = 2.5;
priceValue.textContent = new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
downPaymentValue.textContent = new Intl.NumberFormat('ru-RU').format(downPayment) + ' ₽ (' + downPaymentPercent + '%)';
termValue.textContent = term + ' лет';
const cashback = price * cashbackPercent / 100;
cashbackAmount.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(cashback)) + ' ₽';
const loanAmount = price - downPayment;
const monthlyRate = 0.06 / 12;
const payments = term * 12;
const monthly = loanAmount * monthlyRate * Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
monthlyPayment.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(monthly)) + ' ₽';
}
updateCalculator();
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});

// From script-streets.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
const activeCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
const activeSelects = Array.from(document.querySelectorAll('select'))
.filter(select => select.value !== '');
const activeTextInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'))
.filter(input => input.value !== '');
const totalFilters = activeCheckboxes.length + activeSelects.length + activeTextInputs.length;
const badge = document.getElementById('activeFilterBadge');
if (totalFilters > 0) {
badge.textContent = totalFilters;
badge.classList.remove('hidden');
} else {
badge.classList.add('hidden');
}
}
document.querySelectorAll('input[type="checkbox"], select, input[type="text"], input[type="number"]').forEach(element => {
});
setupDropdowns();
setupTypewriter();
initCarousels();
updateActiveFiltersCount();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceInput = document.getElementById('price-input');
const priceSlider = document.getElementById('price');
const initialInput = document.getElementById('initial-input');
const initialSlider = document.getElementById('initial');
const termInput = document.getElementById('term-input');
const termSlider = document.getElementById('term');
const rateSelect = document.getElementById('rate');
const creditSumEl = document.getElementById('credit-sum');
const monthlyPaymentEl = document.getElementById('monthly-payment');
const overpaymentEl = document.getElementById('overpayment');
const cashbackEl = document.getElementById('cashback');
const cashbackCheckbox = document.querySelector('input[name="cashback"]');
let value = input.value.replace(/\s/g, '');
if (!isNaN(value)) {
slider.value = value;
updateCalculator();
}
});
input.value = formatFn(slider.value);
updateCalculator();
});
}
return parseInt(value).toLocaleString('ru-RU');
}
return value;
}
connectInputAndSlider(priceInput, priceSlider, formatPrice);
connectInputAndSlider(initialInput, initialSlider, formatPercent);
connectInputAndSlider(termInput, termSlider, formatPercent);
const price = parseInt(priceInput.value.replace(/\s/g, '')) || 5000000;
const initialPercent = parseInt(initialSlider.value) || 15;
const termYears = parseInt(termSlider.value) || 15;
const ratePercent = parseFloat(rateSelect.value) || 14.99;
const cashbackPercentage = 2;
let loanAmount;
const programType = rateSelect.options[rateSelect.selectedIndex].text;
if (programType.includes('Семейная') || programType.includes('Сельская')) {
const maxLoan = 6000000;
const requiredDownPayment = Math.max(0, price - maxLoan);
const calculatedDownPayment = price * initialPercent / 100;
const effectiveDownPayment = Math.max(requiredDownPayment, calculatedDownPayment);
loanAmount = price - effectiveDownPayment;
if (calculatedDownPayment < requiredDownPayment) {
initialInput.classList.add('border-red-500');
} else {
initialInput.classList.remove('border-red-500');
}
}
else if (programType.includes('IT')) {
const maxLoan = 9000000;
const requiredDownPayment = Math.max(0, price - maxLoan);
const calculatedDownPayment = price * initialPercent / 100;
const effectiveDownPayment = Math.max(requiredDownPayment, calculatedDownPayment);
loanAmount = price - effectiveDownPayment;
if (calculatedDownPayment < requiredDownPayment) {
initialInput.classList.add('border-red-500');
} else {
initialInput.classList.remove('border-red-500');
}
}
else {
loanAmount = price * (100 - initialPercent) / 100;
initialInput.classList.remove('border-red-500');
}
const monthlyRate = ratePercent / 100 / 12;
const payments = termYears * 12;
const monthlyPayment = loanAmount * monthlyRate *
Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
const totalPayment = monthlyPayment * payments;
const totalOverpayment = totalPayment - loanAmount;
let cashback = 0;
if (cashbackCheckbox.checked) {
cashback = price * cashbackPercentage / 100;
}
creditSumEl.textContent = formatPrice(Math.round(loanAmount)) + ' ₽';
monthlyPaymentEl.textContent = formatPrice(Math.round(monthlyPayment)) + ' ₽';
overpaymentEl.textContent = formatPrice(Math.round(totalOverpayment)) + ' ₽';
cashbackEl.textContent = formatPrice(Math.round(cashback)) + ' ₽';
}
[priceSlider, initialSlider, termSlider, rateSelect, cashbackCheckbox].forEach(el => {
});
updateCalculator();
});
const initialInput = document.getElementById('initial-input');
const initialSlider = document.getElementById('initial');
const currentValue = parseInt(initialInput.value) || 0;
const price = parseInt(document.getElementById('price-input').value.replace(/\s/g, '')) || 8000000;
const programType = document.getElementById('rate').options[document.getElementById('rate').selectedIndex].text;
let newValue = currentValue + 1;
let maxValue = 40;
if (programType.includes('Семейная') || programType.includes('Сельская')) {
maxValue = Math.min(40, Math.max(100 - (6000000 / price) * 100, 0));
} else if (programType.includes('IT')) {
maxValue = Math.min(40, Math.max(100 - (9000000 / price) * 100, 0));
}
if (newValue > maxValue) {
newValue = maxValue;
}
if (newValue <= maxValue) {
initialInput.value = newValue;
initialSlider.value = newValue;
document.querySelector('input[name="initial-percent"]').value = newValue;
updateCalculator();
}
}
const initialInput = document.getElementById('initial-input');
const currentValue = parseInt(initialInput.value) || 0;
const minValue = 0;
if (currentValue > minValue) {
const newValue = currentValue - 1;
initialInput.value = newValue;
document.getElementById('initial').value = newValue;
document.querySelector('input[name="initial-percent"]').value = newValue;
updateCalculator();
}
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});
const mapContainer = document.getElementById('districtMap');
const currentDistrict = "Черемушки (ЧМР)";
const districtCoords = [
[38.9730, 45.0370],
[38.9770, 45.0390],
[38.9790, 45.0340],
[38.9750, 45.0310],
[38.9710, 45.0340]
];
console.log(`Карта района "${currentDistrict}" инициализирована`);
}
document.querySelectorAll('section.faq button').forEach(button => {
const answer = button.nextElementSibling;
const icon = button.querySelector('i');
if (answer.style.display === 'none' || !answer.style.display) {
answer.style.display = 'block';
icon.classList.remove('fa-chevron-down');
icon.classList.add('fa-chevron-up');
} else {
answer.style.display = 'none';
icon.classList.remove('fa-chevron-up');
icon.classList.add('fa-chevron-down');
}
});
});
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
e.preventDefault();
document.querySelector(this.getAttribute('href')).scrollIntoView({
behavior: 'smooth'
});
});
});
const initGallery = () => {
const galleryContainer = document.querySelector('.gallery-container');
const gallerySlides = document.querySelectorAll('.gallery-slide');
const galleryNavButtons = document.querySelectorAll('.gallery-nav button');
if (!galleryContainer) return;
galleryNavButtons[0].classList.add('bg-blue-600');
galleryNavButtons[0].classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryNavButtons.forEach(button => {
const slideIndex = parseInt(button.getAttribute('data-slide'));
const slide = gallerySlides[slideIndex];
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
button.classList.add('bg-blue-600');
button.classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryContainer.scrollTo({
left: slide.offsetLeft - galleryContainer.offsetLeft - 16,
behavior: 'smooth'
});
});
});
const scrollPosition = galleryContainer.scrollLeft + galleryContainer.offsetWidth / 2;
gallerySlides.forEach((slide, index) => {
const slideStart = slide.offsetLeft - galleryContainer.offsetLeft;
const slideEnd = slideStart + slide.offsetWidth;
if (scrollPosition > slideStart && scrollPosition < slideEnd) {
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
galleryNavButtons[index].classList.add('bg-blue-600');
galleryNavButtons[index].classList.remove('bg-blue-200', 'hover:bg-blue-400');
}
});
});
let touchStartX = 0;
let touchEndX = 0;
touchStartX = e.changedTouches[0].screenX;
}, {passive: true});
touchEndX = e.changedTouches[0].screenX;
handleSwipe();
}, {passive: true});
if (touchEndX < touchStartX - 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex < gallerySlides.length - 1) {
galleryNavButtons[currentSlideIndex + 1].click();
}
}
if (touchEndX > touchStartX + 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex > 0) {
galleryNavButtons[currentSlideIndex - 1].click();
}
}
}
};
initGallery();
alert('Функция "Показать границы" будет работать с реальным API Яндекс.Карт');
});
alert('Функция "Основные объекты" будет работать с реальным API Яндекс.Карт');
});
});

// From script-rural-mortgage.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
const activeCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
const activeSelects = Array.from(document.querySelectorAll('select'))
.filter(select => select.value !== '');
const activeTextInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'))
.filter(input => input.value !== '');
const totalFilters = activeCheckboxes.length + activeSelects.length + activeTextInputs.length;
const badge = document.getElementById('activeFilterBadge');
if (totalFilters > 0) {
badge.textContent = totalFilters;
badge.classList.remove('hidden');
} else {
badge.classList.add('hidden');
}
}
document.querySelectorAll('input[type="checkbox"], select, input[type="text"], input[type="number"]').forEach(element => {
});
setupDropdowns();
setupTypewriter();
initCarousels();
updateActiveFiltersCount();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceInput = document.getElementById('price-input');
const priceSlider = document.getElementById('price');
const initialInput = document.getElementById('initial-input');
const initialSlider = document.getElementById('initial');
const termInput = document.getElementById('term-input');
const termSlider = document.getElementById('term');
const rateSelect = document.getElementById('rate');
const creditSumEl = document.getElementById('credit-sum');
const monthlyPaymentEl = document.getElementById('monthly-payment');
const overpaymentEl = document.getElementById('overpayment');
const cashbackEl = document.getElementById('cashback');
const cashbackCheckbox = document.querySelector('input[name="cashback"]');
let value = input.value.replace(/\s/g, '');
if (!isNaN(value)) {
slider.value = value;
updateCalculator();
}
});
input.value = formatFn(slider.value);
updateCalculator();
});
}
return parseInt(value).toLocaleString('ru-RU');
}
return value;
}
connectInputAndSlider(priceInput, priceSlider, formatPrice);
connectInputAndSlider(initialInput, initialSlider, formatPercent);
connectInputAndSlider(termInput, termSlider, formatPercent);
const price = parseInt(priceInput.value.replace(/\s/g, '')) || 5000000;
const initialPercent = parseInt(initialSlider.value) || 15;
const termYears = parseInt(termSlider.value) || 15;
const ratePercent = parseFloat(rateSelect.value) || 14.99;
const cashbackPercentage = 2;
let loanAmount;
const programType = rateSelect.options[rateSelect.selectedIndex].text;
if (programType.includes('Семейная') || programType.includes('Сельская')) {
const maxLoan = 6000000;
const requiredDownPayment = Math.max(0, price - maxLoan);
const calculatedDownPayment = price * initialPercent / 100;
const effectiveDownPayment = Math.max(requiredDownPayment, calculatedDownPayment);
loanAmount = price - effectiveDownPayment;
if (calculatedDownPayment < requiredDownPayment) {
initialInput.classList.add('border-red-500');
} else {
initialInput.classList.remove('border-red-500');
}
}
else if (programType.includes('IT')) {
const maxLoan = 9000000;
const requiredDownPayment = Math.max(0, price - maxLoan);
const calculatedDownPayment = price * initialPercent / 100;
const effectiveDownPayment = Math.max(requiredDownPayment, calculatedDownPayment);
loanAmount = price - effectiveDownPayment;
if (calculatedDownPayment < requiredDownPayment) {
initialInput.classList.add('border-red-500');
} else {
initialInput.classList.remove('border-red-500');
}
}
else {
loanAmount = price * (100 - initialPercent) / 100;
initialInput.classList.remove('border-red-500');
}
const monthlyRate = ratePercent / 100 / 12;
const payments = termYears * 12;
const monthlyPayment = loanAmount * monthlyRate *
Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
const totalPayment = monthlyPayment * payments;
const totalOverpayment = totalPayment - loanAmount;
let cashback = 0;
if (cashbackCheckbox.checked) {
cashback = price * cashbackPercentage / 100;
}
creditSumEl.textContent = formatPrice(Math.round(loanAmount)) + ' ₽';
monthlyPaymentEl.textContent = formatPrice(Math.round(monthlyPayment)) + ' ₽';
overpaymentEl.textContent = formatPrice(Math.round(totalOverpayment)) + ' ₽';
cashbackEl.textContent = formatPrice(Math.round(cashback)) + ' ₽';
}
[priceSlider, initialSlider, termSlider, rateSelect, cashbackCheckbox].forEach(el => {
});
updateCalculator();
});
const initialInput = document.getElementById('initial-input');
const initialSlider = document.getElementById('initial');
const currentValue = parseInt(initialInput.value) || 0;
const price = parseInt(document.getElementById('price-input').value.replace(/\s/g, '')) || 8000000;
const programType = document.getElementById('rate').options[document.getElementById('rate').selectedIndex].text;
let newValue = currentValue + 1;
let maxValue = 40;
if (programType.includes('Семейная') || programType.includes('Сельская')) {
maxValue = Math.min(40, Math.max(100 - (6000000 / price) * 100, 0));
} else if (programType.includes('IT')) {
maxValue = Math.min(40, Math.max(100 - (9000000 / price) * 100, 0));
}
if (newValue > maxValue) {
newValue = maxValue;
}
if (newValue <= maxValue) {
initialInput.value = newValue;
initialSlider.value = newValue;
document.querySelector('input[name="initial-percent"]').value = newValue;
updateCalculator();
}
}
const initialInput = document.getElementById('initial-input');
const currentValue = parseInt(initialInput.value) || 0;
const minValue = 0;
if (currentValue > minValue) {
const newValue = currentValue - 1;
initialInput.value = newValue;
document.getElementById('initial').value = newValue;
document.querySelector('input[name="initial-percent"]').value = newValue;
updateCalculator();
}
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});
const mapContainer = document.getElementById('districtMap');
const currentDistrict = "Черемушки (ЧМР)";
const districtCoords = [
[38.9730, 45.0370],
[38.9770, 45.0390],
[38.9790, 45.0340],
[38.9750, 45.0310],
[38.9710, 45.0340]
];
console.log(`Карта района "${currentDistrict}" инициализирована`);
}
document.querySelectorAll('section.faq button').forEach(button => {
const answer = button.nextElementSibling;
const icon = button.querySelector('i');
if (answer.style.display === 'none' || !answer.style.display) {
answer.style.display = 'block';
icon.classList.remove('fa-chevron-down');
icon.classList.add('fa-chevron-up');
} else {
answer.style.display = 'none';
icon.classList.remove('fa-chevron-up');
icon.classList.add('fa-chevron-down');
}
});
});
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
e.preventDefault();
document.querySelector(this.getAttribute('href')).scrollIntoView({
behavior: 'smooth'
});
});
});
const initGallery = () => {
const galleryContainer = document.querySelector('.gallery-container');
const gallerySlides = document.querySelectorAll('.gallery-slide');
const galleryNavButtons = document.querySelectorAll('.gallery-nav button');
if (!galleryContainer) return;
galleryNavButtons[0].classList.add('bg-blue-600');
galleryNavButtons[0].classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryNavButtons.forEach(button => {
const slideIndex = parseInt(button.getAttribute('data-slide'));
const slide = gallerySlides[slideIndex];
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
button.classList.add('bg-blue-600');
button.classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryContainer.scrollTo({
left: slide.offsetLeft - galleryContainer.offsetLeft - 16,
behavior: 'smooth'
});
});
});
const scrollPosition = galleryContainer.scrollLeft + galleryContainer.offsetWidth / 2;
gallerySlides.forEach((slide, index) => {
const slideStart = slide.offsetLeft - galleryContainer.offsetLeft;
const slideEnd = slideStart + slide.offsetWidth;
if (scrollPosition > slideStart && scrollPosition < slideEnd) {
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
galleryNavButtons[index].classList.add('bg-blue-600');
galleryNavButtons[index].classList.remove('bg-blue-200', 'hover:bg-blue-400');
}
});
});
let touchStartX = 0;
let touchEndX = 0;
touchStartX = e.changedTouches[0].screenX;
}, {passive: true});
touchEndX = e.changedTouches[0].screenX;
handleSwipe();
}, {passive: true});
if (touchEndX < touchStartX - 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex < gallerySlides.length - 1) {
galleryNavButtons[currentSlideIndex + 1].click();
}
}
if (touchEndX > touchStartX + 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex > 0) {
galleryNavButtons[currentSlideIndex - 1].click();
}
}
}
};
initGallery();
alert('Функция "Показать границы" будет работать с реальным API Яндекс.Карт');
});
alert('Функция "Основные объекты" будет работать с реальным API Яндекс.Карт');
});
});

// From script-tsentralnyy.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
const activeCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
const activeSelects = Array.from(document.querySelectorAll('select'))
.filter(select => select.value !== '');
const activeTextInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'))
.filter(input => input.value !== '');
const totalFilters = activeCheckboxes.length + activeSelects.length + activeTextInputs.length;
const badge = document.getElementById('activeFilterBadge');
if (totalFilters > 0) {
badge.textContent = totalFilters;
badge.classList.remove('hidden');
} else {
badge.classList.add('hidden');
}
}
document.querySelectorAll('input[type="checkbox"], select, input[type="text"], input[type="number"]').forEach(element => {
});
setupDropdowns();
setupTypewriter();
initCarousels();
updateActiveFiltersCount();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceRange = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');
const downPaymentRange = document.getElementById('downPaymentRange');
const downPaymentValue = document.getElementById('downPaymentValue');
const termRange = document.getElementById('termRange');
const termValue = document.getElementById('termValue');
const cashbackAmount = document.getElementById('cashbackAmount');
const monthlyPayment = document.getElementById('monthlyPayment');
const price = parseInt(priceRange.value);
const downPayment = parseInt(downPaymentRange.value);
const downPaymentPercent = Math.round((downPayment / price) * 100);
const term = parseInt(termRange.value);
const cashbackPercent = 2.5;
priceValue.textContent = new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
downPaymentValue.textContent = new Intl.NumberFormat('ru-RU').format(downPayment) + ' ₽ (' + downPaymentPercent + '%)';
termValue.textContent = term + ' лет';
const cashback = price * cashbackPercent / 100;
cashbackAmount.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(cashback)) + ' ₽';
const loanAmount = price - downPayment;
const monthlyRate = 0.06 / 12;
const payments = term * 12;
const monthly = loanAmount * monthlyRate * Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
monthlyPayment.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(monthly)) + ' ₽';
}
updateCalculator();
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});
const mapContainer = document.getElementById('districtMap');
const currentDistrict = "Черемушки (ЧМР)";
const districtCoords = [
[38.9730, 45.0370],
[38.9770, 45.0390],
[38.9790, 45.0340],
[38.9750, 45.0310],
[38.9710, 45.0340]
];
console.log(`Карта района "${currentDistrict}" инициализирована`);
}
document.querySelectorAll('section.faq button').forEach(button => {
const answer = button.nextElementSibling;
const icon = button.querySelector('i');
if (answer.style.display === 'none' || !answer.style.display) {
answer.style.display = 'block';
icon.classList.remove('fa-chevron-down');
icon.classList.add('fa-chevron-up');
} else {
answer.style.display = 'none';
icon.classList.remove('fa-chevron-up');
icon.classList.add('fa-chevron-down');
}
});
});
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
e.preventDefault();
document.querySelector(this.getAttribute('href')).scrollIntoView({
behavior: 'smooth'
});
});
});
const initGallery = () => {
const galleryContainer = document.querySelector('.gallery-container');
const gallerySlides = document.querySelectorAll('.gallery-slide');
const galleryNavButtons = document.querySelectorAll('.gallery-nav button');
if (!galleryContainer) return;
galleryNavButtons[0].classList.add('bg-blue-600');
galleryNavButtons[0].classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryNavButtons.forEach(button => {
const slideIndex = parseInt(button.getAttribute('data-slide'));
const slide = gallerySlides[slideIndex];
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
button.classList.add('bg-blue-600');
button.classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryContainer.scrollTo({
left: slide.offsetLeft - galleryContainer.offsetLeft - 16,
behavior: 'smooth'
});
});
});
const scrollPosition = galleryContainer.scrollLeft + galleryContainer.offsetWidth / 2;
gallerySlides.forEach((slide, index) => {
const slideStart = slide.offsetLeft - galleryContainer.offsetLeft;
const slideEnd = slideStart + slide.offsetWidth;
if (scrollPosition > slideStart && scrollPosition < slideEnd) {
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
galleryNavButtons[index].classList.add('bg-blue-600');
galleryNavButtons[index].classList.remove('bg-blue-200', 'hover:bg-blue-400');
}
});
});
let touchStartX = 0;
let touchEndX = 0;
touchStartX = e.changedTouches[0].screenX;
}, {passive: true});
touchEndX = e.changedTouches[0].screenX;
handleSwipe();
}, {passive: true});
if (touchEndX < touchStartX - 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex < gallerySlides.length - 1) {
galleryNavButtons[currentSlideIndex + 1].click();
}
}
if (touchEndX > touchStartX + 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex > 0) {
galleryNavButtons[currentSlideIndex - 1].click();
}
}
}
};
initGallery();
alert('Функция "Показать границы" будет работать с реальным API Яндекс.Карт');
});
alert('Функция "Основные объекты" будет работать с реальным API Яндекс.Карт');
});
});

// From script-v2lk.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
primary: '#0088CC',
secondary: '#39F',
dark: '#222',
light: '#F5F5F5',
accent: '#FF6B00'
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const notificationButtons = [
document.getElementById('notification-button'),
document.getElementById('notification-button-mobile')
];
const notificationBadges = [
document.getElementById('notification-badge'),
document.getElementById('notification-badge-mobile')
];
const notificationDropdown = document.getElementById('notification-dropdown');
const notificationDropdownMobile = document.getElementById('notification-dropdown-mobile');
if (dropdown.classList.contains('show')) {
dropdown.classList.remove('show');
setTimeout(() => {
dropdown.style.display = 'none';
}, 300);
} else {
dropdown.style.display = 'block';
setTimeout(() => {
dropdown.classList.add('show');
}, 10);
notificationBadges.forEach(badge => {
if (badge) badge.classList.add('hidden');
});
}
}
toggleDropdown(notificationDropdown);
}
toggleDropdown(notificationDropdownMobile);
}
if (notificationDropdown.classList.contains('show')) {
notificationDropdown.classList.remove('show');
setTimeout(() => {
notificationDropdown.style.display = 'none';
}, 300);
}
if (notificationDropdownMobile.classList.contains('show')) {
notificationDropdownMobile.classList.remove('show');
setTimeout(() => {
notificationDropdownMobile.style.display = 'none';
}, 300);
}
}
const desktopButton = document.getElementById('notification-button');
const desktopButton2 = document.getElementById('notification-button-2');
if (desktopButton) {
e.stopPropagation();
toggleNotifications();
});
}
if (desktopButton2) {
e.stopPropagation();
toggleNotifications();
});
}
const mobileButton = document.getElementById('notification-button-mobile');
if (mobileButton) {
e.stopPropagation();
toggleNotificationsMobile();
});
}
const desktopBadge = document.getElementById('notification-badge');
const mobileBadge = document.getElementById('notification-badge-mobile');
if (desktopBadge) {
e.stopPropagation();
toggleNotifications();
});
}
if (mobileBadge) {
e.stopPropagation();
toggleNotificationsMobile();
});
}
closeNotifications();
});
e.stopPropagation();
});
notificationBadge.textContent = count;
notificationBadge.classList.remove('hidden');
}
const userMenuButton = document.getElementById('user-menu-button');
const userMenu = document.getElementById('user-menu');
e.stopPropagation();
userMenu.classList.toggle('hidden');
});
userMenu.classList.add('hidden');
});
const dropdownButton = document.getElementById('contact-dropdown-button');
const dropdownMenu = document.getElementById('contact-dropdown-menu');
e.stopPropagation();
dropdownMenu.classList.toggle('hidden');
});
dropdownMenu.classList.add('hidden');
});
const pages = {
'cashback': document.getElementById('cashback-page'),
'applications': document.getElementById('applications-page'),
'favorites': document.getElementById('favorites-page'),
'collections': document.getElementById('collections-page'),
'settings': document.getElementById('settings-page'),
'manager': document.getElementById('manager-page'),
'documents': document.getElementById('documents-page'),
'placeholder': document.getElementById('placeholder-page'),
'cashback': document.getElementById('cashback')
};
const statsCards = document.querySelector('.grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-4.gap-4.mb-6');
const mainSections = document.querySelector('.grid.grid-cols-1.lg\\:grid-cols-3.gap-6');
Object.values(pages).forEach(page => {
page.classList.add('hidden');
});
if (pages[pageId]) {
pages[pageId].classList.remove('hidden');
}
const showMainSections = !pageId;
statsCards.classList.toggle('hidden', !showMainSections);
mainSections.classList.toggle('hidden', !showMainSections);
document.querySelectorAll('.sidebar-item').forEach(item => {
item.classList.remove('active');
if (item.querySelector(`[data-page="${pageId}"]`)) {
item.classList.add('active');
}
});
}
Object.values(pages).forEach(page => {
page.classList.add('hidden');
});
if (pages[pageId]) {
pages[pageId].classList.remove('hidden');
}
const showMainCards = !pageId;
statsCards.classList.toggle('hidden', !showMainCards);
mainSections.classList.toggle('hidden', !showMainCards);
document.querySelectorAll('.sidebar-item').forEach(item => {
item.classList.remove('active');
if (item.querySelector(`[data-page="${pageId}"]`)) {
item.classList.add('active');
}
});
}
document.querySelectorAll('[data-page]').forEach(link => {
e.preventDefault();
const pageId = this.getAttribute('data-page');
showPage(pageId);
window.location.hash = pageId;
});
});
if (!e.target.closest('[data-page]')) {
e.preventDefault();
showPage('');
window.location.hash = '';
}
});
const pageId = window.location.hash.substring(1);
showPage(pageId);
});
const initialPage = window.location.hash.substring(1);
showPage(initialPage);
});
const newAppBtn = document.getElementById('new-application-btn');
const newAppDropdown = document.getElementById('new-application-dropdown');
if (newAppBtn && newAppDropdown) {
e.stopPropagation();
newAppDropdown.classList.toggle('hidden');
});
newAppDropdown.classList.add('hidden');
});
e.stopPropagation();
});
}
});
document.getElementById('new-application-modal').classList.remove('hidden');
});
document.getElementById('new-application-modal').classList.add('hidden');
});
if (e.target === this) {
this.classList.add('hidden');
}
});

// From script-votochno-kruglikovskii.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
const activeCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
const activeSelects = Array.from(document.querySelectorAll('select'))
.filter(select => select.value !== '');
const activeTextInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'))
.filter(input => input.value !== '');
const totalFilters = activeCheckboxes.length + activeSelects.length + activeTextInputs.length;
const badge = document.getElementById('activeFilterBadge');
if (totalFilters > 0) {
badge.textContent = totalFilters;
badge.classList.remove('hidden');
} else {
badge.classList.add('hidden');
}
}
document.querySelectorAll('input[type="checkbox"], select, input[type="text"], input[type="number"]').forEach(element => {
});
setupDropdowns();
setupTypewriter();
initCarousels();
updateActiveFiltersCount();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceRange = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');
const downPaymentRange = document.getElementById('downPaymentRange');
const downPaymentValue = document.getElementById('downPaymentValue');
const termRange = document.getElementById('termRange');
const termValue = document.getElementById('termValue');
const cashbackAmount = document.getElementById('cashbackAmount');
const monthlyPayment = document.getElementById('monthlyPayment');
const price = parseInt(priceRange.value);
const downPayment = parseInt(downPaymentRange.value);
const downPaymentPercent = Math.round((downPayment / price) * 100);
const term = parseInt(termRange.value);
const cashbackPercent = 2.5;
priceValue.textContent = new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
downPaymentValue.textContent = new Intl.NumberFormat('ru-RU').format(downPayment) + ' ₽ (' + downPaymentPercent + '%)';
termValue.textContent = term + ' лет';
const cashback = price * cashbackPercent / 100;
cashbackAmount.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(cashback)) + ' ₽';
const loanAmount = price - downPayment;
const monthlyRate = 0.06 / 12;
const payments = term * 12;
const monthly = loanAmount * monthlyRate * Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
monthlyPayment.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(monthly)) + ' ₽';
}
updateCalculator();
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});
const mapContainer = document.getElementById('districtMap');
const currentDistrict = "Черемушки (ЧМР)";
const districtCoords = [
[38.9730, 45.0370],
[38.9770, 45.0390],
[38.9790, 45.0340],
[38.9750, 45.0310],
[38.9710, 45.0340]
];
console.log(`Карта района "${currentDistrict}" инициализирована`);
}
document.querySelectorAll('section.faq button').forEach(button => {
const answer = button.nextElementSibling;
const icon = button.querySelector('i');
if (answer.style.display === 'none' || !answer.style.display) {
answer.style.display = 'block';
icon.classList.remove('fa-chevron-down');
icon.classList.add('fa-chevron-up');
} else {
answer.style.display = 'none';
icon.classList.remove('fa-chevron-up');
icon.classList.add('fa-chevron-down');
}
});
});
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
e.preventDefault();
document.querySelector(this.getAttribute('href')).scrollIntoView({
behavior: 'smooth'
});
});
});
const initGallery = () => {
const galleryContainer = document.querySelector('.gallery-container');
const gallerySlides = document.querySelectorAll('.gallery-slide');
const galleryNavButtons = document.querySelectorAll('.gallery-nav button');
if (!galleryContainer) return;
galleryNavButtons[0].classList.add('bg-blue-600');
galleryNavButtons[0].classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryNavButtons.forEach(button => {
const slideIndex = parseInt(button.getAttribute('data-slide'));
const slide = gallerySlides[slideIndex];
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
button.classList.add('bg-blue-600');
button.classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryContainer.scrollTo({
left: slide.offsetLeft - galleryContainer.offsetLeft - 16,
behavior: 'smooth'
});
});
});
const scrollPosition = galleryContainer.scrollLeft + galleryContainer.offsetWidth / 2;
gallerySlides.forEach((slide, index) => {
const slideStart = slide.offsetLeft - galleryContainer.offsetLeft;
const slideEnd = slideStart + slide.offsetWidth;
if (scrollPosition > slideStart && scrollPosition < slideEnd) {
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
galleryNavButtons[index].classList.add('bg-blue-600');
galleryNavButtons[index].classList.remove('bg-blue-200', 'hover:bg-blue-400');
}
});
});
let touchStartX = 0;
let touchEndX = 0;
touchStartX = e.changedTouches[0].screenX;
}, {passive: true});
touchEndX = e.changedTouches[0].screenX;
handleSwipe();
}, {passive: true});
if (touchEndX < touchStartX - 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex < gallerySlides.length - 1) {
galleryNavButtons[currentSlideIndex + 1].click();
}
}
if (touchEndX > touchStartX + 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex > 0) {
galleryNavButtons[currentSlideIndex - 1].click();
}
}
}
};
initGallery();
alert('Функция "Показать границы" будет работать с реальным API Яндекс.Карт');
});
alert('Функция "Основные объекты" будет работать с реальным API Яндекс.Карт');
});
});

// From script-zapadny.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
const activeCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
const activeSelects = Array.from(document.querySelectorAll('select'))
.filter(select => select.value !== '');
const activeTextInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'))
.filter(input => input.value !== '');
const totalFilters = activeCheckboxes.length + activeSelects.length + activeTextInputs.length;
const badge = document.getElementById('activeFilterBadge');
if (totalFilters > 0) {
badge.textContent = totalFilters;
badge.classList.remove('hidden');
} else {
badge.classList.add('hidden');
}
}
document.querySelectorAll('input[type="checkbox"], select, input[type="text"], input[type="number"]').forEach(element => {
});
setupDropdowns();
setupTypewriter();
initCarousels();
updateActiveFiltersCount();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceRange = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');
const downPaymentRange = document.getElementById('downPaymentRange');
const downPaymentValue = document.getElementById('downPaymentValue');
const termRange = document.getElementById('termRange');
const termValue = document.getElementById('termValue');
const cashbackAmount = document.getElementById('cashbackAmount');
const monthlyPayment = document.getElementById('monthlyPayment');
const price = parseInt(priceRange.value);
const downPayment = parseInt(downPaymentRange.value);
const downPaymentPercent = Math.round((downPayment / price) * 100);
const term = parseInt(termRange.value);
const cashbackPercent = 2.5;
priceValue.textContent = new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
downPaymentValue.textContent = new Intl.NumberFormat('ru-RU').format(downPayment) + ' ₽ (' + downPaymentPercent + '%)';
termValue.textContent = term + ' лет';
const cashback = price * cashbackPercent / 100;
cashbackAmount.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(cashback)) + ' ₽';
const loanAmount = price - downPayment;
const monthlyRate = 0.06 / 12;
const payments = term * 12;
const monthly = loanAmount * monthlyRate * Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
monthlyPayment.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(monthly)) + ' ₽';
}
updateCalculator();
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});
const mapContainer = document.getElementById('districtMap');
const currentDistrict = "Черемушки (ЧМР)";
const districtCoords = [
[38.9730, 45.0370],
[38.9770, 45.0390],
[38.9790, 45.0340],
[38.9750, 45.0310],
[38.9710, 45.0340]
];
console.log(`Карта района "${currentDistrict}" инициализирована`);
}
document.querySelectorAll('section.faq button').forEach(button => {
const answer = button.nextElementSibling;
const icon = button.querySelector('i');
if (answer.style.display === 'none' || !answer.style.display) {
answer.style.display = 'block';
icon.classList.remove('fa-chevron-down');
icon.classList.add('fa-chevron-up');
} else {
answer.style.display = 'none';
icon.classList.remove('fa-chevron-up');
icon.classList.add('fa-chevron-down');
}
});
});
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
e.preventDefault();
document.querySelector(this.getAttribute('href')).scrollIntoView({
behavior: 'smooth'
});
});
});
const initGallery = () => {
const galleryContainer = document.querySelector('.gallery-container');
const gallerySlides = document.querySelectorAll('.gallery-slide');
const galleryNavButtons = document.querySelectorAll('.gallery-nav button');
if (!galleryContainer) return;
galleryNavButtons[0].classList.add('bg-blue-600');
galleryNavButtons[0].classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryNavButtons.forEach(button => {
const slideIndex = parseInt(button.getAttribute('data-slide'));
const slide = gallerySlides[slideIndex];
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
button.classList.add('bg-blue-600');
button.classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryContainer.scrollTo({
left: slide.offsetLeft - galleryContainer.offsetLeft - 16,
behavior: 'smooth'
});
});
});
const scrollPosition = galleryContainer.scrollLeft + galleryContainer.offsetWidth / 2;
gallerySlides.forEach((slide, index) => {
const slideStart = slide.offsetLeft - galleryContainer.offsetLeft;
const slideEnd = slideStart + slide.offsetWidth;
if (scrollPosition > slideStart && scrollPosition < slideEnd) {
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
galleryNavButtons[index].classList.add('bg-blue-600');
galleryNavButtons[index].classList.remove('bg-blue-200', 'hover:bg-blue-400');
}
});
});
let touchStartX = 0;
let touchEndX = 0;
touchStartX = e.changedTouches[0].screenX;
}, {passive: true});
touchEndX = e.changedTouches[0].screenX;
handleSwipe();
}, {passive: true});
if (touchEndX < touchStartX - 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex < gallerySlides.length - 1) {
galleryNavButtons[currentSlideIndex + 1].click();
}
}
if (touchEndX > touchStartX + 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex > 0) {
galleryNavButtons[currentSlideIndex - 1].click();
}
}
}
};
initGallery();
alert('Функция "Показать границы" будет работать с реальным API Яндекс.Карт');
});
alert('Функция "Основные объекты" будет работать с реальным API Яндекс.Карт');
});
});

// From script-9i-kilometr.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
const activeCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
const activeSelects = Array.from(document.querySelectorAll('select'))
.filter(select => select.value !== '');
const activeTextInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'))
.filter(input => input.value !== '');
const totalFilters = activeCheckboxes.length + activeSelects.length + activeTextInputs.length;
const badge = document.getElementById('activeFilterBadge');
if (totalFilters > 0) {
badge.textContent = totalFilters;
badge.classList.remove('hidden');
} else {
badge.classList.add('hidden');
}
}
document.querySelectorAll('input[type="checkbox"], select, input[type="text"], input[type="number"]').forEach(element => {
});
setupDropdowns();
setupTypewriter();
initCarousels();
updateActiveFiltersCount();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceRange = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');
const downPaymentRange = document.getElementById('downPaymentRange');
const downPaymentValue = document.getElementById('downPaymentValue');
const termRange = document.getElementById('termRange');
const termValue = document.getElementById('termValue');
const cashbackAmount = document.getElementById('cashbackAmount');
const monthlyPayment = document.getElementById('monthlyPayment');
const price = parseInt(priceRange.value);
const downPayment = parseInt(downPaymentRange.value);
const downPaymentPercent = Math.round((downPayment / price) * 100);
const term = parseInt(termRange.value);
const cashbackPercent = 2.5;
priceValue.textContent = new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
downPaymentValue.textContent = new Intl.NumberFormat('ru-RU').format(downPayment) + ' ₽ (' + downPaymentPercent + '%)';
termValue.textContent = term + ' лет';
const cashback = price * cashbackPercent / 100;
cashbackAmount.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(cashback)) + ' ₽';
const loanAmount = price - downPayment;
const monthlyRate = 0.06 / 12;
const payments = term * 12;
const monthly = loanAmount * monthlyRate * Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
monthlyPayment.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(monthly)) + ' ₽';
}
updateCalculator();
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});
const mapContainer = document.getElementById('districtMap');
const currentDistrict = "Черемушки (ЧМР)";
const districtCoords = [
[38.9730, 45.0370],
[38.9770, 45.0390],
[38.9790, 45.0340],
[38.9750, 45.0310],
[38.9710, 45.0340]
];
console.log(`Карта района "${currentDistrict}" инициализирована`);
}
document.querySelectorAll('section.faq button').forEach(button => {
const answer = button.nextElementSibling;
const icon = button.querySelector('i');
if (answer.style.display === 'none' || !answer.style.display) {
answer.style.display = 'block';
icon.classList.remove('fa-chevron-down');
icon.classList.add('fa-chevron-up');
} else {
answer.style.display = 'none';
icon.classList.remove('fa-chevron-up');
icon.classList.add('fa-chevron-down');
}
});
});
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
e.preventDefault();
document.querySelector(this.getAttribute('href')).scrollIntoView({
behavior: 'smooth'
});
});
});
const initGallery = () => {
const galleryContainer = document.querySelector('.gallery-container');
const gallerySlides = document.querySelectorAll('.gallery-slide');
const galleryNavButtons = document.querySelectorAll('.gallery-nav button');
if (!galleryContainer) return;
galleryNavButtons[0].classList.add('bg-blue-600');
galleryNavButtons[0].classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryNavButtons.forEach(button => {
const slideIndex = parseInt(button.getAttribute('data-slide'));
const slide = gallerySlides[slideIndex];
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
button.classList.add('bg-blue-600');
button.classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryContainer.scrollTo({
left: slide.offsetLeft - galleryContainer.offsetLeft - 16,
behavior: 'smooth'
});
});
});
const scrollPosition = galleryContainer.scrollLeft + galleryContainer.offsetWidth / 2;
gallerySlides.forEach((slide, index) => {
const slideStart = slide.offsetLeft - galleryContainer.offsetLeft;
const slideEnd = slideStart + slide.offsetWidth;
if (scrollPosition > slideStart && scrollPosition < slideEnd) {
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
galleryNavButtons[index].classList.add('bg-blue-600');
galleryNavButtons[index].classList.remove('bg-blue-200', 'hover:bg-blue-400');
}
});
});
let touchStartX = 0;
let touchEndX = 0;
touchStartX = e.changedTouches[0].screenX;
}, {passive: true});
touchEndX = e.changedTouches[0].screenX;
handleSwipe();
}, {passive: true});
if (touchEndX < touchStartX - 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex < gallerySlides.length - 1) {
galleryNavButtons[currentSlideIndex + 1].click();
}
}
if (touchEndX > touchStartX + 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex > 0) {
galleryNavButtons[currentSlideIndex - 1].click();
}
}
}
};
initGallery();
alert('Функция "Показать границы" будет работать с реальным API Яндекс.Карт');
});
alert('Функция "Основные объекты" будет работать с реальным API Яндекс.Карт');
});
});

// From script-developer.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
document.getElementById('showAllApartments').addEventListener('click', function() {
alert('Загрузка всех 120 квартир...');
});
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
const activeCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
const activeSelects = Array.from(document.querySelectorAll('select'))
.filter(select => select.value !== '');
const activeTextInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'))
.filter(input => input.value !== '');
const totalFilters = activeCheckboxes.length + activeSelects.length + activeTextInputs.length;
const badge = document.getElementById('activeFilterBadge');
if (totalFilters > 0) {
badge.textContent = totalFilters;
badge.classList.remove('hidden');
} else {
badge.classList.add('hidden');
}
}
document.querySelectorAll('input[type="checkbox"], select, input[type="text"], input[type="number"]').forEach(element => {
});
setupDropdowns();
setupTypewriter();
initCarousels();
updateActiveFiltersCount();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceRange = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');
const downPaymentRange = document.getElementById('downPaymentRange');
const downPaymentValue = document.getElementById('downPaymentValue');
const termRange = document.getElementById('termRange');
const termValue = document.getElementById('termValue');
const cashbackAmount = document.getElementById('cashbackAmount');
const monthlyPayment = document.getElementById('monthlyPayment');
const price = parseInt(priceRange.value);
const downPayment = parseInt(downPaymentRange.value);
const downPaymentPercent = Math.round((downPayment / price) * 100);
const term = parseInt(termRange.value);
const cashbackPercent = 2.5;
priceValue.textContent = new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
downPaymentValue.textContent = new Intl.NumberFormat('ru-RU').format(downPayment) + ' ₽ (' + downPaymentPercent + '%)';
termValue.textContent = term + ' лет';
const cashback = price * cashbackPercent / 100;
cashbackAmount.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(cashback)) + ' ₽';
const loanAmount = price - downPayment;
const monthlyRate = 0.06 / 12;
const payments = term * 12;
const monthly = loanAmount * monthlyRate * Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
monthlyPayment.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(monthly)) + ' ₽';
}
updateCalculator();
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});

// From script-developer-mortgage.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
const activeCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
const activeSelects = Array.from(document.querySelectorAll('select'))
.filter(select => select.value !== '');
const activeTextInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'))
.filter(input => input.value !== '');
const totalFilters = activeCheckboxes.length + activeSelects.length + activeTextInputs.length;
const badge = document.getElementById('activeFilterBadge');
if (totalFilters > 0) {
badge.textContent = totalFilters;
badge.classList.remove('hidden');
} else {
badge.classList.add('hidden');
}
}
document.querySelectorAll('input[type="checkbox"], select, input[type="text"], input[type="number"]').forEach(element => {
});
setupDropdowns();
setupTypewriter();
initCarousels();
updateActiveFiltersCount();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceInput = document.getElementById('price-input');
const priceSlider = document.getElementById('price');
const initialInput = document.getElementById('initial-input');
const initialSlider = document.getElementById('initial');
const termInput = document.getElementById('term-input');
const termSlider = document.getElementById('term');
const rateSelect = document.getElementById('rate');
const creditSumEl = document.getElementById('credit-sum');
const monthlyPaymentEl = document.getElementById('monthly-payment');
const overpaymentEl = document.getElementById('overpayment');
const cashbackEl = document.getElementById('cashback');
const cashbackCheckbox = document.querySelector('input[name="cashback"]');
let value = input.value.replace(/\s/g, '');
if (!isNaN(value)) {
slider.value = value;
updateCalculator();
}
});
input.value = formatFn(slider.value);
updateCalculator();
});
}
return parseInt(value).toLocaleString('ru-RU');
}
return value;
}
connectInputAndSlider(priceInput, priceSlider, formatPrice);
connectInputAndSlider(initialInput, initialSlider, formatPercent);
connectInputAndSlider(termInput, termSlider, formatPercent);
const price = parseInt(priceInput.value.replace(/\s/g, '')) || 5000000;
const initialPercent = parseInt(initialSlider.value) || 15;
const termYears = parseInt(termSlider.value) || 15;
const ratePercent = parseFloat(rateSelect.value) || 14.99;
const cashbackPercentage = 2;
let loanAmount;
const programType = rateSelect.options[rateSelect.selectedIndex].text;
if (programType.includes('Семейная') || programType.includes('Сельская')) {
const maxLoan = 6000000;
const requiredDownPayment = Math.max(0, price - maxLoan);
const calculatedDownPayment = price * initialPercent / 100;
const effectiveDownPayment = Math.max(requiredDownPayment, calculatedDownPayment);
loanAmount = price - effectiveDownPayment;
if (calculatedDownPayment < requiredDownPayment) {
initialInput.classList.add('border-red-500');
} else {
initialInput.classList.remove('border-red-500');
}
}
else if (programType.includes('IT')) {
const maxLoan = 9000000;
const requiredDownPayment = Math.max(0, price - maxLoan);
const calculatedDownPayment = price * initialPercent / 100;
const effectiveDownPayment = Math.max(requiredDownPayment, calculatedDownPayment);
loanAmount = price - effectiveDownPayment;
if (calculatedDownPayment < requiredDownPayment) {
initialInput.classList.add('border-red-500');
} else {
initialInput.classList.remove('border-red-500');
}
}
else {
loanAmount = price * (100 - initialPercent) / 100;
initialInput.classList.remove('border-red-500');
}
const monthlyRate = ratePercent / 100 / 12;
const payments = termYears * 12;
const monthlyPayment = loanAmount * monthlyRate *
Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
const totalPayment = monthlyPayment * payments;
const totalOverpayment = totalPayment - loanAmount;
let cashback = 0;
if (cashbackCheckbox.checked) {
cashback = price * cashbackPercentage / 100;
}
creditSumEl.textContent = formatPrice(Math.round(loanAmount)) + ' ₽';
monthlyPaymentEl.textContent = formatPrice(Math.round(monthlyPayment)) + ' ₽';
overpaymentEl.textContent = formatPrice(Math.round(totalOverpayment)) + ' ₽';
cashbackEl.textContent = formatPrice(Math.round(cashback)) + ' ₽';
}
[priceSlider, initialSlider, termSlider, rateSelect, cashbackCheckbox].forEach(el => {
});
updateCalculator();
});
const initialInput = document.getElementById('initial-input');
const initialSlider = document.getElementById('initial');
const currentValue = parseInt(initialInput.value) || 0;
const price = parseInt(document.getElementById('price-input').value.replace(/\s/g, '')) || 8000000;
const programType = document.getElementById('rate').options[document.getElementById('rate').selectedIndex].text;
let newValue = currentValue + 1;
let maxValue = 40;
if (programType.includes('Семейная') || programType.includes('Сельская')) {
maxValue = Math.min(40, Math.max(100 - (6000000 / price) * 100, 0));
} else if (programType.includes('IT')) {
maxValue = Math.min(40, Math.max(100 - (9000000 / price) * 100, 0));
}
if (newValue > maxValue) {
newValue = maxValue;
}
if (newValue <= maxValue) {
initialInput.value = newValue;
initialSlider.value = newValue;
document.querySelector('input[name="initial-percent"]').value = newValue;
updateCalculator();
}
}
const initialInput = document.getElementById('initial-input');
const currentValue = parseInt(initialInput.value) || 0;
const minValue = 0;
if (currentValue > minValue) {
const newValue = currentValue - 1;
initialInput.value = newValue;
document.getElementById('initial').value = newValue;
document.querySelector('input[name="initial-percent"]').value = newValue;
updateCalculator();
}
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});
const mapContainer = document.getElementById('districtMap');
const currentDistrict = "Черемушки (ЧМР)";
const districtCoords = [
[38.9730, 45.0370],
[38.9770, 45.0390],
[38.9790, 45.0340],
[38.9750, 45.0310],
[38.9710, 45.0340]
];
console.log(`Карта района "${currentDistrict}" инициализирована`);
}
document.querySelectorAll('section.faq button').forEach(button => {
const answer = button.nextElementSibling;
const icon = button.querySelector('i');
if (answer.style.display === 'none' || !answer.style.display) {
answer.style.display = 'block';
icon.classList.remove('fa-chevron-down');
icon.classList.add('fa-chevron-up');
} else {
answer.style.display = 'none';
icon.classList.remove('fa-chevron-up');
icon.classList.add('fa-chevron-down');
}
});
});
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
e.preventDefault();
document.querySelector(this.getAttribute('href')).scrollIntoView({
behavior: 'smooth'
});
});
});
const initGallery = () => {
const galleryContainer = document.querySelector('.gallery-container');
const gallerySlides = document.querySelectorAll('.gallery-slide');
const galleryNavButtons = document.querySelectorAll('.gallery-nav button');
if (!galleryContainer) return;
galleryNavButtons[0].classList.add('bg-blue-600');
galleryNavButtons[0].classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryNavButtons.forEach(button => {
const slideIndex = parseInt(button.getAttribute('data-slide'));
const slide = gallerySlides[slideIndex];
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
button.classList.add('bg-blue-600');
button.classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryContainer.scrollTo({
left: slide.offsetLeft - galleryContainer.offsetLeft - 16,
behavior: 'smooth'
});
});
});
const scrollPosition = galleryContainer.scrollLeft + galleryContainer.offsetWidth / 2;
gallerySlides.forEach((slide, index) => {
const slideStart = slide.offsetLeft - galleryContainer.offsetLeft;
const slideEnd = slideStart + slide.offsetWidth;
if (scrollPosition > slideStart && scrollPosition < slideEnd) {
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
galleryNavButtons[index].classList.add('bg-blue-600');
galleryNavButtons[index].classList.remove('bg-blue-200', 'hover:bg-blue-400');
}
});
});
let touchStartX = 0;
let touchEndX = 0;
touchStartX = e.changedTouches[0].screenX;
}, {passive: true});
touchEndX = e.changedTouches[0].screenX;
handleSwipe();
}, {passive: true});
if (touchEndX < touchStartX - 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex < gallerySlides.length - 1) {
galleryNavButtons[currentSlideIndex + 1].click();
}
}
if (touchEndX > touchStartX + 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex > 0) {
galleryNavButtons[currentSlideIndex - 1].click();
}
}
}
};
initGallery();
alert('Функция "Показать границы" будет работать с реальным API Яндекс.Карт');
});
alert('Функция "Основные объекты" будет работать с реальным API Яндекс.Карт');
});
});

// From script-developers.js
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
setupDropdowns();
setupTypewriter();
initCarousels();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceRange = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');
const downPaymentRange = document.getElementById('downPaymentRange');
const downPaymentValue = document.getElementById('downPaymentValue');
const termRange = document.getElementById('termRange');
const termValue = document.getElementById('termValue');
const cashbackAmount = document.getElementById('cashbackAmount');
const monthlyPayment = document.getElementById('monthlyPayment');
const price = parseInt(priceRange.value);
const downPayment = parseInt(downPaymentRange.value);
const downPaymentPercent = Math.round((downPayment / price) * 100);
const term = parseInt(termRange.value);
const cashbackPercent = 2.5;
priceValue.textContent = new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
downPaymentValue.textContent = new Intl.NumberFormat('ru-RU').format(downPayment) + ' ₽ (' + downPaymentPercent + '%)';
termValue.textContent = term + ' лет';
const cashback = price * cashbackPercent / 100;
cashbackAmount.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(cashback)) + ' ₽';
const loanAmount = price - downPayment;
const monthlyRate = 0.06 / 12;
const payments = term * 12;
const monthly = loanAmount * monthlyRate * Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
monthlyPayment.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(monthly)) + ' ₽';
}
updateCalculator();
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});

// From script-family-mortage.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
const activeCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
const activeSelects = Array.from(document.querySelectorAll('select'))
.filter(select => select.value !== '');
const activeTextInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'))
.filter(input => input.value !== '');
const totalFilters = activeCheckboxes.length + activeSelects.length + activeTextInputs.length;
const badge = document.getElementById('activeFilterBadge');
if (totalFilters > 0) {
badge.textContent = totalFilters;
badge.classList.remove('hidden');
} else {
badge.classList.add('hidden');
}
}
document.querySelectorAll('input[type="checkbox"], select, input[type="text"], input[type="number"]').forEach(element => {
});
setupDropdowns();
setupTypewriter();
initCarousels();
updateActiveFiltersCount();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceInput = document.getElementById('price-input');
const priceSlider = document.getElementById('price');
const initialInput = document.getElementById('initial-input');
const initialSlider = document.getElementById('initial');
const termInput = document.getElementById('term-input');
const termSlider = document.getElementById('term');
const rateSelect = document.getElementById('rate');
const creditSumEl = document.getElementById('credit-sum');
const monthlyPaymentEl = document.getElementById('monthly-payment');
const overpaymentEl = document.getElementById('overpayment');
const cashbackEl = document.getElementById('cashback');
const cashbackCheckbox = document.querySelector('input[name="cashback"]');
let value = input.value.replace(/\s/g, '');
if (!isNaN(value)) {
slider.value = value;
updateCalculator();
}
});
input.value = formatFn(slider.value);
updateCalculator();
});
}
return parseInt(value).toLocaleString('ru-RU');
}
return value;
}
connectInputAndSlider(priceInput, priceSlider, formatPrice);
connectInputAndSlider(initialInput, initialSlider, formatPercent);
connectInputAndSlider(termInput, termSlider, formatPercent);
const price = parseInt(priceInput.value.replace(/\s/g, '')) || 5000000;
const initialPercent = parseInt(initialSlider.value) || 15;
const termYears = parseInt(termSlider.value) || 15;
const ratePercent = parseFloat(rateSelect.value) || 14.99;
const cashbackPercentage = 2;
let loanAmount;
const programType = rateSelect.options[rateSelect.selectedIndex].text;
if (programType.includes('Семейная') || programType.includes('Сельская')) {
const maxLoan = 6000000;
const requiredDownPayment = Math.max(0, price - maxLoan);
const calculatedDownPayment = price * initialPercent / 100;
const effectiveDownPayment = Math.max(requiredDownPayment, calculatedDownPayment);
loanAmount = price - effectiveDownPayment;
if (calculatedDownPayment < requiredDownPayment) {
initialInput.classList.add('border-red-500');
} else {
initialInput.classList.remove('border-red-500');
}
}
else if (programType.includes('IT')) {
const maxLoan = 9000000;
const requiredDownPayment = Math.max(0, price - maxLoan);
const calculatedDownPayment = price * initialPercent / 100;
const effectiveDownPayment = Math.max(requiredDownPayment, calculatedDownPayment);
loanAmount = price - effectiveDownPayment;
if (calculatedDownPayment < requiredDownPayment) {
initialInput.classList.add('border-red-500');
} else {
initialInput.classList.remove('border-red-500');
}
}
else {
loanAmount = price * (100 - initialPercent) / 100;
initialInput.classList.remove('border-red-500');
}
const monthlyRate = ratePercent / 100 / 12;
const payments = termYears * 12;
const monthlyPayment = loanAmount * monthlyRate *
Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
const totalPayment = monthlyPayment * payments;
const totalOverpayment = totalPayment - loanAmount;
let cashback = 0;
if (cashbackCheckbox.checked) {
cashback = price * cashbackPercentage / 100;
}
creditSumEl.textContent = formatPrice(Math.round(loanAmount)) + ' ₽';
monthlyPaymentEl.textContent = formatPrice(Math.round(monthlyPayment)) + ' ₽';
overpaymentEl.textContent = formatPrice(Math.round(totalOverpayment)) + ' ₽';
cashbackEl.textContent = formatPrice(Math.round(cashback)) + ' ₽';
}
[priceSlider, initialSlider, termSlider, rateSelect, cashbackCheckbox].forEach(el => {
});
updateCalculator();
});
const initialInput = document.getElementById('initial-input');
const initialSlider = document.getElementById('initial');
const currentValue = parseInt(initialInput.value) || 0;
const price = parseInt(document.getElementById('price-input').value.replace(/\s/g, '')) || 8000000;
const programType = document.getElementById('rate').options[document.getElementById('rate').selectedIndex].text;
let newValue = currentValue + 1;
let maxValue = 40;
if (programType.includes('Семейная') || programType.includes('Сельская')) {
maxValue = Math.min(40, Math.max(100 - (6000000 / price) * 100, 0));
} else if (programType.includes('IT')) {
maxValue = Math.min(40, Math.max(100 - (9000000 / price) * 100, 0));
}
if (newValue > maxValue) {
newValue = maxValue;
}
if (newValue <= maxValue) {
initialInput.value = newValue;
initialSlider.value = newValue;
document.querySelector('input[name="initial-percent"]').value = newValue;
updateCalculator();
}
}
const initialInput = document.getElementById('initial-input');
const currentValue = parseInt(initialInput.value) || 0;
const minValue = 0;
if (currentValue > minValue) {
const newValue = currentValue - 1;
initialInput.value = newValue;
document.getElementById('initial').value = newValue;
document.querySelector('input[name="initial-percent"]').value = newValue;
updateCalculator();
}
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});
const mapContainer = document.getElementById('districtMap');
const currentDistrict = "Черемушки (ЧМР)";
const districtCoords = [
[38.9730, 45.0370],
[38.9770, 45.0390],
[38.9790, 45.0340],
[38.9750, 45.0310],
[38.9710, 45.0340]
];
console.log(`Карта района "${currentDistrict}" инициализирована`);
}
document.querySelectorAll('section.faq button').forEach(button => {
const answer = button.nextElementSibling;
const icon = button.querySelector('i');
if (answer.style.display === 'none' || !answer.style.display) {
answer.style.display = 'block';
icon.classList.remove('fa-chevron-down');
icon.classList.add('fa-chevron-up');
} else {
answer.style.display = 'none';
icon.classList.remove('fa-chevron-up');
icon.classList.add('fa-chevron-down');
}
});
});
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
e.preventDefault();
document.querySelector(this.getAttribute('href')).scrollIntoView({
behavior: 'smooth'
});
});
});
const initGallery = () => {
const galleryContainer = document.querySelector('.gallery-container');
const gallerySlides = document.querySelectorAll('.gallery-slide');
const galleryNavButtons = document.querySelectorAll('.gallery-nav button');
if (!galleryContainer) return;
galleryNavButtons[0].classList.add('bg-blue-600');
galleryNavButtons[0].classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryNavButtons.forEach(button => {
const slideIndex = parseInt(button.getAttribute('data-slide'));
const slide = gallerySlides[slideIndex];
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
button.classList.add('bg-blue-600');
button.classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryContainer.scrollTo({
left: slide.offsetLeft - galleryContainer.offsetLeft - 16,
behavior: 'smooth'
});
});
});
const scrollPosition = galleryContainer.scrollLeft + galleryContainer.offsetWidth / 2;
gallerySlides.forEach((slide, index) => {
const slideStart = slide.offsetLeft - galleryContainer.offsetLeft;
const slideEnd = slideStart + slide.offsetWidth;
if (scrollPosition > slideStart && scrollPosition < slideEnd) {
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
galleryNavButtons[index].classList.add('bg-blue-600');
galleryNavButtons[index].classList.remove('bg-blue-200', 'hover:bg-blue-400');
}
});
});
let touchStartX = 0;
let touchEndX = 0;
touchStartX = e.changedTouches[0].screenX;
}, {passive: true});
touchEndX = e.changedTouches[0].screenX;
handleSwipe();
}, {passive: true});
if (touchEndX < touchStartX - 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex < gallerySlides.length - 1) {
galleryNavButtons[currentSlideIndex + 1].click();
}
}
if (touchEndX > touchStartX + 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex > 0) {
galleryNavButtons[currentSlideIndex - 1].click();
}
}
}
};
initGallery();
alert('Функция "Показать границы" будет работать с реальным API Яндекс.Карт');
});
alert('Функция "Основные объекты" будет работать с реальным API Яндекс.Карт');
});
});

// From script-kkb.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
const activeCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
const activeSelects = Array.from(document.querySelectorAll('select'))
.filter(select => select.value !== '');
const activeTextInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'))
.filter(input => input.value !== '');
const totalFilters = activeCheckboxes.length + activeSelects.length + activeTextInputs.length;
const badge = document.getElementById('activeFilterBadge');
if (totalFilters > 0) {
badge.textContent = totalFilters;
badge.classList.remove('hidden');
} else {
badge.classList.add('hidden');
}
}
document.querySelectorAll('input[type="checkbox"], select, input[type="text"], input[type="number"]').forEach(element => {
});
setupDropdowns();
setupTypewriter();
initCarousels();
updateActiveFiltersCount();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceRange = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');
const downPaymentRange = document.getElementById('downPaymentRange');
const downPaymentValue = document.getElementById('downPaymentValue');
const termRange = document.getElementById('termRange');
const termValue = document.getElementById('termValue');
const cashbackAmount = document.getElementById('cashbackAmount');
const monthlyPayment = document.getElementById('monthlyPayment');
const price = parseInt(priceRange.value);
const downPayment = parseInt(downPaymentRange.value);
const downPaymentPercent = Math.round((downPayment / price) * 100);
const term = parseInt(termRange.value);
const cashbackPercent = 2.5;
priceValue.textContent = new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
downPaymentValue.textContent = new Intl.NumberFormat('ru-RU').format(downPayment) + ' ₽ (' + downPaymentPercent + '%)';
termValue.textContent = term + ' лет';
const cashback = price * cashbackPercent / 100;
cashbackAmount.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(cashback)) + ' ₽';
const loanAmount = price - downPayment;
const monthlyRate = 0.06 / 12;
const payments = term * 12;
const monthly = loanAmount * monthlyRate * Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
monthlyPayment.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(monthly)) + ' ₽';
}
updateCalculator();
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});
const mapContainer = document.getElementById('districtMap');
const currentDistrict = "Черемушки (ЧМР)";
const districtCoords = [
[38.9730, 45.0370],
[38.9770, 45.0390],
[38.9790, 45.0340],
[38.9750, 45.0310],
[38.9710, 45.0340]
];
console.log(`Карта района "${currentDistrict}" инициализирована`);
}
document.querySelectorAll('section.faq button').forEach(button => {
const answer = button.nextElementSibling;
const icon = button.querySelector('i');
if (answer.style.display === 'none' || !answer.style.display) {
answer.style.display = 'block';
icon.classList.remove('fa-chevron-down');
icon.classList.add('fa-chevron-up');
} else {
answer.style.display = 'none';
icon.classList.remove('fa-chevron-up');
icon.classList.add('fa-chevron-down');
}
});
});
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
e.preventDefault();
document.querySelector(this.getAttribute('href')).scrollIntoView({
behavior: 'smooth'
});
});
});
const initGallery = () => {
const galleryContainer = document.querySelector('.gallery-container');
const gallerySlides = document.querySelectorAll('.gallery-slide');
const galleryNavButtons = document.querySelectorAll('.gallery-nav button');
if (!galleryContainer) return;
galleryNavButtons[0].classList.add('bg-blue-600');
galleryNavButtons[0].classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryNavButtons.forEach(button => {
const slideIndex = parseInt(button.getAttribute('data-slide'));
const slide = gallerySlides[slideIndex];
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
button.classList.add('bg-blue-600');
button.classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryContainer.scrollTo({
left: slide.offsetLeft - galleryContainer.offsetLeft - 16,
behavior: 'smooth'
});
});
});
const scrollPosition = galleryContainer.scrollLeft + galleryContainer.offsetWidth / 2;
gallerySlides.forEach((slide, index) => {
const slideStart = slide.offsetLeft - galleryContainer.offsetLeft;
const slideEnd = slideStart + slide.offsetWidth;
if (scrollPosition > slideStart && scrollPosition < slideEnd) {
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
galleryNavButtons[index].classList.add('bg-blue-600');
galleryNavButtons[index].classList.remove('bg-blue-200', 'hover:bg-blue-400');
}
});
});
let touchStartX = 0;
let touchEndX = 0;
touchStartX = e.changedTouches[0].screenX;
}, {passive: true});
touchEndX = e.changedTouches[0].screenX;
handleSwipe();
}, {passive: true});
if (touchEndX < touchStartX - 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex < gallerySlides.length - 1) {
galleryNavButtons[currentSlideIndex + 1].click();
}
}
if (touchEndX > touchStartX + 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex > 0) {
galleryNavButtons[currentSlideIndex - 1].click();
}
}
}
};
initGallery();
alert('Функция "Показать границы" будет работать с реальным API Яндекс.Карт');
});
alert('Функция "Основные объекты" будет работать с реальным API Яндекс.Карт');
});
});

// From script-ksk.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
const activeCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
const activeSelects = Array.from(document.querySelectorAll('select'))
.filter(select => select.value !== '');
const activeTextInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'))
.filter(input => input.value !== '');
const totalFilters = activeCheckboxes.length + activeSelects.length + activeTextInputs.length;
const badge = document.getElementById('activeFilterBadge');
if (totalFilters > 0) {
badge.textContent = totalFilters;
badge.classList.remove('hidden');
} else {
badge.classList.add('hidden');
}
}
document.querySelectorAll('input[type="checkbox"], select, input[type="text"], input[type="number"]').forEach(element => {
});
setupDropdowns();
setupTypewriter();
initCarousels();
updateActiveFiltersCount();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceRange = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');
const downPaymentRange = document.getElementById('downPaymentRange');
const downPaymentValue = document.getElementById('downPaymentValue');
const termRange = document.getElementById('termRange');
const termValue = document.getElementById('termValue');
const cashbackAmount = document.getElementById('cashbackAmount');
const monthlyPayment = document.getElementById('monthlyPayment');
const price = parseInt(priceRange.value);
const downPayment = parseInt(downPaymentRange.value);
const downPaymentPercent = Math.round((downPayment / price) * 100);
const term = parseInt(termRange.value);
const cashbackPercent = 2.5;
priceValue.textContent = new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
downPaymentValue.textContent = new Intl.NumberFormat('ru-RU').format(downPayment) + ' ₽ (' + downPaymentPercent + '%)';
termValue.textContent = term + ' лет';
const cashback = price * cashbackPercent / 100;
cashbackAmount.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(cashback)) + ' ₽';
const loanAmount = price - downPayment;
const monthlyRate = 0.06 / 12;
const payments = term * 12;
const monthly = loanAmount * monthlyRate * Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
monthlyPayment.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(monthly)) + ' ₽';
}
updateCalculator();
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});
const mapContainer = document.getElementById('districtMap');
const currentDistrict = "Черемушки (ЧМР)";
const districtCoords = [
[38.9730, 45.0370],
[38.9770, 45.0390],
[38.9790, 45.0340],
[38.9750, 45.0310],
[38.9710, 45.0340]
];
console.log(`Карта района "${currentDistrict}" инициализирована`);
}
document.querySelectorAll('section.faq button').forEach(button => {
const answer = button.nextElementSibling;
const icon = button.querySelector('i');
if (answer.style.display === 'none' || !answer.style.display) {
answer.style.display = 'block';
icon.classList.remove('fa-chevron-down');
icon.classList.add('fa-chevron-up');
} else {
answer.style.display = 'none';
icon.classList.remove('fa-chevron-up');
icon.classList.add('fa-chevron-down');
}
});
});
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
e.preventDefault();
document.querySelector(this.getAttribute('href')).scrollIntoView({
behavior: 'smooth'
});
});
});
const initGallery = () => {
const galleryContainer = document.querySelector('.gallery-container');
const gallerySlides = document.querySelectorAll('.gallery-slide');
const galleryNavButtons = document.querySelectorAll('.gallery-nav button');
if (!galleryContainer) return;
galleryNavButtons[0].classList.add('bg-blue-600');
galleryNavButtons[0].classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryNavButtons.forEach(button => {
const slideIndex = parseInt(button.getAttribute('data-slide'));
const slide = gallerySlides[slideIndex];
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
button.classList.add('bg-blue-600');
button.classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryContainer.scrollTo({
left: slide.offsetLeft - galleryContainer.offsetLeft - 16,
behavior: 'smooth'
});
});
});
const scrollPosition = galleryContainer.scrollLeft + galleryContainer.offsetWidth / 2;
gallerySlides.forEach((slide, index) => {
const slideStart = slide.offsetLeft - galleryContainer.offsetLeft;
const slideEnd = slideStart + slide.offsetWidth;
if (scrollPosition > slideStart && scrollPosition < slideEnd) {
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
galleryNavButtons[index].classList.add('bg-blue-600');
galleryNavButtons[index].classList.remove('bg-blue-200', 'hover:bg-blue-400');
}
});
});
let touchStartX = 0;
let touchEndX = 0;
touchStartX = e.changedTouches[0].screenX;
}, {passive: true});
touchEndX = e.changedTouches[0].screenX;
handleSwipe();
}, {passive: true});
if (touchEndX < touchStartX - 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex < gallerySlides.length - 1) {
galleryNavButtons[currentSlideIndex + 1].click();
}
}
if (touchEndX > touchStartX + 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex > 0) {
galleryNavButtons[currentSlideIndex - 1].click();
}
}
}
};
initGallery();
alert('Функция "Показать границы" будет работать с реальным API Яндекс.Карт');
});
alert('Функция "Основные объекты" будет работать с реальным API Яндекс.Карт');
});
});

// From script-location.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
const activeCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
const activeSelects = Array.from(document.querySelectorAll('select'))
.filter(select => select.value !== '');
const activeTextInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'))
.filter(input => input.value !== '');
const totalFilters = activeCheckboxes.length + activeSelects.length + activeTextInputs.length;
const badge = document.getElementById('activeFilterBadge');
if (totalFilters > 0) {
badge.textContent = totalFilters;
badge.classList.remove('hidden');
} else {
badge.classList.add('hidden');
}
}
document.querySelectorAll('input[type="checkbox"], select, input[type="text"], input[type="number"]').forEach(element => {
});
setupDropdowns();
setupTypewriter();
initCarousels();
updateActiveFiltersCount();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceRange = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');
const downPaymentRange = document.getElementById('downPaymentRange');
const downPaymentValue = document.getElementById('downPaymentValue');
const termRange = document.getElementById('termRange');
const termValue = document.getElementById('termValue');
const cashbackAmount = document.getElementById('cashbackAmount');
const monthlyPayment = document.getElementById('monthlyPayment');
const price = parseInt(priceRange.value);
const downPayment = parseInt(downPaymentRange.value);
const downPaymentPercent = Math.round((downPayment / price) * 100);
const term = parseInt(termRange.value);
const cashbackPercent = 2.5;
priceValue.textContent = new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
downPaymentValue.textContent = new Intl.NumberFormat('ru-RU').format(downPayment) + ' ₽ (' + downPaymentPercent + '%)';
termValue.textContent = term + ' лет';
const cashback = price * cashbackPercent / 100;
cashbackAmount.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(cashback)) + ' ₽';
const loanAmount = price - downPayment;
const monthlyRate = 0.06 / 12;
const payments = term * 12;
const monthly = loanAmount * monthlyRate * Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
monthlyPayment.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(monthly)) + ' ₽';
}
updateCalculator();
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});
const mapContainer = document.getElementById('districtMap');
const currentDistrict = "Черемушки (ЧМР)";
const districtCoords = [
[38.9730, 45.0370],
[38.9770, 45.0390],
[38.9790, 45.0340],
[38.9750, 45.0310],
[38.9710, 45.0340]
];
console.log(`Карта района "${currentDistrict}" инициализирована`);
}
document.querySelectorAll('section.faq button').forEach(button => {
const answer = button.nextElementSibling;
const icon = button.querySelector('i');
if (answer.style.display === 'none' || !answer.style.display) {
answer.style.display = 'block';
icon.classList.remove('fa-chevron-down');
icon.classList.add('fa-chevron-up');
} else {
answer.style.display = 'none';
icon.classList.remove('fa-chevron-up');
icon.classList.add('fa-chevron-down');
}
});
});
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
e.preventDefault();
document.querySelector(this.getAttribute('href')).scrollIntoView({
behavior: 'smooth'
});
});
});
const initGallery = () => {
const galleryContainer = document.querySelector('.gallery-container');
const gallerySlides = document.querySelectorAll('.gallery-slide');
const galleryNavButtons = document.querySelectorAll('.gallery-nav button');
if (!galleryContainer) return;
galleryNavButtons[0].classList.add('bg-blue-600');
galleryNavButtons[0].classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryNavButtons.forEach(button => {
const slideIndex = parseInt(button.getAttribute('data-slide'));
const slide = gallerySlides[slideIndex];
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
button.classList.add('bg-blue-600');
button.classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryContainer.scrollTo({
left: slide.offsetLeft - galleryContainer.offsetLeft - 16,
behavior: 'smooth'
});
});
});
const scrollPosition = galleryContainer.scrollLeft + galleryContainer.offsetWidth / 2;
gallerySlides.forEach((slide, index) => {
const slideStart = slide.offsetLeft - galleryContainer.offsetLeft;
const slideEnd = slideStart + slide.offsetWidth;
if (scrollPosition > slideStart && scrollPosition < slideEnd) {
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
galleryNavButtons[index].classList.add('bg-blue-600');
galleryNavButtons[index].classList.remove('bg-blue-200', 'hover:bg-blue-400');
}
});
});
let touchStartX = 0;
let touchEndX = 0;
touchStartX = e.changedTouches[0].screenX;
}, {passive: true});
touchEndX = e.changedTouches[0].screenX;
handleSwipe();
}, {passive: true});
if (touchEndX < touchStartX - 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex < gallerySlides.length - 1) {
galleryNavButtons[currentSlideIndex + 1].click();
}
}
if (touchEndX > touchStartX + 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex > 0) {
galleryNavButtons[currentSlideIndex - 1].click();
}
}
}
};
initGallery();
alert('Функция "Показать границы" будет работать с реальным API Яндекс.Карт');
});
alert('Функция "Основные объекты" будет работать с реальным API Яндекс.Карт');
});
});

// From script-manager.js
document.querySelector('.fa-bars').addEventListener('click', function() {
document.querySelector('.hidden.md\\:flex').classList.toggle('hidden');
});
const statsData = {
clients: 142,
requests: 24,
buildings: 18,
cashback: 1240500
};
document.querySelectorAll('[data-stat]').forEach(el => {
const stat = el.getAttribute('data-stat');
el.textContent = statsData[stat];
});
});

// From script-maternal-capital.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
const activeCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
const activeSelects = Array.from(document.querySelectorAll('select'))
.filter(select => select.value !== '');
const activeTextInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'))
.filter(input => input.value !== '');
const totalFilters = activeCheckboxes.length + activeSelects.length + activeTextInputs.length;
const badge = document.getElementById('activeFilterBadge');
if (totalFilters > 0) {
badge.textContent = totalFilters;
badge.classList.remove('hidden');
} else {
badge.classList.add('hidden');
}
}
document.querySelectorAll('input[type="checkbox"], select, input[type="text"], input[type="number"]').forEach(element => {
});
setupDropdowns();
setupTypewriter();
initCarousels();
updateActiveFiltersCount();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceInput = document.getElementById('price-input');
const priceSlider = document.getElementById('price');
const initialInput = document.getElementById('initial-input');
const initialSlider = document.getElementById('initial');
const termInput = document.getElementById('term-input');
const termSlider = document.getElementById('term');
const rateSelect = document.getElementById('rate');
const creditSumEl = document.getElementById('credit-sum');
const monthlyPaymentEl = document.getElementById('monthly-payment');
const overpaymentEl = document.getElementById('overpayment');
const cashbackEl = document.getElementById('cashback');
const cashbackCheckbox = document.querySelector('input[name="cashback"]');
let value = input.value.replace(/\s/g, '');
if (!isNaN(value)) {
slider.value = value;
updateCalculator();
}
});
input.value = formatFn(slider.value);
updateCalculator();
});
}
return parseInt(value).toLocaleString('ru-RU');
}
return value;
}
connectInputAndSlider(priceInput, priceSlider, formatPrice);
connectInputAndSlider(initialInput, initialSlider, formatPercent);
connectInputAndSlider(termInput, termSlider, formatPercent);
const price = parseInt(priceInput.value.replace(/\s/g, '')) || 5000000;
const initialPercent = parseInt(initialSlider.value) || 15;
const termYears = parseInt(termSlider.value) || 15;
const ratePercent = parseFloat(rateSelect.value) || 14.99;
const cashbackPercentage = 2;
let loanAmount;
const programType = rateSelect.options[rateSelect.selectedIndex].text;
if (programType.includes('Семейная') || programType.includes('Сельская')) {
const maxLoan = 6000000;
const requiredDownPayment = Math.max(0, price - maxLoan);
const calculatedDownPayment = price * initialPercent / 100;
const effectiveDownPayment = Math.max(requiredDownPayment, calculatedDownPayment);
loanAmount = price - effectiveDownPayment;
if (calculatedDownPayment < requiredDownPayment) {
initialInput.classList.add('border-red-500');
} else {
initialInput.classList.remove('border-red-500');
}
}
else if (programType.includes('IT')) {
const maxLoan = 9000000;
const requiredDownPayment = Math.max(0, price - maxLoan);
const calculatedDownPayment = price * initialPercent / 100;
const effectiveDownPayment = Math.max(requiredDownPayment, calculatedDownPayment);
loanAmount = price - effectiveDownPayment;
if (calculatedDownPayment < requiredDownPayment) {
initialInput.classList.add('border-red-500');
} else {
initialInput.classList.remove('border-red-500');
}
}
else {
loanAmount = price * (100 - initialPercent) / 100;
initialInput.classList.remove('border-red-500');
}
const monthlyRate = ratePercent / 100 / 12;
const payments = termYears * 12;
const monthlyPayment = loanAmount * monthlyRate *
Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
const totalPayment = monthlyPayment * payments;
const totalOverpayment = totalPayment - loanAmount;
let cashback = 0;
if (cashbackCheckbox.checked) {
cashback = price * cashbackPercentage / 100;
}
creditSumEl.textContent = formatPrice(Math.round(loanAmount)) + ' ₽';
monthlyPaymentEl.textContent = formatPrice(Math.round(monthlyPayment)) + ' ₽';
overpaymentEl.textContent = formatPrice(Math.round(totalOverpayment)) + ' ₽';
cashbackEl.textContent = formatPrice(Math.round(cashback)) + ' ₽';
}
[priceSlider, initialSlider, termSlider, rateSelect, cashbackCheckbox].forEach(el => {
});
updateCalculator();
});
const initialInput = document.getElementById('initial-input');
const initialSlider = document.getElementById('initial');
const currentValue = parseInt(initialInput.value) || 0;
const price = parseInt(document.getElementById('price-input').value.replace(/\s/g, '')) || 8000000;
const programType = document.getElementById('rate').options[document.getElementById('rate').selectedIndex].text;
let newValue = currentValue + 1;
let maxValue = 40;
if (programType.includes('Семейная') || programType.includes('Сельская')) {
maxValue = Math.min(40, Math.max(100 - (6000000 / price) * 100, 0));
} else if (programType.includes('IT')) {
maxValue = Math.min(40, Math.max(100 - (9000000 / price) * 100, 0));
}
if (newValue > maxValue) {
newValue = maxValue;
}
if (newValue <= maxValue) {
initialInput.value = newValue;
initialSlider.value = newValue;
document.querySelector('input[name="initial-percent"]').value = newValue;
updateCalculator();
}
}
const initialInput = document.getElementById('initial-input');
const currentValue = parseInt(initialInput.value) || 0;
const minValue = 0;
if (currentValue > minValue) {
const newValue = currentValue - 1;
initialInput.value = newValue;
document.getElementById('initial').value = newValue;
document.querySelector('input[name="initial-percent"]').value = newValue;
updateCalculator();
}
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});
const mapContainer = document.getElementById('districtMap');
const currentDistrict = "Черемушки (ЧМР)";
const districtCoords = [
[38.9730, 45.0370],
[38.9770, 45.0390],
[38.9790, 45.0340],
[38.9750, 45.0310],
[38.9710, 45.0340]
];
console.log(`Карта района "${currentDistrict}" инициализирована`);
}
document.querySelectorAll('section.faq button').forEach(button => {
const answer = button.nextElementSibling;
const icon = button.querySelector('i');
if (answer.style.display === 'none' || !answer.style.display) {
answer.style.display = 'block';
icon.classList.remove('fa-chevron-down');
icon.classList.add('fa-chevron-up');
} else {
answer.style.display = 'none';
icon.classList.remove('fa-chevron-up');
icon.classList.add('fa-chevron-down');
}
});
});
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
e.preventDefault();
document.querySelector(this.getAttribute('href')).scrollIntoView({
behavior: 'smooth'
});
});
});
const initGallery = () => {
const galleryContainer = document.querySelector('.gallery-container');
const gallerySlides = document.querySelectorAll('.gallery-slide');
const galleryNavButtons = document.querySelectorAll('.gallery-nav button');
if (!galleryContainer) return;
galleryNavButtons[0].classList.add('bg-blue-600');
galleryNavButtons[0].classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryNavButtons.forEach(button => {
const slideIndex = parseInt(button.getAttribute('data-slide'));
const slide = gallerySlides[slideIndex];
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
button.classList.add('bg-blue-600');
button.classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryContainer.scrollTo({
left: slide.offsetLeft - galleryContainer.offsetLeft - 16,
behavior: 'smooth'
});
});
});
const scrollPosition = galleryContainer.scrollLeft + galleryContainer.offsetWidth / 2;
gallerySlides.forEach((slide, index) => {
const slideStart = slide.offsetLeft - galleryContainer.offsetLeft;
const slideEnd = slideStart + slide.offsetWidth;
if (scrollPosition > slideStart && scrollPosition < slideEnd) {
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
galleryNavButtons[index].classList.add('bg-blue-600');
galleryNavButtons[index].classList.remove('bg-blue-200', 'hover:bg-blue-400');
}
});
});
let touchStartX = 0;
let touchEndX = 0;
touchStartX = e.changedTouches[0].screenX;
}, {passive: true});
touchEndX = e.changedTouches[0].screenX;
handleSwipe();
}, {passive: true});
if (touchEndX < touchStartX - 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex < gallerySlides.length - 1) {
galleryNavButtons[currentSlideIndex + 1].click();
}
}
if (touchEndX > touchStartX + 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex > 0) {
galleryNavButtons[currentSlideIndex - 1].click();
}
}
}
};
initGallery();
alert('Функция "Показать границы" будет работать с реальным API Яндекс.Карт');
});
alert('Функция "Основные объекты" будет работать с реальным API Яндекс.Карт');
});
});

// From script-military-mortgage.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
const activeCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
const activeSelects = Array.from(document.querySelectorAll('select'))
.filter(select => select.value !== '');
const activeTextInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'))
.filter(input => input.value !== '');
const totalFilters = activeCheckboxes.length + activeSelects.length + activeTextInputs.length;
const badge = document.getElementById('activeFilterBadge');
if (totalFilters > 0) {
badge.textContent = totalFilters;
badge.classList.remove('hidden');
} else {
badge.classList.add('hidden');
}
}
document.querySelectorAll('input[type="checkbox"], select, input[type="text"], input[type="number"]').forEach(element => {
});
setupDropdowns();
setupTypewriter();
initCarousels();
updateActiveFiltersCount();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceInput = document.getElementById('price-input');
const priceSlider = document.getElementById('price');
const initialInput = document.getElementById('initial-input');
const initialSlider = document.getElementById('initial');
const termInput = document.getElementById('term-input');
const termSlider = document.getElementById('term');
const rateSelect = document.getElementById('rate');
const creditSumEl = document.getElementById('credit-sum');
const monthlyPaymentEl = document.getElementById('monthly-payment');
const overpaymentEl = document.getElementById('overpayment');
const cashbackEl = document.getElementById('cashback');
const cashbackCheckbox = document.querySelector('input[name="cashback"]');
let value = input.value.replace(/\s/g, '');
if (!isNaN(value)) {
slider.value = value;
updateCalculator();
}
});
input.value = formatFn(slider.value);
updateCalculator();
});
}
return parseInt(value).toLocaleString('ru-RU');
}
return value;
}
connectInputAndSlider(priceInput, priceSlider, formatPrice);
connectInputAndSlider(initialInput, initialSlider, formatPercent);
connectInputAndSlider(termInput, termSlider, formatPercent);
const price = parseInt(priceInput.value.replace(/\s/g, '')) || 5000000;
const initialPercent = parseInt(initialSlider.value) || 15;
const termYears = parseInt(termSlider.value) || 15;
const ratePercent = parseFloat(rateSelect.value) || 14.99;
const cashbackPercentage = 2;
let loanAmount;
const programType = rateSelect.options[rateSelect.selectedIndex].text;
if (programType.includes('Семейная') || programType.includes('Сельская')) {
const maxLoan = 6000000;
const requiredDownPayment = Math.max(0, price - maxLoan);
const calculatedDownPayment = price * initialPercent / 100;
const effectiveDownPayment = Math.max(requiredDownPayment, calculatedDownPayment);
loanAmount = price - effectiveDownPayment;
if (calculatedDownPayment < requiredDownPayment) {
initialInput.classList.add('border-red-500');
} else {
initialInput.classList.remove('border-red-500');
}
}
else if (programType.includes('IT')) {
const maxLoan = 9000000;
const requiredDownPayment = Math.max(0, price - maxLoan);
const calculatedDownPayment = price * initialPercent / 100;
const effectiveDownPayment = Math.max(requiredDownPayment, calculatedDownPayment);
loanAmount = price - effectiveDownPayment;
if (calculatedDownPayment < requiredDownPayment) {
initialInput.classList.add('border-red-500');
} else {
initialInput.classList.remove('border-red-500');
}
}
else {
loanAmount = price * (100 - initialPercent) / 100;
initialInput.classList.remove('border-red-500');
}
const monthlyRate = ratePercent / 100 / 12;
const payments = termYears * 12;
const monthlyPayment = loanAmount * monthlyRate *
Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
const totalPayment = monthlyPayment * payments;
const totalOverpayment = totalPayment - loanAmount;
let cashback = 0;
if (cashbackCheckbox.checked) {
cashback = price * cashbackPercentage / 100;
}
creditSumEl.textContent = formatPrice(Math.round(loanAmount)) + ' ₽';
monthlyPaymentEl.textContent = formatPrice(Math.round(monthlyPayment)) + ' ₽';
overpaymentEl.textContent = formatPrice(Math.round(totalOverpayment)) + ' ₽';
cashbackEl.textContent = formatPrice(Math.round(cashback)) + ' ₽';
}
[priceSlider, initialSlider, termSlider, rateSelect, cashbackCheckbox].forEach(el => {
});
updateCalculator();
});
const initialInput = document.getElementById('initial-input');
const initialSlider = document.getElementById('initial');
const currentValue = parseInt(initialInput.value) || 0;
const price = parseInt(document.getElementById('price-input').value.replace(/\s/g, '')) || 8000000;
const programType = document.getElementById('rate').options[document.getElementById('rate').selectedIndex].text;
let newValue = currentValue + 1;
let maxValue = 40;
if (programType.includes('Семейная') || programType.includes('Сельская')) {
maxValue = Math.min(40, Math.max(100 - (6000000 / price) * 100, 0));
} else if (programType.includes('IT')) {
maxValue = Math.min(40, Math.max(100 - (9000000 / price) * 100, 0));
}
if (newValue > maxValue) {
newValue = maxValue;
}
if (newValue <= maxValue) {
initialInput.value = newValue;
initialSlider.value = newValue;
document.querySelector('input[name="initial-percent"]').value = newValue;
updateCalculator();
}
}
const initialInput = document.getElementById('initial-input');
const currentValue = parseInt(initialInput.value) || 0;
const minValue = 0;
if (currentValue > minValue) {
const newValue = currentValue - 1;
initialInput.value = newValue;
document.getElementById('initial').value = newValue;
document.querySelector('input[name="initial-percent"]').value = newValue;
updateCalculator();
}
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});
const mapContainer = document.getElementById('districtMap');
const currentDistrict = "Черемушки (ЧМР)";
const districtCoords = [
[38.9730, 45.0370],
[38.9770, 45.0390],
[38.9790, 45.0340],
[38.9750, 45.0310],
[38.9710, 45.0340]
];
console.log(`Карта района "${currentDistrict}" инициализирована`);
}
document.querySelectorAll('section.faq button').forEach(button => {
const answer = button.nextElementSibling;
const icon = button.querySelector('i');
if (answer.style.display === 'none' || !answer.style.display) {
answer.style.display = 'block';
icon.classList.remove('fa-chevron-down');
icon.classList.add('fa-chevron-up');
} else {
answer.style.display = 'none';
icon.classList.remove('fa-chevron-up');
icon.classList.add('fa-chevron-down');
}
});
});
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
e.preventDefault();
document.querySelector(this.getAttribute('href')).scrollIntoView({
behavior: 'smooth'
});
});
});
const initGallery = () => {
const galleryContainer = document.querySelector('.gallery-container');
const gallerySlides = document.querySelectorAll('.gallery-slide');
const galleryNavButtons = document.querySelectorAll('.gallery-nav button');
if (!galleryContainer) return;
galleryNavButtons[0].classList.add('bg-blue-600');
galleryNavButtons[0].classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryNavButtons.forEach(button => {
const slideIndex = parseInt(button.getAttribute('data-slide'));
const slide = gallerySlides[slideIndex];
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
button.classList.add('bg-blue-600');
button.classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryContainer.scrollTo({
left: slide.offsetLeft - galleryContainer.offsetLeft - 16,
behavior: 'smooth'
});
});
});
const scrollPosition = galleryContainer.scrollLeft + galleryContainer.offsetWidth / 2;
gallerySlides.forEach((slide, index) => {
const slideStart = slide.offsetLeft - galleryContainer.offsetLeft;
const slideEnd = slideStart + slide.offsetWidth;
if (scrollPosition > slideStart && scrollPosition < slideEnd) {
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
galleryNavButtons[index].classList.add('bg-blue-600');
galleryNavButtons[index].classList.remove('bg-blue-200', 'hover:bg-blue-400');
}
});
});
let touchStartX = 0;
let touchEndX = 0;
touchStartX = e.changedTouches[0].screenX;
}, {passive: true});
touchEndX = e.changedTouches[0].screenX;
handleSwipe();
}, {passive: true});
if (touchEndX < touchStartX - 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex < gallerySlides.length - 1) {
galleryNavButtons[currentSlideIndex + 1].click();
}
}
if (touchEndX > touchStartX + 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex > 0) {
galleryNavButtons[currentSlideIndex - 1].click();
}
}
}
};
initGallery();
alert('Функция "Показать границы" будет работать с реальным API Яндекс.Карт');
});
alert('Функция "Основные объекты" будет работать с реальным API Яндекс.Карт');
});
});

// From script-password-mail.js
});
function toggleEmail() {
const regEmail = document.getElementById('registration-email');
const resetEmail = document.getElementById('password-reset-email');
if(regEmail.classList.contains('hidden')) {
regEmail.classList.remove('hidden');
resetEmail.classList.add('hidden');
} else {
regEmail.classList.add('hidden');
resetEmail.classList.remove('hidden');
}
}

// From script-rassrochka.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
const activeCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
const activeSelects = Array.from(document.querySelectorAll('select'))
.filter(select => select.value !== '');
const activeTextInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'))
.filter(input => input.value !== '');
const totalFilters = activeCheckboxes.length + activeSelects.length + activeTextInputs.length;
const badge = document.getElementById('activeFilterBadge');
if (totalFilters > 0) {
badge.textContent = totalFilters;
badge.classList.remove('hidden');
} else {
badge.classList.add('hidden');
}
}
document.querySelectorAll('input[type="checkbox"], select, input[type="text"], input[type="number"]').forEach(element => {
});
setupDropdowns();
setupTypewriter();
initCarousels();
updateActiveFiltersCount();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceInput = document.getElementById('price-input');
const priceSlider = document.getElementById('price');
const initialInput = document.getElementById('initial-input');
const initialSlider = document.getElementById('initial');
const termInput = document.getElementById('term-input');
const termSlider = document.getElementById('term');
const rateSelect = document.getElementById('rate');
const creditSumEl = document.getElementById('credit-sum');
const monthlyPaymentEl = document.getElementById('monthly-payment');
const overpaymentEl = document.getElementById('overpayment');
const cashbackEl = document.getElementById('cashback');
const cashbackCheckbox = document.querySelector('input[name="cashback"]');
let value = input.value.replace(/\s/g, '');
if (!isNaN(value)) {
slider.value = value;
updateCalculator();
}
});
input.value = formatFn(slider.value);
updateCalculator();
});
}
return parseInt(value).toLocaleString('ru-RU');
}
return value;
}
connectInputAndSlider(priceInput, priceSlider, formatPrice);
connectInputAndSlider(initialInput, initialSlider, formatPercent);
connectInputAndSlider(termInput, termSlider, formatPercent);
const price = parseInt(priceInput.value.replace(/\s/g, '')) || 5000000;
const initialPercent = parseInt(initialSlider.value) || 15;
const termYears = parseInt(termSlider.value) || 15;
const ratePercent = parseFloat(rateSelect.value) || 14.99;
const cashbackPercentage = 2;
let loanAmount;
const programType = rateSelect.options[rateSelect.selectedIndex].text;
if (programType.includes('Семейная') || programType.includes('Сельская')) {
const maxLoan = 6000000;
const requiredDownPayment = Math.max(0, price - maxLoan);
const calculatedDownPayment = price * initialPercent / 100;
const effectiveDownPayment = Math.max(requiredDownPayment, calculatedDownPayment);
loanAmount = price - effectiveDownPayment;
if (calculatedDownPayment < requiredDownPayment) {
initialInput.classList.add('border-red-500');
} else {
initialInput.classList.remove('border-red-500');
}
}
else if (programType.includes('IT')) {
const maxLoan = 9000000;
const requiredDownPayment = Math.max(0, price - maxLoan);
const calculatedDownPayment = price * initialPercent / 100;
const effectiveDownPayment = Math.max(requiredDownPayment, calculatedDownPayment);
loanAmount = price - effectiveDownPayment;
if (calculatedDownPayment < requiredDownPayment) {
initialInput.classList.add('border-red-500');
} else {
initialInput.classList.remove('border-red-500');
}
}
else {
loanAmount = price * (100 - initialPercent) / 100;
initialInput.classList.remove('border-red-500');
}
const monthlyRate = ratePercent / 100 / 12;
const payments = termYears * 12;
const monthlyPayment = loanAmount * monthlyRate *
Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
const totalPayment = monthlyPayment * payments;
const totalOverpayment = totalPayment - loanAmount;
let cashback = 0;
if (cashbackCheckbox.checked) {
cashback = price * cashbackPercentage / 100;
}
creditSumEl.textContent = formatPrice(Math.round(loanAmount)) + ' ₽';
monthlyPaymentEl.textContent = formatPrice(Math.round(monthlyPayment)) + ' ₽';
overpaymentEl.textContent = formatPrice(Math.round(totalOverpayment)) + ' ₽';
cashbackEl.textContent = formatPrice(Math.round(cashback)) + ' ₽';
}
[priceSlider, initialSlider, termSlider, rateSelect, cashbackCheckbox].forEach(el => {
});
updateCalculator();
});
const initialInput = document.getElementById('initial-input');
const initialSlider = document.getElementById('initial');
const currentValue = parseInt(initialInput.value) || 0;
const price = parseInt(document.getElementById('price-input').value.replace(/\s/g, '')) || 8000000;
const programType = document.getElementById('rate').options[document.getElementById('rate').selectedIndex].text;
let newValue = currentValue + 1;
let maxValue = 40;
if (programType.includes('Семейная') || programType.includes('Сельская')) {
maxValue = Math.min(40, Math.max(100 - (6000000 / price) * 100, 0));
} else if (programType.includes('IT')) {
maxValue = Math.min(40, Math.max(100 - (9000000 / price) * 100, 0));
}
if (newValue > maxValue) {
newValue = maxValue;
}
if (newValue <= maxValue) {
initialInput.value = newValue;
initialSlider.value = newValue;
document.querySelector('input[name="initial-percent"]').value = newValue;
updateCalculator();
}
}
const initialInput = document.getElementById('initial-input');
const currentValue = parseInt(initialInput.value) || 0;
const minValue = 0;
if (currentValue > minValue) {
const newValue = currentValue - 1;
initialInput.value = newValue;
document.getElementById('initial').value = newValue;
document.querySelector('input[name="initial-percent"]').value = newValue;
updateCalculator();
}
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});
const mapContainer = document.getElementById('districtMap');
const currentDistrict = "Черемушки (ЧМР)";
const districtCoords = [
[38.9730, 45.0370],
[38.9770, 45.0390],
[38.9790, 45.0340],
[38.9750, 45.0310],
[38.9710, 45.0340]
];
console.log(`Карта района "${currentDistrict}" инициализирована`);
}
document.querySelectorAll('section.faq button').forEach(button => {
const answer = button.nextElementSibling;
const icon = button.querySelector('i');
if (answer.style.display === 'none' || !answer.style.display) {
answer.style.display = 'block';
icon.classList.remove('fa-chevron-down');
icon.classList.add('fa-chevron-up');
} else {
answer.style.display = 'none';
icon.classList.remove('fa-chevron-up');
icon.classList.add('fa-chevron-down');
}
});
});
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
e.preventDefault();
document.querySelector(this.getAttribute('href')).scrollIntoView({
behavior: 'smooth'
});
});
});
const initGallery = () => {
const galleryContainer = document.querySelector('.gallery-container');
const gallerySlides = document.querySelectorAll('.gallery-slide');
const galleryNavButtons = document.querySelectorAll('.gallery-nav button');
if (!galleryContainer) return;
galleryNavButtons[0].classList.add('bg-blue-600');
galleryNavButtons[0].classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryNavButtons.forEach(button => {
const slideIndex = parseInt(button.getAttribute('data-slide'));
const slide = gallerySlides[slideIndex];
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
button.classList.add('bg-blue-600');
button.classList.remove('bg-blue-200', 'hover:bg-blue-400');
galleryContainer.scrollTo({
left: slide.offsetLeft - galleryContainer.offsetLeft - 16,
behavior: 'smooth'
});
});
});
const scrollPosition = galleryContainer.scrollLeft + galleryContainer.offsetWidth / 2;
gallerySlides.forEach((slide, index) => {
const slideStart = slide.offsetLeft - galleryContainer.offsetLeft;
const slideEnd = slideStart + slide.offsetWidth;
if (scrollPosition > slideStart && scrollPosition < slideEnd) {
galleryNavButtons.forEach(btn => {
btn.classList.add('bg-blue-200', 'hover:bg-blue-400');
btn.classList.remove('bg-blue-600');
});
galleryNavButtons[index].classList.add('bg-blue-600');
galleryNavButtons[index].classList.remove('bg-blue-200', 'hover:bg-blue-400');
}
});
});
let touchStartX = 0;
let touchEndX = 0;
touchStartX = e.changedTouches[0].screenX;
}, {passive: true});
touchEndX = e.changedTouches[0].screenX;
handleSwipe();
}, {passive: true});
if (touchEndX < touchStartX - 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex < gallerySlides.length - 1) {
galleryNavButtons[currentSlideIndex + 1].click();
}
}
if (touchEndX > touchStartX + 50) {
const currentSlideIndex = Array.from(gallerySlides).findIndex(slide => {
const rect = slide.getBoundingClientRect();
return rect.left >= galleryContainer.getBoundingClientRect().left;
});
if (currentSlideIndex > 0) {
galleryNavButtons[currentSlideIndex - 1].click();
}
}
}
};
initGallery();
alert('Функция "Показать границы" будет работать с реальным API Яндекс.Карт');
});
alert('Функция "Основные объекты" будет работать с реальным API Яндекс.Карт');
});
});

// From script-reviews.js
tailwind.config = {
theme: {
extend: {
colors: {
ton: {
blue: '#0088cc',
dark: '#222426',
light: '#f5f5f5',
accent: '#00a3e0',
}
},
fontFamily: {
sans: ['Inter', 'sans-serif'],
},
}
}
}
const content = document.getElementById(`faq-content-${id}`);
const icon = document.getElementById(`faq-icon-${id}`);
content.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
function openContactForm() {
document.getElementById('contactModal').classList.remove('hidden');
}
function closeContactForm() {
document.getElementById('contactModal').classList.add('hidden');
}
document.getElementById('contactForm').addEventListener('submit', function(e) {
e.preventDefault();
const formData = new FormData(this);
const data = Object.fromEntries(formData);
console.log('Contact form data:', data);
alert('Спасибо за ваше сообщение! Мы свяжемся с вами в ближайшее время.');
closeContactForm();
this.reset();
});
document.getElementById('contactModal').addEventListener('click', function(e) {
if (e.target === this) {
closeContactForm();
}
});
if (e.key === 'Escape') {
closeContactForm();
}
});
const dropdown = element.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
const isOpen = menu.classList.contains('open');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
dropdown.querySelector('.dropdown-btn').classList.toggle('open');
}
const dropdown = button.closest('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
if (openMenu !== menu) {
openMenu.classList.remove('open');
openMenu.previousElementSibling.classList.remove('open');
}
});
menu.classList.toggle('open');
button.classList.toggle('open');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
if (window.innerWidth >= 768) return;
const group = header.closest('.footer-menu-group');
const submenu = group.querySelector('.footer-submenu');
const icon = header.querySelector('svg');
submenu.classList.toggle('hidden');
icon.classList.toggle('rotate-180');
}
if (!e.target.closest('.dropdown')) {
document.querySelectorAll('.dropdown-menu').forEach(menu => {
menu.classList.remove('open');
menu.previousElementSibling.classList.remove('open');
});
}
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
const prevBtn = carousel.querySelector('.carousel-prev');
const nextBtn = carousel.querySelector('.carousel-next');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === currentIndex);
});
}
if (prevBtn) {
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
}
if (nextBtn) {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
}
dots.forEach((dot, index) => {
currentIndex = index;
updateCarousel();
});
});
let interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
interval = setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
});
});
const el = document.getElementById('typewriter');
const changingTexts = [
"кэшбеком до 5%",
"платежами в подарок",
"выгодой до 500 000 ₽"
];
let part = '';
const staticPrefix = 'с ';
let textIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let deletingSpeed = 50;
let pauseAfterType = 2000;
let pauseAfterDelete = 500;
const fullChangingText = changingTexts[textIndex];
if (isDeleting) {
part = fullChangingText.substring(0, part.length - 1);
el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
if (part === '') {
isDeleting = false;
textIndex = (textIndex + 1) % changingTexts.length;
setTimeout(tick, pauseAfterDelete);
} else {
setTimeout(tick, deletingSpeed);
}
} else {
part = fullChangingText.substring(0, part.length + 1);
el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
if (part === fullChangingText) {
isDeleting = true;
setTimeout(tick, pauseAfterType);
} else {
setTimeout(tick, typingSpeed);
}
}
}
el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
setTimeout(tick, 1000);
}
setTimeout(function() {
document.querySelector('.loading-animation').style.display = 'none';
}, 2000);
});
const menu = document.getElementById('mobileMenu');
menu.classList.toggle('hidden');
if (menu.classList.contains('hidden')) {
document.querySelectorAll('.mobile-submenu').forEach(submenu => {
submenu.classList.add('hidden');
});
}
}
const submenu = document.getElementById(id);
submenu.classList.toggle('hidden');
}
document.getElementById('applicationModal').classList.remove('hidden');
}
document.getElementById('loginModal').classList.remove('hidden');
}
closeModal('loginModal');
document.getElementById('registerModal').classList.remove('hidden');
}
document.getElementById(modalId).classList.add('hidden');
}
closeModal('loginModal');
document.getElementById('accountModal').classList.remove('hidden');
}
closeModal('accountModal');
}
const panel = document.getElementById('filtersPanel');
panel.classList.toggle('hidden');
this.querySelector('i').classList.toggle('fa-sliders-h');
this.querySelector('i').classList.toggle('fa-times');
});
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const items = inner.querySelectorAll('.carousel-item');
const dots = carousel.querySelectorAll('.carousel-dot');
dots[0].classList.add('active');
const firstClone = inner.firstElementChild.cloneNode(true);
const lastClone = inner.lastElementChild.cloneNode(true);
inner.appendChild(firstClone);
inner.insertBefore(lastClone, inner.firstElementChild);
let currentIndex = 1;
const itemWidth = items[0].clientWidth;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
let interval = setInterval(nextSlide, 5000);
currentIndex++;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
currentIndex--;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
}
let realIndex = currentIndex;
if (currentIndex === 0) realIndex = items.length - 2;
if (currentIndex === items.length - 1) realIndex = 1;
dots.forEach((dot, index) => {
dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
});
}
if (currentIndex === 0) {
inner.style.transition = 'none';
currentIndex = items.length - 2;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
} else if (currentIndex === items.length - 1) {
inner.style.transition = 'none';
currentIndex = 1;
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}
});
if (carousel.querySelector('.carousel-next')) {
clearInterval(interval);
nextSlide();
interval = setInterval(nextSlide, 5000);
});
}
if (carousel.querySelector('.carousel-prev')) {
clearInterval(interval);
prevSlide();
interval = setInterval(nextSlide, 5000);
});
}
dots.forEach((dot, index) => {
clearInterval(interval);
currentIndex = index + 1;
inner.style.transition = 'transform 0.5s ease-in-out';
inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
updateDots();
interval = setInterval(nextSlide, 5000);
});
});
});
}
setupDropdowns();
setupTypewriter();
initCarousels();
document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
if (this.classList.contains('active')) {
this.classList.remove('active');
} else {
if (btn.classList.contains('class-filter-btn')) {
btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
}
this.classList.add('active');
}
updateSelectedFilters();
});
});
const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
if (activeFilters.length > 0) {
document.getElementById('selectedFilters').classList.remove('hidden');
} else {
document.getElementById('selectedFilters').classList.add('hidden');
}
}
});
const priceRange = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');
const downPaymentRange = document.getElementById('downPaymentRange');
const downPaymentValue = document.getElementById('downPaymentValue');
const termRange = document.getElementById('termRange');
const termValue = document.getElementById('termValue');
const cashbackAmount = document.getElementById('cashbackAmount');
const monthlyPayment = document.getElementById('monthlyPayment');
const price = parseInt(priceRange.value);
const downPayment = parseInt(downPaymentRange.value);
const downPaymentPercent = Math.round((downPayment / price) * 100);
const term = parseInt(termRange.value);
const cashbackPercent = 2.5;
priceValue.textContent = new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
downPaymentValue.textContent = new Intl.NumberFormat('ru-RU').format(downPayment) + ' ₽ (' + downPaymentPercent + '%)';
termValue.textContent = term + ' лет';
const cashback = price * cashbackPercent / 100;
cashbackAmount.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(cashback)) + ' ₽';
const loanAmount = price - downPayment;
const monthlyRate = 0.06 / 12;
const payments = term * 12;
const monthly = loanAmount * monthlyRate * Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
monthlyPayment.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(monthly)) + ' ₽';
}
updateCalculator();
document.querySelectorAll('.carousel').forEach(carousel => {
const inner = carousel.querySelector('.carousel-inner');
const prev = carousel.querySelector('.carousel-prev');
const next = carousel.querySelector('.carousel-next');
const items = carousel.querySelectorAll('img');
let currentIndex = 0;
inner.style.transform = `translateX(-${currentIndex * 100}%)`;
}
currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
updateCarousel();
});
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
});
setInterval(() => {
currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
updateCarousel();
}, 5000);
});
const modals = document.querySelectorAll('.modal');
modals.forEach(modal => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
});
