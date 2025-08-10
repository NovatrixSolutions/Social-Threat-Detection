// Three.js threat visualization
document.addEventListener('DOMContentLoaded', function() {
    const threatViz = document.getElementById('threatViz');
    let scene, camera, renderer, particles;
    
    // Only initialize if element exists
    if (threatViz) {
        initThreatVisualization();
    }
    
    function initThreatVisualization() {
        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
        renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        renderer.setSize(threatViz.clientWidth, threatViz.clientHeight);
        threatViz.appendChild(renderer.domElement);
        
        // Create particles
        const geometry = new THREE.BufferGeometry();
        const particleCount = 100;
        const positions = new Float32Array(particleCount * 3);
        
        for (let i = 0; i < particleCount; i++) {
            positions[i * 3] = (Math.random() - 0.5) * 10;
            positions[i * 3 + 1] = (Math.random() - 0.5) * 10;
            positions[i * 3 + 2] = (Math.random() - 0.5) * 10;
        }
        
        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        
        const material = new THREE.PointsMaterial({
            color: 0x00c6ff,
            size: 0.1,
            transparent: true,
            opacity: 0.8,
            sizeAttenuation: true
        });
        
        particles = new THREE.Points(geometry, material);
        scene.add(particles);
        
        // Add danger particles (red)
        const dangerGeometry = new THREE.BufferGeometry();
        const dangerPositions = new Float32Array(10 * 3);
        
        for (let i = 0; i < 10; i++) {
            dangerPositions[i * 3] = (Math.random() - 0.5) * 8;
            dangerPositions[i * 3 + 1] = (Math.random() - 0.5) * 8;
            dangerPositions[i * 3 + 2] = (Math.random() - 0.5) * 8;
        }
        
        dangerGeometry.setAttribute('position', new THREE.BufferAttribute(dangerPositions, 3));
        
        const dangerMaterial = new THREE.PointsMaterial({
            color: 0xff3e3e,
            size: 0.15,
            transparent: true,
            opacity: 0.9,
            sizeAttenuation: true
        });
        
        const dangerParticles = new THREE.Points(dangerGeometry, dangerMaterial);
        scene.add(dangerParticles);
        
        camera.position.z = 5;
        
        // Animation loop
        function animate() {
            requestAnimationFrame(animate);
            
            particles.rotation.x += 0.001;
            particles.rotation.y += 0.002;
            dangerParticles.rotation.x += 0.002;
            dangerParticles.rotation.y += 0.001;
            
            renderer.render(scene, camera);
        }
        
        animate();
        
        // Handle window resize
        window.addEventListener('resize', () => {
            camera.aspect = threatViz.clientWidth / threatViz.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(threatViz.clientWidth, threatViz.clientHeight);
        });
    }
});