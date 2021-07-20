$(document).ready(function () {
  $(".custom-select,#vehicle_no").change(function () {
    console.log("changed");
    if ($(".custom-select").val() === "entry") {
      if ($("#vehicle_no").val() != "") {
        console.log("ajdsk");
        $.ajax({
          type: "POST",
          url: "/vehicles/checkReg/",
          data: {
            entry: $("#vehicle_no").val(),
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").prop(
              "value"
            ),
          },
          dataType: "json",
          success: function (data) {
            if (data.is_success) {
              $("#checkvehinfo").attr("style", "display : block !important");
              $("#checkvehinfo").text(data.message);
              $("#entry-info").fadeOut(1000);
              $("#entry-info input").attr("required", false);
              setTimeout(() => {
                $("#checkvehinfo").attr("style", "display : none !important");
              }, 2000);
            } else {
              if (data.FlowError) {
                console.log("FLowError");
                $("#checkvehinfo").attr(
                  "style",
                  "display : block !important; background-color:red !important"
                );
                $("#checkvehinfo").text(data.message);
                $("#entry-info").fadeOut(1000);
                $("#entry-info input").attr("required", false);
                setTimeout(() => {
                  $("#checkvehinfo").attr("style", "display : none !important");
                }, 2000);
              } else {
                $("#entry-info").fadeIn(1000);
                $("#entry-info input").attr("required", true);
              }
            }
          },
        });
      } else {
        $("#checkvehinfo").attr(
          "style",
          "display : block !important; background-color: red !important"
        );
        $("#checkvehinfo").text("First enter the Vehicle number ");
        $(".custom-select").val("");
        // $("#checkvehinfo").attr("style", "display : none !important;");
        setTimeout(() => {
          $("#checkvehinfo").attr("style", "display : none !important;");
        }, 1000);
      }
    } else {
      $("#entry-info").fadeOut(1000);
      $("#entry-info input").attr("required", false);
    }
  });
});

setTimeout(() => {
  $("#messages").fadeOut("slow");
}, 3000);
