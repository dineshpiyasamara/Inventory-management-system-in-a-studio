 

// search products from inventory
function tableSearch(){
    let input, filter, table, tr, td, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");

    for(let i=0; i<tr.length; i++){
        td = tr[i].getElementsByTagName("td")[1];
        if(td){
            txtValue = td.textContent || td.innerText;
            if(txtValue.toUpperCase().indexOf(filter) > -1){
                tr[i].style.display = "";
            }
            else{
                tr[i].style.display = "none";
            }
        }
    }
}


// change selling price
function changeSellingPrice(product_code, selling_price){
    document.getElementById('product_code').value = product_code;
    document.getElementById('selling_price').value = selling_price;
}

// add item data to sales form
const selectedProduct = document.getElementById('item-data');
if(selectedProduct){
    selectedProduct.addEventListener('change', (e)=>{
        const product = e.target.value;
    
        const xhr = new XMLHttpRequest();
        xhr.open('GET', `/other-item-json/${product}/`, true);
        xhr.onload = function(){
            if(this.status == 200){
                const otherData = JSON.parse(this.responseText);
    
                document.getElementById("category").value = otherData.data[0].category;
                document.getElementById("color").value = otherData.data[0].color;
                document.getElementById("description").value = otherData.data[0].description;
                
                document.getElementById("selling_price").value = otherData.price
                tot();
            }
        }
        xhr.send();
    })
}

// set total price from qty and selling price
function tot(){
    var sellingPrice = document.getElementById("selling_price").value
    var qty = document.getElementById("qty").value
    var total = sellingPrice*qty
    if (!isNaN(total)){
        document.getElementById('total').value = total.toFixed(2)
    }
}



// fill other values in purchase
function fillPurchase(){
    var input = document.getElementById("product_code");

    const xhr = new XMLHttpRequest();
    xhr.open('GET', `/other-item-json/${input.value}/`, true);
    xhr.onload = function(){
        if(this.status == 200){
            const otherData = JSON.parse(this.responseText);

            document.getElementById("category").value = otherData.data[0].category;
            document.getElementById("color").value = otherData.data[0].color;
            document.getElementById("description").value = otherData.data[0].description;
            document.getElementById("purchase_price").value = otherData.data[0].purchase_price;
            document.getElementById("selling_price").value = otherData.price;
        }
        else{
            document.getElementById("category").value = "";
            document.getElementById("color").value = "";
            document.getElementById("description").value = "";
            document.getElementById("purchase_price").value = "";
            document.getElementById("selling_price").value = "";
        }
    }
    xhr.send();
}


// remove user
function removeUser(name){
    const msg = "Do you want to remove "+name+"?";
    document.getElementById("to-remove-user").innerHTML = msg;
    document.getElementById("label-to-remove-user").value = name;
}

const toggleCollapse = document.querySelector('.toggle-collapse');
const nav = document.querySelector('.nav');

if(toggleCollapse){
    toggleCollapse.addEventListener('click', () =>{
        nav.classList.toggle('collapse');
    });   
}


// handle models
const openModalButtons = document.querySelectorAll('[data-modal-target]')
const closeModalButtons = document.querySelectorAll('[data-close-button]')
const overlay = document.getElementById('overlay')

openModalButtons.forEach(button => {
  button.addEventListener('click', () => {
    const modal = document.querySelector(button.dataset.modalTarget)
    openModal(modal)
  })
})

if(overlay){
    overlay.addEventListener('click', () => {
        const modals = document.querySelectorAll('.modal.active')
        modals.forEach(modal => {
          closeModal(modal)
        })
      })
}

if(closeModalButtons){
    closeModalButtons.forEach(button => {
        button.addEventListener('click', () => {
          const modal = button.closest('.modal')
          closeModal(modal)
        })
      })
}

function openModal(modal) {
    if (modal == null) return
    modal.classList.add('active')
    overlay.classList.add('active')
}

function closeModal(modal) {
    if (modal == null) return
    modal.classList.remove('active')
    overlay.classList.remove('active')
}

// form validation
const purchase_form = document.getElementById('purchase-form');
const sales_form = document.getElementById('sales-form');

const product_code = document.getElementById('product_code');
const category = document.getElementById('category');
const color = document.getElementById('color');
const description = document.getElementById('description');
const purchase_price = document.getElementById('purchase_price');
const selling_price = document.getElementById('selling_price');
const qty = document.getElementById('qty');
const total = document.getElementById('total');

const organization = document.getElementById('organization');
const address = document.getElementById('address');
const phone_number = document.getElementById('phone_number');
const customer_name = document.getElementById('name');


// purchase form validation
if (purchase_form){
    purchase_form.addEventListener('submit', (e)=>{

        purchase_checkInputs();

        if(product_code.parentElement.className === 'single-item not-valid' || category.parentElement.className === 'single-item not-valid' || purchase_price.parentElement.className === 'single-item not-valid' || selling_price.parentElement.className === 'single-item not-valid' || qty.parentElement.className === 'single-item not-valid'){
            e.preventDefault();
        }
    })
}

function purchase_checkInputs(){
    const product_code_value = product_code.value.trim();
    const category_value = category.value.trim();
    const purchase_price_value = purchase_price.value.trim();
    const selling_price_value = selling_price.value.trim();
    const qty_value = qty.value.trim();

    if (product_code_value === ''){
        setErrorFor(product_code, "Cannot be blank");
    }else{
        setSuccessFor(product_code)
    }

    if (category_value === ''){
        setErrorFor(category, "Cannot be blank");
    }else{
        setSuccessFor(category)
    }

    if (purchase_price_value === ''){
        setErrorFor(purchase_price, "Cannot be blank");
    }else if(isNaN(purchase_price_value)){
        setErrorFor(purchase_price, "Invalid input");
    }else{
        setSuccessFor(purchase_price)
    }

    if (selling_price_value === ''){
        setErrorFor(selling_price, "Cannot be blank");
    }else if(isNaN(selling_price_value)){
        setErrorFor(selling_price, "Invalid input");
    }else{
        setSuccessFor(selling_price)
    }

    if (qty_value === ''){
        setErrorFor(qty, "Cannot be blank");
    }else{
        setSuccessFor(qty);
    }

    setSuccessFor(color);
    setSuccessFor(description);
    setSuccessFor(organization);
    setSuccessFor(address);
    setSuccessFor(phone_number);
}

// sales form validation
if(sales_form){
    sales_form.addEventListener('submit', (e)=>{
        sales_checkInputs();

        if(selectedProduct.parentElement.parentElement.className === 'single-item not-valid' || category.parentElement.className === 'single-item not-valid' || selling_price.parentElement.className === 'single-item not-valid' || qty.parentElement.className === 'single-item not-valid'){
            e.preventDefault();
        }
    })
}

function sales_checkInputs(){
    const selectedProduct_value = selectedProduct.value.trim();
    const category_value = category.value.trim();
    const selling_price_value = selling_price.value.trim();
    const qty_value = qty.value.trim();
    const total_value = total.value.trim();

    if(selectedProduct_value === ''){
        setErrorFor(selectedProduct.parentElement, "Cannot be blank");
    }else{
        setSuccessFor(selectedProduct.parentElement)
    }

    if (category_value === ''){
        setErrorFor(category, "Cannot be blank");
    }else{
        setSuccessFor(category)
    }

    if (selling_price_value === ''){
        setErrorFor(selling_price, "Cannot be blank");
    }else if(isNaN(selling_price_value)){
        setErrorFor(selling_price, "Invalid input");
    }else{
        setSuccessFor(selling_price)
    }

    if (qty_value === ''){
        setErrorFor(qty, "Cannot be blank");
    }else{
        setSuccessFor(qty);
    }

    if (total_value === ''){
        setErrorFor(total, "Cannot be blank");
    }else if(isNaN(total_value)){
        setErrorFor(total, "Invalid input");
    }else{
        setSuccessFor(total);
    }

    setSuccessFor(color);
    setSuccessFor(description);
    setSuccessFor(customer_name);
    setSuccessFor(address);
    setSuccessFor(phone_number);
}


function setErrorFor(input, msg){
    const single_item = input.parentElement;
    single_item.className = 'single-item not-valid';
    const small = single_item.querySelector("small");
    small.innerText = msg;
}

function setSuccessFor(input){
    const single_item = input.parentElement;
    single_item.className = 'single-item valid';
}

// highlight selected item in nav-bar

const path = window.location.pathname;

if(path === '/inventory/'){
    const current_page = document.getElementById('nav-inventory');
    highlight_link(current_page);
}else if(path === '/purchase-items/'){
    const current_page = document.getElementById('nav-purchase');
    highlight_link(current_page);
}else if(path === '/sell-items/'){
    const current_page = document.getElementById('nav-sell');
    highlight_link(current_page);
}else if(path === '/employees/'){
    const current_page = document.getElementById('nav-employee');
    highlight_link(current_page);
}

function highlight_link(page){
    page.className = "nav-link selected-nav";
}

// digital clock in nav-bar

function updateClock(){
    let now = new Date();
    
    let dname = now.getDay();
    let mo = now.getMonth();
    let dnum = now.getDate();
    let yr = now.getFullYear();
    let hou = now.getHours();
    let min = now.getMinutes();
    let sec = now.getSeconds();
    let pe = "AM";

    if(hou == 0){
        hou = 12;
    }

    if(hou >12){
        hou = hou - 12;
        pe = "PM";
    }

    if(hou.toString().length === 1){
        hou = "0".concat(hou);
    }
    
    if(min.toString().length === 1){
        min = "0".concat(min);
    }
    
    if(sec.toString().length === 1){
        sec = "0".concat(sec);
    }

    Number.prototype.pad = function(digits){
        for(let n = this.toString(); n.length<digits; n=0+n){
            return n;
        }
    }

    let months = ["JAN","FEB","MARCH","APRIL","MAY","JUNE","JULY","AUG","SEP","OCT","NOV","DEC"];
    let week = ["SUN,","MON,","TUE,","WED,","THU,","FRI,","SAT,","SUN,"];
    let ids = ["dayname","month","daynum","year","hour","minutes","seconds","period"];
    let values = [week[dname],months[mo],dnum,yr,hou,min,sec,pe];

    for(let i=0; i<ids.length; i++){
        document.getElementById(ids[i]).firstChild.nodeValue = values[i];
    }
}

function initClock(){
    updateClock();
    window.setInterval("updateClock()", 1000);
}