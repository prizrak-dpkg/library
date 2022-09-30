const sendData = async (destination, method, data, afterResponse) => {
  const serverResponse = await fetch(destination, {
    headers: {
      "X-CSRFToken": document.querySelector("input[name=csrfmiddlewaretoken]")
        .value,
    },
    method: method,
    body: data,
  });
  const serializedResponse = await serverResponse.json();
  afterResponse(serializedResponse);
};

const createButton = (buttonText) => {
  const button = document.createElement("button");
  button.classList.add("main__primary-button");
  button.innerText = buttonText;
  return button;
};

const createInput = (labelText, inputType, inputValue, inputPlaceholder) => {
  const inputContainer = document.createElement("div");
  const label = document.createElement("label");
  const span = document.createElement("span");
  const input = document.createElement("input");
  inputContainer.classList.add("input");
  label.classList.add("input__label");
  span.classList.add("input__label-text");
  span.innerText = labelText;
  input.classList.add("input__input");
  input.setAttribute("type", inputType);
  input.value = `${inputValue ? inputValue : ""}`;
  input.placeholder = `${inputPlaceholder ? inputPlaceholder : ""}`;
  label.insertAdjacentElement("beforeend", span);
  label.insertAdjacentElement("beforeend", input);
  inputContainer.insertAdjacentElement("beforeend", label);
  return [inputContainer, input];
};

const createSelect = (
  labelText,
  selectValue,
  selectOptions,
  selectPlaceholder
) => {
  const selectContainer = document.createElement("div");
  const label = document.createElement("label");
  const span = document.createElement("span");
  const select = document.createElement("select");
  const placeholder = document.createElement("option");
  selectContainer.classList.add("input");
  label.classList.add("input__label");
  span.classList.add("input__label-text");
  span.innerText = labelText;
  select.classList.add("input__input", "input__input--placeholder");
  placeholder.hidden = true;
  placeholder.value = "";
  placeholder.innerText = selectPlaceholder;
  select.insertAdjacentElement("beforeend", placeholder);
  selectOptions.forEach((selectOption) => {
    const option = document.createElement("option");
    option.value = `${selectOption.id}`;
    option.innerText = selectOption.name;
    select.insertAdjacentElement("beforeend", option);
  });
  select.addEventListener("change", () => {
    if (select.value == "") {
      select.classList.add("input__input--placeholder");
    } else {
      select.classList.remove("input__input--placeholder");
    }
  });
  select.value = `${selectValue ? selectValue : ""}`;
  selectValue ? select.classList.remove("input__input--placeholder") : null;
  label.insertAdjacentElement("beforeend", span);
  label.insertAdjacentElement("beforeend", select);
  selectContainer.insertAdjacentElement("beforeend", label);
  return [selectContainer, select];
};

const createAlerts = (container, details) => {
  const list = document.createElement("ul");
  const detail = details.reduce(
    (previousValue, currentValue) =>
      previousValue + `<li>* ${currentValue.field}: ${currentValue.error}</li>`,
    ""
  );
  list.classList.add("main__list");
  list.innerHTML = detail;
  container.innerHTML = "";
  container.insertAdjacentElement("beforeend", list);
};

const sendModal = (destination, data) => {
  sendData(destination, "POST", data, (response) => {
    if (response.response) {
      window.location.replace(response.redirect);
    } else {
      const modalFooter = document.querySelector("#modalFooter");
      createAlerts(modalFooter, response.detail);
    }
  });
};

const createReturnBookLoanForm = (buttonText, data) => {
  const form = document.createElement("form");
  const [bookLoan, bookLoanSelect] = createSelect(
    "Libro",
    "",
    data?.book_loan_options,
    "Seleccione el libro a devolver"
  );
  const sendButton = createButton(buttonText);
  form.classList.add("main__form");
  form.insertAdjacentElement("beforeend", bookLoan);
  form.insertAdjacentElement("beforeend", sendButton);
  sendButton.addEventListener("click", (event) => {
    event.preventDefault();
    const loanData = new FormData();
    loanData.append(
      "return_book",
      JSON.stringify({
        key: bookLoanSelect.value,
      })
    );
    sendModal("/library/bookloan/", loanData);
  });
  return form;
};

const queryUserBookLoans = (destination, data, buttonText) => {
  sendData(destination, "POST", data, (response) => {
    if (response.response) {
      const modalBody = document.querySelector("#modalBody");
      const form = createReturnBookLoanForm(buttonText, response.data);
      if (modalBody.childElementCount > 2) {
        modalBody.lastElementChild.remove();
      }
      modalBody.insertAdjacentElement("beforeend", form);
    } else {
      const modalFooter = document.querySelector("#modalFooter");
      createAlerts(modalFooter, response.detail);
    }
  });
};

const createCategoryForm = (buttonText, update, data) => {
  const form = document.createElement("form");
  const [category, categoryInput] = createInput(
    "Categoría",
    "text",
    data?.name,
    "Ingrese el nombre de la categoría"
  );
  const [standarLoan, standarLoanInput] = createInput(
    "Días de préstamo",
    "number",
    data?.standar_loan,
    "Ingrese el número de días de préstamo"
  );
  const [penaltyPayment, penaltyPaymentInput] = createInput(
    "Penalidad diaria",
    "number",
    data?.penalty_payment,
    "Ingrese el valor de la penalidad diaria"
  );
  const sendButton = createButton(buttonText);
  form.classList.add("main__form");
  form.insertAdjacentElement("beforeend", category);
  form.insertAdjacentElement("beforeend", standarLoan);
  form.insertAdjacentElement("beforeend", penaltyPayment);
  form.insertAdjacentElement("beforeend", sendButton);
  sendButton.addEventListener("click", (event) => {
    event.preventDefault();
    const categoryData = new FormData();
    if (update) {
      categoryData.append(
        "update_category",
        JSON.stringify({
          id: data.id,
          name: categoryInput.value,
          standar_loan: standarLoanInput.value,
          penalty_payment: penaltyPaymentInput.value,
        })
      );
    } else {
      categoryData.append(
        "create_category",
        JSON.stringify({
          name: categoryInput.value,
          standar_loan: standarLoanInput.value,
          penalty_payment: penaltyPaymentInput.value,
        })
      );
    }
    sendModal("/library/category/", categoryData);
  });
  return form;
};

const createBookForm = (buttonText, update, data) => {
  const form = document.createElement("form");
  const [title, titleInput] = createInput(
    "Título",
    "text",
    data?.title,
    "Ingrese el título del libro"
  );
  const [author, authorSelect] = createSelect(
    "Autor",
    data?.author,
    data?.author_options,
    "Seleccione el autor del libro"
  );
  const [publisher, publisherSelect] = createSelect(
    "Editorial",
    data?.publisher,
    data?.publisher_options,
    "Seleccione la editorial del libro"
  );
  const [category, categorySelect] = createSelect(
    "Categoría",
    data?.category,
    data?.category_options,
    "Seleccione la categoría del libro"
  );
  const [language, languageSelect] = createSelect(
    "Idioma",
    data?.language,
    data?.language_options,
    "Seleccione el idioma del libro"
  );
  const [numberPages, numberPagesInput] = createInput(
    "Número de páginas",
    "number",
    data?.number_pages,
    "Ingrese el número de páginas del libro"
  );
  const [yearPublication, yearPublicationInput] = createInput(
    "Año de publicación",
    "number",
    data?.year_publication,
    "Ingrese el año de publicación del libro"
  );
  const [availableUnits, availableUnitsInput] = createInput(
    "Unidades disponibles",
    "number",
    data?.available_units,
    "Ingrese el número de unidades disponibles del libro"
  );
  const sendButton = createButton(buttonText);
  form.classList.add("main__form");
  form.insertAdjacentElement("beforeend", title);
  form.insertAdjacentElement("beforeend", author);
  form.insertAdjacentElement("beforeend", publisher);
  form.insertAdjacentElement("beforeend", category);
  form.insertAdjacentElement("beforeend", language);
  form.insertAdjacentElement("beforeend", numberPages);
  form.insertAdjacentElement("beforeend", yearPublication);
  form.insertAdjacentElement("beforeend", availableUnits);
  form.insertAdjacentElement("beforeend", sendButton);
  sendButton.addEventListener("click", (event) => {
    event.preventDefault();
    const bookData = new FormData();
    if (update) {
      bookData.append(
        "update_book",
        JSON.stringify({
          id: data.id,
          title: titleInput.value,
          author: authorSelect.value,
          publisher: publisherSelect.value,
          category: categorySelect.value,
          language: languageSelect.value,
          number_pages: numberPagesInput.value,
          year_publication: yearPublicationInput.value,
          available_units: availableUnitsInput.value,
        })
      );
    } else {
      bookData.append(
        "create_book",
        JSON.stringify({
          title: titleInput.value,
          author: authorSelect.value,
          publisher: publisherSelect.value,
          category: categorySelect.value,
          language: languageSelect.value,
          number_pages: numberPagesInput.value,
          year_publication: yearPublicationInput.value,
          available_units: availableUnitsInput.value,
        })
      );
    }
    sendModal("/library/book/", bookData);
  });
  return form;
};

const createBookLoanForm = (buttonText, data) => {
  const form = document.createElement("form");
  const [documentNumber, documentNumberInput] = createInput(
    "Documento",
    "number",
    "",
    "Ingrese el número de documento del usuario"
  );
  const div = document.createElement("div");
  const spanTitle = document.createElement("span");
  const spanAuthor = document.createElement("span");
  const spanAvailable = document.createElement("span");
  const spanUnits = document.createElement("span");
  const sendButton = createButton(buttonText);
  div.classList.add("main__book-detail");
  spanTitle.classList.add("main__content-title", "main__content-title--center");
  spanAuthor.classList.add(
    "main__content-title--small",
    "main__content-title--thin"
  );
  spanAvailable.classList.add("main__content-title--available-units");
  spanUnits.classList.add("main__content-title--small");
  spanTitle.innerText = data?.title;
  spanAuthor.innerText = data?.author;
  spanAvailable.innerText = data?.available_units;
  spanUnits.innerText = "Unidades disponibles";
  div.insertAdjacentElement("beforeend", spanTitle);
  div.insertAdjacentElement("beforeend", spanAuthor);
  div.insertAdjacentElement("beforeend", spanAvailable);
  div.insertAdjacentElement("beforeend", spanUnits);
  form.classList.add("main__form");
  form.insertAdjacentElement("beforeend", div);
  form.insertAdjacentElement("beforeend", documentNumber);
  form.insertAdjacentElement("beforeend", sendButton);
  sendButton.addEventListener("click", (event) => {
    event.preventDefault();
    const loanData = new FormData();
    loanData.append(
      "book_loan",
      JSON.stringify({
        book: data.id,
        document_number: documentNumberInput.value,
      })
    );
    sendModal("/library/bookloan/", loanData);
  });
  return form;
};

const createUserBookLoanForm = (buttonText) => {
  const form = document.createElement("form");
  const [documentNumber, documentNumberInput] = createInput(
    "Documento",
    "number",
    "",
    "Ingrese el número de documento del usuario"
  );
  const sendButton = createButton("Buscar usuario");
  form.classList.add("main__form");
  form.insertAdjacentElement("beforeend", documentNumber);
  form.insertAdjacentElement("beforeend", sendButton);
  sendButton.addEventListener("click", (event) => {
    event.preventDefault();
    const loanData = new FormData();
    loanData.append(
      "user_book_loans",
      JSON.stringify({
        document_number: documentNumberInput.value,
      })
    );
    queryUserBookLoans("/library/bookloan/", loanData, buttonText);
  });
  return form;
};

const createDebtForm = (buttonText, data) => {
  const form = document.createElement("form");
  const div = document.createElement("div");
  const spanDebt = document.createElement("span");
  const spanUser = document.createElement("span");
  const spanPenalties = document.createElement("span");
  const spanUnits = document.createElement("span");
  const sendButton = createButton(buttonText);
  div.classList.add("main__book-detail");
  spanDebt.classList.add("main__content-title", "main__content-title--center");
  spanUser.classList.add(
    "main__content-title--small",
    "main__content-title--thin"
  );
  spanPenalties.classList.add("main__content-title--available-units");
  spanUnits.classList.add("main__content-title--small");
  spanDebt.innerText = data?.debt;
  spanUser.innerText = data?.user;
  spanPenalties.innerText = data?.penalties;
  spanUnits.innerText = "Sanciones por pagar";
  div.insertAdjacentElement("beforeend", spanDebt);
  div.insertAdjacentElement("beforeend", spanUser);
  div.insertAdjacentElement("beforeend", spanPenalties);
  div.insertAdjacentElement("beforeend", spanUnits);
  form.classList.add("main__form");
  form.insertAdjacentElement("beforeend", div);
  form.insertAdjacentElement("beforeend", sendButton);
  sendButton.addEventListener("click", (event) => {
    event.preventDefault();
    const debtData = new FormData();
    debtData.append(
      "pay_debts",
      JSON.stringify({
        debts: data,
      })
    );
    sendModal("/library/debt/", debtData, buttonText);
  });
  return form;
};

const createUserForm = (buttonText, update, data) => {
  const form = document.createElement("form");
  const [documentNumber, documentNumberInput] = createInput(
    "Documento",
    "number",
    data?.document_number,
    "Ingrese número de documento"
  );
  const [firstName, firstNameInput] = createInput(
    "Nombres",
    "text",
    data?.first_name,
    "Ingrese nombres"
  );
  const [lastName, lastNameInput] = createInput(
    "Apellidos",
    "text",
    data?.last_name,
    "Ingrese apellidos"
  );
  const [email, emailInput] = createInput(
    "E-mail",
    "email",
    data?.email,
    "Ingrese e-mail"
  );
  const [address, addressInput] = createInput(
    "Dirección",
    "text",
    data?.address,
    "Ingrese dirección"
  );
  const [phone, phoneInput] = createInput(
    "Teléfono",
    "number",
    data?.phone,
    "Ingrese teléfono"
  );
  const sendButton = createButton(buttonText);
  form.classList.add("main__form");
  form.insertAdjacentElement("beforeend", documentNumber);
  form.insertAdjacentElement("beforeend", firstName);
  form.insertAdjacentElement("beforeend", lastName);
  form.insertAdjacentElement("beforeend", email);
  form.insertAdjacentElement("beforeend", address);
  form.insertAdjacentElement("beforeend", phone);
  form.insertAdjacentElement("beforeend", sendButton);
  sendButton.addEventListener("click", (event) => {
    event.preventDefault();
    const userData = new FormData();
    if (update) {
      userData.append(
        "update_user",
        JSON.stringify({
          id: data.id,
          document_number: documentNumberInput.value,
          first_name: firstNameInput.value,
          last_name: lastNameInput.value,
          email: emailInput.value,
          address: addressInput.value,
          phone: phoneInput.value,
        })
      );
    } else {
      userData.append(
        "create_user",
        JSON.stringify({
          document_number: documentNumberInput.value,
          first_name: firstNameInput.value,
          last_name: lastNameInput.value,
          email: emailInput.value,
          address: addressInput.value,
          phone: phoneInput.value,
        })
      );
    }
    sendModal("/library/user/", userData);
  });
  return form;
};
