const { Client, GatewayIntentBits } = require('discord.js');
const { joinVoiceChannel, createAudioReceiver, EndBehaviorType } = require('@discordjs/voice');
const fs = require('fs');
const prism = require('prism-media');

// Load settings.json for bot token and configurations
const config = require('./config/settings.json');

// Debugging: Print the token length (not full token for security)
console.log("🔍 Bot Token Length:", config.DISCORD_BOT_TOKEN.length);
console.log("🔍 First 5 characters of token:", config.DISCORD_BOT_TOKEN.slice(0, 5) + '...');

// Ensure the bot token exists before logging in
if (!config.DISCORD_BOT_TOKEN || config.DISCORD_BOT_TOKEN.length < 50) {
    console.error("❌ ERROR: Invalid or missing bot token. Please check settings.json!");
    process.exit(1);
}

// Create the bot client with necessary intents
const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildVoiceStates,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ]
});

// Event: Bot is ready
client.once('ready', () => {
    console.log(`✅ Logged in as ${client.user.tag}`);
});

// Event: Bot receives a command in a text channel
client.on('messageCreate', async (message) => {
    if (message.content === '!join') {
        if (!message.member.voice.channel) {
            return message.reply('❌ You must be in a voice channel to use this command!');
        }

        const connection = joinVoiceChannel({
            channelId: message.member.voice.channelId,
            guildId: message.guild.id,
            adapterCreator: message.guild.voiceAdapterCreator,
        });

        message.reply('✅ Joined and recording!');
        startRecording(connection);
    }
});

// Function: Start recording voice channel
function startRecording(connection) {
    const receiver = connection.receiver;

    receiver.speaking.on('start', (userId) => {
        console.log(`🎙️ Recording user ${userId}`);

        const audioStream = receiver.subscribe(userId, {
            end: { behavior: EndBehaviorType.AfterSilence, duration: 1000 }
        });

        const outputPath = `./recordings/${userId}.pcm`;
        const outputStream = fs.createWriteStream(outputPath);

        const decoder = new prism.opus.Decoder({ rate: 48000, channels: 2, frameSize: 960 });
        audioStream.pipe(decoder).pipe(outputStream);

        audioStream.on('end', () => {
            console.log(`✅ Finished recording ${userId}`);
        });
    });
}

// Attempt to log in with bot token
client.login(config.DISCORD_BOT_TOKEN).catch((error) => {
    console.error("❌ Failed to login! Error:", error);
    console.error("🔎 Check if the token is correct and your bot is in a server.");
});
