
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


    const warningSigns =
        Array.isArray(
            employee.warning_signs
        )
            ? employee.warning_signs
            : [];


    const recommendations =
        Array.isArray(
            employee.recommendations
        )
            ? employee.recommendations
            : [];


    const warningsHTML =
        warningSigns.length > 0

            ? warningSigns
                .map(
                    item =>
                        `<li>${escapeHtml(item)}</li>`
                )
                .join("")

            : "<li>موردی ثبت نشده است</li>";


    const recommendationsHTML =
        recommendations.length > 0

            ? recommendations
                .map(
                    item =>
                        `<li>${escapeHtml(item)}</li>`
                )
                .join("")

            : "<li>موردی ثبت نشده است</li>";


    return `
        <div class="col-12 col-lg-6">

            <div class="card employee-card h-100 shadow-sm">

                <div class="card-body p-4">


                    <!-- Header -->

                    <div class="d-flex justify-content-between align-items-start">

                        <div>

                            <div class="text-muted small">
                                کارمند
                            </div>

                            <h4 class="fw-bold mb-0">
                                ${escapeHtml(
                                    employee.employee_id
                                )}
                            </h4>

                        </div>


                        <span
                            class="badge ${riskClass} fs-6 px-3 py-2"
                        >
                            ${riskText}
                        </span>

                    </div>


                    <hr>


                    <!-- Risk -->

                    <div class="row text-center mb-4">

                        <div class="col-6">

                            <div class="text-muted small">
                                امتیاز ریسک
                            </div>

                            <div class="fs-2 fw-bold">
                                ${employee.risk_score}
                            </div>

                        </div>


                        <div class="col-6">

                            <div class="text-muted small">
                                وضعیت
                            </div>

                            <div class="fs-5 fw-bold mt-2">
                                ${riskText}
                            </div>

                        </div>

                    </div>


                    <!-- Explanation -->

                    <div class="mb-4">

                        <h6 class="fw-bold">
                            توضیحات تحلیل
                        </h6>

                        <p class="text-muted mb-0">
                            ${escapeHtml(
                                employee.explanation || "-"
                            )}
                        </p>

                    </div>


                    <!-- Warning Signs -->

                    <div class="mb-4">

                        <h6 class="fw-bold">
                            نشانه‌های هشدار
                        </h6>

                        <ul class="mb-0">
                            ${warningsHTML}
                        </ul>

                    </div>


                    <!-- Recommendations -->

                    <div>

                        <h6 class="fw-bold">
                            پیشنهادهای مدیریتی
                        </h6>

                        <ul class="mb-0">
                            ${recommendationsHTML}
                        </ul>

                    </div>


                </div>

            </div>

        </div>
    `;
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

