// js/results.js
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Vanta.js background
    VANTA.NET({
        el: "#vanta-bg",
        color: 0x0072ff,
        backgroundColor: 0x021027,
        points: 15.00,
        maxDistance: 25.00,
        spacing: 20.00
    });

    // Initialize 3D visualization
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(document.getElementById('threatViz').clientWidth, 
                    document.getElementById('threatViz').clientHeight);
    document.getElementById('threatViz').appendChild(renderer.domElement);

    // Create floating platform icons in 3D space
    const platforms = ['twitter', 'reddit', 'youtube', 'newsapi', 'gnewsapi'];
    const platformObjects = [];
    
    platforms.forEach((platform, i) => {
        const geometry = new THREE.SphereGeometry(0.5, 32, 32);
        const material = new THREE.MeshBasicMaterial({ 
            color: i % 2 === 0 ? 0xff4444 : 0x4444ff,
            transparent: true,
            opacity: 0.8
        });
        const sphere = new THREE.Mesh(geometry, material);
        
        // Position in a circle
        sphere.position.x = Math.cos(i * 2 * Math.PI / platforms.length) * 3;
        sphere.position.z = Math.sin(i * 2 * Math.PI / platforms.length) * 3;
        sphere.position.y = 0;
        
        sphere.userData.platform = platform;
        scene.add(sphere);
        platformObjects.push(sphere);
    });

    camera.position.z = 5;

    // Animation loop
    function animate() {
        requestAnimationFrame(animate);
        
        platformObjects.forEach((obj, i) => {
            obj.rotation.x += 0.01;
            obj.rotation.y += 0.01;
            obj.position.y = Math.sin(Date.now() * 0.001 + i) * 0.5;
        });
        
        renderer.render(scene, camera);
    }
    animate();

    // Platform click handlers
    document.querySelectorAll('.platform-card').forEach(card => {
        card.addEventListener('click', function() {
            const platform = this.getAttribute('data-platform');
            // Add ripple effect
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                window.location.href = `platform-${platform}.html`;
            }, 300);
        });
    });
});