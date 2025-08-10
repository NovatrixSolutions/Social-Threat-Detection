// 3D Visualization for dashboard
document.addEventListener('DOMContentLoaded', function() {
    const threatViz = document.getElementById('threatViz');
    if (!threatViz) return;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(threatViz.clientWidth, threatViz.clientHeight);
    threatViz.appendChild(renderer.domElement);
    
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
        color: 0x00c6ff,
        transparent: true,
        opacity: 0.8
    });
    
    const particlesMesh = new THREE.Points(particlesGeo, particlesMat);
    scene.add(particlesMesh);
    
    // Add danger particles
    const dangerParticlesGeo = new THREE.BufferGeometry();
    const dangerPosArray = new Float32Array(20 * 3);
    
    for(let i = 0; i < dangerPosArray.length; i++) {
        dangerPosArray[i] = (Math.random() - 0.5) * 8;
    }
    
    dangerParticlesGeo.setAttribute('position', new THREE.BufferAttribute(dangerPosArray, 3));
    
    const dangerParticlesMat = new THREE.PointsMaterial({
        size: 0.1,
        color: 0xff3e3e,
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
        dangerParticlesMesh.rotation.x += 0.002;
        dangerParticlesMesh.rotation.y += 0.001;
        
        renderer.render(scene, camera);
    }
    
    animate();
});