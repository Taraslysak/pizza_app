enableLogoutButton()

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
