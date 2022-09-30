document.addEventListener("DOMContentLoaded", () => {
  const modal = document.querySelector("#modal");
  const modalTitle = document.querySelector("#modalTitle");
  const modalBody = document.querySelector("#modalBody");
  const createCategory = document.querySelector("#createCategory");
  createCategory.addEventListener("click", () => {
    modalTitle.innerText = "Crear categoría";
    const form = createCategoryForm("Crear categoría", false);
    modalBody.insertAdjacentElement("beforeend", form);
    modal.classList.add("modal--is-open");
  });
  Array.from(document.getElementsByClassName("edit__button")).forEach(
    (item) => {
      item.addEventListener("click", (event) => {
        const categoryId = event.currentTarget.dataset.id;
        const data = new FormData();
        data.append("get_category", JSON.stringify({ id: categoryId }));
        sendData("/library/category/", "POST", data, (response) => {
          if (response.response) {
            modalTitle.innerText = "Editar categoría";
            const form = createCategoryForm(
              "Editar categoría",
              true,
              response.data
            );
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
        data.append("delete_category", JSON.stringify({ id: categoryId }));
        sendData("/library/category/", "POST", data, (response) => {
          if (response.response) {
            window.location.replace(response.redirect);
          } else {
            const mainContentContainer = document.querySelector(
              ".main__content-container"
            );
            const div = document.createElement("div");
            div.classList.add("main__information");
            if (mainContentContainer.childElementCount > 5) {
              mainContentContainer.remove(
                mainContentContainer.lastElementChild
              );
            }
            createAlerts(div, response.detail);
            mainContentContainer.insertAdjacentElement("beforeend", div);
          }
        });
      });
    }
  );
});
