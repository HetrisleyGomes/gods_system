async function abrirMecha() {
    showLoader("Carregando mecha...");

    try {
        const response = await fetch(`/mecha/${ficha_global.id}`);
        const data = await response.json();

        if (!data.has_mecha) {
            window.location.href = data.redirect_to;
            return;
        }

        renderMecha(data.mecha['body'], data.ficha['body']);

    } catch (err) {
        console.error(err);
        alert("Erro ao carregar mecha");
    } finally {
        hideLoader();
    }
}


function renderMecha(mecha, ficha) {

    const html = `
    <div class="mecha-view">

        <!-- Cabeçalho -->
        <header class="ficha-header ${ficha.cor}">
            <h2><span id="mecha-nome" class="nome-personagem">${mecha.nome}</span></h2>

            <div class="status-bar">
                <div class="status status-editavel-2"
                    data-tipo="vida"
                    data-id="${mecha.id}"
                    data-atual="${mecha.vida_atual}"
                    data-max="${mecha.vida}">
                    ❤️ Vida :
                    <span class="valor">${mecha.vida_atual}</span> /
                    <span class="max">${mecha.vida}</span>
                </div>

                <div class="status status-editavel" data-tipo="energia" data-atual="${ficha.energia_atual}" data-max="${ficha.energia}" data-id="${ficha.id}">
                    ⚡Energia: <span class="valor">${ficha.energia_atual}</span>/<span class="max">${ficha.energia}</span>
                </div>

                <div class="status">
                    🛡️ Armadura:
                    <span id="armadura">${mecha.armadura}</span>
                </div>
            </div>
        </header>

        <!-- Atributos -->
        <section class="ficha-bloco">
            <h3>Atributos</h3>

            <div class="atributos mod-container">
                <label for="mod">Modificador</label>
                <input type="number" class="mod" data-tipo="mod" data-id="mod" id="mod" max="5" min="-5">
            </div>

            <div class="atributos a-mecha">
                <button class="atributo-btn" data-atributo="combate" data-valor="${mecha.combate}" data-personagem="${mecha.nome} de ${ficha.nome_personagem}">
                    <span class="attr-nome">Combate</span>
                    <span class="attr-valor">${mecha.combate}</span>
                </button>
                <button class="atributo-btn" data-atributo="pontaria" data-valor="${mecha.pontaria}" data-personagem="${mecha.nome} de ${ficha.nome_personagem}">
                    <span class="attr-nome">Pontaria</span>
                    <span class="attr-valor">${mecha.pontaria}</span>
                </button>
                <button class="atributo-btn" data-atributo="defesa" data-valor="${mecha.defesa}" data-personagem="${mecha.nome} de ${ficha.nome_personagem}">
                    <span class="attr-nome">Defesa</span>
                    <span class="attr-valor">${mecha.defesa}</span>
                </button>
                <button class="atributo-btn" data-atributo="forca" data-valor="${mecha.forca}" data-personagem="${mecha.nome} de ${ficha.nome_personagem}">
                    <span class="attr-nome">Força</span>
                    <span class="attr-valor">${mecha.forca}</span>
                </button>
            </div>
        </section>

        <!-- Armas -->
        <section class="ficha-bloco">
            <h3>Armas</h3>
            <div class="armas-grid" id="armas-container">
                ${renderArmas(mecha.armas, mecha.nome, ficha.nome_personagem)}
            </div>
        </section>

        <!-- Habilidades -->
        <section class="ficha-bloco">
            <h3>Habilidades</h3>
            <ul id="habilidades-list">
            ${mecha.habilidades.map(h => `<li class="poder-mecha" data-poder="${h}" data-personagem="${mecha.nome} de ${ficha.nome_personagem}">${h}</li>`).join("")}
            </ul>
        </section>

    </div>
    `;

    trocarView(html);
};

function renderArmas(armas, mecha, nome) {
    if (!armas.length) {
        return "<p>Nenhuma arma equipada.</p>";
    }
    nome_format = mecha + " de " + nome
    return armas.map(ar => `
        <div class="equipamento" data-nome="${ar.nome}" data-dano="${ar.dano}" data-efeito="${ar.efeito}" data-tipo_dano="${ar.tipo}" data-personagem="${nome_format}">
            <strong>${ar.nome}</strong>
            <p><strong>Dano:</strong> ${ar.dano}</p>
            <p><strong>Tipo:</strong> ${ar.tipo}</p>
            <small class="full-grid">${ar.efeito}</small>
        </div>
    `).join("");
}

document.addEventListener("click", e => {
    const status = e.target.closest(".status-editavel-2");
    if (!status) return;

    iniciarEdicaoStatus2(status);
});

function iniciarEdicaoStatus2(status) {// vida ou energia
    const atual = Number(status.dataset.atual);
    const max = Number(status.dataset.max);

    status.innerHTML = `
        ❤️ Vida :
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

    input.addEventListener("blur", () => finalizarEdicaoStatusMecha(status, input));
    input.addEventListener("keydown", e => {
        if (e.key === "Enter") input.blur();
        if (e.key === "Escape") cancelarEdicaoStatusMecha(status);
    });
}

function finalizarEdicaoStatusMecha(status, input) {
    const novoValor = Math.max(0, Math.min(
        Number(input.value),
        Number(status.dataset.max)
    ));

    status.dataset.atual = novoValor;

    status.innerHTML = `
        ❤️ Vida :
        <span class="valor">${novoValor}</span>
        /
        <span class="max">${status.dataset.max}</span>
    `;

    // 🔮 GANCHO FUTURO:
    // enviar para backend 
    salvar_backend_mecha(status.dataset.tipo, novoValor, status.dataset.id);
}

function cancelarEdicaoStatusMecha(status) {
    status.innerHTML = `
        ❤️ Vida :
        <span class="valor">${status.dataset.atual}</span>
        /
        <span class="max">${status.dataset.max}</span>
    `;
}

async function salvar_backend_mecha(tipo, valor, id){
    showLoader("Salvando status...");

    try {
        const response = await fetch(`/ficha/${id}/${valor}`);
        if (!response.ok) throw new Error("Erro ao salvar status da ficha");

        const data = await response.json();
    } catch (err) {
        console.error(err);
        alert("Erro ao carregar a ficha");
    } finally {
        hideLoader();
    }
    
}