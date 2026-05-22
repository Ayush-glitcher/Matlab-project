let auxAttempts = 0;
let rootsAttempts = 0;
let ycAttempts = 0;
let ypAttempts = 0;
// =========================
// ODE SOLVER
// =========================

let actualSolution = {};


// START LEARNING

async function startLearning(){

    const equation =
        document.getElementById(
            "equationInput"
        ).value;

    const response =
        await fetch("/get_solution",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            equation:equation
        })

    });

    actualSolution =
        await response.json();

    document.getElementById(
        "step1"
    ).classList.add("active");

}


// CHECK AUXILIARY EQUATION
function checkAux(){

    const userAnswer =
        document.getElementById(
            "auxInput"
        ).value;

    const cleanedUser =
        userAnswer
        .replaceAll(" ","")
        .replaceAll("^","**")
        .toLowerCase();

    const cleanedActual =
        actualSolution
            .auxiliary_equation
            .replaceAll(" ","")
            .replaceAll("^","**")
            .toLowerCase();

    if(cleanedUser === cleanedActual){

        document.getElementById(
            "auxFeedback"
        ).innerHTML =
            "✅ Correct";

        document.getElementById(
            "step2"
        ).classList.add("active");

    }else{

        auxAttempts++;

        if(auxAttempts >= 3){

            document.getElementById(
                "auxFeedback"
            ).innerHTML = `

❌ Incorrect

<br><br>

<button onclick="showAuxHint()">

Show Hint

</button>

            `;

        }else{

            document.getElementById(
                "auxFeedback"
            ).innerHTML =
                `❌ Try again (${auxAttempts}/3)`;

        }

    }

}
function showAuxHint(){

    document.getElementById(
        "auxFeedback"
    ).innerHTML += `

<br><br>

💡 Hint:

Replace:
y'' → m²
<br>
y → 1
<br>
Then form polynomial in m.

    `;

}

// CHECK ROOTS
function checkRoots(){

    const userAnswer =
        document.getElementById(
            "rootsInput"
        ).value;

    const cleanedUser =
        userAnswer
        .replaceAll(" ","")
        .toLowerCase();

    const actualRoots =
        actualSolution.roots
        .join(",")
        .replaceAll(" ","")
        .toLowerCase();

    if(cleanedUser === actualRoots){

        document.getElementById(
            "rootsFeedback"
        ).innerHTML =
            "✅ Correct";

        document.getElementById(
            "step3"
        ).classList.add("active");

    }else{

        rootsAttempts++;

        if(rootsAttempts >= 3){

            document.getElementById(
                "rootsFeedback"
            ).innerHTML = `

❌ Incorrect Roots

<br><br>

<button onclick="showRootsHint()">

Show Hint

</button>

            `;

        }else{

            document.getElementById(
                "rootsFeedback"
            ).innerHTML =
                `❌ Try Again (${rootsAttempts}/3)`;

        }

    }

}
function showRootsHint(){

    document.getElementById(
        "rootsFeedback"
    ).innerHTML += `

<br><br>

💡 Hint:

Solve the auxiliary equation:

m² + 4 = 0
<br>
Take square root of both sides.
<br>
Remember:

√(-1) = i

    `;

}

// CHECK YC
function checkYC(){

    const userAnswer =
        document.getElementById(
            "ycInput"
        ).value;

    const cleanedUser =
        userAnswer
        .replaceAll(" ","")
        .replaceAll("^","**")
        .toLowerCase();

    const cleanedActual =
        actualSolution
            .complementary_solution
            .replaceAll(" ","")
            .replaceAll("^","**")
            .toLowerCase();

    if(cleanedUser === cleanedActual){

        document.getElementById(
            "ycFeedback"
        ).innerHTML =
            "✅ Correct";

        document.getElementById(
            "step4"
        ).classList.add("active");

    }else{

        ycAttempts++;

        if(ycAttempts >= 3){

            document.getElementById(
                "ycFeedback"
            ).innerHTML = `

❌ Incorrect yc

<br><br>

<button onclick="showYCHint()">

Show Hint

</button>

            `;

        }else{

            document.getElementById(
                "ycFeedback"
            ).innerHTML =
                `❌ Try Again (${ycAttempts}/3)`;

        }

    }

}
function showYCHint(){

    document.getElementById(
        "ycFeedback"
    ).innerHTML += `

<br><br>

💡 General Hint for yc:

1. Solve the auxiliary equation.
<br>
2. Find the roots.
<br>
3. Use root rules:
<br>
• Distinct real roots:
  y_c =
  C1*e^(m1*x)
  +
  C2*e^(m2*x)
<br>
• Repeated roots:
  y_c =
  (C1 + C2*x)e^(m*x)
<br>
• Complex roots:
  a ± bi
<br>
  y_c =
  e^(a*x)(
    C1*cos(b*x)
    +
    C2*sin(b*x)
  )
<br>
4. Substitute your roots into the correct form.

    `;

}

// CHECK YP
function checkYP(){

    const userAnswer =
        document.getElementById(
            "ypInput"
        ).value;

    const cleanedUser =
        userAnswer
        .replaceAll(" ","")
        .replaceAll("^","**")
        .toLowerCase();

    const cleanedActual =
        actualSolution
            .particular_solution
            .replaceAll(" ","")
            .replaceAll("^","**")
            .toLowerCase();

    if(cleanedUser === cleanedActual){

        document.getElementById(
            "ypFeedback"
        ).innerHTML =
            "✅ Correct";

        document.getElementById(
            "finalStep"
        ).classList.add("active");

    }else{

        ypAttempts++;

        if(ypAttempts >= 3){

            document.getElementById(
                "ypFeedback"
            ).innerHTML = `

❌ Incorrect yp

<br><br>

<button onclick="showYPHint()">

Show Hint

</button>

            `;

        }else{

            document.getElementById(
                "ypFeedback"
            ).innerHTML =
                `❌ Try Again (${ypAttempts}/3)`;

        }

    }

}
function showYPHint(){

    document.getElementById(
        "ypFeedback"
    ).innerHTML += `

<br><br>

💡 General Hint for yp:
<br>
1. Look at the RHS function.
<br>
2. Choose trial form:
<br>
• e^(ax)
  → A*e^(ax)
<br>
• sin(ax), cos(ax)
  → A*cos(ax) + B*sin(ax)
<br>
• Polynomial:
  → Ax + B
  or higher polynomial
<br>
• Combination:
  Use combined trial form.
<br>
3. VERY IMPORTANT:
<br>
If trial form already appears in yc,
multiply entire trial solution by x.
<br>
If still repeated,
multiply again by x².
<br>
4. Substitute yp into the ODE
and solve coefficients.

    `;

}
// SHOW FINAL SOLUTION

function showFinalSolution(){

    document.getElementById(
        "finalResult"
    ).innerHTML = `

General Solution y=yc + yp:

${actualSolution.general_solution}

    `;

}

// =========================
// DARK / LIGHT MODE
// =========================

document.addEventListener(
    "DOMContentLoaded",
    () => {

    const themeToggle =
        document.getElementById("themeToggle");

    // Button may not exist on all pages

    if(themeToggle){

        // LOAD SAVED THEME

        const savedTheme =
            localStorage.getItem("theme");

        if(savedTheme === "dark"){

            document.body.classList.add(
                "dark-mode"
            );

            themeToggle.innerHTML = "☀️";

        }else{

            themeToggle.innerHTML = "🌙";

        }

        // TOGGLE THEME

        themeToggle.addEventListener(
            "click",
            () => {

            document.body.classList.toggle(
                "dark-mode"
            );

            if(
                document.body.classList.contains(
                    "dark-mode"
                )
            ){

                localStorage.setItem(
                    "theme",
                    "dark"
                );

                themeToggle.innerHTML = "☀️";

            }else{

                localStorage.setItem(
                    "theme",
                    "light"
                );

                themeToggle.innerHTML = "🌙";

            }

        });

    }

});