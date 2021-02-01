// Preview image in creator bar after upload
const loadFile = function(event) {
    let output = document.querySelector('#preview-uploaded-img');
    let output_two = document.querySelector('#view-img');
    output.src = URL.createObjectURL(event.target.files[0]);
    output_two.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
        URL.revokeObjectURL(output.src);
        document.querySelector('.preview-img').style.display = 'flex';
    }
    output_two.onload = function() {
        URL.revokeObjectURL(output.src);
    }
};

// event listeners for creating product form to display live
if(document.querySelector('#store-heading')){
    document.querySelector('#store-heading').addEventListener('input', function() {
        changeValue('store-heading', 'edit-heading');
    });
}

if(document.querySelector('#item-name')){
    document.querySelector('#item-name').addEventListener('input', function() {
        changeValue('item-name', 'edit-title');
    });
}

if(document.querySelector('#edit-textarea')){
    document.querySelector('#edit-textarea').addEventListener('input', function() {
        changeValue('edit-textarea', 'edit-description');
    });
}

if(document.querySelector('#store-price')){
    document.querySelector('#store-price').addEventListener('input', function() {
        changeValue('store-price', 'edit-price');
    });
}

if(document.querySelector('#store-contact')){
    document.querySelector('#store-contact').addEventListener('input', function() {
        changeValue('store-contact', 'edit-contact');
    });
}

// remove email error when typing // email check is then performed when user clicks submit
if(document.querySelector('#email')){
    document.querySelector('#email').addEventListener('input', function(){
        if(document.querySelector('#email')){
            document.querySelectorAll('.auth-error')[0].style.display = 'none';
        }
    })
}

// call checkPasswordsMatch when user enters their confirmation password 
if(document.querySelector('#confirm_password')){
    document.querySelector('#confirm_password').addEventListener('input', function(){
        checkPasswordsMatch();
    })
}
if(document.querySelector('#password')){
    document.querySelector('#password').addEventListener('input', function(){
        checkPasswordsMatch();
    })
}

// function to change input values live whilst the user creates a product

function changeValue(id, div){
    var text = document.getElementById(id).value;

    if(id === 'store-heading'){
        document.querySelector('#edit-copyright').innerHTML = '© ' + text + ' 2021'
        document.querySelector('#' + div).innerHTML = text;
    }
    
    else if(id === 'store-price'){
        if(document.querySelector('#currency').selectedIndex === 0){
            document.querySelector('#' + div).innerHTML = '£' + text;
        }
        else{
            document.querySelector('#' + div).innerHTML = '$' + text;
        }
    }
    else if(id === 'store-contact'){
        document.querySelector('#' + div).innerHTML = 'Contact: ' + text;
    }
    else{
        document.querySelector('#' + div).innerHTML = text;
    }
}

// function to visually change the currency if a user changes it after typing in the price

function changeCurrency(){
    if(document.querySelector('#currency').selectedIndex == 1){
        const x = document.querySelector('#edit-price').innerHTML;
        const xu = x.replace('£', '$');
        document.querySelector('#edit-price').innerHTML = xu;
    }
    else{
        const x = document.querySelector('#edit-price').innerHTML;
        const xu = x.replace('$', '£');
        document.querySelector('#edit-price').innerHTML = xu;
    }
    document.querySelector('#edit-price').textContent[0].replace('£', '$');
}

// email regex 

function validateEmail(email) {
    const re = /\S+@\S+\.\S+/;
    return re.test(String(email).toLowerCase());
}

// Check product form is valid

function checkProductForm(){
    if(document.querySelector('#store-heading').value != '' && document.querySelector('#item-name').value != '' && document.querySelector('#edit-textarea').value != '' && document.querySelector('#edit-textarea').value  && document.querySelector('#store-price').value != '' && document.querySelector('#store-contact').value && document.querySelector('.upload-img-input').value != '' && validateEmail(document.querySelector('#store-contact').value)){
        document.querySelector('.add-product-details').style.display = 'none';
        document.querySelector('.register').style.display = 'block';
    }
}

// Check passwords

function checkPasswordsMatch(){
    if(document.querySelector('#password').value != document.querySelector('#confirm_password').value){
        document.querySelectorAll('.auth-error')[1].style.display = 'block';
        document.querySelector('.form-submit').setAttribute('disabled', 'true');
    }
    else{
        document.querySelectorAll('.auth-error')[1].style.display = 'none';
        document.querySelector('.form-submit').removeAttribute('disabled');
        checkPasswordLength();
    }
}

function checkPasswordLength(){
    if(document.querySelector('#confirm_password').value.length < 8){
        document.querySelectorAll('.auth-error')[2].style.display = 'block';
        document.querySelector('.form-submit').setAttribute('disabled', 'true');
    }
    else{
        document.querySelectorAll('.auth-error')[2].style.display = 'none';
        document.querySelector('.form-submit').removeAttribute('disabled');
    }
}

// Check email is valid && submit form 

async function checkEmail(email){
    const response = await fetch(`/auth/check/${email}`)
    let is404 = true;

    if(response.status === 404){
        is404 = false;
    }
   
    document.querySelector('.auth-error').style.display = is404 ? 'none' : 'block'
    return is404;
}

async function submitEditForm(){
    if(await checkEmail(document.querySelector('#email').value)){
        document.querySelector('.edit-form').submit();
    }
}

// user dashboard 

// Open side menu

function openNav(){
    document.querySelector('.mobile-menu').style.display = 'none';
    document.querySelector('.left').style.display = 'block';
    document.querySelector('.right').style.display = 'none';
    document.querySelector('.close-menu').style.display = 'block';
    var x = document.querySelectorAll('.return-home');
    var i;
    for (i = 0; i < x.length; i++){
        x[i].style.paddingTop = '20px';
    }
}

function closeNav(){
    document.querySelector('.mobile-menu').style.display = 'block';
    document.querySelector('.left').style.display = 'none';
    document.querySelector('.right').style.display = 'block';
    document.querySelector('.close-menu').style.display = 'none';
    var x = document.querySelectorAll('.return-home');
    var i;
    for (i = 0; i < x.length; i++){
        x[i].style.paddingTop = '0px';
    }
}

function goHome(){
    document.querySelector('.left').classList.remove('order-width');
    document.querySelector('.edit-product-wrapper').style.display = 'none';
    document.querySelector('.dashboard-links').style.display = 'block';
    document.querySelector('.settings').style.display = 'none';
    document.querySelector('.order-tab').style.display = 'none';
    document.querySelector('.show-order-information').style.display = 'none';
    document.querySelector('.view-edit-container').style.display = 'block';
}

function showStore(){
    document.querySelector('.dashboard-links').style.display = 'none';
    document.querySelector('.edit-product-wrapper.dashboard').style.display = 'block';
    document.querySelector('.settings').style.display = 'none';
    document.querySelector('.show-order-information').style.display = 'none';
}

function showSettings(){
    document.querySelector('.dashboard-links').style.display = 'none';
    document.querySelector('.edit-product-wrapper.dashboard').style.display = 'none';
    document.querySelector('.settings').style.display = 'block';
    document.querySelector('.show-order-information').style.display = 'none';
}

function showOrders(){
    document.querySelector('.dashboard-links').style.display = 'none';
    document.querySelector('.edit-product-wrapper.dashboard').style.display = 'none';
    document.querySelector('.settings').style.display = 'none';
    document.querySelector('.order-tab').style.display = 'block';
    document.querySelector('.left').classList.add('order-width');
    document.querySelector('.view-edit-container').style.display = 'none';
}

// Check contact email is valid when user edits their product 

function validateEditForm() {
    if(validateEmail(document.querySelector('#store-contact').value)){
        if(document.querySelector('#store-heading').value != '' && document.querySelector('#item-name').value != '' && document.querySelector('#edit-textarea').value != '' && document.querySelector('#store-price').value != ''){
            document.querySelector('.edit-form').submit();
        }
    }
    else{
        document.querySelector('.contact-email-error').style.display = 'block';
    }
}


// If user is on dashboard remove required attribute since user can't delete their image, can only change it
if(document.querySelector('.dashboard')){
    document.querySelector('#item_img').removeAttribute('required');
}

// Fetch order details and display without reload

async function fetchOrder(order_id){
    const result = await fetch(`/show/order/${order_id}`)
    const response = await result.json();
    
    document.querySelector('.show-order-information').style.display = 'block';
    document.querySelector('.order-update-success').style.display = 'none';
    
    document.querySelector('#view-order-number').innerHTML = 'ORDER #' + response.order_id;
    document.querySelector('#view-order-email').innerHTML = 'EMAIL: ' + response.email;
    document.querySelector('#view-order-shipping').innerHTML = response.name + '<br>' + response.line_one + '<br>' + response.line_two + '<br>' + response.city + '<br>' + response.post_code + '<br>' + response.country;
    if(response.status === 'Paid'){
        document.querySelector('.order-complete').style.display = 'block';
        document.querySelector('.order-complete').setAttribute('onclick', `updateOrderStatus('${response.order_id}')`)
    }
}

// Update order status

async function updateOrderStatus(order_id){
    const result = await fetch(`/show/order/${order_id}/update/status`);
    
    if(result.status === 400){
        document.querySelector('.order-update-fail').style.display = 'block';
    }
    else{
        document.querySelector('.order-complete').style.display = 'none';
        document.querySelector(`.order-status-${order_id} span`).innerHTML = 'Fulfilled';
        document.querySelector('.order-update-success').style.display = 'block';
    }
}

// check if store name is available 

async function checkStoreAvailability(){
    const store_url = document.querySelector('#store_url').value
    if(store_url.length < 3){
        document.querySelector('.store-url-error').style.display = 'block';
    }
    else{
        document.querySelector('.store-url-error').style.display = 'none';
        const response = await fetch(`/url/check/${store_url}`)
        if (response.status === 400){
            document.querySelector('.url-error').style.display = 'block';
        }
        else{
            document.querySelector('#url-anchor').innerHTML = `https://usell.com/@${store_url}`;
            document.querySelector('#url-anchor').href = `/@${store_url}`;
            document.querySelector('.url-error').style.display = 'none';
        }
    }
}

// Stripe

const stripe = Stripe('STRIPE_PUBLIC_API_KEY');

async function createCheckoutSession(store_url){
    document.cookie = `store_url=${store_url}; expires=Fri, 31 Dec 9999 23:59:59 GMT`;
    document.querySelector('.return-to-dashboard').style.display = 'none';
    document.querySelector('.loading-container').style.display = 'flex';
    const response = await fetch('/checkout');
    const session = await response.json();

    result = await stripe.redirectToCheckout({
        sessionId: session
    })
}