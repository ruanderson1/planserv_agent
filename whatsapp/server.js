const express = require('express');
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const bodyParser = require('body-parser');
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const app = express();
app.use(bodyParser.json());

// Sua chave da API da OpenAI
// const apiKey = -----

// Inicializando o cliente WhatsApp
const client = new Client({
    authStrategy: new LocalAuth()
});

// Gerando QR code para autenticação
client.on('qr', qr => {
    qrcode.generate(qr, { small: true });
    console.log('Escaneie o QR code acima para conectar seu número de WhatsApp.');
});

// Evento quando o cliente está pronto
client.on('ready', () => {
    console.log('Cliente está pronto! Agora você pode enviar e receber mensagens.');
    client.isReady = true;
});

// Tratando falha de autenticação
client.on('auth_failure', (msg) => {
    console.error('Erro de autenticação:', msg);
    client.isReady = false;
});

// Tratando desconexão
client.on('disconnected', (reason) => {
    console.log('Cliente desconectado:', reason);
    client.isReady = false;
    reconnectClient();
});

// Função para reconectar o cliente após desconexões
function reconnectClient() {
    console.log('Tentando reconectar...');
    client.initialize();
}

// // Função para processar mensagens de áudio e transcrevê-las usando a API OpenAI
// async function handleAudioMessage(message) {
//     const media = await message.downloadMedia();

//     if (!media || !media.mimetype.startsWith('audio')) {
//         console.error("A mensagem não contém áudio válido.");
//         return;
//     }

//     const buffer = Buffer.from(media.data, 'base64'); // Converte para buffer
//     const form = new FormData();
//     form.append('file', buffer, {
//         filename: 'transcription.wav',
//         contentType: media.mimetype,
//         knownLength: buffer.length,
//     });
//     form.append('model', 'whisper-1');
//     form.append('language', 'pt');

//     const formHeaders = form.getHeaders();

//     try {
//         // Fazendo a requisição para a API da OpenAI
//         const response = await axios.post('https://api.openai.com/v1/audio/transcriptions', form, {
//             headers: {
//                 ...formHeaders,
//                 'Authorization': `Bearer ${apiKey}`,
//             },
//         });

//         if (response.data?.text) {
//             console.log("TRANSCRIPTION:", response.data.text);

//             // Enviar a transcrição para o servidor Python para obter uma resposta
//             const pythonResponse = await axios.post('http://127.0.0.1:8000/query', {
//                 question: response.data.text,
//                 number: message.from,
//             });

//             const pythonResponseText = pythonResponse.data.message;
//             console.log("Resposta do servidor Python:", pythonResponseText);

//             // Enviar a resposta do servidor Python para o WhatsApp
//             await client.sendMessage(message.from, pythonResponseText);
//         } else {
//             console.error("Nenhuma transcrição recebida.");
//             await client.sendMessage(message.from, "Desculpe, não foi possível transcrever o áudio.");
//         }
//     } catch (error) {
//         console.error("Erro ao transcrever o áudio ou obter resposta do Python:", error.response?.data || error.message);
//         await client.sendMessage(message.from, "Desculpe, houve um erro ao processar o áudio.");
//     }
// }

// Evento quando uma mensagem é recebida
client.on('message', async (message) => {
    if (message.hasMedia) {
        console.log(`Mensagem de mídia recebida de ${message.from}`);
        try {
            await handleAudioMessage(message);
        } catch (error) {
            console.error("Erro ao lidar com a mensagem de mídia:", error.message);
        }
    } else {
        console.log(`Mensagem de texto recebida de ${message.from}: ${message.body}`);
        // Processar mensagens de texto como de costume
        try {
            const response = await axios.post('http://127.0.0.1:8000/query', {
                question: message.body,
                number: message.from,
            });

            const responseData = response.data.message;
            await client.sendMessage(message.from, responseData);
            console.log('Resposta enviada para o WhatsApp!');
        } catch (error) {
            console.error('Erro ao processar mensagem de texto:', error.message);
            await client.sendMessage(message.from, 'Opa, houve um erro. Tente novamente mais tarde.');
        }
    }
});

// Inicializando o cliente WhatsApp
client.initialize();

// Iniciando o servidor Express
app.listen(3000, () => {
    console.log('Servidor rodando na porta 3000');
});
