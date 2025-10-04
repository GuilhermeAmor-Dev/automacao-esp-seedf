// assets/js/auth.js

document.addEventListener('DOMContentLoaded', () => {
    
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', (event) => {
            event.preventDefault(); // Impede o envio tradicional do formulário
            console.log('Tentativa de login...');

            // TODO: 1. Coletar os dados dos campos (email, password)
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // TODO: 2. Validar os dados (ex: campos não podem estar vazios)
            if (!email || !password) {
                alert('Por favor, preencha todos os campos.');
                return;
            }

            // TODO: 3. Fazer a chamada para a API de login (fetch)
            console.log({ email, password });
            alert('Lógica de login a ser implementada!');

            // Exemplo de redirecionamento após sucesso:
            // window.location.href = '/dashboard.html'; 
        });
    }

    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', (event) => {
            event.preventDefault();
            console.log('Tentativa de registro...');

            // TODO: Coletar, validar e enviar dados para a API de registro
            alert('Lógica de registro a ser implementada!');
        });
    }

    const forgotPasswordForm = document.getElementById('forgotPasswordForm');
    if (forgotPasswordForm) {
        const step1 = document.getElementById('step1');
        const step2 = document.getElementById('step2');

        forgotPasswordForm.addEventListener('submit', (event) => {
            event.preventDefault();

            // Verifica qual etapa está visível para decidir o que fazer
            if (step1.style.display !== 'none') {
                // --- LÓGICA DA ETAPA 1 ---
                const matricula = document.getElementById('matricula').value;
                const email = document.getElementById('email').value;

                if (!matricula && !email) {
                    alert('Por favor, preencha a Matrícula ou o Email.');
                    return;
                }

                console.log('Solicitando redefinição para:', { matricula, email });

                // TODO: Chamar a API do backend para enviar o link/código de recuperação.
                
                // Por enquanto, vamos apenas simular o sucesso e avançar para a próxima etapa.
                alert('Um link de recuperação foi enviado para seu email (simulação).');

                step1.style.display = 'none'; // Esconde a etapa 1
                step2.style.display = 'block'; // Mostra a etapa 2

            } else {
                // --- LÓGICA DA ETAPA 2 ---
                const newPassword = document.getElementById('newPassword').value;
                const confirmNewPassword = document.getElementById('confirmNewPassword').value;

                if (!newPassword || !confirmNewPassword) {
                    alert('Por favor, preencha os dois campos de senha.');
                    return;
                }

                if (newPassword !== confirmNewPassword) {
                    alert('As senhas não coincidem. Tente novamente.');
                    return;
                }

                console.log('Enviando nova senha para a API...');

                // TODO: Chamar a API do backend para salvar a nova senha.

                // Simula o sucesso e redireciona para o login
                alert('Senha redefinida com sucesso!');
                window.location.href = 'login.html';
            }
        });
    }
});