const btn = document.getElementById("btn-submit");
const result_container = document.getElementById("result-container");
const input_species = document.getElementById("species");
const image_base_url = "http://www.daejeon.go.kr/FileUpload/ANI/";
const canvas = document.getElementById("upload-canvas");

let can_loading = false;
let page_count = 1;
const page_num = 12;

let pred = []; // 유사도 검색을 위한 행렬
let on_sim = false; // 유사도 검색 여부

let on_inputs = [false, false, false, false]; // 검색 조건 입력 여부

let top_result = "";

function show(id) {
    $(id).css("display", "block");
    $(id).css("height", "100%");
    $(id).css("opacity", "1");
}

function scroll(id, idx) {
    if (on_inputs[idx]) {
        return;
    }
    on_inputs[idx] = true;
    window.scrollBy({
        top: $(id).outerHeight(true),
        behavior: "smooth",
    });
}

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
        if ($(this).val() != 3) {
            show("#upload-input");
        } else {
            show("#gender-input");
        }
        scroll("#class-input", 0);
        change_species();
    });

    $("button.image2").click(function () {
        show("#gender-input");
        scroll("#upload-input", 1);
    });

    $("input:radio[name=gender]").on("change", function () {
        show("#species-input");
        show("#btn-submit");
        scroll("#gender-input", 2);
        change_species();
        $("#species").val(top_result);
    });

    change_species();
};

setInterval(function () {
    if (detectBottom() && can_loading) {
        can_loading = false;
        setTimeout(function () {
            search(true);
            can_loading = true;
        }, 500);
    }
}, 200);

function loadFile(input) {
    show("#gender-input");
    var file = input.files[0];
    var newImage = document.createElement("img");
    url = URL.createObjectURL(file);
    newImage.src = url;
    newImage.style.height = "224px";
    newImage.className = "upload-img";
    const img = new Image();
    img.src = url;
    img.onload = function () {
        $("#image-container").html(newImage);
        $("#image-container").css("margin-top", "50px");

        let csrftoken = document.getElementsByName("csrfmiddlewaretoken")[0]
            .value;

        // 캔버스를 가져와서 이미지를 그린다음에
        var ctx = canvas.getContext("2d");
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        // 224x224 크기로 캔버스에 그리기
        ctx.drawImage(img, 0, 0, 224, 224);

        // 이미지를 base64로 인코딩한다.
        var dataURL = canvas.toDataURL();

        let formData = new FormData();
        formData.append(
            "classification",
            $("input:radio[name=classification]:checked").val()
        );
        formData.append("image_data", dataURL);

        console.log(formData);

        $.ajax({
            type: "POST",
            url: "/upload/",
            headers: { "X-CSRFToken": csrftoken },
            cache: false,
            data: formData,
            processData: false,
            contentType: false,
        }).done(function (data) {
            $(".add-desc").removeAttr("hidden");
            pred = data.predict;
            on_sim = true;
            result = data.ranks;
            // Eng to Kor
            for (let i = 0; i < result.length; i++) {
                result[i] = eng_to_kor[result[i]];
            }
            top_result = result[0];
            // console.log(top_result);
            $("#add-container").html("");
            $("#species").val(top_result);
            for (let i = 1; i <= 3; i++) {
                let div = document.createElement("div");
                div.className = "add-item";
                div.innerHTML = `
                <button class="add-button">${result[i]}</button>
                `;
                $("#add-container").append(div);
            }
            $(".add-button").click(function () {
                $("#species").val($(this).text());
            });
        });
    };
}

function detectBottom() {
    var scrollTop = $(window).scrollTop();
    var innerHeight = $(window).innerHeight();
    var scrollHeight = $("body").prop("scrollHeight");
    if (scrollTop + innerHeight >= scrollHeight - 400) {
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
        page_count = 1;
        result_container.innerHTML = "";
        $("#search-container").removeAttr("hidden");
        if (!is_filter) {
            document
                .getElementById("result-container")
                .scrollIntoView({ block: "start", behavior: "smooth" });
        }
    }

    let csrftoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    haircolors = [];
    let i = 0;
    $("button.color").each(function () {
        haircolors.push(!$(this).hasClass("offon-button"));
    });

    species = getKeyByValue(id_to_name, $("#species").val());
    if (species == undefined) {
        species = 0;
    }

    let data = {
        classification: Number(
            $("input:radio[name=classification]:checked").val()
        ),
        gender: Number($("input:radio[name=gender]:checked").val()),
        gu: Number($("#gu").val()),
        species: Number(species),
        haircolors: haircolors,
        age: Number($("#age").val()),
        weight: $("#weight").val(),
        status: Number($("#status").val()),
        page: page_count,
        on_sim: on_sim,
        pred: on_sim ? JSON.stringify(pred) : 0,
    };

    // console.log(data);

    $("#no-result").hide();
    $("#loading").show();

    $.ajax({
        type: "POST",
        url: "/search/",
        headers: { "X-CSRFToken": csrftoken },
        cache: false,
        data: JSON.stringify(data),
    }).done(function (data) {
        // console.log(data);

        const no_additional_result = data.total_count < page_num * page_count;

        count_stack = page_num * (page_count - 1);

        if (data.count == 0) {
            // 검색 결과가 없을 경우
            page_count = 1;
        } else if (!is_append) {
            // 로딩이 아닌 검색일 경우
            page_count = 2;
        } else {
            // 로딩일 경우
            page_count += 1;
        }

        // 검색 결과가 없으면 no-result를 보여준다.
        if (data.count == 0 && !is_append) $("#no-result").show();
        else $("#no-result").hide();

        // 더 이상 검색 결과가 없으면 로딩을 숨긴다.
        if (no_additional_result) {
            $("#loading").hide();
            can_loading = false;
        } else {
            $("#loading").show();
            can_loading = true;
        }

        if (data.count == 0) {
            return;
        }

        result = JSON.parse(data.result);
        for (let i = 0; i < data.count; i++) {
            let src;
            if (result[i].filepath != null) {
                src = image_base_url + result[i].filepath;
            } else {
                src = $("#no-image").text();
            }

            // descMain: 종, 믹스여부, 공고 상태, 발견 날짜
            let descMain = id_to_name[result[i].species];
            if (descMain != "믹스" && result[i].is_mix == 1) {
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
            if (i + count_stack < data.sim_count) {
                descSub += " / AI 검색";
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
