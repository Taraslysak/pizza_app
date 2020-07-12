import {Cart} from './cart.js'
import {ConfirmWindow} from './confirmWindow.js'

renderLogoutButton()
addCartStatusListener()

document.querySelector('.cart-icon-button').onclick = Cart.show;

document.querySelector('.button-return').onclick = Cart.hide;
document.querySelector('.button-checkout').onclick = ConfirmWindow.show;
document.querySelector('.button-confirm').onclick = ConfirmWindow.confirmPurchase;
document.querySelector('.button-reject-confirmation').onclick = ConfirmWindow.hide;


function renderLogoutButton(){
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
        return updateButton.onclick = Cart.addItem;
    })
}
