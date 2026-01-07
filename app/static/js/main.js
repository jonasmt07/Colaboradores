/**
 * Arquivo: app/static/js/main.js
 * Contém toda a lógica de interação do cliente (Frontend).
 */

/* ==========================================================================
   FUNCIONALIDADE GLOBAL: Copiar Ramal
   ========================================================================== */
function copyRamal(buttonElement, ramalText) {
    if (!ramalText) return;

    navigator.clipboard.writeText(ramalText).then(() => {
        const defaultContent = buttonElement.querySelector('.default-content');
        const successContent = buttonElement.querySelector('.success-content');

        if (defaultContent && successContent) {
            // Esconde número, mostra feedback
            defaultContent.classList.add('hidden');
            successContent.classList.remove('hidden');
            successContent.classList.add('flex');
            
            // Muda cor para verde
            buttonElement.classList.remove('bg-slate-50', 'text-slate-700', 'hover:bg-emerald-500', 'hover:text-white');
            buttonElement.classList.add('bg-emerald-50', 'text-emerald-600', 'border-emerald-200');

            // Restaura após 2 segundos
            setTimeout(() => {
                defaultContent.classList.remove('hidden');
                successContent.classList.add('hidden');
                successContent.classList.remove('flex');
                
                buttonElement.classList.remove('bg-emerald-50', 'text-emerald-600', 'border-emerald-200');
                buttonElement.classList.add('bg-slate-50', 'text-slate-700', 'hover:bg-emerald-500', 'hover:text-white');
            }, 2000);
        }
    }).catch(err => {
        console.error('Erro ao copiar ramal:', err);
        alert('Não foi possível copiar automaticamente.');
    });
}

/* ==========================================================================
   PÁGINA HOME: Filtros de Pesquisa (Versão Corrigida)
   ========================================================================== */
function filterHome() {
    const input = document.getElementById('homeSearchInput');
    const select = document.getElementById('homeUnitSelect');
    
    if (!input || !select) return;

    // Força tudo para minúsculo e remove espaços nas pontas
    const text = input.value.toLowerCase().trim();
    const unitFilter = select.value.toLowerCase().trim();
    
    const items = document.querySelectorAll('.employee-item-wrapper');
    let count = 0;

    items.forEach(item => {
        // Pega os dados do HTML (já devem estar em minúsculo pelo Jinja, mas garantimos aqui)
        const name = (item.dataset.name || '').toLowerCase();
        const unit = (item.dataset.unit || '').toLowerCase();
        const cargo = (item.dataset.cargo || '').toLowerCase();
        const ramal = item.innerText.toLowerCase(); // Procura também no texto visível (para achar ramal)

        // Lógica de filtro mais permissiva
        // Se digitou texto: procura no nome, cargo, unidade ou ramal
        const matchText = !text || 
                          name.includes(text) || 
                          unit.includes(text) || 
                          cargo.includes(text) ||
                          ramal.includes(text);

        // Se selecionou unidade: a unidade do item TEM que ser igual à selecionada
        const matchUnit = !unitFilter || unit === unitFilter;

        if (matchText && matchUnit) {
            item.classList.remove('hidden');
            count++;
        } else {
            item.classList.add('hidden');
        }
    });
    
    // Atualiza o contador na tela
    const countElement = document.getElementById('resultsCount');
    if (countElement) {
        // Se não tiver filtro nenhum, mostra o total geral
        if (!text && !unitFilter) {
            countElement.innerHTML = items.length + ' Registros Encontrados';
        } else {
            countElement.innerHTML = count + ' Registros Encontrados';
        }
    }
}

/* ==========================================================================
   PÁGINA ADMIN (DASHBOARD): Modal, Tabela e Edição
   ========================================================================== */

// Filtro da Tabela do Admin
function filterTable() {
    const input = document.getElementById('searchInput');
    if (!input) return; // Se não estiver no admin, para a execução
    
    const term = input.value.toLowerCase();
    const rows = document.querySelectorAll('#employeeTable tbody tr');
    
    rows.forEach(row => {
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(term) ? '' : 'none';
    });
}

// Prepara os dados para edição
function handleEdit(buttonElement) {
    const data = JSON.parse(buttonElement.getAttribute('data-json'));
    // Chama o modal em modo 'edit'. Passamos null no botão pois não precisamos ler URL externa
    openModal('edit', data, null); 
}

// Fecha o Modal
function closeModal() {
    const modal = document.getElementById('modalForm');
    if (modal) modal.classList.add('hidden');
}

/**
 * Abre o Modal (Pode ser Novo ou Editar)
 * @param {string} mode - 'add' ou 'edit'
 * @param {object} data - Objeto com dados do funcionário (se edit)
 * @param {HTMLElement} buttonElement - O botão que foi clicado (para ler data-add-url no modo add)
 */
function openModal(mode, data = null, buttonElement = null) {
    const modal = document.getElementById('modalForm');
    const form = document.getElementById('employeeForm');
    const currentPhotoText = document.getElementById('currentPhotoText');
    const photoNameSpan = document.getElementById('f_foto_nome');
    const fileInput = document.getElementById('f_foto');
    const modalTitle = document.getElementById('modalTitle');
    
    // Verificação de segurança
    if (!modal || !form) return;

    modal.classList.remove('hidden');
    
    // Limpa o input de arquivo sempre que abrir
    if(fileInput) fileInput.value = '';
    
    if (mode === 'add') {
        if(modalTitle) modalTitle.innerText = 'Novo Colaborador';
        
        // Lê a URL que passamos no HTML via data-add-url="{{ url_for(...) }}"
        if (buttonElement && buttonElement.dataset.addUrl) {
             form.action = buttonElement.dataset.addUrl;
        }
        
        form.reset();
        if(currentPhotoText) currentPhotoText.classList.add('hidden');

    } else {
        if(modalTitle) modalTitle.innerText = 'Editar Colaborador';
        
        // A rota de edição é fixa no backend (/admin/edit/<id>)
        form.action = "/admin/edit/" + data.id;
        
        // Preenche os campos
        if(document.getElementById('f_nome')) document.getElementById('f_nome').value = data.nome;
        if(document.getElementById('f_cargo')) document.getElementById('f_cargo').value = data.cargo;
        if(document.getElementById('f_email')) document.getElementById('f_email').value = data.email;
        if(document.getElementById('f_ramal')) document.getElementById('f_ramal').value = data.ramal;
        if(document.getElementById('f_unidade')) document.getElementById('f_unidade').value = data.Unidade; 
        if(document.getElementById('f_nome_unidade')) document.getElementById('f_nome_unidade').value = data.nome_unidade;
        
        // Lógica da foto atual
        if (data.fotoUrl && !data.fotoUrl.includes('http')) {
            if(currentPhotoText) {
                currentPhotoText.classList.remove('hidden');
                if(photoNameSpan) photoNameSpan.innerText = data.fotoUrl;
            }
        } else {
            if(currentPhotoText) currentPhotoText.classList.add('hidden');
        }
    }
}

// Fecha o modal se clicar fora dele (fundo escuro)
window.onclick = function(event) {
    const modal = document.getElementById('modalForm');
    if (modal && event.target == modal) {
        closeModal();
    }
}