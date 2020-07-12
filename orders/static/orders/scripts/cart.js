import { CartItem } from "./cartItem.js"


export class Cart {

    static show() {

        fetch('/render-cart')
            .then(response => {
                if (response.status == 200){
                    return response.json()
                } else{
                    throw Error(response.statusText);
                }
            })
            .then(data => {
                Cart.clear();
                Cart.populate(data);
                document.querySelector('.cart-view').style.display = 'block'
            }).catch(error => console.log(error))
    }

    static hide() {
        document.querySelector('.cart-view').style.display = 'none'
    }

    static clear() {
        document.querySelector('.cart-area').innerHTML = '';
    }

    static populate(data) {
            if (data.items) {
                data.items.forEach(item => Cart.renderItem(data, item));
                Cart.updateTotal(data.total);
            }
        }

    static renderItem(data, item) {

        let cartArea = document.querySelector('.cart-area');

        let itemContainer = document.createElement('div');
        itemContainer.className = 'item-container';

        let itemArea = Cart.createItemArea(item);

        let name = Cart.createName();

        if (item.type === 'Pizza') {
            if (item.option != 'Special') {
                name.innerHTML = `${item.size} ${item.name} ${item.type} with ${item.option}`;
            }
            else {
                name.innerHTML = `${item.option} ${item.size} ${item.name} ${item.type}`;
            }

            Cart.addToppingSelects(item, name, data);
        }
        else if (item.type === 'Sub') {
            name.innerHTML = `${item.size} ${item.type} with ${item.name}`;
            if (item.additional_extras === true) {
                Cart.addExtraCheckboxes(data.extras.additional, name);
            }
            Cart.addExtraCheckboxes(data.extras.basic, name)
        }
        else if (item.type === 'Dinner Platter') {
            name.innerHTML = `${item.size} ${item.name} ${item.type}`;
        }
        else {
            name.innerHTML = `${item.name} ${item.type}`;
        }

        let itemPrice = Cart.createItemPrice(item);

        let removeItemButton = Cart.createRemoveItemButton(item);

        itemArea.appendChild(name);
        itemArea.appendChild(itemPrice);
        itemArea.appendChild(removeItemButton);
        itemContainer.appendChild(itemArea);
        itemContainer.appendChild(document.createElement('hr'));
        cartArea.appendChild(itemContainer);
    }

    static addToppingSelects(item, name, data) {
        for (let toppingSelectCount = 0; toppingSelectCount < item.toppings_quantity; toppingSelectCount++) {

            let toppingSelect = Cart.createToppingSelect();
            toppingSelect.onchange = Cart.enableCheckoutIfAllToppingsSelected
            name.appendChild(toppingSelect);

            let defaultToppingOption = Cart.createDefaultToppingOption();
            toppingSelect.appendChild(defaultToppingOption);

            for (let toppingOptionCount = 0; toppingOptionCount < data.toppings.length; toppingOptionCount++) {
                let toppingOption = Cart.createToppingoption(data, toppingOptionCount);
                toppingSelect.appendChild(toppingOption);
            }

        }
    }

    static createRemoveItemButton(item) {
        let removeItemButton = document.createElement('button');
        removeItemButton.className = 'button remove-item-button';
        removeItemButton.innerHTML = 'Remove';
        removeItemButton.dataset.item_id = item.id;
        removeItemButton.onclick = Cart.removeItem;
        return removeItemButton;
    }

    static addExtraCheckboxes(extras, name) {
        for (let extrasCounter = 0; extrasCounter < extras.length; extrasCounter++) {

            let checkboxContainer = Cart.createCheckboxContainer();

            let extraCheckbox = Cart.createExtraCheckbox(extras, extrasCounter);

            checkboxContainer.appendChild(extraCheckbox);

            let extraLabel = Cart.createExtraLabel(extras, extrasCounter);

            checkboxContainer.appendChild(extraLabel);
            name.appendChild(checkboxContainer);
        }
    }

    static addItem() {
        fetch(`add-item/${parseInt(this.dataset.meal_id)}`)
            .then(response => response.json())
            .then(data => {
                Cart.updateStatusCounter(data.cartStatusCounter);
                Cart.updateTotal(data.total);
            })
    }

    static removeItem() {
        fetch(`remove-item/${parseInt(this.dataset.item_id)}`)
            .then(response => response.json())
            .then(data => {
                this.parentElement.parentElement.remove();
                Cart.updateStatusCounter(data.cartStatusCounter);
                Cart.updateTotal(data.total);
            })
    }

    static updateStatusCounter(counter) {
        var cartStatus = this.getElement('.cart-status')
        if (!cartStatus) {
            console.log("can't find cart status")
            return
        }

        var cartButton = this.getElement('.cart-icon-button')
        if (!cartButton) {
            console.log("can't find cart icon button")
            return
        }

        if (counter > 0) {
            cartStatus.innerHTML = counter;
            cartButton.disabled = false;
        } else {
            cartStatus.innerHTML = null;
            cartButton.disabled = true;
        }

    }

    static getElement(elementName) {
        try {
            var element = document.querySelector(elementName);
            return element
        }
        catch (error) {
            console.log(error);
        }
    }

    static updateSubPrice() {

        let subPriceDiv = this.parentElement.parentElement.parentElement.querySelector('.item-price');
        let totalPrice = document.querySelector('.total-value')

        if (this.checked === true) {
            subPriceDiv.innerHTML = `${(parseFloat(subPriceDiv.innerHTML) + parseFloat(this.dataset.price)).toFixed(2)} USD`
            totalPrice.innerHTML = `${(parseFloat(totalPrice.innerHTML) + parseFloat(this.dataset.price)).toFixed(2)} USD`
        }
        else if (this.checked === false) {
            subPriceDiv.innerHTML = `${(parseFloat(subPriceDiv.innerHTML) - parseFloat(this.dataset.price)).toFixed(2)} USD`
            totalPrice.innerHTML = `${(parseFloat(totalPrice.innerHTML) - parseFloat(this.dataset.price)).toFixed(2)} USD`
        }
    }

    static updateTotal(total) {
        document.querySelector('.total-value').innerHTML = `${total} USD`;
    }

    static createToppingSelect() {
        let toppingSelect = document.createElement('select');
        toppingSelect.className = 'topping_select';
        
        return toppingSelect;
    }

    static enableCheckoutIfAllToppingsSelected(){
        let toppingSelects = document.querySelectorAll('.topping_select');
        toppingSelects = Array.prototype.map.call(toppingSelects, select => select.value)
        let confirmButton = document.querySelector('.button-checkout')
        if (!toppingSelects.includes('None')){
            confirmButton.disabled = false
        } else{
            confirmButton.disabled = true
        }
    }

    static createToppingoption(data, toppingOptionCount) {
        let toppingOption = document.createElement('option');
        toppingOption.innerHTML = data.toppings[toppingOptionCount].name;
        toppingOption.dataset.id = data.toppings[toppingOptionCount].id;
        return toppingOption;
    }

    static createDefaultToppingOption() {
        let defaultToppingOption = document.createElement('option');
        defaultToppingOption.innerHTML = 'None';
        defaultToppingOption.defaultSelected = true;
        return defaultToppingOption;
    }

    static createName() {
        let name = document.createElement('div');
        name.className = 'item-name';
        return name;
    }

    static createCheckboxContainer() {
        let checkboxContainer = document.createElement('div');
        checkboxContainer.className = 'checkbox-container';
        return checkboxContainer;
    }

    static createExtraLabel(extras, extrasCounter) {
        let extraLabel = document.createElement('label');
        extraLabel.className = 'extra-label';
        extraLabel.innerHTML = `Extra ${extras[extrasCounter].name} (+${extras[extrasCounter].price} USD)`;
        return extraLabel;
    }

    static createExtraCheckbox(extras, extrasCounter) {
        let extraCheckbox = document.createElement('input');
        extraCheckbox.className = 'extra-checkbox';
        extraCheckbox.type = 'checkbox';
        extraCheckbox.checked = false;
        extraCheckbox.dataset.price = extras[extrasCounter].price;
        extraCheckbox.dataset.id = extras[extrasCounter].id;
        extraCheckbox.onchange = Cart.updateSubPrice
        return extraCheckbox;
    }
    

    static createItemArea(item) {
        let itemArea = document.createElement('div');
        itemArea.className = 'item-area';
        itemArea.dataset.id = item.id;
        return itemArea;
    }

    static createItemPrice(item) {
        let itemPrice = document.createElement('div');
        itemPrice.className = 'item-price';
        itemPrice.innerHTML = `${item.price} USD`;
        return itemPrice;
    }

}
