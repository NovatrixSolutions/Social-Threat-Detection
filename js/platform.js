// API Configuration (same as above)
const API_CONFIG = {
    BASE_URL: 'http://127.0.0.1:5000/api',
    ENDPOINTS: {
        HEALTH: '/health',
        SCAN_ALL: '/scan/all',
        REDDIT: '/reddit/scan',
        TWITTER: '/twitter/scan',
        YOUTUBE: '/youtube/scan',
        GNEWS: '/gnews/scan',
        NEWSAPI: '/newsapi/scan'
    }
};

async function callAPI(endpoint, params = {}) {
    try {
        const url = new URL(API_CONFIG.BASE_URL + endpoint);
        Object.entries(params).forEach(([key, value]) => {
            if (value !== null && value !== undefined) {
                url.searchParams.append(key, value);
            }
        });

        const response = await fetch(url.toString());
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Vanta.js
    try {
        if (typeof VANTA !== 'undefined') {
            VANTA.NET({
                el: "#vanta-bg",
                color: 0x1DA1F2,
                backgroundColor: 0x021027,
                points: 15.00,
                maxDistance: 25.00,
                spacing: 20.00
            });
        }
    } catch (error) {
        console.warn('Vanta.js initialization failed:', error);
    }

    // Initialize 3D visualization
    initThreatVisualization();

    // **REAL SEARCH FUNCTIONALITY WITH BACKEND**
    const searchBtn = document.getElementById('searchBtn');
    const searchInput = document.getElementById('searchInput');

    if (searchBtn) searchBtn.addEventListener('click', analyzeKeywords);
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') analyzeKeywords();
        });
    }

    // Report generation
    const generateReportBtn = document.getElementById('generateReportBtn');
    if (generateReportBtn) {
        generateReportBtn.addEventListener('click', function() {
            this.textContent = 'Generating Report...';
            this.disabled = true;

            setTimeout(() => {
                alert('Report generated successfully!');
                this.textContent = 'Generate Comprehensive Report';
                this.disabled = false;
            }, 1500);
        });
    }
});

function initThreatVisualization() {
    const threatVizElement = document.getElementById('threatViz');
    if (!threatVizElement || typeof THREE === 'undefined') return;

    try {
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75,
            threatVizElement.clientWidth / threatVizElement.clientHeight,
            0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });

        renderer.setSize(threatVizElement.clientWidth, threatVizElement.clientHeight);
        threatVizElement.appendChild(renderer.domElement);

        // Create particles
        const particlesGeo = new THREE.BufferGeometry();
        const particlesCnt = 500;
        const posArray = new Float32Array(particlesCnt * 3);

        for(let i = 0; i < particlesCnt * 3; i++) {
            posArray[i] = (Math.random() - 0.5) * 10;
        }

        particlesGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

        const particlesMat = new THREE.PointsMaterial({
            size: 0.05,
            color: 0x1DA1F2,
            transparent: true,
            opacity: 0.8
        });

        const particlesMesh = new THREE.Points(particlesGeo, particlesMat);
        scene.add(particlesMesh);

        // Add danger particles
        const dangerParticlesGeo = new THREE.BufferGeometry();
        const dangerPosArray = new Float32Array(30 * 3);

        for(let i = 0; i < dangerPosArray.length; i++) {
            dangerPosArray[i] = (Math.random() - 0.5) * 8;
        }

        dangerParticlesGeo.setAttribute('position', new THREE.BufferAttribute(dangerPosArray, 3));

        const dangerParticlesMat = new THREE.PointsMaterial({
            size: 0.1,
            color: 0xff4d4d,
            transparent: true,
            opacity: 0.9
        });

        const dangerParticlesMesh = new THREE.Points(dangerParticlesGeo, dangerParticlesMat);
        scene.add(dangerParticlesMesh);

        camera.position.z = 5;

        function animate() {
            requestAnimationFrame(animate);

            particlesMesh.rotation.x += 0.001;
            particlesMesh.rotation.y += 0.002;
            dangerParticlesMesh.rotation.x += 0.003;
            dangerParticlesMesh.rotation.y += 0.001;

            renderer.render(scene, camera);
        }
        animate();

        window.addEventListener('resize', () => {
            camera.aspect = threatVizElement.clientWidth / threatVizElement.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(threatVizElement.clientWidth, threatVizElement.clientHeight);
        });

    } catch (error) {
        console.warn('3D visualization initialization failed:', error);
    }
}

// **REAL KEYWORD ANALYSIS WITH BACKEND**
async function analyzeKeywords() {
    const searchInput = document.getElementById('searchInput');
    const keywords = searchInput ? searchInput.value.trim() : '';

    if (!keywords) {
        alert('Please enter keywords to search for');
        return;
    }

    const searchBtn = document.getElementById('searchBtn');
    if (searchBtn) {
        searchBtn.textContent = 'Analyzing...';
        searchBtn.disabled = true;
    }

    try {
        const platform = getCurrentPlatform();
        console.log('Analyzing platform:', platform, 'with keywords:', keywords);

        let endpoint, params;

        switch(platform) {
            case 'twitter':
                endpoint = API_CONFIG.ENDPOINTS.TWITTER;
                params = { query: keywords, limit: 20 };
                break;
            case 'reddit':
                endpoint = API_CONFIG.ENDPOINTS.REDDIT;
                params = { subreddit: keywords, limit: 10 };
                break;
            case 'youtube':
                endpoint = API_CONFIG.ENDPOINTS.YOUTUBE;
                params = { query: keywords, limit: 15 };
                break;
            case 'gnews':
                endpoint = API_CONFIG.ENDPOINTS.GNEWS;
                params = { query: keywords, limit: 15 };
                break;
            case 'newsapi':
                endpoint = API_CONFIG.ENDPOINTS.NEWSAPI;
                params = { query: keywords, limit: 15 };
                break;
            default:
                throw new Error('Unknown platform: ' + platform);
        }

        // **CALL REAL BACKEND API**
        const results = await callAPI(endpoint, params);
        showRealResults(results, keywords, platform);

    } catch (error) {
        console.error('Analysis failed:', error);

        const errorMessage = error.message.includes('Failed to fetch')
            ? 'Unable to connect to server. Please ensure API is running.'
            : `Analysis failed: ${error.message}`;

        alert(errorMessage);
        showFallbackResults(keywords);

    } finally {
        if (searchBtn) {
            searchBtn.textContent = 'Analyze';
            searchBtn.disabled = false;
        }
    }
}

function getCurrentPlatform() {
    const urlParams = new URLSearchParams(window.location.search);
    const platformFromUrl = urlParams.get('platform');

    if (platformFromUrl) return platformFromUrl.toLowerCase();

    const currentPage = window.location.pathname.split('/').pop();
    if (currentPage.includes('twitter')) return 'twitter';
    if (currentPage.includes('reddit')) return 'reddit';
    if (currentPage.includes('youtube')) return 'youtube';
    if (currentPage.includes('gnews')) return 'gnews';
    if (currentPage.includes('newsapi')) return 'newsapi';

    console.warn('Could not determine platform, defaulting to twitter');
    return 'twitter';
}

// **SHOW REAL API RESULTS**
function showRealResults(results, keywords, platform) {
    const resultsSection = document.getElementById('resultsSection');
    const container = document.getElementById('tweetsContainer');

    if (!resultsSection || !container) {
        console.error('Results elements not found');
        return;
    }

    resultsSection.style.display = 'block';
    container.innerHTML = '';

    // Update header
    const resultsHeader = document.querySelector('.results-header');
    if (resultsHeader) {
        resultsHeader.innerHTML = `
            <h3>🔍 ${platform.toUpperCase()} Analysis Results for "${keywords}"</h3>
            <p>Scan completed: ${new Date().toLocaleString()}</p>
        `;
    }

    if (results.success && results.data?.detections && results.data.detections.length > 0) {
        // Show statistics
        const statsDiv = document.createElement('div');
        statsDiv.className = 'scan-stats';
        statsDiv.innerHTML = `
            <div class="stat-grid">
                <div class="stat-item">
                    <span class="stat-number">${results.data.threats_found || 0}</span>
                    <span class="stat-label">Threats Found</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">${getItemsScanned(results.data)}</span>
                    <span class="stat-label">Items Scanned</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">${Math.round((results.data.threats_found / getItemsScanned(results.data)) * 100) || 0}%</span>
                    <span class="stat-label">Detection Rate</span>
                </div>
            </div>
        `;
        container.appendChild(statsDiv);

        // Show individual detections
        results.data.detections.forEach((detection, index) => {
            const detectionEl = document.createElement('div');
            detectionEl.className = 'detection-card';
            detectionEl.innerHTML = `
                <div class="detection-header">
                    <div class="detection-user">
                        <strong>${detection.author || detection.username || 'Unknown User'}</strong>
                        <span class="detection-type">${detection.type || 'content'}</span>
                    </div>
                    <div class="confidence-badge confidence-${getConfidenceLevel(detection.confidence)}">
                        ${Math.round((detection.confidence || 0) * 100)}% Confidence
                    </div>
                </div>
                <div class="detection-content">
                    ${detection.content || detection.text_preview || detection.title || 'No content available'}
                </div>
                <div class="detection-meta">
                    <span class="detection-time">
                        📅 ${formatDate(detection.created_at || detection.created_utc || detection.published_at)}
                    </span>
                    ${detection.keywords_found && detection.keywords_found.length > 0 ?
                        `<span class="detection-keywords">🔍 ${detection.keywords_found.join(', ')}</span>` : ''}
                    ${getDetectionUrl(detection) ?
                        `<a href="${getDetectionUrl(detection)}" target="_blank" class="view-original">View Original</a>` : ''}
                </div>
            `;
            container.appendChild(detectionEl);
        });
    } else if (results.success) {
        container.innerHTML = `
            <div class="no-results">
                <h4>✅ No threats detected</h4>
                <p>No threatening content found with "${keywords}" on ${platform}.</p>
                <p>This platform appears clean for these search terms.</p>
            </div>
        `;
    } else {
        container.innerHTML = `
            <div class="error-results">
                <h4>❌ Scan Error</h4>
                <p>Error: ${results.error || 'Unknown error'}</p>
                <p>Please try again or contact support.</p>
            </div>
        `;
    }

    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Helper functions
function getItemsScanned(data) {
    return data?.posts_scanned || data?.tweets_scanned || data?.videos_scanned || data?.articles_scanned || 0;
}

function getConfidenceLevel(confidence) {
    const conf = confidence || 0;
    if (conf >= 0.8) return 'high';
    if (conf >= 0.5) return 'medium';
    return 'low';
}

function formatDate(dateString) {
    if (!dateString) return 'Recent';
    try {
        return new Date(dateString).toLocaleString();
    } catch {
        return dateString;
    }
}

function getDetectionUrl(detection) {
    return detection.url || detection.post_url || detection.tweet_url || detection.video_url || '';
}

function showFallbackResults(keywords) {
    const resultsSection = document.getElementById('resultsSection');
    const container = document.getElementById('tweetsContainer');

    if (!resultsSection || !container) return;

    resultsSection.style.display = 'block';
    container.innerHTML = `
        <div class="fallback-results">
            <h4>⚠️ API Connection Failed</h4>
            <p>Could not connect to the threat detection API.</p>
            <ul>
                <li>Ensure API server is running on http://127.0.0.1:5000</li>
                <li>Check your internet connection</li>
                <li>Verify no firewall is blocking the connection</li>
            </ul>
            <button onclick="analyzeKeywords()" class="retry-btn">🔄 Retry Analysis</button>
        </div>
    `;

    resultsSection.scrollIntoView({ behavior: 'smooth' });
}
