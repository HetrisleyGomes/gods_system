const viewContainer = document.getElementById("view-container");
const menuItems = document.querySelectorAll(".menu-item");

var ficha_global;

document.querySelectorAll(".menu-item").forEach(btn => {
    btn.addEventListener("click", async () => {
        const view = btn.dataset.view;
        
        if (!view) return;
        
        if (view == 0) {
            verificarMestre();
            return;
        }
        
        showLoader("Carregando ficha...");

        try {
            const response = await fetch(`/ficha/${view}/json`);
            if (!response.ok) throw new Error("Erro ao buscar ficha");

            const data = await response.json();
            renderFicha(data);
        } catch (err) {
            console.error(err);
            alert("Erro ao carregar a ficha");
        } finally {
            hideLoader();
        }
    });
});

async function verificarMestre() {
    const salaId = document.getElementById("sala_id").value;
    const statusResp = await fetch(`/sala/${salaId}/mestre/status`);
    const status = await statusResp.json();

    if (!status.is_mestre) {
        const senha = prompt("Digite a senha do mestre:");
        if (!senha) return;

        const loginResp = await fetch(`/sala/${salaId}/mestre/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ senha })
        });

        if (!loginResp.ok) {
            alert("Senha incorreta");
            return;
        }
    }
    showLoader("Carregando Mestre...");
    try {
        const notesResp = await fetch(`/sala/${salaId}/mestre/notes`);
        const data = await notesResp.json();

        const fichasResp = await fetch(`/sala/${salaId}/get_fichas`);
        const fichas = await fichasResp.json();

        renderMestre(data, fichas);
    } catch (err) {
            console.error(err);
            alert("Erro ao carregar mestre");
    } finally {
        hideLoader();
    }
}


function renderMestre(data, fichas) {
    const html = `
        <session class="mestre-view">
        <!-- TOPO -->
        <header class="mestre-header">
            <h2 class="nome-personagem">Mestre</h2>
        </header>
        <div class="controllers roll-group">
        <div>
            <label for="modificator-master">Modificador</label>
            <input type="number" class="controller-input" data-tipo="mod" id="modificator-master" placeholder="0">
        </div>
        <div>
            <label for="dice-master">Dado</label>
            <input type="text" class="controller-input" data-tipo="dice" id="dice-master" placeholder="2d6">
            <button class="roll-btn" data-origem="mestre">Rolar dado</button>
        </div>
        </div>
        <div class="notebook">
            <textarea class="notes" id="notes">${data['notes'] ?? ""}</textarea>
            <button class="save-notes" data-id="${data.id}">Salvar notas</button>
        </div>
        </session>

        <session class="players-view">
            <div class="mini-ficha-container">
                ${renderfichas(fichas)}
            </div>
        </session>
    `;

    trocarView(html);
}

function renderFicha(data) {
    const ficha = data['body'];
    ficha_global = ficha;

    const html = `
    <section class="ficha" data-personagem="${ficha.nome_personagem}">

        <!-- TOPO -->
        <header class="ficha-header ${ficha.cor}">
            <h2 class="nome-personagem">${ficha.nome_personagem}</h2>

            <div class="status-bar">
                <div class="status status-editavel" data-tipo="vida" data-atual="${ficha.vida_atual}" data-max="${ficha.vida}" data-id="${ficha.id}">
                    ❤️ Vida: <span class="valor">${ficha.vida_atual}</span>/<span class="max">${ficha.vida}</span>
                </div>
                <div class="status status-editavel" data-tipo="energia" data-atual="${ficha.energia_atual}" data-max="${ficha.energia}" data-id="${ficha.id}">
                    ⚡Energia: <span class="valor">${ficha.energia_atual}</span>/<span class="max">${ficha.energia}</span>
                </div>
                <div class="status">
                    🛡️ Armadura: <span class="armadura">${ficha.armadura}</span>
                </div>
            </div>

            </header>

        <div class="construtores">
            <div class="construtor-divisor">
            <span>Ranger ${ficha.cor}</span>
            <span>${ficha.especie}</span>
            <span>${ficha.arquetipo}</span>
            </div>

            <div class="construtor-divisor">
            ${ficha.xp > (ficha.nivel + 7) ? "Pode subir de nível!" : ""}
            <span>XP: ${ficha.xp}</span>
            <span>Nível: ${ficha.nivel}</span>
            </div>
        </div>

        <!-- ATRIBUTOS -->
        <section class="ficha-bloco">
            <h3>Atributos</h3>

            <div class="atributos mod-container">
                <label for="mod">Modificador</label>
                <input type="number" class="mod" data-tipo="mod" data-id="mod" id="mod" max="5" min="-5">
            </div>

            <div class="atributos principais">
                ${renderAtributos(ficha, [
                    "forca", "constituicao", "inteligencia",
                    "destreza", "carisma"
                ])}
            </div>

            <div class="atributos secundarios">
                ${renderAtributos(ficha, [
                    "combate", "atletismo", "tecnologia",
                    "percepcao", "conhecimento", "pontaria",
                    "furtividade", "atuacao", "iniciativa"
                ])}
            </div>
        </section>

        <!-- EDITORES -->
        <section class="ficha-bloco">
            <a href="/ficha/editar/${ ficha.id }"><button class="atributo-btn">Editar ficha</button></a>
            <a href="/equipamentos/${ ficha.id }"><button class="atributo-btn">Editar equipamentos</button></a>
            <a href="/poderes/${ ficha.id }"><button class="atributo-btn">Editar poderes</button></a>
            <button class="atributo-btn" id="btn-mecha" onclick="abrirMecha()">Mecha</button>

        </section>

        <!-- EQUIPAMENTOS -->
        <section class="ficha-bloco">
            <h3>Equipamentos</h3>

            <ul class="equipamentos">
                ${renderEquipamentos(ficha.equipamentos || [], ficha)}
            </ul>
        </section>

        <!-- PODERES -->
        <section class="ficha-bloco">
            <h3>Poderes</h3>

            <div class="poderes">
                ${renderPoderes(ficha.poderes || [], ficha)}
            </div>
        </section>

    </section>
    `;

    trocarView(html);
}

function renderAtributos(ficha, lista) {
    return lista.map(attr => `
        <button class="atributo-btn"
            data-atributo="${attr}"
            data-valor="${ficha[attr]}"
            data-personagem="${ficha.nome_personagem}">
            <span class="attr-nome">${attr}</span>
            <span class="attr-valor">${ficha[attr]}</span>
        </button>
    `).join("");
}

function renderEquipamentos(equipamentos, ficha) {
    return equipamentos.map(eq => `
        <li class="equipamento"
            data-nome="${eq.nome}"
            data-dano="${eq.dano}"
            data-efeito="${eq.efeito}"
            data-tipo_dano="${eq.tipo_dano}"
            data-personagem="${ficha.nome_personagem}">
            
            <strong>${eq.nome}</strong>
            <span></span>
            <span>${eq.tipo_arma} | ${eq.tipo_dano}</span>
            <span>${eq.dano}</span>
            <span class="full-grid">${eq.efeito}</span>
        </li>
    `).join("");
}

function renderPoderes(poderes, ficha) {
    return poderes.map(p => `
        <div class="poder-card"
            data-nome="${p.nome}"
            data-descricao="${p.descricao}"
            data-personagem="${ficha.nome_personagem}">
            
            <h4>${p.nome}</h4>
            <p>${p.descricao.replace(/\r?\n/g, "<br>")}</p>
        </div>
    `).join("");
}

function renderfichas(fichas) {
    return fichas.map(p => `
        <div class="mini-ficha" id="mini-ficha-${p.id}">
            <header class="mini-ficha-header">
                <p class="nome-personagem"> ${p.nome_personagem} </p>
                <div class="mini-cor ${p.cor}"></div>
            </header>
            <div class="bars-container" title="Vida">
                <div class="life-bar-container">
                    <div class="life-bar" data-max="${p.vida}" style="width: ${p.vida_atual / p.vida * 100}%">
                    </div>
                </div>
                <div class="energy-bar-container" title="Energia">
                    <div class="energy-bar" data-max="${p.energia}" style="width: ${p.energia_atual / p.energia * 100}%">
                    </div>
                </div>
            </div>
            <div class="mini-status">
                <div class="mini-status-container">
                    <div class="mini-status-item forca" title="Força">
                     ${p.forca}
                    </div>
                    <div class="mini-status-item constituicao" title="Constituição">
                     ${p.constituicao}
                    </div>
                    <div class="mini-status-item inteligencia" title="Inteligência">
                     ${p.inteligencia}
                    </div>
                    <div class="mini-status-item destreza" title="Destreza">
                     ${p.destreza}
                    </div>
                    <div class="mini-status-item carisma" title="Carisma">
                     ${p.carisma}
                    </div>
                </div>
            </div>
        </div>
        `).join("");
}

// LOGS
const salaId = document.getElementById("sala_id").value;

// entra na room
socket.emit("join_sala", { sala_id: salaId });

// carrega logs antigos
async function carregarLogsIniciais() {
    const resp = await fetch(`/sala/${salaId}/logs`);
    const data = await resp.json();

    data.logs.forEach(adicionarLog);
}

carregarLogsIniciais();
