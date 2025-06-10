const MAX_SELECTION = 5;
const MAX_STAT = 200;

function showAlertModal(message) {
  const modalBody = document.getElementById("alertModalBody");
  modalBody.innerHTML = message;

  const alertModal = new bootstrap.Modal(document.getElementById("alertModal"));
  alertModal.show();
}

async function loadPokemonOptions() {
  const response = await fetch("https://pokeapi.co/api/v2/pokemon?limit=1025");
  const data = await response.json();

  const pokemonOptions = await Promise.all(
    data.results.map(async (pokemon, index) => {
      const id = index + 1;
      const img = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${id}.png`;
      const name = pokemon.name.charAt(0).toUpperCase() + pokemon.name.slice(1);
      return {
        value: pokemon.name,
        label: name,
        img: img,
      };
    })
  );

  const select = document.getElementById("pokemon-select");
  pokemonOptions.forEach((p) => {
    const option = document.createElement(`option`);
    option.value = p.value;
    option.textContent = p.label;
    option.setAttribute(
      "data-content",
      `<img src="${p.img}" width="24" class="me-2">${p.label}`
    );
    select.appendChild(option);
  });

  $(".selectpicker").selectpicker("refresh");

  // Recarrega o selectpicker depois de adicionar as opções
  $(".selectpicker").selectpicker({
    noneSelectedText: "Escolha os Pokémon...",
    maxOptions: MAX_SELECTION,
  });
}

function getTypeColor(type) {
  const typeColors = {
    normal: "#A8A77A",
    fire: "#EE8130",
    water: "#6390F0",
    electric: "#F7D02C",
    grass: "#7AC74C",
    ice: "#96D9D6",
    fighting: "#C22E28",
    poison: "#A33EA1",
    ground: "#E2BF65",
    flying: "#A98FF3",
    psychic: "#F95587",
    bug: "#A6B91A",
    rock: "#B6A136",
    ghost: "#735797",
    dragon: "#6F35FC",
    dark: "#705746",
    steel: "#B7B7CE",
    fairy: "#D685AD",
  };

  return typeColors[type] || "#777"; // Cor cinza padrão
}

function formatOption(option) {
  if (!option.id) return option.text;
  return $(`
        <span><img src="${option.img}" class="img-icon" /> ${option.text}</span>
      `);
}

function getStatColor(stat) {
  if (stat >= 130) return "bg-primary"; // azul
  if (stat >= 90) return "bg-warning"; // amarelo
  return "bg-danger"; // vermelho
}

function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

async function renderRecommendations(pokemonList) {
  const container = document.getElementById("pokemon-cards");
  container.innerHTML = ""; // Limpa cards antigos

  for (const pkm of pokemonList) {
    try {
      const response = await fetch(
        `https://pokeapi.co/api/v2/pokemon/${pkm.name.toLowerCase()}`
      );
      const data = await response.json();

      const types = data.types
        .map(
          (t) =>
            `<span class="badge me-1 text-white" style="background-color: ${getTypeColor(
              t.type.name
            )}">${capitalize(t.type.name)}</span>`
        )
        .join("");

      const statsHtml = data.stats
        .map((stat) => {
          const value = stat.base_stat;
          const percent = Math.min((value / MAX_STAT) * 100, 100);
          return `
    <div class="mb-1"><strong>${capitalize(
      stat.stat.name.replace("-", " ")
    )}:</strong> ${value}</div>
    <div class="progress mb-2" style="height: 8px;">
      <div class="progress-bar ${getStatColor(
        value
      )}" style="width: ${percent}%;"></div>
    </div>
  `;
        })
        .join("");

      const card = `
        <div class="card bg-secondary text-white p-3" style="width: 18rem;">
          <h5 class="card-title text-center">${capitalize(pkm.name)}</h5>
          <img src="${
            data.sprites.front_default
          }" class="card-img-top mx-auto" style="width: 96px;" alt="${
        pkm.name
      }">
          <div class="text-center my-2">${types}</div>
          <div class="card-body">${statsHtml}</div>
        </div>
      `;

      container.insertAdjacentHTML("beforeend", card);
    } catch (error) {
      console.error("Erro ao carregar Pokémon:", pkm.name, error);
    }
  }
}

$("#submit-btn").click(async () => {
  const selected = $("#pokemon-select").val();
  if (!selected.length) {
    showAlertModal("Selecione pelo menos 1 Pokémon antes de continuar.");
    return;
  }

  try {
    loading.style.display = "block";
    const response = await fetch("http://localhost:8000/recommend", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ selected_pokemon: selected }),
    });

    if (!response.ok) {
      throw new Error(`Erro do servidor: ${response.status}`);
    }

    const data = await response.json();
    renderRecommendations(data);
  } catch (error) {
    showAlertModal(
      "Erro de conexão com o servidor. Verifique se a API está rodando corretamente.<br><br><code>" +
        error.message +
        "</code>"
    );
  } finally {
    loading.style.display = "none";
  }
});

loadPokemonOptions();
