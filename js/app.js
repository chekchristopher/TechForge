"use strict";

/*
 * TechForge Academy
 * Main application logic
 */

fetch('app/data/programmes.json')
const state = {
    programmes: [],
    filteredProgrammes: [],
    selectedProgramme: null
};

const elements = {
    grid: document.getElementById("programmeGrid"),
    loading: document.getElementById("loadingState"),
    error: document.getElementById("errorState"),
    empty: document.getElementById("emptyState"),

    search: document.getElementById("searchInput"),
    category: document.getElementById("categoryFilter"),
    status: document.getElementById("statusFilter"),

    summary: document.getElementById("resultsSummary"),

    retry: document.getElementById("retryButton"),
    clearFilters: document.getElementById("clearFiltersButton"),

    programmeModal: document.getElementById("programmeModal"),
    modalBody: document.getElementById("modalBody"),
    modalClose: document.getElementById("modalClose"),
    modalOverlay: document.getElementById("modalOverlay"),

    registrationModal:
        document.getElementById("registrationModal"),

    registrationClose:
        document.getElementById("registrationClose"),

    registrationOverlay:
        document.getElementById("registrationOverlay"),

    registrationForm:
        document.getElementById("registrationForm"),

    registrationProgramme:
        document.getElementById("registrationProgramme"),

    successMessage:
        document.getElementById("successMessage"),

    mobileMenuButton:
        document.getElementById("mobileMenuButton"),

    navigation:
        document.getElementById("mainNavigation")
};


/* =========================
   INITIALIZATION
========================= */

document.addEventListener("DOMContentLoaded", initialize);

function initialize() {
    attachEventListeners();
    loadProgrammes();
}


/* =========================
   DATA
========================= */

async function loadProgrammes() {

    showLoadingState();

    try {

        const response = await fetch("data/programmes.json");

        if (!response.ok) {
            throw new Error(
                `HTTP error: ${response.status}`
            );
        }

        const programmes = await response.json();

        if (!Array.isArray(programmes)) {
            throw new Error("Invalid programme data.");
        }

        state.programmes = programmes;
        state.filteredProgrammes = programmes;

        populateCategoryFilter();
        renderProgrammes();

    } catch (error) {

        console.error(
            "Programme loading failed:",
            error
        );

        showErrorState();
    }
}


/* =========================
   FILTERING
========================= */

function filterProgrammes() {

    const searchTerm =
        elements.search.value
            .trim()
            .toLowerCase();

    const selectedCategory =
        elements.category.value;

    const selectedStatus =
        elements.status.value;

    state.filteredProgrammes =
        state.programmes.filter(programme => {

            const searchableText = `
                ${programme.name}
                ${programme.category}
                ${programme.instructor}
                ${programme.description}
            `.toLowerCase();

            const matchesSearch =
                searchableText.includes(searchTerm);

            const matchesCategory =
                selectedCategory === "all" ||
                programme.category === selectedCategory;

            const matchesStatus =
                selectedStatus === "all" ||
                programme.status === selectedStatus;

            return (
                matchesSearch &&
                matchesCategory &&
                matchesStatus
            );
        });

    renderProgrammes();
}


function populateCategoryFilter() {

    const categories = [
        ...new Set(
            state.programmes.map(
                programme => programme.category
            )
        )
    ];

    categories.sort();

    categories.forEach(category => {

        const option =
            document.createElement("option");

        option.value = category;
        option.textContent = category;

        elements.category.appendChild(option);
    });
}


/* =========================
   RENDERING
========================= */

function renderProgrammes() {

    hideAllStates();

    const programmes =
        state.filteredProgrammes;

    elements.summary.textContent =
        `${programmes.length} programme${
            programmes.length === 1 ? "" : "s"
        } found`;

    if (programmes.length === 0) {
        elements.empty.classList.remove("hidden");
        return;
    }

    elements.grid.innerHTML =
        programmes
            .map(createProgrammeCard)
            .join("");
}


function createProgrammeCard(programme) {

    const statusLabel =
        capitalize(programme.status);

    const statusClass =
        `status-${programme.status}`;

    const registrationDisabled =
        programme.status === "closed" ||
        programme.availableSlots === 0;

    return `
        <article class="programme-card">

            <div class="card-top">

                <span class="category">
                    ${escapeHTML(programme.category)}
                </span>

                <span class="status ${statusClass}">
                    ${statusLabel}
                </span>

            </div>

            <div class="card-body">

                <h3>
                    ${escapeHTML(programme.name)}
                </h3>

                <p class="card-description">
                    ${escapeHTML(programme.description)}
                </p>

                <div class="programme-meta">

                    <div class="meta-item">
                        <span class="meta-label">
                            Duration
                        </span>

                        <span class="meta-value">
                            ${escapeHTML(programme.duration)}
                        </span>
                    </div>

                    <div class="meta-item">
                        <span class="meta-label">
                            Start date
                        </span>

                        <span class="meta-value">
                            ${formatDate(programme.startDate)}
                        </span>
                    </div>

                    <div class="meta-item">
                        <span class="meta-label">
                            Instructor
                        </span>

                        <span class="meta-value">
                            ${escapeHTML(programme.instructor)}
                        </span>
                    </div>

                    <div class="meta-item">
                        <span class="meta-label">
                            Available slots
                        </span>

                        <span class="meta-value">
                            ${programme.availableSlots}
                        </span>
                    </div>

                </div>

            </div>

            <div class="card-footer">

                <span class="price">
                    ${formatCurrency(programme.price)}
                </span>

                <button
                    class="card-button"
                    data-action="details"
                    data-id="${programme.id}"
                >
                    View details →
                </button>

            </div>

        </article>
    `;
}


/* =========================
   PROGRAMME DETAILS
========================= */

function openProgrammeDetails(id) {

    const programme =
        state.programmes.find(
            item => item.id === id
        );

    if (!programme) {
        return;
    }

    state.selectedProgramme = programme;

    const canRegister =
        programme.status !== "closed" &&
        programme.availableSlots > 0;

    elements.modalBody.innerHTML = `

        <span class="details-category">
            ${escapeHTML(programme.category)}
        </span>

        <h2 class="details-title">
            ${escapeHTML(programme.name)}
        </h2>

        <p class="details-description">
            ${escapeHTML(programme.description)}
        </p>

        <div class="details-list">

            <div class="details-item">
                <small>Duration</small>
                <strong>${escapeHTML(programme.duration)}</strong>
            </div>

            <div class="details-item">
                <small>Price</small>
                <strong>${formatCurrency(programme.price)}</strong>
            </div>

            <div class="details-item">
                <small>Start date</small>
                <strong>${formatDate(programme.startDate)}</strong>
            </div>

            <div class="details-item">
                <small>Instructor</small>
                <strong>${escapeHTML(programme.instructor)}</strong>
            </div>

            <div class="details-item">
                <small>Available slots</small>
                <strong>${programme.availableSlots}</strong>
            </div>

            <div class="details-item">
                <small>Status</small>
                <strong>${capitalize(programme.status)}</strong>
            </div>

        </div>

        <button
            class="primary-button full-width"
            id="registerButton"
            ${canRegister ? "" : "disabled"}
        >
            ${
                canRegister
                    ? "Register for this programme"
                    : "Registration unavailable"
            }
        </button>
    `;

    elements.programmeModal.classList.remove("hidden");

    const registerButton =
        document.getElementById("registerButton");

    if (canRegister) {
        registerButton.addEventListener(
            "click",
            () => {
                closeProgrammeModal();
                openRegistrationModal(programme);
            }
        );
    }

    elements.modalClose.focus();
}


function closeProgrammeModal() {
    elements.programmeModal.classList.add("hidden");
}


/* =========================
   REGISTRATION
========================= */

function openRegistrationModal(programme) {

    state.selectedProgramme = programme;

    elements.registrationProgramme.textContent =
        `${programme.name} · ${formatCurrency(programme.price)}`;

    elements.registrationForm.reset();

    clearValidationErrors();

    elements.successMessage.classList.add("hidden");

    elements.registrationModal.classList.remove("hidden");

    document.getElementById("fullName").focus();
}


function closeRegistrationModal() {
    elements.registrationModal.classList.add("hidden");
}


function validateRegistrationForm() {

    clearValidationErrors();

    let valid = true;

    const fullName =
        document.getElementById("fullName");

    const email =
        document.getElementById("email");

    const phone =
        document.getElementById("phone");

    const experience =
        document.getElementById("experience");

    const terms =
        document.getElementById("terms");


    if (fullName.value.trim().length < 2) {

        showFieldError(
            "fullName",
            "Please enter your full name."
        );

        valid = false;
    }


    const emailPattern =
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailPattern.test(email.value.trim())) {

        showFieldError(
            "email",
            "Please enter a valid email address."
        );

        valid = false;
    }


    const phonePattern =
        /^[0-9+\-\s()]{7,20}$/;

    if (!phonePattern.test(phone.value.trim())) {

        showFieldError(
            "phone",
            "Please enter a valid phone number."
        );

        valid = false;
    }


    if (!experience.value) {

        showFieldError(
            "experience",
            "Please select your experience level."
        );

        valid = false;
    }


    if (!terms.checked) {

        document.getElementById(
            "termsError"
        ).textContent =
            "You must accept the registration terms.";

        valid = false;
    }

    return valid;
}


function handleRegistrationSubmit(event) {

    event.preventDefault();

    if (!validateRegistrationForm()) {
        return;
    }

    const submitButton =
        elements.registrationForm.querySelector(
            "button[type='submit']"
        );

    submitButton.disabled = true;
    submitButton.textContent = "Submitting...";


    // Simulate API request.
    setTimeout(() => {

        elements.successMessage.classList.remove(
            "hidden"
        );

        submitButton.disabled = false;
        submitButton.textContent =
            "Complete registration";

        console.info(
            "Registration submitted:",
            {
                programme:
                    state.selectedProgramme?.name,
                name:
                    document.getElementById(
                        "fullName"
                    ).value,
                email:
                    document.getElementById(
                        "email"
                    ).value
            }
        );

    }, 900);
}


/* =========================
   VALIDATION HELPERS
========================= */

function showFieldError(fieldName, message) {

    const error =
        document.getElementById(
            `${fieldName}Error`
        );

    if (error) {
        error.textContent = message;
    }
}


function clearValidationErrors() {

    document
        .querySelectorAll(".field-error")
        .forEach(element => {
            element.textContent = "";
        });
}


/* =========================
   UI STATES
========================= */

function hideAllStates() {

    elements.loading.classList.add("hidden");
    elements.error.classList.add("hidden");
    elements.empty.classList.add("hidden");
    elements.grid.classList.remove("hidden");
}


function showLoadingState() {

    elements.loading.classList.remove("hidden");
    elements.error.classList.add("hidden");
    elements.empty.classList.add("hidden");
    elements.grid.classList.add("hidden");
}


function showErrorState() {

    elements.loading.classList.add("hidden");
    elements.grid.classList.add("hidden");
    elements.empty.classList.add("hidden");
    elements.error.classList.remove("hidden");
}


/* =========================
   EVENT LISTENERS
========================= */

function attachEventListeners() {

    elements.search.addEventListener(
        "input",
        filterProgrammes
    );

    elements.category.addEventListener(
        "change",
        filterProgrammes
    );

    elements.status.addEventListener(
        "change",
        filterProgrammes
    );


    elements.grid.addEventListener(
        "click",
        event => {

            const button =
                event.target.closest(
                    "[data-action='details']"
                );

            if (!button) {
                return;
            }

            openProgrammeDetails(
                Number(button.dataset.id)
            );
        }
    );


    elements.retry.addEventListener(
        "click",
        loadProgrammes
    );


    elements.clearFilters.addEventListener(
        "click",
        clearFilters
    );


    elements.modalClose.addEventListener(
        "click",
        closeProgrammeModal
    );

    elements.modalOverlay.addEventListener(
        "click",
        closeProgrammeModal
    );


    elements.registrationClose.addEventListener(
        "click",
        closeRegistrationModal
    );

    elements.registrationOverlay.addEventListener(
        "click",
        closeRegistrationModal
    );


    elements.registrationForm.addEventListener(
        "submit",
        handleRegistrationSubmit
    );


    document.addEventListener(
        "keydown",
        event => {

            if (event.key !== "Escape") {
                return;
            }

            closeProgrammeModal();
            closeRegistrationModal();
        }
    );


    elements.mobileMenuButton.addEventListener(
        "click",
        toggleMobileNavigation
    );


    elements.navigation.addEventListener(
        "click",
        event => {

            if (event.target.tagName === "A") {
                closeMobileNavigation();
            }
        }
    );
}


/* =========================
   NAVIGATION
========================= */

function toggleMobileNavigation() {

    const isOpen =
        elements.navigation.classList.toggle(
            "active"
        );

    elements.mobileMenuButton.setAttribute(
        "aria-expanded",
        String(isOpen)
    );
}


function closeMobileNavigation() {

    elements.navigation.classList.remove(
        "active"
    );

    elements.mobileMenuButton.setAttribute(
        "aria-expanded",
        "false"
    );
}


/* =========================
   FILTER HELPERS
========================= */

function clearFilters() {

    elements.search.value = "";
    elements.category.value = "all";
    elements.status.value = "all";

    filterProgrammes();
}


/* =========================
   FORMATTERS
========================= */

function formatCurrency(amount) {

    return new Intl.NumberFormat(
        "en-NG",
        {
            style: "currency",
            currency: "NGN",
            maximumFractionDigits: 0
        }
    ).format(amount);
}


function formatDate(dateString) {

    return new Intl.DateTimeFormat(
        "en-NG",
        {
            day: "numeric",
            month: "short",
            year: "numeric"
        }
    ).format(new Date(dateString));
}


function capitalize(value) {

    return value.charAt(0).toUpperCase() +
        value.slice(1);
}


/* =========================
   SECURITY / OUTPUT HELPER
========================= */

function escapeHTML(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}