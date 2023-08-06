const DATANUM = 295;
const divProgress = document.getElementById("progress");
// const SERVICE_KEY = "your service key"

const classes = [
    "adoptionStatusCd",
    "age",
    "animalSeq",
    "classification",
    "fileNm",
    "filePath",
    "foundPlace",
    "gender",
    "gu",
    "hairColor",
    "hitCnt",
    "memo",
    "modDtTm",
    "regDtTm",
    "regId",
    "rescueDate",
    "species",
    "weight",
];
let idx_count = 0;

main();

async function main() {
    let csv = "\ufeff" + "index,";
    for (let i = 0; i < classes.length; i++) {
        csv += classes[i] + ",";
    }
    csv += "\n";

    idx_count = 0; // 열 하나당 1씩 증가
    let i_count = 0; // 진행도 표시용
    for (let i = 1; i <= DATANUM; i++) {
        try {
            let result = await getData(i);
            console.log("complete: " + i);
            csv += makeList(result, i_count);
            divProgress.innerHTML = `진행도: ${i}/${DATANUM} (${Math.floor(
                (i / DATANUM) * 100
            )}%)`;
            i_count++;
        } catch (error) {
            console.log(error);
        }
    }

    // csv 파일 다운로드
    let hiddenElement = document.createElement("a");
    hiddenElement.href = "data:text/csv;charset=utf-8," + encodeURI(csv);
    hiddenElement.target = "_blank";
    hiddenElement.download = "data.csv";
    hiddenElement.click();
}

async function getData(idx) {
    let promise = new Promise((resolve, reject) => {
        var xhr = new XMLHttpRequest();
        var url =
            "http://apis.data.go.kr/6300000/animalDaejeonService/animalDaejeonList"; /*URL*/
        var queryParams =
            "?" +
            encodeURIComponent("serviceKey") +
            "=" +
            SERVICE_KEY; /*Service Key*/
        queryParams +=
            "&" +
            encodeURIComponent("pageNo") +
            "=" +
            encodeURIComponent(idx.toString()); /**/
        xhr.open("GET", url + queryParams);
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4) {
                // console.log(this.responseText);
                resolve(xhr.responseText);
            }
        };

        xhr.send("");
    });
    return promise;
}

function makeList(data) {
    // console.log(data);

    // const textResult = document.getElementById("result");

    // HTML 객체로 변환
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(data, "text/xml");

    // ServiceResult
    const ServiceResult = xmlDoc.getElementsByTagName("MsgBody")[0];
    // const resultStr = ServiceResult.innerHTML;

    // count는 ServiceResult 자식 노드의 개수
    const count = ServiceResult.childElementCount;

    // csv 파일로 저장
    let csv = "";
    for (let i = 0; i < count; i++) {
        csv += idx_count.toString() + ",";
        let child = ServiceResult.children[i];
        for (let j = 0; j < classes.length; j++) {
            let label = classes[j];
            try {
                let text = child.getElementsByTagName(label)[0].innerHTML;
                text = text.replace(/,/g, " &");
                csv += text;
            } catch (error) {}
            csv += ",";
        }
        idx_count++;
        csv += "\n";
    }

    return csv;
}

// queryParams +=
//     "&" +
//     encodeURIComponent("pageNo") +
//     "=" +
//     encodeURIComponent("1"); /**/
// queryParams +=
//     "&" +
//     encodeURIComponent("numOfRows") +
//     "=" +
//     encodeURIComponent("10"); /**/
// queryParams +=
//     "&" +
//     encodeURIComponent("searchCondition") +
//     "=" +
//     encodeURIComponent("1"); /**/
// queryParams +=
//     "&" +
//     encodeURIComponent("searchCondition2") +
//     "=" +
//     encodeURIComponent("1"); /**/
// queryParams +=
//     "&" +
//     encodeURIComponent("searchCondition3") +
//     "=" +
//     encodeURIComponent("1"); /**/
// queryParams +=
//     "&" +
//     encodeURIComponent("species") +
//     "=" +
//     encodeURIComponent("진도"); /**/
// queryParams +=
//     "&" +
//     encodeURIComponent("memo") +
//     "=" +
//     encodeURIComponent("콧물"); /**/
// queryParams +=
//     "&" +
//     encodeURIComponent("regId") +
//     "=" +
//     encodeURIComponent("123-1"); /**/
// queryParams +=
//     "&" +
//     encodeURIComponent("gubun") +
//     "=" +
//     encodeURIComponent("수,암"); /**/
// queryParams +=
//     "&" +
//     encodeURIComponent("searchKeyword") +
//     "=" +
//     encodeURIComponent("개,콧물감기"); /**/
