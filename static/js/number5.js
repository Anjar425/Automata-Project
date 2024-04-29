const showFormDFA = () => {
    const stateAmount = parseInt(document.getElementById("dfa-state-amount").value);
    const transitionAmount = parseInt(document.getElementById("transition-amount").value); // Mengubah 'parent' menjadi 'parseInt'

    const formElement = document.getElementById("form");

    while (formElement.firstChild) {
        formElement.removeChild(formElement.firstChild);
    }

    if (stateAmount > 0) {
        // Label Start State Selection 
        var selectStartLabel = document.createElement("p");
        selectStartLabel.id = "select_start_label";
        selectStartLabel.classList.add = "hidden", "text-gray-200", "font-semibold", "text-md", "m-2";
        selectStartLabel.textContent = "Select Start States"; // Menambahkan teks ke dalam elemen <p>
        formElement.appendChild(selectStartLabel);

        // Start State Selection 
        var selectStart = document.createElement("select");
        selectStart.name = "start_states";
        selectStart.id = "start_states";
        selectStart.className = "bg-blue-700 text-gray-200 w-1/6 py-2 rounded-md text-md font-bold text-center remove-arrow";
        formElement.appendChild(selectStart);

        // State Container
        var stateContainer = document.createElement("div");
        stateContainer.id = "state-container";
        stateContainer.classList.add("flex", "flex-row", "flex-nowrap", "gap-10", "w-full", "p-10", "grow-1", "overflow-y-auto", "no-scrollbar", "horizontal-scroll");
        formElement.appendChild(stateContainer);

        for (let index = 0; index < stateAmount; index++) {
            // Select Start State
            selectStart.innerHTML += `
            <option value="Q${index}">Q${index}</option>`;

            // Container State Form
            stateContainer.innerHTML += `
            <article class="border-2 border-gray-800 w-96 hover:scale-110 transition duration-500 shrink-0 rounded-lg h-80 items-center p-5 gap-3 overflow-y-auto">
                <p class="text-center font-bold text-3xl text-white">Q${index}</p>
                <p class="text-gray-200 font-semibold text-xl text-center my-3">Transition List</p>
                <div class="flex flex-row w-full justify-center items-center gap-2 mb-3">
                    <input class="" type="checkbox" name="finishing_states" id="finishing_states" value="Q${index}"/>
                    <label for="vehicle1">Finishing States</label>
                </div>
            
                <div class="flex flex-col justify-center items-center text-center w-full gap-5">
                    <div id="input-transition${index}" class="grid grid-cols-3 w-full gap-4 overflow-y-auto overflow-hidden">
                        <p>From</p>
                        <p>Transition</p>
                        <p>To</p>
                    </div>
                </div>
            </article>`;

            for (let transition = 0; transition < transitionAmount; transition++) {
                const inputTransition = document.getElementById("input-transition" + index);

                inputTransition.innerHTML += `
                <input class="bg-gray-600/25 border-[1px] border-gray-700 py-2 rounded-md font-semibold text-center" type="text" name="dfa" id="dfa" value="Q${index}" readonly/>
                <input class="bg-gray-600/25 border-[1px] border-gray-700 py-2 rounded-md font-semibold text-center" type="text" name="dfa" id="dfa" value="${transition}" readonly/>
                <select id="selection_transition${transition}${index}" class="bg-gray-600/25 border-[1px] border-gray-700 py-2 rounded-md font-semibold text-center" type="text" name="dfa" id="dfa" required> </select>
            `;
                const selection_transition = document.getElementById("selection_transition" + transition + index);
                for (let i = 0; i < stateAmount; i++) {
                    selection_transition.innerHTML += `
                <option value="Q${i}">Q${i}</option>`;
                }

            }
        }
        formElement.innerHTML += `
        <p class="text-gray-200 font-semibold text-lg text-center my-3">Input String</p>
        <input type="text" name="type" id="type" value="dfa"/>
        <input class="bg-gray-600/25 border-[1px] border-gray-700 py-2 rounded-md font-semibold text-center" type="text" name="test_string" id="test_string" required/>
        <button type="submit" class="bg-green-700 px-4 py-2 rounded-md my-5 font-bold">MINIMIZE DFA</button>`;
    }
};

const showFormRegex = () => {
    const stateAmount = parseInt(document.getElementById("dfa-state-amount").value);
    const transitionAmount = parseInt(document.getElementById("transition-amount").value); // Mengubah 'parent' menjadi 'parseInt'

    const formElement = document.getElementById("form");

    while (formElement.firstChild) {
        formElement.removeChild(formElement.firstChild);
    }

        formElement.innerHTML += `
        <label class="text-gray-200 font-semibold text-lg text-center my-3" for="regex">Enter Regular Expression</label>
        <input class="bg-gray-600/25 border-[1px] border-gray-700 py-2 rounded-md font-semibold text-center" type="text" id="regex" name="regex" required>
        <p class="text-gray-200 font-semibold text-lg text-center my-3">Input String</p>
        <input class="bg-gray-600/25 border-[1px] border-gray-700 py-2 rounded-md font-semibold text-center" type="text" name="test_string" id="test_string" required/>
        <button type="submit" class="bg-green-700 px-4 py-2 rounded-md my-5 font-bold">MINIMIZE DFA</button>`;
    
};



var transition = 0; 
function addTransition (state, stateAmount,transitionAmount,  x) {
    transition = transition + parseInt(x);
    const inputTransition = document.getElementById("input-transition" + state);
    inputTransition.innerHTML += `
    <input class="bg-gray-600/25 border-[1px] border-gray-700 py-2 rounded-md font-semibold text-center" type="text" name="dfa" id="dfa" value="Q${state}" readonly/>
    <select id="alphabets${transition}${state}" class="bg-gray-600/25 border-[1px] border-gray-700 py-2 rounded-md font-semibold text-center" type="text" name="dfa" id="dfa" required> </select>
    <select id="selection_transition${transition}${state}" class="bg-gray-600/25 border-[1px] border-gray-700 py-2 rounded-md font-semibold text-center" type="text" name="dfa" id="dfa" required> </select>
`;
    
    const selection_transition = document.getElementById("selection_transition" + transition + state);
    for (let index = 0; index < stateAmount; index++) {
        selection_transition.innerHTML += `
                <option value="Q${index}">Q${index}</option>`;
        
    }

    const alphabets = document.getElementById("alphabets" + transition + state);
    for (let index = 0; index < transitionAmount; index++) {
        if (index === 0){
            alphabets.innerHTML += `
            <option value="e">ε</option>`;  
        } else {
            alphabets.innerHTML += `
            <option value="${index-1}">${index-1}</option>`;  
        }
   
    }
}

const showFormNFA = () => {
    const stateAmount = parseInt(document.getElementById("dfa-state-amount").value);
    const transitionAmount = parseInt(document.getElementById("transition-amount").value); // Mengubah 'parent' menjadi 'parseInt'

    const formElement = document.getElementById("form");

    while (formElement.firstChild) {
        formElement.removeChild(formElement.firstChild);
    }

    if (stateAmount > 0) {
        // Label Start State Selection 
        var selectStartLabel = document.createElement("p");
        selectStartLabel.id = "select_start_label";
        selectStartLabel.classList.add = "hidden", "text-gray-200", "font-semibold", "text-md", "m-2";
        selectStartLabel.textContent = "Select Start States"; // Menambahkan teks ke dalam elemen <p>
        formElement.appendChild(selectStartLabel);

        // Start State Selection 
        var selectStart = document.createElement("select");
        selectStart.name = "start_states";
        selectStart.id = "start_states";
        selectStart.className = "bg-blue-700 text-gray-200 w-1/6 py-2 rounded-md text-md font-bold text-center remove-arrow";
        formElement.appendChild(selectStart);

        // State Container
        var stateContainer = document.createElement("div");
        stateContainer.id = "state-container";
        stateContainer.classList.add("flex", "flex-row", "flex-nowrap", "gap-10", "w-full", "p-10", "grow-1", "overflow-y-auto", "no-scrollbar", "horizontal-scroll");
        formElement.appendChild(stateContainer);

        for (let index = 0; index < stateAmount; index++) {
            // Select Start State
            selectStart.innerHTML += `
            <option value="Q${index}">Q${index}</option>`;

            // Container State Form
            stateContainer.innerHTML += `
            <article class="flex flex-col items-center border-2 border-gray-800 w-96 hover:scale-110 transition duration-500 shrink-0 rounded-lg h-80 items-center p-5 gap-3 overflow-y-auto">
                <p class="text-center font-bold text-3xl text-white">Q${index}</p>
                <p class="text-gray-200 font-semibold text-xl text-center">Transition List</p>
                <div class="flex flex-row w-full justify-center items-center gap-2 mb-3">
                    <input class="" type="checkbox" name="finishing_states" id="finishing_states" value="Q${index}"/>
                    <label for="vehicle1">Finishing States</label>
                </div>
            
                <div class="flex flex-col justify-center items-center text-center w-full gap-5">
                    <div id="input-transition${index}" class="grid grid-cols-3 w-full gap-4 overflow-y-auto overflow-hidden justify-center items-center">
                        <p>From</p>
                        <p>Transition</p>
                        <p>To</p>
                    </div>
                </div>
                <button class="col-span-3 justify-self-center self-center bg-gray-600/25 border-[1px] border-gray-700 py-2 px-2 rounded-md font-semibold text-center" type="button" onclick="addTransition(${index}, ${stateAmount}, ${transitionAmount}, 1)"> Add Transition </button>
            </article>`;
        }
        formElement.innerHTML += `
        <input type="text" class="hidden" name="type" id="type" value="nfa"/>
        <button type="submit" class="bg-green-700 px-4 py-2 rounded-md my-5 font-bold">CONVERT DFA</button>`;
    }
};

