enableLogoutButton()
addCartStatusListener()

document.querySelector('.cart-icon-button').onclick = showCart
document.querySelector('.button-checkout').onclick = hideCart

function enableLogoutButton(){
    let logoutButton = document.querySelector('.button-logout');
    if (window.location.pathname === '/login'){

        logoutButton.innerHTML = 'Register'

        logoutButton.onclick = () =>{
            location.pathname = '/register';
        }

    } else if (window.location.pathname === '/register'){

        logoutButton.innerHTML = 'Login'

        logoutButton.onclick = () =>{
            location.pathname = '/login';
        }

    } else {

        logoutButton.onclick = () =>{

            location.pathname = '/logout';

        }
    }
}

function addCartStatusListener(){
    document.querySelectorAll('.update-cart').forEach(updateButton => {
        return updateButton.onclick = updateCart;
    })
}


 function updateCart(){
    //updateCartStatusCounter();
    fetch(`update-cart/${parseInt(this.dataset.meal)}`)
    .then(response => response.json())
    .then(data => {
        updateCartStatusCounter();
        return console.log(data.answer);
    })
 }


function updateCartStatusCounter(){
    cartIcon = getCartIcon()
    cartIcon.innerHTML ++;
     
}


function resetCartSatusCounter(){
    cartIcon = getCartIcon()
    cartIcon.innerHTML = null
}


function getCartIcon(){
    try{
        var cartIcon = document.querySelector('.cart-status');
        return cartIcon
    }
    catch (error){
        console.log(error);
    }
}

function showCart(){
    document.querySelector('.cart-view').style.display = 'block'
    console.log('shown')
}

function hideCart(){
    document.querySelector('.cart-view').style.display = 'none'
    console.log('hidden')
}
