window.onload = function () {
    $('.content').on('click', '.menu-subcategories-a', function (event) {
        event.preventDefault();
        let products_link = $(this).attr('href') + '/ajax';
        $.ajax(products_link, {
            success: function (data) {
                console.log(data);
                $('.product-list').html(data.result);
            }
        })
    })
};
