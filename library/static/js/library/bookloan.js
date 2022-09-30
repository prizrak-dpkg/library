document.addEventListener("DOMContentLoaded", () => {
  const modal = document.querySelector("#modal");
  const modalTitle = document.querySelector("#modalTitle");
  const modalBody = document.querySelector("#modalBody");
  const returnBook = document.querySelector("#returnBook");
  returnBook.addEventListener("click", () => {
    const data = new FormData();
    modalTitle.innerText = "Registrar devolución";
    const form = createUserBookLoanForm("Registrar devolución");
    modalBody.insertAdjacentElement("beforeend", form);
    modal.classList.add("modal--is-open");
  });
  Array.from(document.getElementsByClassName("loan__button")).forEach(
    (item) => {
      item.addEventListener("click", (event) => {
        const bookId = event.currentTarget.dataset.id;
        const data = new FormData();
        data.append("get_bookloan", JSON.stringify({ id: bookId }));
        sendData("/library/bookloan/", "POST", data, (response) => {
          if (response.response) {
            modalTitle.innerText = "Registrar préstamo";
            const form = createBookLoanForm(
              "Registrar préstamo",
              response.data
            );
            modalBody.insertAdjacentElement("beforeend", form);
            modal.classList.add("modal--is-open");
          }
        });
      });
    }
  );
});
