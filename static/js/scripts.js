
// scripts.js
// Autor: Gemini
// Fecha: 26-09-2025
// Descripción: Script para obtener, filtrar y mostrar datos de consultas.

document.addEventListener('DOMContentLoaded', () => {
    // Si estamos en la página de historial (identificada por la presencia de la tabla), iniciamos la lógica.
    if (document.getElementById('consultas-tbody')) {
        iniciarPaginaHistorial();
    }
});

// Almacenamiento temporal de los datos de consulta para no tener que pedirlos de nuevo.
let consultasData = [];

/**
 * Inicializa la página de historial: obtiene datos y configura el filtro.
 */
function iniciarPaginaHistorial() {
    fetchConsultas();

    // Listener para el modal, para cargar datos dinámicamente cuando se muestra.
    const detalleModal = document.getElementById('detalleModal');
    if (detalleModal) {
        detalleModal.addEventListener('show.bs.modal', event => {
            const button = event.relatedTarget;
            const consultaId = button.getAttribute('data-bs-id');
            cargarDetallesModal(consultaId);
        });
    }

    // Listener para el campo de filtro.
    const filtroInput = document.getElementById('filtro-input');
    if (filtroInput) {
        filtroInput.addEventListener('keyup', () => {
            const textoFiltro = filtroInput.value.toLowerCase();
            const consultasFiltradas = consultasData.filter(consulta => {
                // El filtro busca en varios campos del objeto de consulta.
                return (
                    consulta.paciente.nombre.toLowerCase().includes(textoFiltro) ||
                    consulta.id_consulta.toLowerCase().includes(textoFiltro) ||
                    consulta.motivo_consulta.toLowerCase().includes(textoFiltro) ||
                    consulta.tratamiento.estado.toLowerCase().includes(textoFiltro) ||
                    consulta.fecha.toLowerCase().includes(textoFiltro)
                );
            });
            renderizarTabla(consultasFiltradas);
        });
    }
}

/**
 * Obtiene los datos de las consultas desde la API backend.
 */
async function fetchConsultas() {
    try {
        const response = await fetch('/api/consultas');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        consultasData = await response.json();
        renderizarTabla(consultasData);
    } catch (error) {
        console.error("Error al obtener las consultas:", error);
        const tbody = document.getElementById('consultas-tbody');
        tbody.innerHTML = `<tr><td colspan="6" class="text-center text-danger">Error al cargar los datos. Verifique la consola.</td></tr>`;
    }
}

/**
 * Renderiza los datos de las consultas en la tabla HTML.
 * @param {Array} consultas - Un array de objetos de consulta.
 */
function renderizarTabla(consultas) {
    const tbody = document.getElementById('consultas-tbody');
    tbody.innerHTML = ''; // Limpiar el cuerpo de la tabla.

    if (consultas.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" class="text-center">No se encontraron resultados para su búsqueda.</td></tr>`;
        return;
    }

    consultas.forEach(consulta => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${consulta.id_consulta}</td>
            <td>${consulta.paciente.nombre}</td>
            <td>${consulta.fecha} ${consulta.hora}</td>
            <td>${consulta.motivo_consulta}</td>
            <td>${obtenerBadgeEstado(consulta.tratamiento.estado)}</td>
            <td>
                <button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#detalleModal" data-bs-id="${consulta.id_consulta}">
                    Ver Detalles
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

/**
 * Devuelve un badge de Bootstrap con un color según el estado del tratamiento.
 * @param {string} estado - El estado del tratamiento.
 * @returns {string} - El HTML del badge.
 */
function obtenerBadgeEstado(estado) {
    let claseBadge = 'bg-secondary';
    if (estado === 'Completado') {
        claseBadge = 'bg-success';
    } else if (estado === 'En progreso') {
        claseBadge = 'bg-warning text-dark';
    } else if (estado === 'Pendiente') {
        claseBadge = 'bg-danger';
    }
    return `<span class="badge ${claseBadge}">${estado}</span>`;
}

/**
 * Carga la información detallada de una consulta en el cuerpo del modal.
 * @param {string} consultaId - El ID de la consulta a mostrar.
 */
function cargarDetallesModal(consultaId) {
    const modalBody = document.getElementById('modal-body-content');
    const consulta = consultasData.find(c => c.id_consulta === consultaId);

    if (!consulta) {
        modalBody.innerHTML = '<p class="text-danger">No se encontraron detalles para esta consulta.</p>';
        return;
    }

    modalBody.innerHTML = `
        <h6>Información del Paciente</h6>
        <div class="info-grid">
            <strong>Nombre:</strong><span>${consulta.paciente.nombre}</span>
            <strong>ID Paciente:</strong><span>${consulta.paciente.id_paciente}</span>
            <strong>Edad:</strong><span>${consulta.paciente.edad}</span>
            <strong>Género:</strong><span>${consulta.paciente.genero}</span>
        </div>

        <h6>Detalles de la Cita</h6>
        <div class="info-grid">
            <strong>Dentista:</strong><span>${consulta.dentista}</span>
            <strong>Fecha:</strong><span>${consulta.fecha}</span>
            <strong>Hora:</strong><span>${consulta.hora}</span>
        </div>

        <h6>Diagnóstico y Tratamiento</h6>
        <p><strong>Motivo:</strong> ${consulta.motivo_consulta}</p>
        <p><strong>Diagnóstico:</strong> ${consulta.diagnostico.descripcion} (Código: ${consulta.diagnostico.codigo_cie})</p>
        <p><strong>Tratamiento:</strong> ${consulta.tratamiento.procedimiento}</p>
        <div class="info-grid">
            <strong>Costo:</strong><span>${consulta.tratamiento.costo_usd}</span>
            <strong>Estado:</strong><span>${obtenerBadgeEstado(consulta.tratamiento.estado)}</span>
        </div>

        <h6>Notas Adicionales</h6>
        <p>${consulta.notas_adicionales || "No hay notas adicionales."}</p>
    `;
}
