export class CartItem{
    static render(data, item) {

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
}