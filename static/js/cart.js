var updateBtns = document.getElementsByClassName('update-cart');

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('productId:', productId, 'Action:', action);

        console.log('USER:', user);
        if (user === 'AnonymousUser') {
            addCookieItem(productId, action);
        } else {
            updateUserOrder(productId, action);
        }
    })
}

function updateUserOrder(productId, action) {
    // This function takes the productId and action from the html element
    // and makes changes to the orderItem with the productId pk
    // This is for logged in user
    console.log('User is authenticated, sending data...');

    var url = '/update_item/';

    fetch(url, {
        method:'POST',
        headers:{
            "Content-Type":'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action':action})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log('data:', data);
        location.reload();
    })
}

function addCookieItem(productId, action) {
    // This function takes the productId and action from the html element
    // and makes changes to the orderItem with the productId pk
    // This is for anonymous user
    if (action =='add') {
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity':1};
        } else {
            cart[productId]['quantity'] += 1;
        }
    }
    if (action =='remove') {
        cart[productId]['quantity'] -= 1;

        if (cart[productId]['quantity'] <= 0) {
            delete cart[productId];
        }
    }
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/;'
    location.reload();
}








