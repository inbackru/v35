// Калькулятор ипотеки
class MortgageCalculator {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.currentProgram = 'family';
        this.calculate();
    }

    setupEventListeners() {
        // Табы программ
        document.querySelectorAll('.mortgage-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                const program = e.currentTarget.dataset.program;
                this.switchProgram(program);
            });
        });

        // Слайдеры
        document.getElementById('property-price').addEventListener('input', () => this.calculate());
        document.getElementById('down-payment').addEventListener('input', () => this.calculate());
        document.getElementById('loan-term').addEventListener('input', () => this.calculate());
        
        // Слайдер процентной ставки
        const rateSlider = document.getElementById('interest-rate');
        if (rateSlider) {
            rateSlider.addEventListener('input', () => this.calculate());
        }
    }

    switchProgram(program) {
        this.currentProgram = program;
        
        // Переключение активного таба
        document.querySelectorAll('.mortgage-tab').forEach(tab => {
            tab.classList.remove('bg-white', 'text-gray-800', 'shadow-sm');
            tab.classList.add('text-gray-600', 'hover:text-gray-800');
        });
        
        const activeTab = document.querySelector(`[data-program="${program}"]`);
        activeTab.classList.remove('text-gray-600', 'hover:text-gray-800');
        activeTab.classList.add('bg-white', 'text-gray-800', 'shadow-sm');
        
        // Переключение блоков результатов
        document.querySelectorAll('.mortgage-result').forEach(result => {
            result.classList.add('hidden');
        });
        document.getElementById(`${program}-result`).classList.remove('hidden');
        
        // Настройка слайдера процентной ставки
        this.setupRateSlider(program);
        
        this.calculate();
    }

    setupRateSlider(program) {
        const rateBlock = document.getElementById('interest-rate-block');
        const rateSlider = document.getElementById('interest-rate');
        const rateDisplay = document.getElementById('rate-display');
        const rateMin = document.getElementById('rate-min');
        const rateMax = document.getElementById('rate-max');
        
        if (program === 'family') {
            rateBlock.classList.add('hidden');
        } else {
            rateBlock.classList.remove('hidden');
            
            if (program === 'basic') {
                rateSlider.min = 9;
                rateSlider.max = 20;
                rateSlider.value = 16;
                rateMin.textContent = '9%';
                rateMax.textContent = '20%';
                rateDisplay.textContent = '16%';
            } else if (program === 'it') {
                rateSlider.min = 3.5;
                rateSlider.max = 6;
                rateSlider.value = 5;
                rateMin.textContent = '3.5%';
                rateMax.textContent = '6%';
                rateDisplay.textContent = '5%';
            }
        }
    }

    calculate() {
        const propertyPrice = parseFloat(document.getElementById('property-price').value);
        const downPaymentPercent = parseFloat(document.getElementById('down-payment').value);
        const loanTermYears = parseFloat(document.getElementById('loan-term').value);
        
        const downPaymentAmount = propertyPrice * (downPaymentPercent / 100);
        let loanAmount = propertyPrice - downPaymentAmount;
        
        // Обновление отображаемых значений
        document.getElementById('price-display').textContent = this.formatPrice(propertyPrice) + ' ₽';
        document.getElementById('down-payment-display').textContent = `${downPaymentPercent}% (${this.formatPrice(downPaymentAmount)} ₽)`;
        document.getElementById('term-display').textContent = `${loanTermYears} лет`;
        
        // Получение процентной ставки в зависимости от программы
        let interestRate;
        
        if (this.currentProgram === 'family') {
            interestRate = 6;
            // Ограничение: кредит до 6 млн
            if (loanAmount > 6000000) {
                loanAmount = 6000000;
            }
        } else if (this.currentProgram === 'basic') {
            interestRate = parseFloat(document.getElementById('interest-rate').value);
            document.getElementById('rate-display').textContent = `${interestRate}%`;
            // Ограничение: кредит до 15 млн
            if (loanAmount > 15000000) {
                loanAmount = 15000000;
            }
        } else if (this.currentProgram === 'it') {
            interestRate = parseFloat(document.getElementById('interest-rate').value);
            document.getElementById('rate-display').textContent = `${interestRate}%`;
            // Ограничение: кредит до 9 млн
            if (loanAmount > 9000000) {
                loanAmount = 9000000;
            }
        }
        
        // Расчет ипотеки
        const monthlyRate = interestRate / 100 / 12;
        const totalMonths = loanTermYears * 12;
        
        let monthlyPayment;
        if (monthlyRate === 0) {
            monthlyPayment = loanAmount / totalMonths;
        } else {
            monthlyPayment = loanAmount * (monthlyRate * Math.pow(1 + monthlyRate, totalMonths)) / (Math.pow(1 + monthlyRate, totalMonths) - 1);
        }
        
        const totalPayment = monthlyPayment * totalMonths;
        const overpayment = totalPayment - loanAmount;
        
        // Обновление результатов
        document.getElementById(`${this.currentProgram}-monthly`).textContent = this.formatPrice(monthlyPayment) + ' ₽';
        document.getElementById(`${this.currentProgram}-overpay`).textContent = this.formatPrice(overpayment) + ' ₽';
        document.getElementById(`${this.currentProgram}-total`).textContent = this.formatPrice(totalPayment) + ' ₽';
    }

    formatPrice(price) {
        return Math.round(price).toLocaleString('ru-RU').replace(/,/g, ' ');
    }
}

// Инициализация калькулятора после загрузки DOM
document.addEventListener('DOMContentLoaded', () => {
    new MortgageCalculator();
});