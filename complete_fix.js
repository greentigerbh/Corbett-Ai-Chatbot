const fs = require('fs');
const file = 'g:\\\\gagan\\\\uncle_bot\\\\newbot.html';
let content = fs.readFileSync(file, 'utf-8');

// Systematically replace all mojibake patterns
content = content.replace(/ðŸŌ²/g, '🌲');
content = content.replace(/ðŸŌŠ/g, '🌊');
content = content.replace(/ðŸ†/g, '🦁');
content = content.replace(/ðŸ"¸/g, '📸');
content = content.replace(/ðŸ"/g, '📷');
content = content.replace(/ðŸ"…/g, '📅');
content = content.replace(/ðŸŌ¿/g, '🌿');
content = content.replace(/ðŸ¯/g, '🏯');
content = content.replace(/ðŸŎ«/g, '🎫');
content = content.replace(/ðŸšŒ/g, '🚌');
content = content.replace(/ðŸ"´/g, '🔴');
content = content.replace(/ðŸŸ /g, '🟠');
content = content.replace(/ðŸŸ¡/g, '🟡');
content = content.replace(/ðŸŸ¢/g, '🟢');
content = content.replace(/ðŸ"„/g, '📄');
content = content.replace(/ðŸ±/g, '🍱');
content = content.replace(/ðŸ™/g, '🙏');
content = content.replace(/ðŸšª/g, '🚪');
content = content.replace(/ðŸŌ„/g, '🌄');
content = content.replace(/ðŸ'‹/g, '👋');
content = content.replace(/ðŸ˜/g, '🐘');

// Text mojibake
content = content.replace(/â€¢/g, '•');
content = content.replace(/â€"/g, '—');
content = content.replace(/â€–/g, '–');
content = content.replace(/â€™/g, "'");
content = content.replace(/â€œ/g, '"');
content = content.replace(/â€/g, '"');
content = content.replace(/â­/g, '★');
content = content.replace(/â°/g, '⏰');
content = content.replace(/â‚¹/g, '₹');

fs.writeFileSync(file, content, 'utf-8');
console.log('All mojibake cleaned!');
