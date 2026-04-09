document.addEventListener("DOMContentLoaded", () => {
  const editProfileBtn = document.getElementById("editProfileBtn");
  const cancelEditBtn = document.getElementById("cancelEditBtn");
  const profileButtons = document.getElementById("profileButtons");
  const profileForm = document.getElementById("profileForm");
  const deleteButtons = document.querySelectorAll(".delete-package");
  const cancelBookingButtons = document.querySelectorAll(".cancel-booking");
  const dashboardTabLinks = document.querySelectorAll('a[data-bs-toggle="tab"]');

  function showOrHideNewInput(selectEl, inputClass) {
    const input = selectEl.closest(".input-group")?.querySelector(inputClass);
    if (!input) return;
    if (selectEl.value === "new") {
      input.style.display = "block";
      input.name = selectEl.name;
      selectEl.name = "";
      input.required = true;
    } else {
      input.style.display = "none";
      input.required = false;
      if (!selectEl.name) {
        selectEl.name = input.name;
        input.name = "";
      }
    }
  }

  function bindDynamicSelects(scope = document) {
    scope.querySelectorAll(".location-select").forEach((selectEl) => {
      selectEl.addEventListener("change", () => showOrHideNewInput(selectEl, ".new-location"));
    });
    scope.querySelectorAll(".vehicle-select").forEach((selectEl) => {
      selectEl.addEventListener("change", () => showOrHideNewInput(selectEl, ".new-vehicle"));
    });
  }

  function bindAddButtons() {
    const locationContainer = document.getElementById("locationContainer");
    const highlightContainer = document.getElementById("highlightContainer");
    const transportContainer = document.getElementById("transportContainer");

    if (locationContainer) {
      locationContainer.addEventListener("click", (e) => {
        const btn = e.target.closest(".add-location, .remove-row");
        if (!btn) return;
        if (btn.classList.contains("add-location")) {
          const row = btn.closest(".input-group");
          const clone = row.cloneNode(true);
          clone.querySelectorAll("input").forEach((i) => {
            i.value = "";
            if (i.classList.contains("new-location")) {
              i.style.display = "none";
              i.required = false;
            }
          });
          const select = clone.querySelector("select");
          if (select) select.selectedIndex = 0;
          btn.classList.remove("add-location", "btn-outline-success");
          btn.classList.add("remove-row", "btn-outline-danger");
          btn.innerHTML = '<i class="fas fa-trash"></i>';
          locationContainer.appendChild(clone);
          bindDynamicSelects(clone);
        } else {
          btn.closest(".input-group")?.remove();
        }
      });
    }

    if (highlightContainer) {
      highlightContainer.addEventListener("click", (e) => {
        const btn = e.target.closest(".add-highlight, .remove-row");
        if (!btn) return;
        if (btn.classList.contains("add-highlight")) {
          const row = btn.closest(".input-group");
          const clone = row.cloneNode(true);
          clone.querySelector("input").value = "";
          btn.classList.remove("add-highlight", "btn-outline-success");
          btn.classList.add("remove-row", "btn-outline-danger");
          btn.innerHTML = '<i class="fas fa-trash"></i>';
          highlightContainer.appendChild(clone);
        } else {
          btn.closest(".input-group")?.remove();
        }
      });
    }

    if (transportContainer) {
      transportContainer.addEventListener("click", (e) => {
        const btn = e.target.closest(".add-transport, .remove-row");
        if (!btn) return;
        if (btn.classList.contains("add-transport")) {
          const row = btn.closest(".input-group");
          const clone = row.cloneNode(true);
          clone.querySelectorAll("input").forEach((i) => {
            i.value = "";
            if (i.classList.contains("new-vehicle")) {
              i.style.display = "none";
              i.required = false;
            }
          });
          const select = clone.querySelector("select");
          if (select) select.selectedIndex = 0;
          btn.classList.remove("add-transport", "btn-outline-success");
          btn.classList.add("remove-row", "btn-outline-danger");
          btn.innerHTML = '<i class="fas fa-trash"></i>';
          transportContainer.appendChild(clone);
          bindDynamicSelects(clone);
        } else {
          btn.closest(".input-group")?.remove();
        }
      });
    }
  }

  function persistDashboardTabs() {
    dashboardTabLinks.forEach((tabLink) => {
      tabLink.addEventListener("shown.bs.tab", (event) => {
        const target = event.target.getAttribute("href");
        if (target) localStorage.setItem("dashboardActiveTab", target);
      });
    });

    const savedTab = localStorage.getItem("dashboardActiveTab");
    if (savedTab) {
      const targetLink = document.querySelector(`a[data-bs-toggle="tab"][href="${savedTab}"]`);
      if (targetLink && window.bootstrap) {
        new bootstrap.Tab(targetLink).show();
      }
    }
  }

  deleteButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const packageTitle = btn.closest(".card")?.querySelector(".card-title")?.textContent?.trim();
      if (packageTitle) btn.setAttribute("title", `Delete ${packageTitle}`);
    });
  });

  cancelBookingButtons.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const ok = confirm("Are you sure you want to cancel this booking?");
      if (!ok) e.preventDefault();
    });
  });

  if (!editProfileBtn || !profileForm) return;

  const editableFields = profileForm.querySelectorAll("input[name], textarea[name]");

  function setEditableState(enabled) {
    editableFields.forEach((field) => {
      field.disabled = !enabled;
    });
    if (profileButtons) profileButtons.style.display = enabled ? "block" : "none";
  }

  editProfileBtn.addEventListener("click", () => setEditableState(true));
  cancelEditBtn?.addEventListener("click", () => setEditableState(false));
  bindDynamicSelects();
  bindAddButtons();
  persistDashboardTabs();
});
