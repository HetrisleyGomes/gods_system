/* ALTERAR VIDA E ENERGIA */
document.addEventListener("click", e => {
    const status = e.target.closest(".status-editavel");
    if (!status) return;

    iniciarEdicaoStatus(status);
});

document.addEventListener("click", e => {
    const button = e.target.closest(".save-notes");
    if (!button) return;

    const nota = document.getElementById("notes").value;
    const id = button.dataset.id;
    if (!nota) return;
    
    save_note(id, nota);
});

function iniciarEdicaoStatus(status) {
    const tipo = status.dataset.tipo; // vida ou energia
    const atual = Number(status.dataset.atual);
    const max = Number(status.dataset.max);

    status.innerHTML = `
        ${tipo === "vida" ? "❤️ Vida " : "⚡ Energia "}
        <input type="number"
               class="status-input"
               min="0"
               max="${max}"
               value="${atual}">
        /
        <span class="max">${max}</span>
    `;

    const input = status.querySelector("input");
    input.focus();
    input.select();

    input.addEventListener("blur", () => finalizarEdicaoStatus(status, input));
    input.addEventListener("keydown", e => {
        if (e.key === "Enter") input.blur();
        if (e.key === "Escape") cancelarEdicaoStatus(status);
    });
}

function finalizarEdicaoStatus(status, input) {
    const novoValor = Math.max(0, Math.min(
        Number(input.value),
        Number(status.dataset.max)
    ));

    status.dataset.atual = novoValor;

    status.innerHTML = `
        ${status.dataset.tipo === "vida" ? "❤️ Vida " : "⚡ Energia "}
        <span class="valor">${novoValor}</span>
        /
        <span class="max">${status.dataset.max}</span>
    `;

    // 🔮 GANCHO FUTURO:
    // enviar para backend 
    salvar_backend(status.dataset.tipo, novoValor, status.dataset.id);
    // socket
    socket.emit("status_update", {
        ficha_id: status.dataset.id,
        tipo: status.dataset.tipo,
        valor: novoValor
    });
}

function cancelarEdicaoStatus(status) {
    status.innerHTML = `
        ${status.dataset.tipo === "vida" ? "❤️ Vida " : "⚡ Energia "}
        <span class="valor">${status.dataset.atual}</span>
        /
        <span class="max">${status.dataset.max}</span>
    `;
}

async function salvar_backend(tipo, valor, id){
    type = 0
    if (tipo === "vida"){
        type = 1
    }

    showLoader("Salvando status...");

    try {
        const response = await fetch(`/ficha/${id}/${type}/${valor}`);
        if (!response.ok) throw new Error("Erro ao salvar status da ficha");
    } catch (err) {
        console.error(err);
        alert("Erro ao carregar a ficha");
    } finally {
        hideLoader();
    }
    
}

async function save_note(id, note) {
    showLoader("Salvando notas...");
    try {
        const response = await fetch(`/sala/${id}/mestre/notes-update`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ notes: note })
        });

        if (!response.ok) throw new Error("Erro ao salvar suas notas");

        const data = await response.json();
        renderMestre(data);

    } catch (err) {
        console.error(err);
        alert("Erro ao carregar a ficha");
    } finally {
        hideLoader();
    }
}

socket.on("status_sync", data => {
    atualizarStatusNoDOM(
        data.ficha_id,
        data.tipo,
        data.valor
    );
    console.log(data)
    atualizarMiniFicha(
        data.ficha_id,
        data.tipo,
        data.valor
    );
});

function atualizarStatusNoDOM(fichaId, tipo, valor) {
    const status = document.querySelector(
        `.status[data-id="${fichaId}"][data-tipo="${tipo}"]`
    );

    if (!status) return;

    status.dataset.atual = valor;

    status.querySelector(".valor").textContent = valor;
}

function atualizarMiniFicha(fichaId, tipo, valorAtual) {
    const miniFicha = document.getElementById(`mini-ficha-${fichaId}`);
    if (!miniFicha) return;

    if (tipo === "vida") {
        const lifeBar = miniFicha.querySelector(".life-bar");
        const maxVida = Number(lifeBar.dataset.max); // vamos ajustar isso
        const percent = (valorAtual / maxVida) * 100;
        lifeBar.style.width = `${percent}%`;
    }

    if (tipo === "energia") {
        const energyBar = miniFicha.querySelector(".energy-bar");
        const maxEnergia = Number(energyBar.dataset.max);
        const percent = (valorAtual / maxEnergia) * 100;
        energyBar.style.width = `${percent}%`;
    }
}

/* TROCAR FICHA  */
function trocarView(novoHTML) {
    const container = document.getElementById("view-container");

    // Anima saída
    container.classList.add("exit");

    requestAnimationFrame(() => {
        container.classList.add("exit-active");
    });

    setTimeout(() => {
        // Troca conteúdo
        container.innerHTML = novoHTML;

        // Reseta classes
        container.classList.remove("exit", "exit-active");
        container.classList.add("enter");

        requestAnimationFrame(() => {
            container.classList.add("enter-active");
        });

        setTimeout(() => {
            container.classList.remove("enter", "enter-active");
        }, 250);

    }, 250);
}

