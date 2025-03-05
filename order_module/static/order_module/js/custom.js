function updateTotal() {
    const freeShippingRadio = document.getElementById("f-option");
    const flatRateRadio = document.getElementById("s-option");
    const totalPriceElement = document.getElementById("total_price_display");
    const shippingCostInput = document.getElementById("shipping_cost");
    const basketTotalInput = document.getElementById("basket_total");

    if (!totalPriceElement || !basketTotalInput || !shippingCostInput) {
        console.error("Error: Some elements are missing for updateTotal()");
        return;
    }

    let basketTotal = parseInt(basketTotalInput.value) || 0;
    let shippingCost = freeShippingRadio?.checked ? 0 : parseInt(shippingCostInput.value) || 0;
    let finalTotal = basketTotal + shippingCost;

    totalPriceElement.innerText = finalTotal.toLocaleString() + " تومان";
}

// Run on page load
document.addEventListener("DOMContentLoaded", function () {
    updateTotal();
    
    // Reattach event listeners every time page updates
    document.body.addEventListener("change", function (event) {
        if (event.target.matches("#f-option, #s-option")) {
            updateTotal();
        }
    });
});