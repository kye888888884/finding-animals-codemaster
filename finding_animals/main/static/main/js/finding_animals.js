const btn = document.getElementById("btn");
const btn_prev = document.getElementById("btn-prev");
const btn_next = document.getElementById("btn-next");
const total_page = document.getElementById("total-page");
const result_container = document.getElementById("result-container");
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
            let div = document.createElement("div");
            div.className = "result";
            div.innerHTML = `
            <div class="result-img">
                <img src="${
                    image_base_url + result[i].filePath
                }" alt="result-img">
            </div>
            <div class="result-info">
                <div class="result-info-title">
                    <h3>${result[i].animalSeq}</h3>
                </div>
            </div>
            `;
            result_container.appendChild(div);
        }
    });
}
