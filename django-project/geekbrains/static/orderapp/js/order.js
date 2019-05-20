window.onload = function () {
    $('.content').on('change', 'input[type="number"], input[type="checkbox"]', orderUpdate);
    $('.content').on('change', 'select', priceUpdate);

    function orderUpdate() {
        let totalForms = parseInt($('#id_order-TOTAL_FORMS').val()) || 0;
        let orderProductsQuantity = 0;
        let orderProductsCost = 0;

        for (let i = 0; i < totalForms; i++) {
            let quantity = parseInt($('#id_order-' + i + '-quantity').val()) || 0;
            let price = parseFloat($('#id_order-' + i + '-price').text().replace(',', '.')) || 0;
            // let isRemoved = $('#id_order-' + i + '-DELETE').is(":checked") ? 0 : 1;
            let isRemoved = ($('#id_order-' + i + '-DELETE').val() || false) ? 0 : 1;

            orderProductsQuantity += quantity * isRemoved;
            orderProductsCost += quantity * price * isRemoved;
        }

        $('.order-products-cost').html(orderProductsCost.toString());
        $('.order-products-quantity').html(orderProductsQuantity.toString());
    }

    function priceUpdate() {
        let productId = $(this).val();
        let updatingId = '#' + $(this)[0].id.replace('product', 'price');

        $.ajax(
            "/products/detail/" + productId,
            {
                headers: {
                    'Content-Type': 'application/json',
                },
                success: function (data) {
                    // process json
                    let price = 0;
                    try {
                        let product = JSON.parse(data);
                        price = product[0]['fields']['price'];
                    } catch (e) {
                        console.error("cannot get product price, " + e.message);
                    }

                    // store and update data
                    $(updatingId).html(price.toString());
                    orderUpdate();
                }
            }
        )
    }

    $('.orderitem-row').formset({
        addText: 'Добавить продукт',
        deleteText: 'Удалить',
        prefix: 'order',
        removed: orderUpdate
    });
};
