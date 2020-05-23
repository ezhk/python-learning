$(document).ready(() => {
  function showForm() {
    document.querySelector(".product-form").removeAttribute("hidden");
    document.querySelector(".product-view").classList.add("form-pop-filter");
  }

  function hideForm() {
    document.querySelector(".product-form").setAttribute("hidden", "hidden");
    document.querySelector(".product-view").classList.remove("form-pop-filter");
  }

  /*
    Get form data and apply classes,
    it needs for correctly suggest work on POST wrong form.
  */
  $("#add-button").on("click", function(e) {
    $.get({
      url: $(this).data("product-form"),

      success: (data) => {
        $("form").replaceWith(data);
        showForm();
      },
    });
  });


  // POST request form action
  $("#save-product").on("click", (e) => {
    e.preventDefault();

    $.post({
      url: $("form").attr("action"),
      data: $("form").serialize(),

      success: (data) => {
        $("table").html(data);
        hideForm();
      },

      error: (data) => {
        $("form").html(data.responseText);
      },
    });
  });

  // Hide form outside click
  $(document).click(function(e) {
    if (
      !$(e.target).closest(".product-form").length &&
      $("form").is(":visible")
    ) {
      hideForm();
    }
  });
});