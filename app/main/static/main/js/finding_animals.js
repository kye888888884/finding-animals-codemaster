const btn = document.getElementById("btn");
const btn_prev = document.getElementById("btn-prev");
const btn_next = document.getElementById("btn-next");
const total_page = document.getElementById("total-page");
const result_container = document.getElementById("result-container");
const input_classification = document.getElementById("classification");
const input_species = document.getElementById("species");
const image_base_url = "http://www.daejeon.go.kr/FileUpload/ANI/";

btn.addEventListener("click", () => {
    $("#page").text("1");
    search();
});
btn_prev.addEventListener("click", () => {
    let page = parseInt($("#page").text());
    if (page > 1) {
        $("#page").text(page - 1);
        search();
    }
});
btn_next.addEventListener("click", () => {
    let page = parseInt($("#page").text());
    let total_page = parseInt($("#total-page").text());
    if (page < total_page) {
        $("#page").text(page + 1);
        search();
    }
});

// #classification의 값이 바뀌면 #species의 값을 바꿔준다.
input_classification.addEventListener("change", change_species);

function add_option(select, value, text) {
    let option = document.createElement("option");
    option.value = value;
    option.innerText = text;
    select.appendChild(option);
}

function change_species() {
    let classification = input_classification.value;
    input_species.innerHTML = "";
    spec_list = specs[classification - 1];
    add_option(input_species, "", "전체");
    for (let i = 0; i < spec_list.length; i++) {
        add_option(input_species, spec_list[i], spec_list[i]);
    }
}

change_species();

function search() {
    let csrftoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    let data = {
        classification: $("#classification").val(),
        gender: $("#gender").val(),
        gu: $("#gu").val(),
        species: $("#species").val(),
        haircolor: $("#haircolor").val(),
        age: $("#age").val(),
        weight: $("#weight").val(),
        status: $("#status").val(),
        page: $("span#page").text(),
    };

    console.log(data);

    $.ajax({
        type: "POST",
        url: "/search/",
        headers: { "X-CSRFToken": csrftoken },
        cache: false,
        data: JSON.stringify(data),
    }).done(function (data) {
        total_page.innerText = (data.total_count / 5).toFixed(0);

        result_container.innerHTML = "";
        result = JSON.parse(data.result);
        for (let i = 0; i < data.count; i++) {
            let src;
            if (result[i].filePath != null) {
                src = image_base_url + result[i].filePath;
            } else {
                src = $("#no-image").text();
            }

            let desc = result[i].species;
            desc += `(${status_list[result[i].adoptionStatusCd]})`;
            if (result[i].rescueDate != null) {
                desc += " / " + result[i].rescueDate + " 발견";
            }

            let div = document.createElement("div");
            div.className = "result";
            div.innerHTML = `
            <div class="result-img">
                <img src="${src}" alt="result-img">
            </div>
            <div class="result-info">
                <div class="result-info-title">
                    <h3>${desc}</h3>
                    <div style="margin-bottom: 20px">발견 장소: ${result[i].foundPlace}</div>
                </div>
            </div>
            `;
            result_container.appendChild(div);
        }
    });
}