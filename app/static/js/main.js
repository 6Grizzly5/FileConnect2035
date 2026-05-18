async function chargerServices() {

    const response = await fetch('/services');

    const services = await response.json();

    const container = document.getElementById('services');

    services.forEach(service => {

        const carte = document.createElement('div');

        carte.className =
            'bg-white p-4 rounded-xl shadow';

        carte.innerHTML = `
            <h2 class="text-xl font-semibold">
                ${service.nom}
            </h2>

            <button
                onclick="prendreTicket(${service.id})"
                class="mt-3 bg-blue-500 text-white px-4 py-2 rounded-lg"
            >
                Choisir
            </button>
        `;

        container.appendChild(carte);

    });

}

async function prendreTicket(id_service) {

    const response = await fetch('/ticket', {

        method: 'POST',

        headers: {
            'Content-Type': 'application/json'
        },

        body: JSON.stringify({
            id_service: id_service
        })

    });

    const data = await response.json();

    window.location.href = `/ticket/${data.id_ticket}`;
}

chargerServices();