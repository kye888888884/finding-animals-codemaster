const btn = document.getElementById("btn-submit");
const result_container = document.getElementById("result-container");
const input_species = document.getElementById("species");
const image_base_url = "http://www.daejeon.go.kr/FileUpload/ANI/";

can_loading = false;
page_count = 1;

window.onload = function () {
    btn.addEventListener("click", () => {
        search();
    });

    $(".onoff-button").click(function () {
        $(this).toggleClass("offon-button");
    });

    $("#status").on("change", function () {
        search(false, true);
    });
    $("#gu").on("change", function () {
        search(false, true);
    });

    $("input:radio[name=classification]").on("change", function () {
        change_species();
    });
    change_species();
};

setInterval(function () {
    if (detectBottom() && can_loading) {
        can_loading = false;
        setTimeout(function () {
            console.log("bottom");
            search(true);
            can_loading = true;
        }, 500);
    }
}, 200);

function detectBottom() {
    var scrollTop = $(window).scrollTop();
    var innerHeight = $(window).innerHeight();
    var scrollHeight = $("body").prop("scrollHeight");
    if (scrollTop + innerHeight >= scrollHeight - 80) {
        return true;
    } else {
        return false;
    }
}

function add_option(select, value, text) {
    let option = document.createElement("option");
    option.value = value;
    option.innerText = text;
    select.appendChild(option);
}

function change_species() {
    let classification = $("input:radio[name=classification]:checked").val();
    input_species.innerHTML = "";
    spec_list = specs[classification - 1];
    add_option(input_species, "", "전체");
    for (let i = 0; i < spec_list.length; i++) {
        add_option(input_species, spec_list[i], spec_list[i]);
    }
}

function search(is_append = false, is_filter = false) {
    if (!is_append) {
        result_container.innerHTML = "";
        $("#search-container").removeAttr("hidden");
        if (!is_filter) {
            $("html, body").animate(
                { scrollTop: $(document).height() - 300 },
                1000
            );
        }
    }

    can_loading = true;

    let csrftoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    haircolors = [];
    let i = 0;
    $("button.color").each(function () {
        haircolors.push(!$(this).hasClass("offon-button"));
    });

    let data = {
        classification: $("input:radio[name=classification]:checked").val(),
        gender: $("input:radio[name=gender]:checked").val(),
        gu: $("#gu").val(),
        species: $("#species").val(),
        haircolors: haircolors,
        age: $("#age").val(),
        weight: $("#weight").val(),
        status: $("#status").val(),
        page: page_count,
    };

    console.log(data);

    $.ajax({
        type: "POST",
        url: "/search/",
        headers: { "X-CSRFToken": csrftoken },
        cache: false,
        data: JSON.stringify(data),
    }).done(function (data) {
        console.log(data);

        if (!is_append) {
            page_count = 1;
        }
        page_count += 1;
        result = JSON.parse(data.result);
        for (let i = 0; i < data.count; i++) {
            let src;
            if (result[i].filepath != null) {
                src = image_base_url + result[i].filepath;
            } else {
                src = $("#no-image").text();
            }

            // descMain: 종, 믹스여부, 공고 상태, 발견 날짜
            let descMain = result[i].species;
            if (result[i].species != "믹스" && result[i].is_mix == 1) {
                descMain += "(믹스)";
            }
            descMain += ` / ${status_list[result[i].status - 1]}`;
            if (result[i].rescue_date != null) {
                descMain += " / " + result[i].rescue_date + " 발견";
            }

            // descSub: 성별, 나이, 몸무게
            let gender = result[i].gender;
            let descSub =
                gender == 1 ? "수컷" : gender == 2 ? "암컷" : "알수없음";
            if (result[i].age != null) {
                descSub += ` / ${result[i].age}`;
            }
            if (result[i].weight != null) {
                descSub += ` / ${result[i].weight}kg`;
            }

            let div = document.createElement("div");
            div.className = "result";
            div.innerHTML = `
            <div class="result-img">
                <img src="${src}" alt="result-img">
            </div>
            <div class="result-info">
                <div class="result-info-title">
                    <h3>${descMain}</h3>
                    <h4>${descSub}</h4>
                    <div style="margin-bottom: 20px">발견 장소: ${result[i].locate}</div>
                </div>
            </div>
            `;
            result_container.appendChild(div);
        }
    });
}
