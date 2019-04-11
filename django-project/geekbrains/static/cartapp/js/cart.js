$("tbody").on( "click",".cart-button",function () {
    var input_object = $(event.target).closest(
        'div'
    ).find(
        '.cart-input-quantity'
    );

    var quantity = parseInt(input_object.attr('value'));
    var cart_id = input_object.attr('name');

    ($(this).val() == "+") ? quantity++ : quantity--;
    $.ajax(
        "/cart/update/" + cart_id + "/quantity/" + quantity,
        {
            success: function (data) {
                $("tbody").html(data.result);
            }
        }
    );
    input_object.val(quantity);
});
