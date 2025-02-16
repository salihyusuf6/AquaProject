const http = require('http');
const fs = require('fs');
const path = require('path');

// MIME türlerini tanımla
const mimeTypes = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.json': 'application/json',
    '.txt': 'text/plain',
    '.ttf': 'font/ttf',          // TrueType Font
    '.otf': 'font/otf',          // OpenType Font
    '.woff': 'font/woff',        // Web Open Font Format
    '.woff2': 'font/woff2',      // Web Open Font Format 2
    '.eot': 'application/vnd.ms-fontobject'
};

// Sunucu oluşturma
const server = http.createServer((req, res) => {
    // Kök dizin isteği için varsayılan dosya
    const requestedPath = req.url === '/' ? '/Home.html' : req.url;

    // URL'yi normalize et ve güvenli hale getir
    const safePath = path.normalize(requestedPath).replace(/^(\.\.[\/\\])+/, '');
    const filePath = path.join(__dirname, 'html', safePath);

    // Dosya uzantısını belirle
    const extname = String(path.extname(filePath)).toLowerCase();
    const contentType = mimeTypes[extname] || 'application/octet-stream';

    // Dosyanın varlığını kontrol et
    fs.stat(filePath, (err, stats) => {
        if (err || !stats.isFile()) {
            // Eğer dosya bulunamazsa 404 döndür
            fs.readFile(path.join(__dirname, 'html', '404.html'), (notFoundErr, notFoundContent) => {
                res.writeHead(404, { 'Content-Type': 'text/html' });
                res.end(notFoundContent || '<h1>404 Not Found</h1>', 'utf-8');
            });
            return;
        }

        // Dosyayı oku ve yanıtla
        fs.readFile(filePath, (readErr, content) => {
            if (readErr) {
                res.writeHead(500, { 'Content-Type': 'text/html' });
                res.end(`<h1>500 Internal Server Error</h1><p>${readErr.message}</p>`, 'utf-8');
                return;
            }
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content, 'utf-8');
        });
    });
});

// Sunucuyu başlat
const PORT = 3000;
server.listen(PORT,'0.0.0.0', () => {
    console.log(`Server running at http://185.240.104.86:${PORT}/`);
});
