document.addEventListener("click", e => {
    const btn = e.target.closest(".atributo-btn");
    if (btn) executarTeste(btn);

    const poder = e.target.closest(".poder-card");
    if (poder) anunciarPoder(poder);

    const mechaPoder = e.target.closest(".poder-mecha");
    if (mechaPoder) anunciarPoderMecha(mechaPoder);


    const equipamento = e.target.closest(".equipamento");
    if (equipamento) executarAtaque(equipamento);
});

function executarTeste(btn) {
    const atributo = btn.dataset.atributo;
    const valorBase = Number(btn.dataset.valor);
    const personagem = btn.dataset.personagem || "Mestre";
    
    const modificador = get_modificador();

    // DADO
    const dados = "2d6";

    const rolagem = rolarDados(dados);
    const resultadoFinal = rolagem.total + valorBase + modificador;

    const log = formatarLog({
        personagem,
        atributo,
        dados,
        base: valorBase,
        modificador,
        rolagem: rolagem.valores,
        total: resultadoFinal
    });

    const salaId = document.getElementById("sala_id").value;

    emitirLog(salaId, log);
}

function executarAtaque(equipamento) {
    const {
        nome,
        dano,
        personagem = "Mestre",
        efeito,
        tipo_dano: tipoDano
    } = equipamento.dataset;

    const salaId = document.getElementById("sala_id").value;

    // 🛡️ Caso especial: Proteção
    if (tipoDano === "Proteção") {
        const log = formatarLogPoder({
            personagem,
            nome,
            descricao: efeito
        });

        emitirLog(salaId, log);
        return;
    }

    // ⚔️ Ataque padrão
    const modificador = get_modificador();
    const rolagem = rolarDados(dano);

    const total = rolagem.total + modificador;

    const log = formatarLogEquip({
        personagem,
        equip_nome: nome,
        equip_dano: dano,
        equip_efeito: efeito,
        modificador,
        rolagem: rolagem.valores,
        total
    });

    emitirLog(salaId, log);
}

function get_modificador(){
    const modificadorInput = document.querySelector(
        'input[data-tipo="mod"]'
    );

    const modificador = modificadorInput
        ? Number(modificadorInput.value || 0)
        : 0;

    return modificador;
}

function emitirLog(salaId, log) {
    socket.emit("log", {
        sala_id: salaId,
        log
    });
}

function rolarDados(expr) {
    const [qtd, faces] = expr.split("d").map(Number);

    const valores = [];
    let total = 0;

    for (let i = 0; i < qtd; i++) {
        const roll = Math.floor(Math.random() * faces) + 1;
        valores.push(roll);
        total += roll;
    }

    return { valores, total };
}

function anunciarPoder(poder) {
    const nome = poder.dataset.nome;
    const descricao = poder.dataset.descricao;
    const personagem = poder.dataset.personagem || "Mestre";

    const salaId = document.getElementById("sala_id").value;

    const log = formatarLogPoder({
        personagem,
        nome,
        descricao
    })

    emitirLog(salaId, log);
}

function anunciarPoderMecha(poder) {
    const personagem = poder.dataset.personagem;
    const poder_desc = poder.dataset.poder;
    const salaId = document.getElementById("sala_id").value;

    const log = `<div class="log-item"><strong>${personagem}</strong> usou <span>${poder_desc}</span></div>`;

    emitirLog(salaId, log);
}

function formatarLog(data) {
    const {
        personagem,
        atributo,
        dados,
        base,
        modificador,
        rolagem,
        total
    } = data;

    const baseStr = base !== 0
        ? ` + ${base}`
        : "";

    const modStr = modificador !== 0
        ? ` + ${modificador}`
        : "";

    return `<div class="log-item"><strong>${personagem}</strong> usou <strong>${atributo}</strong> <span class="log-dados">[${dados}${baseStr}${modStr}]</span> → <span class="log-resultado">${total}</span> <small>(rolagem: ${rolagem.join(", ")})</small></div>`;
}

function formatarLogEquip(data) {
        const {
        personagem,
        equip_nome,
        equip_dano,
        equip_efeito,
        modificador,
        rolagem,
        total
    } = data;

    const modStr = modificador !== 0
        ? ` + ${modificador}`
        : "";

    return `<div class="log-item"><strong>${personagem}</strong> usou <strong>${equip_nome}</strong> <span class="log-dados">[${equip_dano}${modStr}]</span> → <span class="log-resultado">${total}</span> <small>(rolagem: ${rolagem.join(", ")})</small><br/><small>${equip_efeito}</small></div>`;
}

function formatarLogPoder(data) {
    const {
        personagem,
        nome,
        descricao
    } = data;

    return `<div class="log-item"><strong>${personagem}</strong> usou <strong>[${nome}]</strong> → <small>${descricao}</small></div>`;
}

function adicionarLog(html) {
    const container = document.getElementById("logs-container");
    container.insertAdjacentHTML("afterbegin", html);
}

socket.on("log_sync", data => {
    adicionarLog(data.log);
});