btnClear = document.getElementById("btnClear");
names = document.getElementById("name");
qty = document.getElementById("qty");
cost = document.getElementById("cost");
price = document.getElementById("price");
img = document.getElementById("img");

function clear() {
    print("Clear")
    names.value = "";
    qty.value = "";
    cost.value = "";
    price.value = "";
    img.value = "";
};