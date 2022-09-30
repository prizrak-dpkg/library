document.addEventListener("DOMContentLoaded", () => {
  const modal = document.querySelector("#modal");
  const modalTitle = document.querySelector("#modalTitle");
  const modalBody = document.querySelector("#modalBody");
  Array.from(document.getElementsByClassName("sanction__button")).forEach(
    (item) => {
      item.addEventListener("click", (event) => {
        const userId = event.currentTarget.dataset.id;
        const data = new FormData();
        data.append("get_debt", JSON.stringify({ id: userId }));
        sendData("/library/debt/", "POST", data, (response) => {
          if (response.response) {
            modalTitle.innerText = "Registrar pago";
            const form = createDebtForm("Registrar pago", response.data);
            modalBody.insertAdjacentElement("beforeend", form);
            modal.classList.add("modal--is-open");
          }
        });
      });
    }
  );
});
