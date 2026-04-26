const currentTheme = localStorage.getItem('theme') || 'light';

if (currentTheme) {
    nightMode(currentTheme);
}

function nightMode(mode){
    const body = document.body;
    const btn = document.getElementById('night-mode-button');
    
    if (mode === 'night'){
        theme = 'night';
        body.classList.add('night-theme');
        btn.src = btn.src.replace('moon-32.png', 'light-32.png');
        localStorage.setItem('theme', 'night');
        btn.onclick = function() { nightMode('light') };

    } else if (mode === 'light'){
        theme = 'light'
        body.classList.remove('night-theme');
        btn.src = btn.src.replace('light-32.png', 'moon-32.png');
        localStorage.setItem('theme', 'light');
        btn.onclick = function() { nightMode('night') };
    }
};