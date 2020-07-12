import { Cart } from "./cart.js";

export class ConfirmWindow {
    

    static show(){
        document.querySelector('.confirm-view').style.display = 'block'
    }
    

    static hide(){
        document.querySelector('.confirm-view').style.display = 'none'
    }


    static confirmPurchase(){
        
        let outputData = {
                        'items': {},
                        'total': parseFloat(document.querySelector('.total-value').innerHTML)
        }

        let items = document.querySelectorAll('.item-area');
        ConfirmWindow.addItemsWithAdditives(items, outputData);

        let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value
        let url = `/confirm-purchase`;
        let init = {
            method: 'POST',
            headers: {
                'Content-Type': 'multipart/formdata',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(outputData)
        }

        fetch(url, init)
        .then(response =>{
            if (!response.ok){
                throw new Error(response.statusText)
            }
            ConfirmWindow.hide()
            Cart.hide()
            Cart.clear()
            Cart.updateStatusCounter(0)
        })
        .catch(error =>{
            console.log('Hey, You`ve got error', error);
        })
    }


    static addItemsWithAdditives(items, outputData) {
        items.forEach(cartItem => {
            ConfirmWindow.addPizzaToppings(cartItem, outputData);
            ConfirmWindow.addSubExtras(cartItem, outputData);
        });
    }

    
    static addPizzaToppings(cartItem, outputData) {
        let toppingSelects = cartItem.querySelectorAll('.topping_select');
        if (toppingSelects.length > 0) {
            let itemToppings = [];
            toppingSelects.forEach(toppingSelect => {
                itemToppings.push(toppingSelect.selectedOptions[0].dataset.id);
            });
            outputData.items[cartItem.dataset.id] = itemToppings;
        }
    }

    static addSubExtras(cartItem, outputData) {
        let extraCheckboxes = cartItem.querySelectorAll('.extra-checkbox');
        if (extraCheckboxes.length > 0) {

            let itemextras = [];
            extraCheckboxes.forEach(checkbox => {
                if (checkbox.checked == true) {
                    itemextras.push(checkbox.dataset.id);
                }
            });
            outputData.items[cartItem.dataset.id] = itemextras;
        }
    }
}