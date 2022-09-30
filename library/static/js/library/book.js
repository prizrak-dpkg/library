document.addEventListener("DOMContentLoaded", () => {
  const modal = document.querySelector("#modal");
  const modalTitle = document.querySelector("#modalTitle");
  const modalBody = document.querySelector("#modalBody");
  const createBook = document.querySelector("#createBook");
  createBook.addEventListener("click", () => {
    const data = new FormData();
    data.append("get_book_options", true);
    sendData("/library/book/", "POST", data, (response) => {
      if (response.response) {
        modalTitle.innerText = "Registrar libro";
        const form = createBookForm("Registrar libro", false, response.data);
        modalBody.insertAdjacentElement("beforeend", form);
        modal.classList.add("modal--is-open");
      }
    });
  });
  Array.from(document.getElementsByClassName("edit__button")).forEach(
    (item) => {
      item.addEventListener("click", (event) => {
        const bookId = event.currentTarget.dataset.id;
        const data = new FormData();
        data.append("get_book", JSON.stringify({ id: bookId }));
        sendData("/library/book/", "POST", data, (response) => {
          if (response.response) {
            modalTitle.innerText = "Editar libro";
            const form = createBookForm("Editar libro", true, response.data);
            modalBody.insertAdjacentElement("beforeend", form);
            modal.classList.add("modal--is-open");
          }
        });
      });
    }
  );
  Array.from(document.getElementsByClassName("delete__button")).forEach(
    (item) => {
      item.addEventListener("click", (event) => {
        const categoryId = event.currentTarget.dataset.id;
        const data = new FormData();
        data.append("delete_book", JSON.stringify({ id: categoryId }));
        sendData("/library/book/", "POST", data, (response) => {
          if (response.response) {
            window.location.replace(response.redirect);
          } else {
            const mainContentContainer = document.querySelector(
              ".main__content-container"
            );
            const div = document.createElement("div");
            div.classList.add("main__information");
            if (mainContentContainer.childElementCount > 5) {
              mainContentContainer.lastElementChild.remove();
            }
            createAlerts(div, response.detail);
            mainContentContainer.insertAdjacentElement("beforeend", div);
          }
        });
      });
    }
  );
});
