const { 
    Client, 
    GatewayIntentBits 
} = require('discord.js');

const { 
    joinVoiceChannel, 
    createAudioPlayer, 
    createAudioResource, 
    AudioPlayerStatus, 
    EndBehaviorType 
} = require('@discordjs/voice');

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const prism = require('prism-media');

const config = require('./config/settings.json');

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildVoiceStates,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ]
});

let connection;
let recordingUser = null;

client.once('ready', () => {
    console.log(`✅ Logged in as ${client.user.tag}`);
});

client.on('messageCreate', async (message) => {
    if (message.content === '!join') {
        if (!message.member.voice.channel) {
            return message.reply('❌ You must be in a voice channel to use this command!');
        }

        connection = joinVoiceChannel({
            channelId: message.member.voice.channelId,
            guildId: message.guild.id,
            adapterCreator: message.guild.voiceAdapterCreator,
        });

        message.reply('✅ Joined the voice channel and ready to listen!');
        startListening();
    }
});

function startListening() {
    const receiver = connection.receiver;

    receiver.speaking.on('start', (userId) => {
        console.log(`🎙️ Recording user ${userId}`);

        // Ensure the recordings directory exists
        if (!fs.existsSync("./recordings")) {
            fs.mkdirSync("./recordings");
        }

        const outputPath = `./recordings/${userId}.pcm`;
        const outputStream = fs.createWriteStream(outputPath);

        // Use Opus decoder to get raw PCM
        const decoder = new prism.opus.Decoder({ rate: 48000, channels: 1, frameSize: 960 });

        const audioStream = receiver.subscribe(userId, {
            end: {
                behavior: EndBehaviorType.AfterSilence,
                duration: 1000 // Stop recording after 1 second of silence
            }
        });

        audioStream.pipe(decoder).pipe(outputStream);

        outputStream.on('finish', () => {
            console.log(`✅ Finished recording ${userId}`);
            processRecording(outputPath);
        });

        outputStream.on('error', (error) => {
            console.error("[ERROR] Writing audio file failed:", error);
        });
    });
}

function processRecording(pcmFile) {
    try {
        console.log(`🎼 Converting ${pcmFile} to WAV...`);
        execSync(`python python-scripts/convert_audio.py`);

        console.log(`📜 Transcribing audio...`);
        execSync(`python python-scripts/transcribe.py`);

        console.log(`🤖 Generating AI response...`);
        execSync(`python python-scripts/generate_response.py`);

        console.log(`🔊 Converting AI response to speech...`);
        execSync(`python python-scripts/text_to_speech.py`);

        console.log(`🎤 Playing AI response...`);
        playLatestAudio();
    } catch (error) {
        console.error('[ERROR] Processing failed:', error);
    }
}

function playLatestAudio() {
    const recordingsDir = './recordings';
    const mp3Files = fs.readdirSync(recordingsDir).filter(file => file.endsWith('.mp3'));

    if (mp3Files.length === 0) return console.log('[ERROR] No MP3 files found.');

    const latestMp3 = mp3Files.sort((a, b) => 
        fs.statSync(path.join(recordingsDir, b)).mtimeMs - fs.statSync(path.join(recordingsDir, a)).mtimeMs
    )[0];

    const resource = createAudioResource(path.join(recordingsDir, latestMp3));
    const player = createAudioPlayer();
    connection.subscribe(player);
    player.play(resource);

    console.log(`🎤 Now playing: ${latestMp3}`);

    player.on(AudioPlayerStatus.Idle, () => {
        console.log('✅ Playback finished.');
    });
}

client.login(config.DISCORD_BOT_TOKEN);
