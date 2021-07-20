$(document).ready(function () {
  $(".custom-select").change(function () {
    $(this).val() === "entry"
      ? $("#entry-info").fadeIn(1000)
      : $("#entry-info").fadeOut(1000);
  });
});
