/**
 * Secure Password Generator
 * Uses Web Crypto API for cryptographically strong randomness
 */

// Character sets
const CHAR_SETS = {
    uppercase: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    lowercase: 'abcdefghijklmnopqrstuvwxyz',
    numbers: '0123456789',
    symbols: '!@#$%^&*()_+-=[]{}|;:,.<>?',
    ambiguous: '0O1lI'
};

// Word list for passphrase generation (common words)
const WORD_LIST = [
    'ability', 'able', 'about', 'above', 'accept', 'account', 'achieve', 'across', 'action', 'activity',
    'actually', 'address', 'admit', 'adult', 'affect', 'after', 'again', 'against', 'agency', 'agent',
    'agree', 'agreement', 'ahead', 'allow', 'almost', 'alone', 'along', 'already', 'also', 'although',
    'always', 'american', 'among', 'amount', 'analysis', 'animal', 'another', 'answer', 'anyone', 'anything',
    'appear', 'apply', 'approach', 'argue', 'around', 'arrive', 'article', 'artist', 'assume', 'attack',
    'attention', 'attorney', 'audience', 'author', 'authority', 'available', 'avoid', 'baby', 'back', 'ball',
    'bank', 'base', 'beautiful', 'because', 'become', 'before', 'begin', 'behavior', 'behind', 'believe',
    'benefit', 'better', 'between', 'beyond', 'billion', 'black', 'blood', 'blue', 'board', 'body',
    'book', 'born', 'both', 'break', 'bring', 'brother', 'budget', 'build', 'building', 'business',
    'call', 'camera', 'campaign', 'cancer', 'candidate', 'capital', 'card', 'care', 'career', 'carry',
    'case', 'catch', 'cause', 'cell', 'center', 'central', 'century', 'certain', 'chair', 'challenge',
    'chance', 'change', 'character', 'charge', 'check', 'child', 'choice', 'choose', 'church', 'citizen',
    'city', 'civil', 'claim', 'class', 'clear', 'close', 'coach', 'cold', 'collection', 'college',
    'color', 'come', 'commercial', 'common', 'community', 'company', 'compare', 'computer', 'concern', 'condition',
    'conference', 'congress', 'consider', 'consumer', 'contain', 'continue', 'control', 'cost', 'could', 'country',
    'couple', 'course', 'court', 'cover', 'create', 'crime', 'cultural', 'culture', 'current', 'customer',
    'dark', 'data', 'daughter', 'dead', 'deal', 'death', 'debate', 'decade', 'decide', 'decision',
    'deep', 'defense', 'degree', 'democratic', 'describe', 'design', 'despite', 'detail', 'determine', 'develop',
    'development', 'difference', 'different', 'difficult', 'dinner', 'direction', 'director', 'discover', 'discuss', 'discussion',
    'disease', 'doctor', 'door', 'down', 'draw', 'dream', 'drive', 'drop', 'drug', 'during',
    'each', 'early', 'east', 'easy', 'economic', 'economy', 'edge', 'education', 'effect', 'effort',
    'eight', 'either', 'election', 'else', 'employee', 'energy', 'enjoy', 'enough', 'enter', 'entire',
    'environment', 'environmental', 'especially', 'establish', 'even', 'evening', 'event', 'ever', 'every', 'everybody',
    'everyone', 'everything', 'evidence', 'exactly', 'example', 'executive', 'exist', 'expect', 'experience', 'expert',
    'explain', 'face', 'fact', 'factor', 'fail', 'fall', 'family', 'fast', 'father', 'fear',
    'federal', 'feel', 'feeling', 'field', 'fight', 'figure', 'fill', 'film', 'final', 'financial',
    'find', 'fine', 'finger', 'finish', 'fire', 'firm', 'first', 'fish', 'five', 'floor',
    'focus', 'follow', 'food', 'foot', 'force', 'foreign', 'forget', 'form', 'former', 'forward',
    'four', 'free', 'friend', 'from', 'front', 'full', 'fund', 'future', 'game', 'garden',
    'general', 'generation', 'girl', 'give', 'glass', 'goal', 'good', 'government', 'great', 'green',
    'ground', 'group', 'grow', 'growth', 'guess', 'gun', 'hair', 'half', 'hand', 'hang',
    'happen', 'happy', 'hard', 'have', 'head', 'health', 'hear', 'heart', 'heat', 'heavy',
    'help', 'here', 'herself', 'high', 'himself', 'history', 'hold', 'home', 'hope', 'hospital',
    'hotel', 'hour', 'house', 'however', 'huge', 'human', 'hundred', 'husband', 'idea', 'identify',
    'image', 'imagine', 'impact', 'important', 'improve', 'include', 'including', 'increase', 'indeed', 'indicate',
    'individual', 'industry', 'information', 'inside', 'instead', 'institution', 'interest', 'interesting', 'international', 'interview',
    'into', 'investment', 'involve', 'issue', 'item', 'itself', 'join', 'just', 'keep', 'kill',
    'kind', 'kitchen', 'know', 'knowledge', 'land', 'language', 'large', 'last', 'late', 'later',
    'laugh', 'lawyer', 'lead', 'leader', 'learn', 'least', 'leave', 'left', 'legal', 'less',
    'letter', 'level', 'life', 'light', 'like', 'likely', 'line', 'list', 'listen', 'little',
    'live', 'local', 'long', 'look', 'lose', 'loss', 'love', 'machine', 'magazine', 'main',
    'maintain', 'major', 'majority', 'make', 'manage', 'management', 'manager', 'many', 'market', 'marriage',
    'material', 'matter', 'maybe', 'mean', 'measure', 'media', 'medical', 'meet', 'meeting', 'member',
    'memory', 'mention', 'message', 'method', 'middle', 'might', 'military', 'million', 'mind', 'minute',
    'miss', 'mission', 'model', 'modern', 'moment', 'money', 'month', 'more', 'morning', 'most',
    'mother', 'mouth', 'move', 'movement', 'movie', 'much', 'music', 'must', 'myself', 'name',
    'nation', 'national', 'natural', 'nature', 'near', 'nearly', 'necessary', 'need', 'network', 'never',
    'news', 'newspaper', 'next', 'nice', 'night', 'none', 'north', 'note', 'nothing', 'notice',
    'number', 'occur', 'offer', 'office', 'officer', 'official', 'often', 'once', 'only', 'onto',
    'open', 'operation', 'opportunity', 'option', 'order', 'organization', 'other', 'others', 'outside', 'over',
    'owner', 'page', 'pain', 'painting', 'paper', 'parent', 'part', 'participant', 'particular', 'particularly',
    'partner', 'party', 'pass', 'past', 'patient', 'pattern', 'peace', 'people', 'perform', 'performance',
    'perhaps', 'period', 'person', 'personal', 'phone', 'physical', 'pick', 'picture', 'piece', 'place',
    'plan', 'plant', 'play', 'player', 'point', 'police', 'policy', 'political', 'politics', 'poor',
    'popular', 'population', 'position', 'positive', 'possible', 'power', 'practice', 'prepare', 'present', 'president',
    'pressure', 'pretty', 'prevent', 'price', 'private', 'probably', 'problem', 'process', 'produce', 'product',
    'production', 'professional', 'professor', 'program', 'project', 'property', 'protect', 'prove', 'provide', 'public',
    'pull', 'purpose', 'push', 'quality', 'question', 'quickly', 'quite', 'race', 'radio', 'raise',
    'range', 'rate', 'rather', 'reach', 'read', 'ready', 'real', 'reality', 'realize', 'really',
    'reason', 'receive', 'recent', 'recently', 'recognize', 'record', 'reduce', 'reflect', 'region', 'relate',
    'relationship', 'religious', 'remain', 'remember', 'remove', 'report', 'represent', 'republican', 'require', 'research',
    'resource', 'respond', 'response', 'responsibility', 'rest', 'result', 'return', 'reveal', 'rich', 'right',
    'rise', 'risk', 'road', 'rock', 'role', 'room', 'rule', 'safe', 'same', 'save',
    'scene', 'school', 'science', 'scientist', 'score', 'season', 'seat', 'second', 'section', 'security',
    'seek', 'seem', 'sell', 'send', 'senior', 'sense', 'series', 'serious', 'serve', 'service',
    'seven', 'several', 'shake', 'share', 'shoot', 'short', 'shot', 'should', 'shoulder', 'show',
    'side', 'sign', 'significant', 'similar', 'simple', 'simply', 'since', 'sing', 'single', 'sister',
    'site', 'situation', 'size', 'skill', 'skin', 'small', 'smile', 'social', 'society', 'soldier',
    'some', 'somebody', 'someone', 'something', 'sometimes', 'soon', 'sort', 'sound', 'source', 'south',
    'southern', 'space', 'speak', 'special', 'specific', 'speech', 'spend', 'sport', 'spring', 'staff',
    'stage', 'stand', 'standard', 'star', 'start', 'state', 'statement', 'station', 'stay', 'step',
    'still', 'stock', 'stop', 'store', 'story', 'strategy', 'street', 'strong', 'structure', 'student',
    'study', 'stuff', 'style', 'subject', 'success', 'successful', 'such', 'suddenly', 'suffer', 'suggest',
    'summer', 'support', 'sure', 'surface', 'system', 'table', 'take', 'talk', 'task', 'teach',
    'teacher', 'team', 'technology', 'television', 'tell', 'tend', 'term', 'test', 'than', 'thank',
    'that', 'their', 'them', 'themselves', 'then', 'theory', 'there', 'these', 'they', 'thing',
    'think', 'third', 'this', 'those', 'though', 'thought', 'thousand', 'threat', 'three', 'through',
    'throughout', 'throw', 'thus', 'time', 'today', 'together', 'tonight', 'total', 'tough', 'toward',
    'town', 'trade', 'traditional', 'training', 'travel', 'treat', 'treatment', 'tree', 'trial', 'trip',
    'trouble', 'true', 'truth', 'turn', 'type', 'under', 'understand', 'unit', 'until', 'upon',
    'usually', 'value', 'various', 'very', 'victim', 'view', 'violence', 'visit', 'voice', 'vote',
    'wait', 'walk', 'wall', 'want', 'watch', 'water', 'weapon', 'wear', 'week', 'weight',
    'well', 'west', 'western', 'what', 'whatever', 'when', 'where', 'whether', 'which', 'while',
    'white', 'whole', 'whom', 'whose', 'wide', 'wife', 'will', 'wind', 'window', 'wish',
    'with', 'within', 'without', 'woman', 'wonder', 'word', 'work', 'worker', 'world', 'worry',
    'would', 'write', 'writer', 'wrong', 'yard', 'yeah', 'year', 'young', 'yourself', 'zone'
];

// Consonants and vowels for pattern-based generation
const CONSONANTS = 'bcdfghjklmnpqrstvwxyz';
const VOWELS = 'aeiou';

// State
let clipboardTimeout = null;
let currentPassword = '';

// Cryptographically secure random number generator
function getSecureRandomNumber(max) {
    const array = new Uint32Array(1);
    window.crypto.getRandomValues(array);
    return array[0] % max;
}

// Get random character from a string
function getRandomChar(chars) {
    return chars[getSecureRandomNumber(chars.length)];
}

// Get character set based on options
function getCharacterSet(options) {
    let charset = '';
    
    if (options.uppercase) charset += CHAR_SETS.uppercase;
    if (options.lowercase) charset += CHAR_SETS.lowercase;
    if (options.numbers) charset += CHAR_SETS.numbers;
    if (options.symbols) charset += CHAR_SETS.symbols;
    
    if (options.excludeAmbiguous && charset) {
        charset = charset.split('').filter(char => !CHAR_SETS.ambiguous.includes(char)).join('');
    }
    
    return charset;
}

// Generate random password
function generatePassword(length, options) {
    const charset = getCharacterSet(options);
    
    if (!charset) {
        return 'Error: Select at least one character type';
    }
    
    let password = '';
    
    // Ensure at least one character from each selected type
    if (options.uppercase) password += getRandomChar(CHAR_SETS.uppercase);
    if (options.lowercase) password += getRandomChar(CHAR_SETS.lowercase);
    if (options.numbers) password += getRandomChar(CHAR_SETS.numbers);
    if (options.symbols) password += getRandomChar(CHAR_SETS.symbols);
    
    // Fill remaining length
    while (password.length < length) {
        password += getRandomChar(charset);
    }
    
    // Shuffle the password using Fisher-Yates algorithm with crypto random
    const passwordArray = password.split('');
    for (let i = passwordArray.length - 1; i > 0; i--) {
        const j = getSecureRandomNumber(i + 1);
        [passwordArray[i], passwordArray[j]] = [passwordArray[j], passwordArray[i]];
    }
    
    return passwordArray.join('');
}

// Generate passphrase (word-based)
function generatePassphrase() {
    const wordCount = 5 + getSecureRandomNumber(3); // 5-7 words
    const words = [];
    
    for (let i = 0; i < wordCount; i++) {
        const word = WORD_LIST[getSecureRandomNumber(WORD_LIST.length)];
        words.push(word.charAt(0).toUpperCase() + word.slice(1));
    }
    
    return words.join('-') + getSecureRandomNumber(100);
}

// Generate pattern-based password (alternating consonants and vowels)
function generatePatternBased(length = 16) {
    let password = '';
    let useConsonant = getSecureRandomNumber(2) === 0;
    
    for (let i = 0; i < length - 2; i++) {
        if (useConsonant) {
            password += getRandomChar(CONSONANTS);
        } else {
            password += getRandomChar(VOWELS);
        }
        useConsonant = !useConsonant;
    }
    
    // Add a number and symbol at random positions
    const numPos = getSecureRandomNumber(password.length);
    password = password.slice(0, numPos) + getRandomChar(CHAR_SETS.numbers) + password.slice(numPos);
    
    const symPos = getSecureRandomNumber(password.length);
    password = password.slice(0, symPos) + getRandomChar(CHAR_SETS.symbols) + password.slice(symPos);
    
    // Capitalize first letter
    password = password.charAt(0).toUpperCase() + password.slice(1);
    
    return password;
}

// Calculate entropy bits
function calculateEntropy(password) {
    let charset = 0;
    
    if (/[a-z]/.test(password)) charset += 26;
    if (/[A-Z]/.test(password)) charset += 26;
    if (/[0-9]/.test(password)) charset += 10;
    if (/[^a-zA-Z0-9]/.test(password)) charset += 32; // symbols
    
    const entropy = password.length * Math.log2(charset);
    return Math.round(entropy);
}

// Estimate crack time
function estimateCrackTime(entropyBits) {
    // Assuming 1 billion guesses per second
    const guessesPerSecond = 1e9;
    const possibleCombinations = Math.pow(2, entropyBits);
    const secondsToCrack = possibleCombinations / (2 * guessesPerSecond); // Average case
    
    if (secondsToCrack < 60) return `${Math.round(secondsToCrack)} seconds`;
    if (secondsToCrack < 3600) return `${Math.round(secondsToCrack / 60)} minutes`;
    if (secondsToCrack < 86400) return `${Math.round(secondsToCrack / 3600)} hours`;
    if (secondsToCrack < 31536000) return `${Math.round(secondsToCrack / 86400)} days`;
    if (secondsToCrack < 31536000 * 100) return `${Math.round(secondsToCrack / 31536000)} years`;
    if (secondsToCrack < 31536000 * 1000) return `${Math.round(secondsToCrack / (31536000 * 100))} centuries`;
    if (secondsToCrack < 31536000 * 1000000) return `${Math.round(secondsToCrack / (31536000 * 1000))} millennia`;
    return 'billions of years';
}

// Update strength meter
function updateStrengthMeter(password) {
    const entropyBits = calculateEntropy(password);
    const crackTime = estimateCrackTime(entropyBits);
    
    // Update displays
    document.getElementById('entropyBits').textContent = `${entropyBits} bits entropy`;
    document.getElementById('crackTime').textContent = `Crack time: ${crackTime}`;
    
    // Determine strength level
    let strength, percentage, color;
    if (entropyBits < 40) {
        strength = 'Very Weak';
        percentage = 20;
        color = '#ff4444';
    } else if (entropyBits < 60) {
        strength = 'Weak';
        percentage = 40;
        color = '#ff8844';
    } else if (entropyBits < 80) {
        strength = 'Medium';
        percentage = 60;
        color = '#ffcc44';
    } else if (entropyBits < 100) {
        strength = 'Strong';
        percentage = 80;
        color = '#88cc44';
    } else {
        strength = 'Very Strong';
        percentage = 100;
        color = '#44cc44';
    }
    
    document.getElementById('strengthLabel').textContent = strength;
    document.getElementById('strengthLabel').style.color = color;
    
    const strengthBar = document.getElementById('strengthBar');
    strengthBar.style.width = `${percentage}%`;
    strengthBar.style.backgroundColor = color;
}

// Get current options
function getCurrentOptions() {
    return {
        length: parseInt(document.getElementById('lengthSlider').value),
        uppercase: document.getElementById('uppercaseCheck').checked,
        lowercase: document.getElementById('lowercaseCheck').checked,
        numbers: document.getElementById('numbersCheck').checked,
        symbols: document.getElementById('symbolsCheck').checked,
        excludeAmbiguous: document.getElementById('ambiguousCheck').checked
    };
}

// Generate and display password
function generateAndDisplay() {
    const options = getCurrentOptions();
    const password = generatePassword(options.length, options);
    
    currentPassword = password;
    document.getElementById('passwordDisplay').value = password;
    updateStrengthMeter(password);
    addToHistory(password);
}

// Copy to clipboard with auto-clear
async function copyToClipboard() {
    const password = document.getElementById('passwordDisplay').value;
    
    if (!password || password.includes('Error:') || password.includes('Click Generate')) {
        return;
    }
    
    try {
        await navigator.clipboard.writeText(password);
        
        // Show notification
        const notification = document.getElementById('copyNotification');
        notification.classList.remove('hidden');
        
        // Clear previous timeout
        if (clipboardTimeout) {
            clearTimeout(clipboardTimeout);
        }
        
        // Auto-clear clipboard after 30 seconds
        clipboardTimeout = setTimeout(async () => {
            await navigator.clipboard.writeText('');
            notification.classList.add('hidden');
        }, 30000);
        
        // Hide notification after 3 seconds
        setTimeout(() => {
            notification.classList.add('hidden');
        }, 3000);
        
    } catch (err) {
        alert('Failed to copy to clipboard');
    }
}

// Add to history
function addToHistory(password) {
    const history = getHistory();
    const timestamp = new Date().toISOString();
    
    history.unshift({ password, timestamp });
    
    // Keep only last 20
    if (history.length > 20) {
        history.splice(20);
    }
    
    localStorage.setItem('passwordHistory', JSON.stringify(history));
    updateHistoryDisplay();
}

// Get history from localStorage
function getHistory() {
    try {
        return JSON.parse(localStorage.getItem('passwordHistory')) || [];
    } catch {
        return [];
    }
}

// Update history display
function updateHistoryDisplay() {
    const history = getHistory();
    const historyList = document.getElementById('historyList');
    
    if (history.length === 0) {
        historyList.innerHTML = '<p class="empty-message">No passwords generated yet.</p>';
        return;
    }
    
    historyList.innerHTML = history.map((item, index) => {
        const date = new Date(item.timestamp);
        const formattedDate = date.toLocaleString();
        return `
            <div class="history-item">
                <span class="history-password">${item.password}</span>
                <span class="history-date">${formattedDate}</span>
                <button class="copy-history-btn" data-index="${index}">Copy</button>
            </div>
        `;
    }).join('');
    
    // Add event listeners to copy buttons
    document.querySelectorAll('.copy-history-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const index = parseInt(e.target.dataset.index);
            const password = history[index].password;
            await navigator.clipboard.writeText(password);
            e.target.textContent = 'Copied!';
            setTimeout(() => {
                e.target.textContent = 'Copy';
            }, 2000);
        });
    });
}

// Clear history
function clearHistory() {
    if (confirm('Are you sure you want to clear all password history?')) {
        localStorage.removeItem('passwordHistory');
        updateHistoryDisplay();
    }
}

// Batch generate passwords
function batchGenerate() {
    const count = parseInt(document.getElementById('batchCount').value);
    const options = getCurrentOptions();
    const batchResults = document.getElementById('batchResults');
    
    const passwords = [];
    for (let i = 0; i < count; i++) {
        passwords.push(generatePassword(options.length, options));
    }
    
    batchResults.innerHTML = passwords.map((pwd, index) => `
        <div class="batch-item">
            <span class="batch-number">${index + 1}.</span>
            <span class="batch-password">${pwd}</span>
            <button class="copy-batch-btn" data-password="${pwd}">Copy</button>
        </div>
    `).join('');
    
    // Add event listeners
    document.querySelectorAll('.copy-batch-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const password = e.target.dataset.password;
            await navigator.clipboard.writeText(password);
            e.target.textContent = 'Copied!';
            setTimeout(() => {
                e.target.textContent = 'Copy';
            }, 2000);
        });
    });
}

// Simple encryption/decryption using AES-GCM
async function encryptData(data, password) {
    const encoder = new TextEncoder();
    const dataBuffer = encoder.encode(JSON.stringify(data));
    
    // Derive key from password
    const keyMaterial = await window.crypto.subtle.importKey(
        'raw',
        encoder.encode(password),
        { name: 'PBKDF2' },
        false,
        ['deriveBits', 'deriveKey']
    );
    
    const salt = window.crypto.getRandomValues(new Uint8Array(16));
    
    const key = await window.crypto.subtle.deriveKey(
        {
            name: 'PBKDF2',
            salt: salt,
            iterations: 100000,
            hash: 'SHA-256'
        },
        keyMaterial,
        { name: 'AES-GCM', length: 256 },
        false,
        ['encrypt']
    );
    
    const iv = window.crypto.getRandomValues(new Uint8Array(12));
    
    const encryptedData = await window.crypto.subtle.encrypt(
        { name: 'AES-GCM', iv: iv },
        key,
        dataBuffer
    );
    
    // Combine salt, iv, and encrypted data
    const result = new Uint8Array(salt.length + iv.length + encryptedData.byteLength);
    result.set(salt, 0);
    result.set(iv, salt.length);
    result.set(new Uint8Array(encryptedData), salt.length + iv.length);
    
    // Convert to base64
    return btoa(String.fromCharCode.apply(null, result));
}

async function decryptData(encryptedBase64, password) {
    const encoder = new TextEncoder();
    const decoder = new TextDecoder();
    
    // Decode base64
    const encryptedData = Uint8Array.from(atob(encryptedBase64), c => c.charCodeAt(0));
    
    // Extract salt, iv, and data
    const salt = encryptedData.slice(0, 16);
    const iv = encryptedData.slice(16, 28);
    const data = encryptedData.slice(28);
    
    // Derive key from password
    const keyMaterial = await window.crypto.subtle.importKey(
        'raw',
        encoder.encode(password),
        { name: 'PBKDF2' },
        false,
        ['deriveBits', 'deriveKey']
    );
    
    const key = await window.crypto.subtle.deriveKey(
        {
            name: 'PBKDF2',
            salt: salt,
            iterations: 100000,
            hash: 'SHA-256'
        },
        keyMaterial,
        { name: 'AES-GCM', length: 256 },
        false,
        ['decrypt']
    );
    
    const decryptedData = await window.crypto.subtle.decrypt(
        { name: 'AES-GCM', iv: iv },
        key,
        data
    );
    
    return JSON.parse(decoder.decode(decryptedData));
}

// Vault functions
// Note: Vault storage uses localStorage which provides browser-level security.
// For maximum security in production, implement server-side encryption with user authentication.
function saveToVault() {
    const password = document.getElementById('passwordDisplay').value;
    const label = document.getElementById('vaultLabel').value.trim();
    
    if (!password || password.includes('Error:') || password.includes('Click Generate')) {
        alert('Please generate a password first');
        return;
    }
    
    if (!label) {
        alert('Please enter a label for this password');
        return;
    }
    
    const vault = getVault();
    const timestamp = new Date().toISOString();
    
    vault.push({ label, password, timestamp });
    localStorage.setItem('passwordVault', JSON.stringify(vault));
    
    document.getElementById('vaultLabel').value = '';
    updateVaultDisplay();
    alert('Password saved to vault!');
}

function getVault() {
    try {
        return JSON.parse(localStorage.getItem('passwordVault')) || [];
    } catch {
        return [];
    }
}

function updateVaultDisplay() {
    const vault = getVault();
    const vaultList = document.getElementById('vaultList');
    
    if (vault.length === 0) {
        vaultList.innerHTML = '<p class="empty-message">No passwords saved yet.</p>';
        return;
    }
    
    vaultList.innerHTML = vault.map((item, index) => {
        const date = new Date(item.timestamp);
        const formattedDate = date.toLocaleString();
        return `
            <div class="vault-item">
                <div class="vault-label">${item.label}</div>
                <div class="vault-password">${item.password}</div>
                <div class="vault-date">${formattedDate}</div>
                <button class="copy-vault-btn" data-index="${index}">Copy</button>
                <button class="delete-vault-btn" data-index="${index}">Delete</button>
            </div>
        `;
    }).join('');
    
    // Add event listeners
    document.querySelectorAll('.copy-vault-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const index = parseInt(e.target.dataset.index);
            const password = vault[index].password;
            await navigator.clipboard.writeText(password);
            e.target.textContent = 'Copied!';
            setTimeout(() => {
                e.target.textContent = 'Copy';
            }, 2000);
        });
    });
    
    document.querySelectorAll('.delete-vault-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            if (confirm('Delete this password from vault?')) {
                const index = parseInt(e.target.dataset.index);
                vault.splice(index, 1);
                localStorage.setItem('passwordVault', JSON.stringify(vault));
                updateVaultDisplay();
            }
        });
    });
}

function clearVault() {
    if (confirm('Are you sure you want to clear the entire vault?')) {
        localStorage.removeItem('passwordVault');
        updateVaultDisplay();
    }
}

// Export functions
function exportHistory() {
    const history = getHistory();
    
    if (history.length === 0) {
        alert('No history to export');
        return;
    }
    
    const data = history.map(item => {
        const date = new Date(item.timestamp).toLocaleString();
        return `${date}: ${item.password}`;
    }).join('\n');
    
    downloadFile('password-history.txt', data);
}

function exportVault() {
    const vault = getVault();
    
    if (vault.length === 0) {
        alert('No vault entries to export');
        return;
    }
    
    const data = vault.map(item => {
        const date = new Date(item.timestamp).toLocaleString();
        return `${item.label}\n  Password: ${item.password}\n  Created: ${date}\n`;
    }).join('\n');
    
    downloadFile('password-vault.txt', data);
}

function downloadFile(filename, content) {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Length slider
    const lengthSlider = document.getElementById('lengthSlider');
    const lengthValue = document.getElementById('lengthValue');
    
    lengthSlider.addEventListener('input', () => {
        lengthValue.textContent = lengthSlider.value;
    });
    
    // Generate button
    document.getElementById('generateBtn').addEventListener('click', generateAndDisplay);
    
    // Copy button
    document.getElementById('copyBtn').addEventListener('click', copyToClipboard);
    
    // Preset buttons
    document.querySelectorAll('.preset-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const length = parseInt(btn.dataset.length);
            lengthSlider.value = length;
            lengthValue.textContent = length;
            generateAndDisplay();
        });
    });
    
    // Memorable password buttons
    document.getElementById('phraseBtn').addEventListener('click', () => {
        const password = generatePassphrase();
        currentPassword = password;
        document.getElementById('passwordDisplay').value = password;
        updateStrengthMeter(password);
        addToHistory(password);
    });
    
    document.getElementById('patternBtn').addEventListener('click', () => {
        const length = parseInt(lengthSlider.value);
        const password = generatePatternBased(length);
        currentPassword = password;
        document.getElementById('passwordDisplay').value = password;
        updateStrengthMeter(password);
        addToHistory(password);
    });
    
    // Batch generation
    document.getElementById('batchGenerateBtn').addEventListener('click', batchGenerate);
    
    // History
    document.getElementById('clearHistoryBtn').addEventListener('click', clearHistory);
    document.getElementById('exportHistoryBtn').addEventListener('click', exportHistory);
    
    // Vault
    document.getElementById('saveToVaultBtn').addEventListener('click', saveToVault);
    document.getElementById('clearVaultBtn').addEventListener('click', clearVault);
    document.getElementById('exportVaultBtn').addEventListener('click', exportVault);
    
    // Initialize displays
    updateHistoryDisplay();
    updateVaultDisplay();
    
    // Auto-generate initial password
    generateAndDisplay();
});
