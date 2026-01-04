// GARANTE O ENVIO DOS DADOS
document.getElementById('criar-ficha-form').addEventListener('submit', function(e) {
  const salaId = document.getElementById('sala_id').value.trim();
  const nome = document.getElementById('nome_personagem').value.trim();

  if (!salaId || salaId.length !== 36) {
    e.preventDefault();
    alert('ID da sala inválido. Certifique-se de que você entrou pela página da sala.');
    return;
  }

  if (!nome || nome.length > 50) {
    e.preventDefault();
    alert('Nome do personagem inválido (obrigatório, até 50 caracteres).');
    return;
  }

  // submit prossegue
});

// SINCRONIZA OS DADOS DO FORM COM O MOSTRADOR LATERAL
document.addEventListener("input", function (e) {
    const field = e.target.getAttribute("data-preview");
    if (!field) return;

    const preview = document.getElementById("pv-" + field);
    if (!preview) return;

    let value = e.target.value;

    // Valores numéricos mostram 0 se vazio
    if (e.target.type === "number" && value.trim() === "") {
        value = "0";
    }

    preview.textContent = value === "" ? "—" : convertValue(value);
});

function convertValue(value) {
  switch (value) {
    case "humano_Terra":
      return "humano";
    case "humano_KO_35":
      return "humano";
    case "humano_Mirinoi":
      return "humano";
    case "humano_Shangri_La":
      return "humano";
    case "humano_Aradok_Ivantus":
      return "humano";
    case "sauriano_Teropode":
      return "sauriano";
    case "sauriano_Ceratopcian":
      return "sauriano";
    case "sauriano_Pterossaurideo":
      return "sauriano";
    default:
      return value;
  } 
}

let bonus_construtores = 5

// VERIFICADOR DOS BONUS CONSTRUTORES
let base = {
    vida: 0,
    energia: 0,
    armadura: 0,
    forca: 0,
    constituicao: 0,
    inteligencia: 0,
    destreza: 0,
    carisma: 0,
    combate: 0,
    atletismo: 0,
    tecnologia: 0,
    percepcao: 0,
    conhecimento: 0,
    pontaria: 0,
    furtividade: 0,
    atuacao: 0,
    iniciativa: 0,
    bonus_construtores: 0
};

let pontosExtras = {
    bonus_construtores: 0,
    distribuidos: {}
};

const bonus = {
    arquetipo: {
        combatente: {
            vida: 8,
            combate: 2,
            constituicao: 1,
            atletismo: 1
        },
        genio: {
            vida: 5,
            inteligencia: 2,
            tecnologia: 1,
            percepcao: 1
        },
        celere: {
            vida: 5,
            atletismo: 2,
            iniciativa: 1,
            percepcao: 1
        },
        guardiao: {
            vida: 6,
            percepcao: 1,
            combate: 1,
            carisma: 2
        },
        peregrino: {
          vida: 7,
          conhecimento: 1,
          percepcao: 1,
          bonus_construtores: 2
        },
        sobrevivente: {
          vida: 9,
          combate: 1,
          percepcao: 1,
          constituicao: 2
        },
        atirador: {
          vida: 5,
          destreza: 1,
          percepcao: 1,
          pontaria: 2
        },
        vanguarda: {
          vida: 10,
          // defesa: 2,
          constituicao: 1,
          combate: 1
        },
        sombra: {
          vida: 5,
          furtividade: 2,
          atuacao: 1,
          destreza: 1
        }
    },

    especie: {
        humano_Terra: { vida: 3, energia: 3, bonus_construtores: 3},
        humano_KO_35: { vida: 3, energia: 5, bonus_construtores: 3 },
        humano_Mirinoi: { vida: 3, energia: 3, bonus_construtores: 3},
        humano_Shangri_La: { vida: 3, energia: 3, bonus_construtores: 3},
        humano_Aradok_Ivantus: { vida: 3, energia: 3, bonus_construtores: 3},
        sphynx: { vida: 2, energia: 4, acrobacia: 2, percepcao: 2 },
        sirians: { vida: 5, energia: 2, constituicao: 2, armadura: 2},
        android: { vida: 4, energia: 5, armadura: 2},
        aquitiano: { vida: 2, energia: 3, percepcao: 1, iniciativa: 2 },
        sauriano_Teropode: { vida: 6, energia: 3, combate:2, atletismo:1 },
        sauriano_Ceratopcian: { vida: 6, energia: 3, constituicao: 2, forca:1 },
        sauriano_Pterossaurideo: { vida: 6, energia: 3, acrobacia: 2, destreza: 1 },
        rafkan: { vida: 3, energia: 5, combate: 1, constituicao: 1 },
        // ...
    },

    cor: {
        vermelho: { energia: 7 },
        azul: { energia: 7 },
        amarelo: { energia: 7 },
        rosa: { energia: 7 },
        verde: { energia: 9 },
        preto: { energia: 7 },
        branco: { energia: 9 },
    }
};

// ----------------- util -----------------
function lerDistribuidosDoDOM() {
  const distribuidos = {};
  const inputs = document.querySelectorAll("#atributos_container .extra");
  inputs.forEach(inp => {
    const attr = inp.getAttribute("data-attr") || inp.getAttribute("data-atributo") || inp.dataset.attr;
    const val = Number(inp.value) || 0;
    distribuidos[attr] = val;
  });
  return distribuidos;
}

// ----------------- recalculador (fonte única) -----------------
function recalcularFicha() {
  // 0) atualiza construtores/bônus (dependendo do select atual)
  atualizarEspecie(); // atualiza pontosExtras.bonus_construtores

  // 1) ler os distribuídos diretamente do DOM (fonte de verdade)
  const distribuidosAtuais = lerDistribuidosDoDOM();
  pontosExtras.distribuidos = { ...distribuidosAtuais }; // sincroniza estado

  // 2) montar calc = base + construtores + distribuídos
  let calc = { ...base };
  const cor = document.getElementById("cor")?.value || "";
  const especie = document.getElementById("especie")?.value || "";
  const arquetipo = document.getElementById("arquetipo")?.value || "";

  if (bonus.cor[cor]) for (let k in bonus.cor[cor]) calc[k] = (calc[k]||0) + bonus.cor[cor][k];
  if (bonus.especie[especie]) for (let k in bonus.especie[especie]) calc[k] = (calc[k]||0) + bonus.especie[especie][k];
  if (bonus.arquetipo[arquetipo]) for (let k in bonus.arquetipo[arquetipo]) calc[k] = (calc[k]||0) + bonus.arquetipo[arquetipo][k];

  for (let k in distribuidosAtuais) {
    if (calc[k] === undefined) calc[k] = 0;
    calc[k] += distribuidosAtuais[k];
  }

  // 3) atualiza preview, hidden json e mostrador
  atualizarPreview(calc);
  const hidden = document.getElementById("atributos_json");
  if (hidden) hidden.value = JSON.stringify(calc);
  atualizarMostradorPontosRestantes();
}


// ----------------- actualiza preview -----------------
function atualizarPreview(calc) {
  for (let atributo in calc) {
    const span = document.getElementById("pv-" + atributo);
    if (span) span.textContent = calc[atributo];
  }
}

// ----------------- atualiza especie (bonus_construtores) -----------------
function atualizarEspecie() {
  const especie = document.getElementById("especie")?.value;
  pontosExtras.bonus_construtores = bonus.especie?.[especie]?.bonus_construtores || 0;
}

// ----------------- mostrador -----------------
function atualizarMostradorPontosRestantes() {
  const container = document.getElementById("atributos_container");
  const maxPontos = parseInt(container?.dataset?.bonus || "0", 10);
  const inputs = document.querySelectorAll("#atributos_container .extra");
  let soma = 0;
  inputs.forEach(inp => soma += Number(inp.value) || 0);
  const total = maxPontos + (pontosExtras.bonus_construtores||0) - soma;
  const mostrador = document.getElementById("pontos-restantes");
  if (mostrador) mostrador.textContent = total;
}

// ----------------- configurar listeners robusto (chamar uma vez) -----------------
function configurarDistribuicaoAtributos() {
  const container = document.getElementById("atributos_container");
  const inputs = Array.from(container.querySelectorAll(".extra"));

  // remove listeners antigos com clone (garante limpeza)
  inputs.forEach((inp,i) => {
    const clone = inp.cloneNode(true);
    clone.dataset.last = inp.dataset.last ?? inp.value ?? 0;
    inp.replaceWith(clone);
    inputs[i] = clone;
  });

  // handler único para todos inputs
  function handleExtraInput(e) {
    const input = e.target;
    const attr = input.getAttribute("data-attr") || input.dataset.attr;
    const container = document.getElementById("atributos_container");
    const maxPontos = parseInt(container?.dataset?.bonus || "0", 10);
    // soma atual (com o novo valor)
    const curInputs = document.querySelectorAll("#atributos_container .extra");
    let soma = 0;
    curInputs.forEach(i => soma += Number(i.value) || 0);

    const limite = maxPontos + (pontosExtras.bonus_construtores || 0);

    if (soma > limite) {
      alert(`Você só pode distribuir ${limite} pontos.`);
      // reverte visualmente
      input.value = input.dataset.last || 0;
      // sincroniza estado com DOM (garante que nada fique sujo)
      pontosExtras.distribuidos[attr] = Number(input.value || 0);
      // recalcula a ficha (lê do DOM e limpa qualquer lixo)
      recalcularFicha();
      return;
    }

    // valor válido → grava
    input.dataset.last = input.value;
    pontosExtras.distribuidos[attr] = Number(input.value || 0);

    // recalcula (vai ler do DOM e atualizar tudo)
    recalcularFicha();
  }

  // adiciona listeners
  inputs.forEach(inp => {
    if (!inp.dataset.last) inp.dataset.last = inp.value || 0;
    inp.addEventListener("input", handleExtraInput);
  });

  // inicializa mostrador e sincroniza uma primeira vez
  atualizarMostradorPontosRestantes();
}

// ----------------- inicializador (executar depois do DOM pronto) -----------------
function initFicha() {
  // configurar selects para disparar recalculo quando mudarem
  document.querySelectorAll("#cor, #especie, #arquetipo").forEach(sel => sel.addEventListener("change", recalcularFicha));

  // configura inputs e listeners
  configurarDistribuicaoAtributos();

  // calculo inicial
  recalcularFicha();
}

// chame initFicha() após DOMContentLoaded
document.addEventListener("DOMContentLoaded", initFicha);