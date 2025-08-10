// js/platform.js
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Vanta.js background
    VANTA.NET({
        el: "#vanta-bg",
        color: 0x1DA1F2,
        backgroundColor: 0x021027,
        points: 15.00,
        maxDistance: 25.00,
        spacing: 20.00
    });

    // Initialize 3D visualization
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, 
        document.getElementById('threatViz').clientWidth / 
        document.getElementById('threatViz').clientHeight, 
        0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(document.getElementById('threatViz').clientWidth, 
                    document.getElementById('threatViz').clientHeight);
    document.getElementById('threatViz').appendChild(renderer.domElement);

    // Create threat visualization
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

    // Animation loop
    function animate() {
        requestAnimationFrame(animate);
        
        particlesMesh.rotation.x += 0.001;
        particlesMesh.rotation.y += 0.002;
        dangerParticlesMesh.rotation.x += 0.003;
        dangerParticlesMesh.rotation.y += 0.001;
        
        renderer.render(scene, camera);
    }
    animate();

    // Search functionality
    document.getElementById('searchBtn').addEventListener('click', analyzeKeywords);
    document.getElementById('searchInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') analyzeKeywords();
    });

    function analyzeKeywords() {
        const keywords = document.getElementById('searchInput').value.trim();
        if (!keywords) return;
        
        // Show loading state
        const searchBtn = document.getElementById('searchBtn');
        searchBtn.textContent = 'Analyzing...';
        searchBtn.disabled = true;
        
        // Simulate API call
        setTimeout(() => {
            showResults(keywords);
            searchBtn.textContent = 'Analyze';
            searchBtn.disabled = false;
        }, 2000);
    }

    function showResults(keywords) {
        document.getElementById('resultsSection').style.display = 'block';
        
        // Simulate fetched tweets
        const tweets = [
            // {
            //     avatar: 'https://randomuser.me/api/portraits/women/43.jpg',
            //     user: '@sarahjane',
            //     content: `I can't believe someone would say "${keywords}" like that. This is clearly harassment!`,
            //     time: '2 hours ago',
            //     likes: '24',
            //     threats: ['hate speech', 'targeted harassment']
            // },
            // {
            //     avatar: 'https://randomuser.me/api/portraits/men/32.jpg',
            //     user: '@johndoe',
            //     content: `Why are people using "${keywords}" in such a derogatory way? This needs to stop.`,
            //     time: '5 hours ago',
            //     likes: '156',
            //     threats: ['bullying']
            // },
            // {
            //     avatar: 'https://randomuser.me/api/portraits/women/65.jpg',
            //     user: '@amandaw',
            //     content: `Just experienced someone using "${keywords}" to demean women. Reporting this immediately.`,
            //     time: '1 day ago',
            //     likes: '89',
            //     threats: ['sexism', 'verbal abuse']
            // }
        ];
        
        const tweetsContainer = document.getElementById('tweetsContainer');
        tweetsContainer.innerHTML = '';
        
        tweets.forEach(tweet => {
            const tweetEl = document.createElement('div');
            tweetEl.className = 'tweet-card';
            tweetEl.innerHTML = `
                <div class="tweet-header">
                    <img src="${tweet.avatar}" alt="User" class="tweet-avatar">
                    <div class="tweet-user">${tweet.user}</div>
                </div>
                <div class="tweet-content">${tweet.content}</div>
                <div class="tweet-meta">
                    <span>${tweet.time}</span>
                    <span>${tweet.likes} likes</span>
                    <span>Threats: ${tweet.threats.join(', ')}</span>
                </div>
            `;
            tweetsContainer.appendChild(tweetEl);
        });
        
        // Scroll to results
        document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
    }

    // Report generation
    document.getElementById('generateReportBtn').addEventListener('click', function() {
        this.textContent = 'Generating Report...';
        setTimeout(() => {
            alert('Report generated successfully!');
            this.textContent = 'Generate Comprehensive Report';
        }, 1500);
    });
});