$(document).ready(function () {
    $("select#id_role").change(function () {
        if ($("select#id_role").val() != "Participant") {
            $("#div_id_weight").hide()
            $("#div_id_rank").hide()
        } else {
            $("#div_id_weight").show()
            $("#div_id_rank").show()
        }
    })
    for (let i = 1; i < 20; i++) {//max level 20 it's equal 2^20 users
        let level = $("div.form-inline.my-2 input[value=" + i + "][type='text']").parent()
            if (i % 2 == 0)
                level.wrapAll("<div class='alert alert-warning'></div>")
            else
                level.wrapAll("<div class='alert alert-info'></div>")
        }

});