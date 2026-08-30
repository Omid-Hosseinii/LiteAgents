
let timerInterval = null;
let startTime = null;

let employees = [];


// ============================================================
// Page Initialization
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        loadEmployees();

        document
            .getElementById("employee-search")
            .addEventListener(
                "input",
                filterEmployees
            );

        document
            .getElementById("risk-filter")
            .addEventListener(
                "change",
                filterEmployees
            );
    }
);


// ============================================================
// Load Employees
// ============================================================

async function loadEmployees() {

    try {

        const response = await fetch(
            "/employees"
        );

        if (!response.ok) {

            throw new Error(
                "خطا در دریافت اطلاعات کارکنان"
            );
        }

        employees =
            await response.json();

        renderEmployees(
            employees
        );

    } catch (error) {

        document
            .getElementById(
                "employees-container"
            )
            .innerHTML = `
                <div class="col-12">
                    <div class="alert alert-danger">
                        ${error.message}
                    </div>
                </div>
            `;
    }
}


// ============================================================
// Render Employees
// ============================================================


function renderEmployees(list) {

    const container =
        document.getElementById(
            "employees-container"
        );

    const empty =
        document.getElementById(
            "employees-empty"
        );

    const count =
        document.getElementById(
            "employee-result-count"
        );


    container.innerHTML = "";


    count.textContent =
        `${list.length} کارمند`;


    if (list.length === 0) {

        empty.classList.remove(
            "d-none"
        );

        updateSummary(
            employees
        );

        return;
    }


    empty.classList.add(
        "d-none"
    );


    list.forEach(
        employee => {

            container.innerHTML +=
                createEmployeeCard(
                    employee
                );
        }
    );


    updateSummary(
        employees
    );
}

function updateSummary(list) {

    const total =
        list.length;


    const high =
        list.filter(
            employee =>
                employee.risk_level === "HIGH"
        ).length;


    const medium =
        list.filter(
            employee =>
                employee.risk_level === "MEDIUM"
        ).length;


    const low =
        list.filter(
            employee =>
                employee.risk_level === "LOW"
        ).length;


    document
        .getElementById(
            "total-employees"
        )
        .textContent =
        total;


    document
        .getElementById(
            "high-risk-employees"
        )
        .textContent =
        high;


    document
        .getElementById(
            "medium-risk-employees"
        )
        .textContent =
        medium;


    document
        .getElementById(
            "low-risk-employees"
        )
        .textContent =
        low;
}



// ============================================================
// Employee Card
// ============================================================


function createEmployeeCard(employee) {

    const riskClass =
        getRiskClass(
            employee.risk_level
        );

    const riskText =
        translateRiskLevel(
            employee.risk_level
        );


    return `
        <div class="col-12 col-md-6 col-xl-4">

            <div class="card employee-card h-100">

                <div class="card-body p-4">


                    <!-- Header -->

                    <div class="employee-header mb-3">

                        <div>

                            <div class="text-muted small">
                                کارمند
                            </div>

                            <div class="employee-id">
                                ${escapeHtml(
                                    employee.employee_id
                                )}
                            </div>

                        </div>


                        <span
                            class="badge ${riskClass} px-3 py-2"
                        >
                            ${riskText}
                        </span>

                    </div>


                    <hr>


                    <!-- Risk Score -->

                    <div class="text-center my-4">

                        <div class="text-muted small">
                            امتیاز ریسک
                        </div>

                        <div class="employee-risk-score">
                            ${employee.risk_score}
                        </div>

                    </div>


                    <!-- Explanation Preview -->

                    <div class="mb-4">

                        <div class="employee-section-title">
                            خلاصه تحلیل
                        </div>

                        <p class="text-muted mb-0">
                            ${escapeHtml(
                                employee.explanation || "-"
                            )}
                        </p>

                    </div>


                    <!-- Details Button -->

                    <button
                        type="button"
                        class="btn btn-outline-primary w-100"
                        onclick='showEmployeeDetails(${JSON.stringify(employee)})'
                    >
                        مشاهده جزئیات
                    </button>


                </div>

            </div>

        </div>
    `;
}


function showEmployeeDetails(employee) {

    document
        .getElementById(
            "modal-employee-id"
        )
        .textContent =
        employee.employee_id;


    const riskLevel =
        document.getElementById(
            "modal-risk-level"
        );


    riskLevel.textContent =
        translateRiskLevel(
            employee.risk_level
        );


    riskLevel.className =
        `badge fs-6 mt-1 ${
            getRiskClass(
                employee.risk_level
            )
        }`;


    document
        .getElementById(
            "modal-risk-score"
        )
        .textContent =
        employee.risk_score;


    document
        .getElementById(
            "modal-explanation"
        )
        .textContent =
        employee.explanation || "-";


    const warningContainer =
        document.getElementById(
            "modal-warning-signs"
        );


    warningContainer.innerHTML = "";


    const warnings =
        Array.isArray(
            employee.warning_signs
        )
            ? employee.warning_signs
            : [];


    if (warnings.length === 0) {

        warningContainer.innerHTML =
            "<li>موردی ثبت نشده است</li>";

    } else {

        warnings.forEach(
            warning => {

                const li =
                    document.createElement(
                        "li"
                    );

                li.textContent =
                    warning;

                warningContainer.appendChild(
                    li
                );
            }
        );
    }


    const recommendationsContainer =
        document.getElementById(
            "modal-recommendations"
        );


    recommendationsContainer.innerHTML =
        "";


    const recommendations =
        Array.isArray(
            employee.recommendations
        )
            ? employee.recommendations
            : [];


    if (
        recommendations.length === 0
    ) {

        recommendationsContainer.innerHTML =
            "<li>موردی ثبت نشده است</li>";

    } else {

        recommendations.forEach(
            recommendation => {

                const li =
                    document.createElement(
                        "li"
                    );

                li.textContent =
                    recommendation;

                recommendationsContainer.appendChild(
                    li
                );
            }
        );
    }


    const modalElement =
        document.getElementById(
            "employeeDetailsModal"
        );


    const modal =
        bootstrap.Modal.getOrCreateInstance(
            modalElement
        );


    modal.show();
}




// ============================================================
// Filters
// ============================================================

function filterEmployees() {

    const search =
        document
            .getElementById(
                "employee-search"
            )
            .value
            .trim()
            .toLowerCase();


    const risk =
        document
            .getElementById(
                "risk-filter"
            )
            .value;


    const filtered =
        employees.filter(
            employee => {

                const matchesSearch =
                    employee.employee_id
                        .toLowerCase()
                        .includes(search);


                const matchesRisk =
                    risk === "ALL"
                    ||
                    employee.risk_level === risk;


                return (
                    matchesSearch
                    &&
                    matchesRisk
                );
            }
        );


    renderEmployees(
        filtered
    );
}


// ============================================================
// Risk Helpers
// ============================================================

function translateRiskLevel(level) {

    switch (level) {

        case "HIGH":
            return "ریسک بالا";

        case "MEDIUM":
            return "ریسک متوسط";

        case "LOW":
            return "ریسک پایین";

        default:
            return "-";
    }
}


function getRiskClass(level) {

    switch (level) {

        case "HIGH":
            return "text-bg-danger";

        case "MEDIUM":
            return "text-bg-warning";

        case "LOW":
            return "text-bg-success";

        default:
            return "text-bg-secondary";
    }
}


// ============================================================
// HTML Safety
// ============================================================

function escapeHtml(value) {

    const div =
        document.createElement(
            "div"
        );

    div.textContent =
        value;

    return div.innerHTML;
}


// ============================================================
// Start Analysis
// ============================================================

document
    .getElementById("start-analysis")
    .addEventListener(
        "click",
        async function () {

            const button = this;

            button.disabled = true;

            hideElement(
                "analysis-complete"
            );

            hideElement(
                "analysis-error"
            );

            showElement(
                "analysis-progress-container"
            );

            showElement(
                "current-employee"
            );

            showElement(
                "analysis-timer"
            );

            setStatus(
                "در حال شروع تحلیل..."
            );

            startTime =
                Date.now();

            startTimer();


            try {

                const response =
                    await fetch(
                        "/analysis/run",
                        {
                            method: "POST"
                        }
                    );


                if (!response.ok) {

                    throw new Error(
                        "خطا در شروع Pipeline"
                    );
                }


                await response.json();

                pollAnalysisStatus();


            } catch (error) {

                stopTimer();

                showError(
                    "خطا در اجرای تحلیل: "
                    + error.message
                );

                button.disabled = false;
            }
        }
    );


// ============================================================
// Run Workflow
// ============================================================

document
    .getElementById("run-workflow")
    .addEventListener(
        "click",
        async function () {

            const button = this;

            button.disabled = true;

            const originalText =
                button.innerText;

            button.innerText =
                "در حال اجرا...";


            setStatus(
                "در حال اجرای Workflow..."
            );


            try {

                const response =
                    await fetch(
                        "/workflow/run",
                        {
                            method: "POST"
                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        data.detail
                        ||
                        "خطا در اجرای Workflow"
                    );
                }


                setStatus(
                    "Workflow با موفقیت اجرا شد."
                );


                // Refresh employee data
                await loadEmployees();


            } catch (error) {

                console.error(
                    "Workflow error:",
                    error
                );


                showError(
                    "خطا در اجرای Workflow: "
                    +
                    error.message
                );


            } finally {

                button.disabled = false;

                button.innerText =
                    originalText;
            }
        }
    );




// ============================================================
// Poll Status
// ============================================================

async function pollAnalysisStatus() {

    try {

        const response =
            await fetch(
                "/analysis/status"
            );


        if (!response.ok) {

            throw new Error(
                "خطا در دریافت وضعیت تحلیل"
            );
        }


        const status =
            await response.json();


        updateUI(
            status
        );


        if (status.running) {

            setTimeout(
                pollAnalysisStatus,
                1000
            );

        } else {

            stopTimer();


            if (status.error) {

                showError(
                    status.error
                );

            } else {

                showComplete(
                    status.elapsed_time
                );

                /*
                 * Pipeline finished.
                 * Reload employee data.
                 */

                await loadEmployees();
            }


            document
                .getElementById(
                    "start-analysis"
                )
                .disabled = false;
        }


    } catch (error) {

        stopTimer();

        showError(
            error.message
        );

        document
            .getElementById(
                "start-analysis"
            )
            .disabled = false;
    }
}


// ============================================================
// Update Analysis UI
// ============================================================

function updateUI(status) {

    const completed =
        status.completed || 0;

    const total =
        status.total || 0;


    let percentage = 0;


    if (total > 0) {

        percentage =
            Math.round(
                (
                    completed
                    /
                    total
                )
                * 100
            );
    }


    document
        .getElementById(
            "progress-text"
        )
        .textContent =
        `${completed} / ${total}`;


    const progress =
        document.getElementById(
            "analysis-progress"
        );


    progress.style.width =
        `${percentage}%`;

    progress.textContent =
        `${percentage}%`;


    document
        .getElementById(
            "employee-id"
        )
        .textContent =
        status.current_employee
        || "-";


    document
        .getElementById(
            "risk-level"
        )
        .textContent =
        translateRiskLevel(
            status.current_risk_level
        );


    document
        .getElementById(
            "risk-score"
        )
        .textContent =
        status.current_risk_score
        ?? "-";


    if (status.running) {

        setStatus(
            "در حال تحلیل اطلاعات کارکنان..."
        );

    } else {

        setStatus(
            "تحلیل به پایان رسید"
        );
    }
}


// ============================================================
// Timer
// ============================================================

function startTimer() {

    stopTimer();

    timerInterval =
        setInterval(
            function () {

                const elapsed =
                    Date.now()
                    -
                    startTime;


                document
                    .getElementById(
                        "timer-value"
                    )
                    .textContent =
                    formatTime(
                        elapsed
                    );

            },
            1000
        );
}


function stopTimer() {

    if (
        timerInterval !== null
    ) {

        clearInterval(
            timerInterval
        );

        timerInterval = null;
    }
}


function formatTime(
    milliseconds
) {

    const totalSeconds =
        Math.floor(
            milliseconds / 1000
        );


    const minutes =
        Math.floor(
            totalSeconds / 60
        );


    const seconds =
        totalSeconds % 60;


    return (
        String(minutes)
            .padStart(2, "0")
        +
        ":"
        +
        String(seconds)
            .padStart(2, "0")
    );
}


// ============================================================
// UI Helpers
// ============================================================

function setStatus(
    message
) {

    document
        .getElementById(
            "analysis-status"
        )
        .innerHTML =
        `<div class="fw-bold">
            ${message}
        </div>`;
}


function showElement(
    id
) {

    document
        .getElementById(id)
        .classList
        .remove("d-none");
}


function hideElement(
    id
) {

    document
        .getElementById(id)
        .classList
        .add("d-none");
}


function showError(
    message
) {

    const element =
        document.getElementById(
            "analysis-error"
        );


    element.textContent =
        message;


    element.classList.remove(
        "d-none"
    );
}


function showComplete(
    seconds
) {

    document
        .getElementById(
            "total-time"
        )
        .textContent =
        formatTime(
            seconds * 1000
        );


    showElement(
        "analysis-complete"
    );
}

