async function renderList() {
    let response = await fetch(`/api/sc/list`);

    console.log(response);
    if (!response.ok) {
        console.error(response);
        return;
    }

    let data = await response.json();
    console.log("1")


    let tbodyEl = document.createElement("tbody");
    for (let item of data) {

        let tdEl;
        console.log("2")

        tdEl = document.createElement("td");
        console.log("3")

        tdEl.innerText = item.term;
        tdEl.className = "col-term";
        console.log("4")

        trEl.append(tdEl);
        console.log("5")

    }

    let tableEl = document.querySelector("#student-table");
    document.querySelector("#student-table > tbody").remove();
    tableEl.append(tbodyEl);
}


document.addEventListener("DOMContentLoaded", (e) => {
    console.log("6")
    renderList();
    renderEditDialog();
});
